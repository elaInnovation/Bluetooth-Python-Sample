from bluepy.btle import Scanner, DefaultDelegate
from ela.bluetooth.advertising.TagFactory import Tagfactory
from ela.bluetooth.advertising.TagBase import TagBase 
import binascii

## 
# @class ScanDelegate
# @brief scan delegate to catch and interpret bluetooth advertising events
class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            print("Discovered device", dev.addr)
        elif isNewData:
            print("Received new data from", dev.addr)

## associate the delegate to the scanner and start it for 10.0 seconds
scanner = Scanner().withDelegate(ScanDelegate())
devices = scanner.scan(10.0)

## display result get from scanner
for dev in devices:
    if( isinstance(dev.rawData, bytes)):
        print("Device %s (%s), RSSI=%d dB, Interpreted ELA Data=%s, RawData=%s" % (dev.addr, dev.addrType, dev.rssi, Tagfactory.getInstance().getTag(dev.rawData).formattedDataSensor ,binascii.b2a_hex(dev.rawData).decode('ascii')))
        for (adtype, desc, value) in dev.getScanData():
            print("  %s = %s" % (desc, value))