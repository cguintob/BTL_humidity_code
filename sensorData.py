import serial               # Lets the Arduino send its information to the server
import datetime             # Contains information about the date and time of either current moments or moments in the past and future
from datetime import date   # Module in "datetime" that specifically accesses the date
import sys                  # Allows the user to use command line arguments

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
    print("Use the following format: python sensorData.py [integer] [datafile].txt\n")
    sys.exit(1)

# Sensor Data
try:
    if (sys.argv[2].endswith(".txt")):
        file1 = sys.argv[2]
    else:
        print("Use the following format: python sensorData.py [integer] [datafile].txt\n")
        sys.exit(1)
except IndexError:
    print("Use the following format: python sensorData.py [integer] [datafile].txt\n")
    sys.exit(1)

''' ================================================================================================================== '''
''' ============================================ PART 2: DATA COLLECTION ============================================= '''
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
                    cur_time = datetime.datetime.now().strftime("%H:%M:%S")   # Named "cur_time" for "current time" so it didn't conflict with time module (if I included it)
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
                            data_file.write(str(cur_time))
                            data_file.write(" ")
                            data_file.write(str(data))
                            data_file.write(" ")
                            print(str(day) + " " + str(cur_time))
                            print("Sensor {0}".format(int(port_num) + 1))
                            print("Humidity: " + data + "%")
                        else:
                            data_file.write(str(data))
                            print("Temperature: " + data + "\u00B0C\n\n")
                            data_file.write("\n")
                            data_file.close()
                        counter += 1
        except KeyboardInterrupt:
            print("\nKeyboardInterrupt")
            sys.exit(1)     

''' ================================================================================================================== '''
''' ============================================== PART 3: SERIAL PORTS ============================================== '''
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
''' ============================================ PART 4: ACKNOWLEDGEMENTS ============================================ '''
''' ================================================================================================================== '''

# Code written by Christian Guinto-Brody for Professor Chris Neu's research group.
