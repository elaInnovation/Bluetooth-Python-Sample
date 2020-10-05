from queue import Queue
from threading import Thread

import sys
import bluepy
from bluepy.btle import Peripheral, DefaultDelegate, BTLEException
from ela.bluetooth.connect.BluepyConnect import BluepyConnect
import ela.bluetooth.connect.elaBleCommands
from datetime import datetime

BLUETOOTH_ADDR_TYPE = bluepy.btle.ADDR_TYPE_PUBLIC # for version >= 220
# BLUETOOTH_ADDR_TYPE = bluepy.btle.ADDR_TYPE_RANDOM # for version <= 220

##
# @fn print_help
def print_help():
    print("[help]\tTo run this script, ou have to respect the following syntax :")
    print("[help]\tsudo python3.7 elaDownloadDataLogger.py <mac_address> <pwd> [OPTION]")
    print("[help]\t\tOPTION\tGNU LONG OPTION\tMeaning")
    print("[help]\t\t-a \t--start\tStart the data logger. Start recording all the data according to the loggin period configured in the tag")
    print("[help]\t\t-r <file>\t--read <file>\tRead the content of data logger and export it on a output file")
    print("[help]\t\t-o \t--stop <file>\tStop the data logger. Stop recording data into the tag")
    print("[help]\t\tOPTIONS DESCRIPTION\tMeaning")
    print("[help]\t\t<mac_address> : stand for the mac address of the target tag")
    print("[help]\t\t<pwd> : stand for the bluetooth password")
    print("[help]\t\t<file> : output file as a text file")

##
# @fn writeDataloggerFile 
# @brief write daa logger in my_file
def writeDataloggerFile(filename, data): 
    my_file = open(filename, "w")    
    my_file.write(data)
    my_file.close()

## 
# @fn start the data logger EN 12830
# @brief start recording data logger EN 12830
# @return status success or failed
def startDataLogger(mac_address, password):
    try:
        #
        # getter on current date
        # dd/mm/YY H:M:S
        # datetime object containing current date and time
        now = datetime.now()
        startDate = now.strftime("%d/%m/%Y %H:%M:%S +00:00")
        print("[info]\t[Configuration]\t==> Start date is : ", startDate)
        #  
        addr_type = BLUETOOTH_ADDR_TYPE
        example = BluepyConnect(mac_address, addr_type)
        msg = "{CMD} {PWD} {DATE}".format(CMD=ela.bluetooth.connect.elaBleCommands.DATALOGGER_START_STR, PWD=password, DATE=startDate)
        example.send(msg)
        example.waitResponse()
    except:
        print("[Exception][startDataLogger] An unexpected exception occurs :", sys.exc_info()[0])
    #
    return True

## 
# @fn download the entire data logger EN 12830
def downloadDataLogger(mac_address, password, filename):
    #
    addr_type = BLUETOOTH_ADDR_TYPE
    example = BluepyConnect(mac_address, addr_type)
    msg = "{CMD} {PWD}".format(CMD=ela.bluetooth.connect.elaBleCommands.READ_DATA_STR, PWD=password)
    example.send(msg)
    result = example.waitResponse()
    writeDataloggerFile(filename, result)
    #    
    return True

## 
# @fn stop the data logger EN 12830
# @brief stop recording data logger EN 12830
# @return status success or failed
def stopDataLogger(mac_address, password):
    #
    addr_type = BLUETOOTH_ADDR_TYPE
    example = BluepyConnect(mac_address, addr_type)
    msg = "{CMD} {PWD}".format(CMD=ela.bluetooth.connect.elaBleCommands.DATALOGGER_STOP_STR, PWD=password)
    example.send(msg)
    example.waitResponse()
    #
    return True

## 
# @fn test_argv
# @brief organize argv
# @return tuple with the different results
#   
def manage_dl_argv():
    #
    mac_address = ""
    success = False
    #
    try:    
        num_arguments = len(sys.argv)
        if (num_arguments >= 3):
            #
            mac_address = str(sys.argv[1])
            password = sys.argv[2]
            outputfile = ""
            for arg in sys.argv:
                if(str(arg) in "-a" or str(arg) in "--start"):                        
                    #
                    print("[info]\t[Configuration]\t==> Start Data Logger Requiered")
                    print("[info]\t[Configuration]\t==> Try to connect to mac address : ", mac_address)
                    #
                    startDataLogger(mac_address, password)
                    #
                    success = True
                    break
                elif(arg in "-r" or arg in "--read"):                        
                    #
                    outputfile = sys.argv[4]
                    print("[info]\t[Configuration]\t==> Get Data Logger Requiered")
                    print("[info]\t[Configuration]\t==> Try to connect to mac address : ", mac_address)
                    print("[info]\t[Configuration]\t==> Flush data in output file : ", outputfile)
                    #
                    downloadDataLogger(mac_address, password, outputfile)
                    #
                    success = True
                    break               
                elif(arg in "-o" or arg in "--stop"):                        
                    print("[info]\t[Configuration]\t==> Stop Data Logger Requiered")
                    print("[info]\t[Configuration]\t==> Try to connect to mac address : ", mac_address)
                    #
                    stopDataLogger(mac_address, password)
                    #
                    success = True
                    break
                else:
                    print("[info]\t[Configuration]\t==> Unknown commands")
                    success = False
        if(False == success):
            print_help()
    except :
        print("[Exception] An unexpected exception occurs for the input arguments :", sys.exc_info()[0])
        print_help()
        success = False
    #
    # return tuple of results
    return success

## 
# @fn main
# @brief main program to start a connection to an ELA Tag  
if __name__ == "__main__":

    # 
    try:
        b_arg_ok = manage_dl_argv()
        if(b_arg_ok):
            print("[elaDownloadDataLogger.py][__main__] The command send to the tag success !")
        else:
            print("[elaDownloadDataLogger.py][__main__][ERROR] Connection to the tag encouter a problem !")
    except:
        print("[elaDownloadDataLogger.py][__main__][ERROR] An exception occurs whilte the program is trying to connect to the tag !!!")
