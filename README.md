# Bluetooth-Python-Sample
Different sample to manage bluetooth for raspberry in Python.

## Build
Here you will find the procedure to manage the sample files and run it directly in your environnement. The target environnement tested and available are:
-   [Raspberry-Pi 3B+](#raspberry-pi-3b+)

### Raspberry-Pi 3B+
To execute the different python sample provide by ELA Bluetooth for the bluetooth, you need to install the different environnement or package :
- Python 3.7
- bluetooth.btle
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
To use the scanner programe, you can use the script **my_script.py**

Run the command  : sudo python3.7 my_script.py timescan file.csv "filters"
Describe different parameters:
