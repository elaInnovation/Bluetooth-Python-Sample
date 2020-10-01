from queue import Queue
from threading import Thread

import sys
import bluepy
from bluepy.btle import Peripheral, DefaultDelegate, BTLEException

## 
# @class BluepyConnect 
# @brief This class is directly inheriting bluepy.btle.DefaultDelegate for notifications,
#        but the delegate could be a separate class
class BluepyConnect(DefaultDelegate):

    def __init__(self, address, type=bluepy.btle.ADDR_TYPE_PUBLIC):
        super().__init__()

        self._peripheral_address = address
        self._peripheral_address_type = type
        self._peripheral = None
        self._characteristics_tx = None

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

    def _bluepy_handler(self):
        """This is the bluepy IO thread
        :return:
        """
        try:
            # Connect to the peripheral
            self._peripheral = Peripheral(self._peripheral_address, self._peripheral_address_type)
            # Set the notification delegate
            self._peripheral.setDelegate(self)

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

                # now that we're subscribed for notifications, waiting for TX/RX...
                while True:
                    while not self._tx_queue.empty():
                        msg = self._tx_queue.get_nowait()
                        msg_bytes = bytes(msg, encoding="utf-8")
                        if(None != self._characteristics_tx):
                            print(">>>Send command : ", msg)
                            self._characteristics_tx.write(msg_bytes)

                    self._peripheral.waitForNotifications(1.0)

        except BTLEException as e:
            print(e)
        finally:
            self._peripheral.disconnect()

    def send(self, message):
        """Call this function to send a BLE message over the UART service
        :param message: Message to send
        :return:
        """

        # put the message in the TX queue
        self._tx_queue.put_nowait(message)

## 
# @fn test_argv
# @brief organize argv
# @return tuple with the different results
#   
def test_argv():
    #
    mac_address = ""
    command = ""
    success = False
    #
    try:    
        num_arguments = len(sys.argv)
        if (num_arguments == 3):
            mac_address = str(sys.argv[1])
            command = str(sys.argv[2])
            print("[info]\t[Configuration]\t==> No filter defined for this record")
            success = True
        else:
            print("[help]\tTo run this script, ou have to respect the following syntax :")
            print("[help]\tsudo python3.7 elaConectSample.py <mac_address> <ela_ble_command>")
            print("[help]\t\t<mac_address> (Mandatory) : tag to connect mac address ")
            print("[help]\t\t<ela_ble_command> (Mandatory) : specific command for ELA Innovation Bluetooth Tag ")
            success = False
    except :
        print("[Exception] An unexpected exception occurs for the input arguments :", sys.exc_info()[0])
        success = False
    #
    # return tuple of results
    return success, mac_address, command

## 
# @fn main
# @brief main program to start a connection to an ELA Tag  
if __name__ == "__main__":

    # NOTE - mac adress format
    #        mac_address = "C2:9C:68:04:76:8E"
    #
    # test if the arguments fullfil the program conditions
    try:
        b_arg_ok, mac_address, command  = test_argv()
        if(b_arg_ok):
            # NOTE - MUST set this appropriately, depending on the type of address that the peripheral is advertising
            # addr_type = bluepy.btle.ADDR_TYPE_PUBLIC
            addr_type = bluepy.btle.ADDR_TYPE_RANDOM

            if mac_address is None:
                print("Need to set the MAC address...")
                exit(1)

            example = BluepyConnect(mac_address, addr_type)
            msg = command
            example.send(msg)

            print("Please enter \"Q\" to qui the program ...")    
            
            while True:
                msg = input()
                if msg.upper() == "Q":
                    break
    except:
        print("[elaConnectSample.py][__main__][ERROR] An exception occurs whilte the program is trying to connect to the tag !!!")
