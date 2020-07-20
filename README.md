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

## Execution
To use the scanner programe, you can use the script **bluetooth_scanner_sample.py**

Run the command  : 
```bash
   sudo python3.7 bluetooth_scanner_sample.py <timescan> <file>.csv <"filters">
  ```
Describe different parameters:

      1st parameter is timescan(s): enter a float number to determine the time requiered to scan
   
      2nd parameter is file.csv   : enter a string; that will be your created file's name. Don't forget the '.csv' extension
   
      3rd parameter are filters   : enter a string; that will determinate each word use to filter our 'file.csv' data writed.
                                    You must write your differente filters like this: "filter1;filter2;filter3;..."
                                    This is a contain filter. You will get only data contain your filter word
                                    
     You must to enter the both first paramters. The 3rd parameter (filters) are not required if you don't want to filter data.
