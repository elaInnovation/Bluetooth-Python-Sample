
from datetime import datetime
from threading import Thread
import sys
import time
import os

## @class DataLoggerDaily 
class DataLoggerDaily(Thread):

    ## @fn __init__ 
    def __init__(self, mac_address):
        super(DataLoggerDaily, self).__init__()   # super() will call Thread.__init__ for you
        self.mac = mac_address

    ##
    # @fn run 
    # @brief background thread definition
    def run(self):  # put inside run your loop
        try:    
            continueExecution = True
            while continueExecution:
                try:
                    #
                    now = datetime.now()
                    currFile = "{YEAR}{MONTH}{DAY}{HOUR}{MIN}{SEC}_output.txt".format(YEAR=now.year,MONTH=now.month,DAY=now.day,HOUR=now.hour,MIN=now.minute,SEC=now.second)
                    command = "sudo python3 elaDownloadDataLogger.py {MAC_ADDR} 123456789A -r {FILENAME}".format(MAC_ADDR=self.mac, FILENAME=currFile)
                    print(command)
                    os.system(command)
                    # sleep on day
                    time.sleep(900)
                except:
                    print("Unexpected error in [startService]:", sys.exc_info()[0])
                    continueExecution = False        
        except:
            print("[datalogger_collect_handler][ERROR] An exception occursin thread !!!")

##
# @fn print_help
def print_help():
    print("[help]\tTo run this script, ou have to respect the following syntax :")
    print("[help]\tsudo python3.7 elaDownloadDataLoggerDaily.py <mac_address>")
    print("[help]\t\t<mac_address> : stand for the mac address of the target tag")

## 
# @fn test_argv
def test_argv():
    success = False
    #
    try:    
        num_arguments = len(sys.argv)
        if (num_arguments >= 2):
            #
            target_mac = str(sys.argv[1])
            success = True
    except:
        print_help()
    #
    return success, target_mac

## 
# @fn main
# @brief main program to start a connection to an ELA Tag  
if __name__ == "__main__":

    # NOTE - mac adress format
    #        mac_address = "C2:9C:68:04:76:8E"
    #
    # test if the arguments fullfil the program conditions
    try:
        b_arg_ok, mac_address  = test_argv()
        if(b_arg_ok):
            #
            if mac_address is None:
                print("Need to set the MAC address...")
                exit(1)
            #
            datalogger_collect_thread = DataLoggerDaily(mac_address)
            datalogger_collect_thread.setDaemon(True)
            datalogger_collect_thread.start()
            #
            print("Please enter \"Q\" to qui the program ...")    
            while True:
                # test exit
                msg = input()
                if msg.upper() == "Q":
                    break
        else:
            print_help()
    except:
        print("[elaDownloadDataLoggerDaily.py][__main__][ERROR] An exception occurs while the program is trying to connect to the tag !!!")