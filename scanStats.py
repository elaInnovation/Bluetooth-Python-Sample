# System import
import sys
import time
import binascii
from datetime import datetime
import threading
import re, argparse
from os import system, name 

# Bluetooth import
from bluepy.btle import Scanner, DefaultDelegate

# static variable
CONST_LOCAL_NAME = "Complete Local Name"

# global variable
filter = ""
timestamp = 5.0
tagPeriod = 1
tagStats = False
globalStats = True

tags = []

class ScanDelegate(DefaultDelegate):
    """
    Scan delegate to catch and interpret bluetooth advertising events
    """
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        """
        Handle new data
        """
        if isNewDev:
            if filter != "":
              self.useFilter(dev)
            else:
              tags.append(dev)

        elif isNewData:
          if filter != "":
              self.useFilter(dev)
          else:
              tags.append(dev)

    def useFilter(self,dev):
      """
      Save tag after filter
      """
      for (adtype, desc, value) in dev.getScanData():
          if (desc == CONST_LOCAL_NAME):
              if filter in value:
                tags.append(dev)

class ScannerEla():
  """
  Scanner class to start and stop scanner
  """
  def startScanner(self):
    """
    Start scanner
    """
    try:
      scanner = Scanner().withDelegate(ScanDelegate())
      devices = scanner.scan(timestamp)
    except:
      pass
            
class PrinterConsole():
  """
  Show on console the stats
  """
  def printer(self):
    """
    Printer infos
    """
    i = 0
    while i <= timestamp:
      self.clear()
      print("Data received : ", len(tags))
      time.sleep(1)
      i += 1
    self.printerEnd()

    
  def printerEnd(self):
    """
    Show stats 
    """
    print("------------- Scan finished -------------")
    print("Time record : ", timestamp)
    if(tagStats):
      print("% success", (len(tags) / timestamp) * 100, "%")
    else:
      listUnique = []
      for dev in tags:
        if dev.addr not in listUnique:
          listUnique.append(dev.addr)

      print("Number of BLE devices scanned : ", len(listUnique))
    sys.exit(0)

  def clear(self): 
    """
    clear console
    """
    if name == 'nt': 
        _ = system('cls') 
    else: 
        _ = system('clear') 
  
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Scan Bluetooth LE Tags')
    filter_group = parser.add_argument_group('filter')
    filter_group.add_argument('--filter', nargs='+', help='Filter for BLE tags. Can be a complete filter like P MAG 000001. Default is None')
    time_group = parser.add_argument_group('time')
    time_group.add_argument('--time', nargs=1, help='Scanning time. Default is 5s')
    opt_group = parser.add_argument_group('tagperiod')
    opt_group.add_argument('--tagperiod', nargs=1, help='Advertising period of the tag. If this parameter is set, stats will include specific tag stats (%% success). Default is 1s')

    args = parser.parse_args()

    if args.filter:
      for txt in args.filter:
        filter += txt + " "
      filter = filter[:len(filter)-1]

    if args.time:
      timestamp = float(args.time[0])

    if args.tagperiod:
      tagStats = True
      tagPeriod = int(args.tagperiod[0])

    scan = ScannerEla()
    t1 = threading.Thread(target=scan.startScanner)
    t1.setDaemon(True)
    t1.start()

    console = PrinterConsole()
    t2 = threading.Thread(target=console.printer)
    t2.setDaemon(True)
    t2.start()

    # Infinite Loop
    while True:
      pass


