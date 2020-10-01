#declare library
from __future__ import print_function
import sys
import binascii

from bluepy.btle import Scanner, DefaultDelegate
from datetime import datetime

#declare global constant
CONST_LOCAL_NAME = "Complete Local Name"
CONST_MAX_SCAN_TIME = 20
headers = [u'Timestamp', u'MacAddress', u'Address Type', u'LocalName', u'RSSI (dBm)', u'RawData']

# declare global variable
g_filters = []

## 
# @class ScanDelegate
# @brief scan delegate to catch and interpret bluetooth advertising events
class ScanDelegate(DefaultDelegate):

    ## @brief list of tags formatted values
    tags_formatted_values = []

    ## 
    # @fn __init__ 
    def __init__(self):
        DefaultDelegate.__init__(self)
    
    ##
    # @fn use_filters
    # @brief use filters get: just write object contains <g_filters>
    # @param [in] name : local name of the tags to match with filter
    # @param [in] entry : formatted line to store in the records
    def use_filters(self, name, entry):
        if(len(g_filters) >= 1):
            for filter in g_filters:
                if(filter in name):
                    self.tags_formatted_values.append(entry)
        elif(len(g_filters) <= 0):
            self.tags_formatted_values.append(entry)

    ##
    # @fn handleDiscovery
    # @brief handle the discovery of a new advertising
    # @param [in] dev : device advertising informations
    # @param [in] isNewDev : is this value a new one
    # @param [in] isNewData : is this value a new data (and the device has already seen once)
    def handleDiscovery(self, dev, isNewDev, isNewData):
        #
        # get a formatted timestamp
        date_time = datetime.fromtimestamp(datetime.timestamp(datetime.now()))
        if isinstance(dev.rawData, bytes):
            #
            # find localname into bluetooth properties
            name = ""
            for (adtype, desc, value) in dev.getScanData():
                if (desc == CONST_LOCAL_NAME):
                    name = value
            # 
            entry = "{DATE};{ADDR};{ADDRTYPE};{NAME};{RSSI};{RAWDATA}".format(ADDR=dev.addr,ADDRTYPE=dev.addrType,RSSI=dev.rssi, NAME=name, RAWDATA=binascii.b2a_hex(dev.rawData).decode('ascii'), DATE=date_time)
            print("Received data from", dev.addr, name)
            self.use_filters(name, entry)

##
# @fn update_filters
# @brief write filters list in g_filters
# @param [in] filters : list of filters 
def update_filters(filters):
    iCurrentFilter = 0
    # split argv with separator
    split_temp_filter = filters.split(";")
    while(iCurrentFilter < len(split_temp_filter)):
        g_filters.append(split_temp_filter[iCurrentFilter])      
        print("[info]\t[Configuration]\t==> Filter found {NUM} : {VALUE} ".format( NUM=iCurrentFilter, VALUE=split_temp_filter[iCurrentFilter]))
        iCurrentFilter += 1 

## 
# @fn test_argv
# @brief organize argv
def test_argv():
    #
    time_scan = 0.0
    file_name = ""
    success = False
    #
    try:    
        num_arguments = len(sys.argv)
        if (num_arguments >= 3):
            time_scan = float(sys.argv[1])
            file_name = str(sys.argv[2])
            print("[info]\t[Configuration]\t==> Record time (seconds) : ", time_scan)
            print("[info]\t[Configuration]\t==> Csv output file : ", file_name)        
        if (num_arguments == 3):
            print("[info]\t[Configuration]\t==> No filter defined for this record")
            success = True
        elif (num_arguments == 4):
            # try to match filter
            update_filters(sys.argv[3])
            success = True
        else:
            print("[help]\tTo run this script, ou have to respect the following syntax :")
            print("[help]\tsudo python3.7 bluetooth_scanner_sample.py <time_float> <string_for_scv_file> <'filters_01';'filters_02';...;'filters_N'>")
            print("[help]\t\t<time_float> (Mandatory) : Use this parameter to define the scanning time (in seconds) from 1.0 to 86400.0")
            print("[help]\t\t<string_for_scv_file> (Mandatory) : As a string to flush all the scan result into the file. Example : my_record.csv ")
            print("[help]\t\t<'filters_01';'filters_02';...;'filters_N'> (Optionnal) : As a list of a string filter separated by ';'")
            success = False
    except :
        print("[Exception] An unexpected exception occurs for the input arguments :", sys.exc_info()[0])
        success = False
    #
    # return tuple of results
    return success, time_scan, file_name

## 
# @fn writeFileHeader
# @brief write into the file a csv header
def writeFileHeader(filename):
    print("[info]\t==>Your output file : ", filename)
    my_file = open(filename, "w")
    header_line = ";".join(headers) + "\n"
    my_file.write(header_line)
    my_file.close()

##
# @fn writeTagsFromList 
# @brief write in my_file
def writeTagsFromList(filename, tags): 
    my_file = open(filename, "a")    
    for tag in tags:
        print("[info]\t==>Flush in file : ", tag)
        line = tag + "\n"
        my_file.write(line)
    my_file.close()

## 
# @fn main
# @brief main program to start recording bluetooth advertising into a csv file  
if __name__ == "__main__":
    """ main program """

    print("[bluetooth_scanner_sample.py][__main__] Enter in Python Bluetooth Advertising Recorder")
    #
    # test if the arguments fullfil the program conditions
    b_arg_ok, time_scan, file_name  = test_argv()
    if(b_arg_ok):
        #
        # create the ourputfile and flush the header
        writeFileHeader(file_name)
        #
        # initialize the timing left
        timing_left = time_scan
        while(timing_left > 0):
            scanDelegate = ScanDelegate()
            scanner = Scanner().withDelegate(scanDelegate)
            try:
                devices = scanner.scan(min([timing_left, CONST_MAX_SCAN_TIME]))
            except :
                print("[Exception] An unexpected exception occurs during the scan :", sys.exc_info()[0])
            writeTagsFromList(file_name, scanDelegate.tags_formatted_values)    
            timing_left = timing_left - CONST_MAX_SCAN_TIME 
            print("[Info] Timing scan left (s) : ", timing_left)
    else:
        print("[bluetooth_scanner_sample.py][__main__][ERROR] The different parameters or the type of parameter is not the one expected !!!")

    print("[bluetooth_scanner_sample.py][__main__] Leaving Python Bluetooth Advertising Recorder")
    
