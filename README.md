# Bluetooth-Python-Sample
Different sample to manage bluetooth for raspberry in Python.

## Build
Here you will find the procedure to manage the sample files and run it directly in your environnement. The target environnement tested and available are:
-   [Raspberry-Pi 3B+](#raspberry-pi-3b+)

### Raspberry-Pi 3B+
To execute the different python sample provide by ELA Bluetooth for the bluetooth, you need to install the different environnement or package :
- Python 3.7
- bluepy

First of all be sure that your raspberry is up to date by executing the following commands:
```bash
   sudo apt-get update
```

Then install python 3.7; you may need to use pip3:

```bash
   sudo apt-get install python3-pip libglib2.0-dev
   sudo pip3 install bluepy
```

## Samples
This repository contains different sample. Accordings to your needs, you can try each files with python to perform the following functions:
- [elaScanSample.py](#elascansamplepy) : use bluetooth through bluepy to scan advertising data from bluetooth
- [elaConnectSample.py](#elaconnectsamplepy) : use bluetooth through bluepy to connect to an ELA Innovation tag and send a command
- [bluetooth_scanner_sample.py](#bluetooth_scanner_samplepy) : use bluetooth through bluepy to scan and record data into a csv file
- [elaScanInterpretedDataSample.py](#elascaninterpreteddatasamplepy) : use bluetooth through bluepy to scan advertising data and use TagFactory class to interpret payload into data sensor information
- [elaDownloadDataLogger.py](#eladownloaddataloggerpy) : use bluetooth connection mode to start, read and stop ELA Innovation Data Logger T EN 12830

### elaScanSample.py
This sample use the scanner during a fix period (10 seconds) and display results as raw payload from Bluetooth Advertising.

Run the command  : 
```bash
   sudo python3 elaScanSample.py
  ```

### elaScanInterpretedDataSample.py
This sample use the scanner during a fix period (10 seconds) and display results as interpreted sensor data from Bluetooth Advertising.

Run the command  : 
```bash
   sudo python3 elaScanInterpretedDataSample.py
  ```

### elaConnectSample.py
This sample use bluetooth and bluepy to connect to an ELA Innovation tag and send command.

Run the command  : 
```bash
   sudo python3 elaConnectSample.py <mac_address> <ela_tag_command>
  ```
Input parameters description:

      1st parameter is mac address: enter a string to specify the tag's mag address. This information is available by scanning and in the Bluetooth Advertisement
   
      2nd parameter is command  : enter a string to specify the command / functionnlaity available for an ELA Innovation Bluetooth Tag


### bluetooth_scanner_sample.py
To use the scanner and record data into a csv file, you can use the script **bluetooth_scanner_sample.py**. This program allows you to record for a defined period and filter to flush the result into a csv file.

Run the command  : 
```bash
   sudo python3 bluetooth_scanner_sample.py <timescan> <file>.csv <"filters">
  ```
Input parameters description:

      1st parameter is timescan(s): enter a float number to determine the time requiered to scan
   
      2nd parameter is file.csv   : enter a string; that will be your created file's name. Don't forget the '.csv' extension
   
      3rd parameter are filters   : enter a string; that will determinate each word use to filter our 'file.csv' data writed.
                                    You must write your differente filters like this: "filter1;filter2;filter3;..."
                                    This is a contain filter. You will get only data contain your filter word.
                                    **The filter algorithm match only if the filter is contained in Bluetooth Local Name**
                                    
     You must to enter the both first parameters. For the 3rd parameter (filters) you have to enter "" if you don't want filter.


### elaDownloadDataLogger.py
This sample use bluetooth and bluepy to connect to an ELA Innovation tag and send command for Data Logger EN 12830. You can Start, Read Data logger EN 12830 (and flush into a text file), and Stop.

Run the command  : 
```bash
   sudo python3 elaDownloadDataLogger.py <mac_address> <password> [OPTION]
  ```
Input parameters description:

      1st parameter is mac address: enter a string to specify the tag's mag address. This information is available by scanning and in the Bluetooth Advertisement
   
      2nd parameter is password  : enter the Bluetooth password configured for you tag to allow EN12830 operations 
   
      3rd parameter are filters  : for the options associated to the fonction
               -a, --start => Start the data logger. Start recording all the data according to the loggin period configured in the tag
               -r <file>, --read <file> => Read the content of data logger and export it on a output file
               -o, --stop => Stop the data logger. Stop recording data into the tag