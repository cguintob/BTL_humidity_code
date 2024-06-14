import serial               # Lets the Arduino send its information to the server
import datetime             # Contains information about the date and time of either current moments or moments in the past and future
from datetime import date   # Module in "datetime" that specifically accesses the date
import sys                  # Allows the user to use command line arguments
import requests             # Allows the user to get information from a url
import random               # Necessary for changing the user-agent used for fetching WTTR data
import time                 # Necessary for addressing requests.exceptions.ConnectionErrors

''' ================================================================================================================== '''
''' ==================================================== OVERVIEW ==================================================== '''
''' ================================================================================================================== '''

''' This script talks with the Arduino to create a data file that contains 
information about the relative humidity and temperature in the production room 
at points in time. When the Arduino sends its data to the "server," this script
(which is run with "python sensorData.py" after the Arduino code has finished 
uploading) takes the data, splices it, and puts each value into a data file when
the value arrives. '''

''' ================================================================================================================== '''
''' ========================================= PART 1: COMMAND-LINE ARGUMENTS ========================================= '''
''' ================================================================================================================== '''

''' To prevent modifying too much code each time I wanted to run a new data 
file, I made the user input their desired data files in the command line for the
program to write to. This code checks to see if the arguments were supplied. If
they were, then define the files and continue; if they weren't, either stop the
program or define a default data file.

UPDATE: I have since added a system argument for the COM port so that I can use
multiple Arduino boards at the same time. Each board connects to a different USB
port on the PC, which means they each have a different COM port. So, the user
can indicate which board they want to use based on the COM port they feed the
program. This update was added 5/17/2024. '''

''' ================================================================================================================== '''

# Port
try:
    port_num = sys.argv[1]
except IndexError:
    print("Use the following format: python sensorData.py [integer] [datafile1].txt [datafile2].txt\n")
    sys.exit(1)

# Sensor Data
try:
    if (sys.argv[2].endswith(".txt")):
        file1 = sys.argv[2]
    else:
        print("Use the following format: python sensorData.py [integer] [datafile1].txt [datafile2].txt\n")
        sys.exit(1)
except IndexError:
    print("Use the following format: python sensorData.py [integer] [datafile1].txt [datafile2].txt\n")
    sys.exit(1)

# Weather Data
try:
    if (sys.argv[3].endswith(".txt")):
        file2 = sys.argv[3]
    else:
        print("Use the following format: python sensorData.py [integer] [datafile1].txt [datafile2].txt\n")
        sys.exit(1)
except IndexError:
    print("Use the following format: python sensorData.py [integer] [datafile1].txt [datafile2].txt\n")
    sys.exit(1)

''' ================================================================================================================== '''
''' ====================================== PART 2: FETCHING DATA FROM WEBSITES ======================================= '''
''' ================================================================================================================== '''

''' I intended to leave my code running for about five days in between my 
Thursday work and Tuesday research meeting and then show a plot of my 
measurements at the meeting, but at about 6 pm after I left, my code "crashed," 
leaving the WTTR data incomplete (i.e. the index and date were printed to the 
data file but the humidity and temperature were not). The reason for the "crash"
was the following error: 

requests.exceptions.SSLError: EOF occurred in violation of protocol (_ssl.c:618)

This error, as I understand, is a result of the server and the website becoming 
out of sync, possibly due to overload (I was fetching data from the website 
every second for several hours before the "crash." So, I opened a session, which
allows for the persistence of certain parameters across requests. The first 
line defines a session opened by requests, the second line defines an adapter 
(used to define interaction methods for an HTTP service, and the third line 
defines a prefix for which the adapter is to be used (any website with this 
prefix will use the adapter. This code was implemented 4/30/2024.

UPDATE 5/3/2024: I added the retry line because my code timed out after about 
three days, which is longer than before, but not optimal. 

UPDATE 6/14/2024: My code was STILL timing out (specifically refusing to 
connect), so I added a list of User_Agents that are chosen by the session at 
random (using random.choice()) from which the request will appear to have been. 
Some of the User-Agents in the list are duplicated at random so that some sites 
are visited more often than others. '''

