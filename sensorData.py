''' This script talks with the Arduino to create a data file
that contains information about the relative humidity and
temperature in the production room at points in time. When
the Arduino sends its data to the "server," this script
(which is run with "python sensorData.py" after the Arduino
code has finished uploading) takes the data, splices it,
and puts each value into a data file when the value arrives. '''

import serial             # Lets the Arduino send its information to the server
import datetime           # Contains information about the date and time of either current moments or moments in the past and future
from datetime import date # Module in "datetime" that specifically accesses the date
import sys                # Allows the user to use command line arguments
import requests           # Allows the user to get information from a url
import keyboard           # Allows for keyboard functionality
import dataReader         # Macro for plotting data

''' To prevent modifying too much code each time I wanted to run a new data file,
I made the user input their desired data files in the command line for the program
to write to. This code checks to see if the arguments were supplied. If they were,
then define the files and continue; if they weren't, either stop the program or
define a default data file.

UPDATE: I have since added a system argument for the COM port so that I can use
multiple Arduino boards at the same time. Each board connects to a different
USB port on the PC, which means they each have a different COM port. So, the user
can indicate which board they want to use based on the COM port they feed the
program. This update was added 5/17/2024. '''
try:
    port_num = sys.argv[1]
except IndexError:
    print("Use the following format: python sensorData.py [integer] [datafile1].txt (OPTIONAL [datafile2].txt)\n")
    sys.exit(1)

try:
    if (sys.argv[2].endswith(".txt")):
        file1 = sys.argv[2]
    else:
        print("Use the following format: python sensorData.py [integer] [datafile1].txt (OPTIONAL [datafile2].txt)\n")
        sys.exit(1)
except IndexError:
    print("Use the following format: python sensorData.py [integer] [datafile1].txt (OPTIONAL [datafile2].txt)\n")
    sys.exit(1)

try:
    if (sys.argv[3].endswith(".txt")):
        file2 = sys.argv[3]
    else:
        print("Use the following format: python sensorData.py [integer] [datafile1].txt (OPTIONAL [datafile2].txt)\n")
        sys.exit(1)
except IndexError:
    print("Use the following format: python sensorData.py [integer] [datafile1].txt (OPTIONAL [datafile2].txt)\n")
    sys.exit(1)

def wait():
    if keyboard.is_pressed("alt"):
        return False
    else:
        return True

''' I intended to leave my code running for about five days in between
my Thursday work and Tuesday research meeting and then show a plot of
my measurements at the meeting, but at about 6 pm after I left, my code
"crashed," leaving the WTTR data incomplete (i.e. the index and date
were printed to the data file but the humidity and temperature were not).
The reason for the "crash" was the following error: 

requests.exceptions.SSLError: EOF occurred in violation of protocol (_ssl.c:618)

This error, as I understand, is a result of the server and the website
becoming out of sync, possibly due to overload (I was fetching data from
the website every second for several hours before the "crash." So, I
opened a session, which allows for the persistence of certain parameters
across requests. The first line defines a session opened by requests, the
second line defines an adapter (used to define interaction methods for an
HTTP service, and the third line defines a prefix for which the adapter is
to be used (any website with this prefix will use the adapter. This code
was implemented 4/30/2024.

UPDATE 5/3/2024: I added the retry line because my code timed out after 
about three days, which is longer than before, but not optimal. '''
sess = requests.Session()
retry = requests.packages.urllib3.util.retry.Retry(total = 5, backoff_factor = 0.1, status_forcelist = [500, 502, 503, 504])
adapter = requests.adapters.HTTPAdapter(max_retries = retry)
sess.mount("http://", adapter)

