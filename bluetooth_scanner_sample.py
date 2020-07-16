#déclaration des librairies

from __future__ import print_function
import sys
import binascii

from bluepy.btle import Scanner, DefaultDelegate
from datetime import datetime

CONST_LOCAL_NAME = "Complete Local Name"

entetes = [u'MacAddress',
     u'ID_Process',
     u'Timestamp',
     u'TimeEllapse',
     u'RSSI (dBm)',
     u'LocalName',
     u'RawData']

tag_history = []


class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
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
                print("Discovered device", dev.addr)
                tag_history.append(entry)
            elif isNewData:
                print("Received new data from", dev.addr)
                tag_history.append(entry)


#déclaration fonction écriture
def ecritureFromList(filepath, tags):
    mon_fichier = open(filepath, "w") # ouvre le fichier en mode écriture ('a' pour modif, 'r' pour read) 
    ligneEntete = ";".join(entetes) + "\n"
    mon_fichier.write(ligneEntete)
    for tag in tags:
        print("%s", tag)
        mon_fichier.write(tag)
    mon_fichier.close()
    return    

def test_argv():
    # PRECONDITIONS => Test si on a le bon nbre d'argument bloc try/except
    nb = len(sys.argv)
    if not (nb == 3):
        return False
    else:
        return True

#programme principal 
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

        #si float et chaine de caractere alors 
        if(b_value_ok):
            scanner = Scanner().withDelegate(ScanDelegate())
            try:
                devices = scanner.scan(time_scan)
            except :
                print("Unexpected error in scan :", sys.exc_info()[0])
            ecritureFromList(file_name, tag_history)
            #not scan
        else:
            print("The type of parameter is not the one expected !!!")

    else:
        print("Wrong arguments : cmd python3.7 <file> <time_float> <string_for_scv_file>")

    print("Done.")
    
