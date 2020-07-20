#declare library
from __future__ import print_function
import sys
import binascii

from bluepy.btle import Scanner, DefaultDelegate
from datetime import datetime

#declare global constant
CONST_LOCAL_NAME = "Complete Local Name"
CONST_MAX_SCAN_TIME = 20

headers = [u'MacAddress',
     u'ID_Process',
     u'Timestamp',
     u'TimeEllapse',
     u'RSSI (dBm)',
     u'LocalName',
     u'RawData']

# declare global variable
tag_history = []
g_filters = []

class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)
    
    #use filters get: just write object contains <g_filters>
    def use_filters(self, name, entry):
        if(len(g_filters) >= 1):
            count_filter = 0
            while (count_filter < len(g_filters)):
                if(g_filters[count_filter] in name):
                    tag_history.append(entry)
                count_filter += 1 
        elif(len(g_filters) <= 0):
            tag_history.append(entry)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        #get timestamp
        now = datetime.now()
        timestamp = datetime.timestamp(now)
        date_time = datetime.fromtimestamp(timestamp)
        if isinstance(dev.rawData, bytes):
            name = ""
            for (adtype, desc, value) in dev.getScanData():
                if (desc == CONST_LOCAL_NAME):
                    name = value
            entry = "\n{ADDR} ({ADDRTYPE});0;{DATE};0; {RSSI};{NAME}; {RAWDATA}".format(ADDR=dev.addr,ADDRTYPE=dev.addrType,RSSI=dev.rssi, NAME=name, RAWDATA=binascii.b2a_hex(dev.rawData).decode('ascii'), DATE=date_time)
            if isNewDev:
                print("Discovered device", dev.addr, name)
                self.use_filters(name, entry)
            elif isNewData:
                print("Received new data from", dev.addr, name)
                self.use_filters(name, entry)

#write in my_file
def ecritureFromList(tags): 
    for tag in tags:
        print("%s", tag)
        my_file.write(tag)
    return    

#write filters list in g_filters
def update_filters():
    temp_filter = ""
    if(4 == len(sys.argv)):
        i = 0
        temp_filter =str(sys.argv[3])                    #get argv:function split with ;
        split_temp_filter = temp_filter.split(";")       #split argv
        while(i < len(split_temp_filter)):               #loop for write in g_filters
            g_filters.append(split_temp_filter[i])      
            print("Filters list: ", split_temp_filter[i])
            print("g_filters: ", g_filters)
            i += 1 
        #look function split with 
        print("Filter found : ", temp_filter)
        
#organize argv
def test_argv():
    nb = len(sys.argv)                 
    if (nb == 3):
        print("No filter")
        return True
    elif (nb == 4):
        # try to match filter
        print("There is probably a filter")
        update_filters()
        return True
    else:
        return False

#main  
if __name__ == "__main__":
    
    # init variables
    time_scan = 0.0
    file_name = ""

    b_arg_ok = test_argv()     #test nbr arg
    if(b_arg_ok):

        b_value_ok = False
        try:
            time_scan = float(sys.argv[1])
            file_name = str(sys.argv[2])
            b_value_ok = True
        except :
            print("Unexpected error:", sys.exc_info()[0])
 
        if(b_value_ok):
            i=0
            #create and write in my_file
            my_file = open(sys.argv[2], "w")
            header_line = ";".join(headers) + "\n"
            my_file.write(header_line)
            # timing left
            timing_left = time_scan
            while(timing_left > 0):
                scanner = Scanner().withDelegate(ScanDelegate())
                try:
                    devices = scanner.scan(min([timing_left, CONST_MAX_SCAN_TIME]))
                except :
                    print("Unexpected error in scan :", sys.exc_info()[0])
                ecritureFromList(tag_history)    
                tag_history = []
                timing_left = timing_left - CONST_MAX_SCAN_TIME 
                print("Timing scan left (s) : ", timing_left)
            my_file.close()
            #not scan
        else:
            print("The type of parameter is not the one expected !!!")

    else:
        print("Wrong arguments : cmd python3.7 <file> <time_float> <string_for_scv_file> <''filters''>")

    print("Done.")
    