''' ================================================================================================================== '''

user_agents = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
               "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0",
               "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_4_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Safari/605.1.15",
               "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.2420.81",
               "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
               "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
               "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0",
               "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 OPR/109.0.0.0",
               "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
               "Mozilla/5.0 (X11; Linux i686; rv:124.0) Gecko/20100101 Firefox/124.0",
               "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0",
               "Mozilla/5.0 (Macintosh; Intel Mac OS X 14.4; rv:124.0) Gecko/20100101 Firefox/124.0",
               "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0",
               "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_4_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Safari/605.1.15",
               "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_4_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 OPR/109.0.0.0",
               "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
               "Mozilla/5.0 (X11; Linux i686; rv:124.0) Gecko/20100101 Firefox/124.0",
               "Mozilla/5.0 (X11; Linux i686; rv:124.0) Gecko/20100101 Firefox/124.0"]
sess = requests.Session()
retry = requests.packages.urllib3.util.retry.Retry(total = 5, backoff_factor = 0.1, status_forcelist = [500, 502, 503, 504])
adapter = requests.adapters.HTTPAdapter(max_retries = retry)
sess.mount("http://", adapter)

''' ================================================================================================================== '''
''' ============================================ PART 3: DATA COLLECTION ============================================= '''
''' ================================================================================================================== '''

''' This function reads the data stream from the Arduino. The COM port tells 
the program where to look for the data, the baudrate lets the program 
synchronize with the Arduino, while the timestamp tells you when the data was 
collected. In the serial.Serial function, "Serial" must be a module in "serial"
that directs the program to the information from the Arduino. Also, 1/timeout is
the frequency at which the port is read. 

There are many components to this part of the program. First, we have a variable 
called "counter" that's used to determine what parameters each of the incoming 
values represents, and we have an indicator variable named "tester" that 
corrected the switching of humidity and temperature from the Arduino and helps 
to prevent any data from being written to files before the Arduino outputs 
"AHT10 running."

We then have a while loop that reads the code if the Arduino sends data to it. 
Each data point is taken from serial (i.e. the serial port, read by the Python 
modules "serial" and "pySerial."), read, decoded, and stripped into a format 
the Python program can understand. Sometimes, the Arduino sends extraneous 
information or makes errors. If they're important things to note, I print them 
to the screen; otherwise, I ignore them. These constitute the if statement and 
the first elif statement in the while loop.

Next, we have an elif statement that runs only if we're collecting a finite set
of data, which is indicated in aht10.ino. Lastly, we have the else statement, 
which actually writes the data into a data file.

The if part of the if-else statement here ignores any data that comes before 
the message "AHT10 running" (before, I would get data that came before the 
message). The else part has the substance. First, we define the day using the 
function date.today(), as well as the time using the function 
datetime.datetime.now().strftime(), which puts the time in a format we want. 
Then, we have a try-except statement that determines whether measurements are 
being sent through the serial port or if a counter is being sent through the 
serial port. If it's a counter, then it will be an integer, and thus the 
isinstance will be true (I had to typecast the data as an int to begin with 
because the data is sent as a string, so if a counter is sent, then that 
typecast as an int will return true, while if measurements are being sent, 
then they will be floats). I then set that data to a counter in the Python 
script, where it will be used to distinguish whether the measurements are 
humidities or temperatures. If we get a ValueError, that means measurements 
are being sent, so we write them to the data file. Since humidities are sent 
first, we write the humidities first and then increase the counter by 1. 
Then, write the temperatures to the data file.

When the temperatures are being written to the data file, we also call back 
to Part 2 and fetch data from WTTR, which gets the current weather 
conditions in Charlottesville. It only needs to be called once per 
iteration of the Arduino reading, hence why I write it with the temperatures.
First, I define the URL from which I'll be requesting to fetch data. Then, I 
use a try-except statement that will get a new request with a new User-Agent 
if there's no connection error (changing the User-Agent should prevent there 
from being connection errors caused by refusal from the website) and write 
the desired data to the desired data file. If there is a connection error, 
the program will pause for a bit, get a new User-Agent, and continue. 

It's important to note that I open and close the data file each time I add a
new set of measurements (hence why I use "a" instead of "w"). I did this in 
case we need to stop data collection but didn't want to lose our data. By 
continuously opening and closing the file, we save the data, preventing it 
from being lost. '''