''' This function reads the data stream from the Arduino. The 
COM port tells the program where to look for the data, the 
baudrate lets the program synchronize with the Arduino, while
the timestamp tells you when the data was collected. In the 
serial.Serial function, "Serial" must be a module in "serial"
that directs the program to the information from the Arduino.
Also,  1/timeout is the frequency at which the port is read. '''
def readserial(comport, baudrate, timestamp = False):
    ser = serial.Serial(comport, baudrate, timeout = 0.1)  

    ''' These counters are used to determine what parameters 
    the values represent. '''
    counter = 0
    count_for_wttr = 0

    ''' This variable is used to correct the switching of the
    humidity and temperature from the Arduino. It predominantly
    helps to prevent any data from being written to files
    before the Arduino outputs "AHT10 running." '''
    tester = 0

    # This while loop reads the code if the Arduino sends data to it.
    while wait():

        ''' Each data point is taken from serial, read, decoded, 
        and stripped into a format the Python program can understand. ''' 
        data = ser.readline().decode().strip()

        ''' The Arduino sends some extraneous information I don't want 
        in the data file, but I let the Python program report it. '''
        if ((data == "Starting up...") or (data == "Sensor not running.") or (data == "AHT10 running")):
            print(data)
            if (data == "AHT10 running"):
                tester = 1
        elif ((data == "") or (data == "0.00") or (data == "-50.00") or (data == "..") or (data == "up..")):
            continue
            
        # This is only run if we're collecting a set number of measurements.
        elif (data == "Done!"):
            print(data)
            dataReader.number(1, 1, file1, file2)
            sys.exit(1)
            
        # This actually puts the data into a data file.
        else:
            if (tester == 0):
                continue
            else:
                ''' Day gives the current date; time gives the current time 
                in hours:minutes:seconds. '''
                day = date.today()
                time = datetime.datetime.now().strftime("%H:%M:%S")
            
                ''' This prevents the data from switching. The
                Arduino now prints a counter to the serial
                monitor, which is heard by Python. This try-
                except statement tests the data to see if it's
                an integer, which indicates that it is the counter.
                If that counter is even, a humidity measurement
                will be written to the file; if that counter
                is odd, a temperature measurement will be
                written to the file. This code was implemented
                5/17/2024. '''
                try:
                    if (isinstance(int(data), int) == True):
                        counter = int(data)
                    else:
                        raise ValueError
                except ValueError:

                    # This writes everything except the temperature to the data file.
                    if (counter % 2 == 0):
                        data_file = open(file1, "a")
                        data_file.write(str(int(0.5 * counter)))
                        data_file.write(" ")
                        data_file.write(str(day))
                        data_file.write(" ")
                        data_file.write(str(time))
                        data_file.write(" ")
                        data_file.write(str(data))
                        data_file.write(" ")
                        print(str(day) + " " + str(time))
                        print("Humidity: " + data + "%")
                        
                    # This writes the temperature to the data file.
                    else:
                        data_file.write(str(data))
                        print("Temperature: " + data + " C\n\n")
                        data_file.write("\n")
                        data_file.close()
                        
                        ''' This uses wttr to get the current weather conditions. It only
                        needs to be called once per iteration of the Arduino reading, so
                        I put it under this else statement. '''
                        weather_data = open(file2, "a")
                        weather_data.write(str(count_for_wttr))
                        weather_data.write(" ")
                        weather_data.write(str(day))
                        weather_data.write(" ")
                        weather_data.write(str(time))
                        weather_data.write(" ")
                        url = "http://wttr.in/Charlottesville?format=%h+%t+%p"
                        res = sess.get(url)
                        converted_string = res.text.translate({ord(i): None for i in "%+F\xb0mm"}) # Replaces all these delimiters with ""
                        weather_data.write(str(converted_string))
                        weather_data.write("\n")
                        weather_data.close()
                        count_for_wttr += 1
                    
                    counter += 1
            
    print("Done!")
    dataReader.number(1, 1, file1, file2)
    sys.exit(1)
            
''' It's important to note that I open and close the data file each
time I add a new set of measurements (hence why I use "a" instead of
"w"). I did this in case we need to stop data collection but didn't
want to lose our data. By continuously opening and closing the file,
we save the data, preventing it from being lost. '''

# This tells the program where to look for the AHT10 program.
if __name__ == '__main__':
    if (int(port_num) == 0):
        readserial('/dev/ttyACM0', 9600, True)
    elif (int(port_num) == 1):
        readserial('/dev/ttyACM1', 9600, True)
    elif (int(port_num) == 2):
        readserial('/dev/ttyACM2', 9600, True)
    elif (int(port_num) == 3):
        readserial('/dev/ttyACM3', 9600, True)
    else:
        print("No COM port specified.")
        sys.exit(1)
    # COM port, Baudrate, Show timestamp
    




# Code written by Christian Guinto-Brody for Professor Chris Neu's research group.
