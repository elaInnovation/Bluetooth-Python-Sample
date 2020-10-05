from queue import Queue
from threading import Thread

import sys
import bluepy
from bluepy.btle import Peripheral, DefaultDelegate, BTLEException

MAX_TIMEOUT = 3.0

## 
# @class BluepyConnect 
# @brief This class is directly inheriting bluepy.btle.DefaultDelegate for notifications,
#        but the delegate could be a separate class
class BluepyConnect(DefaultDelegate):

    ## @brief store the downloaded data from data logger
    downloadedData = ""

    def __init__(self, address, type=bluepy.btle.ADDR_TYPE_PUBLIC):
        super().__init__()

        self._peripheral_address = address
        self._peripheral_address_type = type
        self._peripheral = None
        self._characteristics_tx = None
        self._timeout_connection = 0.0
        self._downloading = False

        # create the TX queue
        self._tx_queue = Queue()

        # start the bluepy IO thread
        self._bluepy_thread = Thread(target=self._bluepy_handler)
        self._bluepy_thread.name = "bluepy_handler"
        self._bluepy_thread.daemon = True
        self._bluepy_thread.start()

    def handleNotification(self, cHandle, data):
        """This is the notification delegate function from DefaultDelegate
        """
        print("\nReceived Notification: " + str(data))
        self.downloadedData += data.decode("utf-8")
        self._timeout_connection = 0.0

    def _bluepy_handler(self):
        """This is the bluepy IO thread
        :return:
        """
        try:
            # Connect to the peripheral
            self._peripheral = Peripheral(self._peripheral_address, self._peripheral_address_type)
            # Set the notification delegate
            self._peripheral.setDelegate(self)
            self._peripheral.setMTU(61)

            # get the list of services
            services = self._peripheral.getServices()

            write_handle = None
            subscribe_handle = None

            # magic stuff for the Nordic UART GATT service
            uart_uuid = "6e400001-b5a3-f393-e0a9-e50e24dcca9e"
            charcteristics_tx_uuid = "6e400002-b5a3-f393-e0a9-e50e24dcca9e"
            uart_write_uuid_prefix = "6e400002"

            # this is general magic GATT stuff
            # notify handles will have a UUID that begins with this
            uart_notify_uuid_prefix = "00002902"
            # these are the byte values that we need to write to subscribe/unsubscribe for notifications
            subscribe_bytes = b'\x01\x00'
            # unsubscribe_bytes = b'\x00\x00'

            # dump out some info for the services that we found
            for service in services:
                print("Found service: " + str(service))
                if str(service.uuid).lower() == uart_uuid:
                    # this is the Nordic UART service that we're looking for
                    chars = service.getCharacteristics()
                    for char in chars:
                        print("  char: " + str(char) + ", handle: " + str(char.handle) +
                              ", props: " + str(char.properties))
                        if(charcteristics_tx_uuid in str(char.uuid)):
                            print("*** Found characteristic TX : ", str(char))
                            self._characteristics_tx = char
                    descs = service.getDescriptors()
                    # this is the important part-
                    # find the handles that we will write to and subscribe for notifications
                    for desc in descs:
                        print("  desc: " + str(desc))
                        str_uuid = str(desc.uuid).lower()
                        if str_uuid.startswith(uart_write_uuid_prefix):
                            write_handle = desc.handle
                            print("*** Found write handle: " + str(write_handle))
                        elif str_uuid.startswith(uart_notify_uuid_prefix):
                            subscribe_handle = desc.handle
                            print("*** Found subscribe handle: " + str(subscribe_handle))

            if write_handle is not None and subscribe_handle is not None:
                # we found the handles that we need

                # this call performs the subscribe for notifications
                response = self._peripheral.writeCharacteristic(subscribe_handle, subscribe_bytes, withResponse=True)

                # clear the downloaded data buffer
                self.downloadedData = ""

                # now that we're subscribed for notifications, waiting for TX/RX...
                self._timeout_connection = 0.0
                self._downloading = True
                while True:
                    while not self._tx_queue.empty():
                        msg = self._tx_queue.get_nowait()
                        msg_bytes = bytes(msg, encoding="utf-8")
                        if(None != self._characteristics_tx):
                            print(">>>Send command : ", msg)
                            self._characteristics_tx.write(msg_bytes)

                    self._peripheral.waitForNotifications(1.0)
                    self._timeout_connection += 1.0
                    if(self._timeout_connection > MAX_TIMEOUT):
                        self._downloading = False
                        print("[BluepyConnect][_bluepy_handler] : Connection Timeout Reached in Thread Send")
                        break
            
            # disconnect the tag
            print("[BluepyConnect][_bluepy_handler] : Disconnect from tag")

        except BTLEException as e:
            print(e)
        finally:
            self._peripheral.disconnect()

    ##
    # @fn waitResponse 
    # @brief wait a response from connection
    def waitResponse(self):
        tempResult = ""
        timeout_wait = 0.0
        self._downloading = True
        while True:
            #
            if(False == self._downloading):
                tempResult = self.downloadedData
                break
            #
            self._timeout_connection += 1.0
            if(timeout_wait > (20 * MAX_TIMEOUT) ):
                print("[BluepyConnect][waitResponse] : Connection Timeout Reached in Thread Send")
                break
        return tempResult    

    def send(self, message):
        """Call this function to send a BLE message over the UART service
        :param message: Message to send
        :return:
        """

        # put the message in the TX queue
        self._tx_queue.put_nowait(message)