''' ================================================================================================================== '''

def readserial(comport, baudrate, timestamp = False):
    ser = serial.Serial(comport, baudrate, timeout = 0.1)  
    counter = 0
    tester = 0
    while True:
        try:
            data = ser.readline().decode().strip()
            if ((data == "Starting up...") or (data == "Sensor not running.") or (data == "AHT10 running")):
                print(data)
                if (data == "AHT10 running"):
                    tester = 1
            elif ((data == "") or (data == "0.00") or (data == "-50.00") or (data == "..") or (data == "up..")):
                continue
            elif (data == "Done!"):
                print(data)
                sys.exit(1)
            else:
                if (tester == 0):
                    continue
                else:
                    day = date.today()
                    time = datetime.datetime.now().strftime("%H:%M:%S")
                    ''' This checks to see if the data from the Arduino 
                    is an integer, indicating that it's a counter. If 
                    that counter is even, a humidity measurement will 
                    be written to the file; if that counter is odd, a 
                    temperature measurement will be written to the 
                    file. This code was implemented 5/17/2024. '''
                    try:
                        if (isinstance(int(data), int) == True):
                            counter = int(data)
                        else:
                            print("Raising ValueError in try portion of try-except statement.")
                            raise ValueError
                    except ValueError:
                        if (counter % 2 == 0):
                            data_file = open(file1, "a")
                            data_file.write(str(port_num))
                            data_file.write(" ")
                            data_file.write(str(day))
                            data_file.write(" ")
                            data_file.write(str(time))
                            data_file.write(" ")
                            data_file.write(str(data))
                            data_file.write(" ")
                            print(str(day) + " " + str(time))
                            print("Sensor {0}".format(int(port_num) + 1))
                            print("Humidity: " + data + "%")
                        else:
                            data_file.write(str(data))
                            print("Temperature: " + data + " C\n\n")
                            data_file.write("\n")
                            data_file.close()
                            url = "http://wttr.in/Charlottesville?format=%h+%t+%p"
                            sess.headers.update({"User-Agent": random.choice(user_agents)})
                            try:
                                res = sess.get(url)
                                converted_string = res.text.translate({ord(i): None for i in "%+F\xb0mm"}) # Replaces all these delimiters with ""
                                weather_data = open(file2, "a")
                                weather_data.write(str(port_num))
                                weather_data.write(" ")
                                weather_data.write(str(day))
                                weather_data.write(" ")
                                weather_data.write(str(time))
                                weather_data.write(" ")
                                weather_data.write(str(converted_string))
                                weather_data.write("\n")
                                weather_data.close()
                            except requests.exceptions.ConnectionError:
                                print("Raising requests.exceptions.ConnectionError")
                                time.sleep(20)
                                print("Ready after 20 seconds of rest.")
                                print("\n")
                                sess.headers.update({"User-Agent": random.cohice(user_agents)})
                                continue     
                        counter += 1
        except KeyboardInterrupt:
            print("\nKeyboardInterrupt")
            sys.exit(1)     
    print("Done!")
    sys.exit(1)

''' ================================================================================================================== '''
''' ============================================== PART 4: SERIAL PORTS ============================================== '''
''' ================================================================================================================== '''

# This tells the program where to look for the AHT10 program.
if __name__ == '__main__':
    if (int(port_num) == 0):
        # Format: readserial([COM port], [Baudrate], [Show timestamp])
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

''' ================================================================================================================== '''
''' ============================================ PART 5: ACKNOWLEDGEMENTS ============================================ '''
''' ================================================================================================================== '''

# Code written by Christian Guinto-Brody for Professor Chris Neu's research group.
