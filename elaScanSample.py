from bluepy.btle import Scanner, DefaultDelegate

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
    print("Device %s (%s), RSSI=%d dB" % (dev.addr, dev.addrType, dev.rssi))
    for (adtype, desc, value) in dev.getScanData():
        print("  %s = %s" % (desc, value))