''' This script talks with the Arduino to create a data file
that contains information about the relative humidity and
temperature in the production room at points in time. When
the Arduino sends its data to the "server," this script
(which is run with "python sensorData.py" after the Arduino
code has finished uploading) takes the data, splices it,
and puts each value into a data file when the value arrives. '''

''' "Serial" lets the Arduino send its information to the server,
where the Python script can access it. "Datetime" contains
information about the date and time of either the current
moment or moments in the past and future. "Date" is a module
in "Datetime" that specifically accesses the date. "Sys" allows the
user'''
import serial             # Lets the Arduino send its information to the server
import datetime           # Contains information about the date and time of either current moments or moments in the past and future
from datetime import date # Module in "datetime" that specifically accesses the date
import sys                # Allows the user to use command line arguments
import requests           # Allows the user to get information from a url

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

    ''' This variable lets us change the data file without 
    modifying too much code. '''
    file1 = sys.argv[1]
    file2 = sys.argv[2]

    ''' This section of code empties the data files each time it is 
    run so that only the data from the most recent run are collected. '''
    init_file1 = open(file1, "w")
    init_file1.write("")
    init_file1.close

    init_file2 = open(file2, "w")
    init_file2.write("")
    init_file2.close

    # This while loop reads the code if the Arduino sends data to it.
    while True:

        ''' Each data point is taken from serial, read, decoded, 
        and stripped into a format the Python program can understand. ''' 
        data = ser.readline().decode().strip()
        
        ''' The Arduino sends some extraneous information I don't want 
        in the data file, but I let the Python program report it. '''
        if ((data == "Starting up...") or (data == "Sensor not running.") or (data == "AHT10 running")):
            print(data)

        # These things are sent by the Arduino and shouldn't be included.
        elif ((data == "") or (data == "0.00") or (data == "-50.00") or (data == "..") or (data == "up..")):
            continue

        # This is only run if we're collecting a set number of measurements.
        elif (data == "Done!"):
            print(data)
            break

        # This actually puts the data into a data file.
        else:
     
            ''' Day gives the current date; time gives the current time 
            in hours:minutes. '''
            day = date.today()
            time = datetime.datetime.now().strftime("%H:%M")
            
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
                print("Humidity: " + data + "%")

            # This writes the temperature to the data file.
            else:
                data_file.write(str(data))
                print("Temperature: " + data + " C")
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
                url = "https://wttr.in/Charlottesville?format=%h+%t+%p"
                res = requests.get(url)
                converted_string = res.text.translate({ord(i): None for i in "%+F\xb0mm"}) # Replaces all these delimiters with ""
                weather_data.write(str(converted_string))
                weather_data.write("\n")
                weather_data.close()
                count_for_wttr += 1

            counter += 1

''' It's important to note that I open and close the data file each
time I add a new set of measurements (hence why I use "a" instead of
"w". I did this in case we need to stop data collection but didn't
want to lose our data. By continuously opening and closing the file,
we save the data, preventing it from being lost. '''

# This tells the program where to look for the AHT10 program.
if __name__ == '__main__':
    readserial('/dev/ttyACM0', 9600, True)
    # COM port, Baudrate, Show timestamp
    







'''-------------------------------------------------------------------------'''


'''
            # This uses wttr to get the current weather conditions
            weather_data = open(file2, "a")
            weather_data.write(str(counter))
            weather_data.write(" ")
            weather_data.write(str(day))
            weather_data.write(" ")
            weather_data.write(str(time))
            weather_data.write(" ")
            url = "https://wttr.in/Charlottesville?format=%h+%t"
            res = requests.get(url)
            weather_data.write(res.text.split(chr(int(u'\xb0'))))
            weather_data.write("\n")
            weather_data.close() '''






''' The code from here on are ideas I was testing and didn't work. '''

# import matplotlib.dates as dates
# time = dates.date2num(datetime.datetime.now())

# timestamps.append(str(time))
# array.append(data)

# array = []
# timestamps = []
# humidities = []
# temps = []
   

'''
  elif (data == "Done gathering data!"):
            print(data)
            for x in range(len(array)):
                if (x % 2 != 1):
                    humidities.append(array[x])
                else:
                    temps.append(array[x])
            print("Done!")
            break
      '''


'''
    data_file = open("data_filel.txt", "w")
    for x in range(int(0.5 * len(array))):
        # data_file = open("data_file.txt", "a")
        data_file.write(timestamps[x])
        data_file.write(" ")
        data_file.write(humidities[x])
        data_file.write(" ")
        data_file.write(temps[x])
        data_file.write("\n")
        # data_file.close()
    data_file.close()
'''
    

'''if (counter % 2 == 0):
                data_file = open("data_file.txt", "a")
                data_file.write(str(time))
                data_file.write(" ")
                data_file.write(str(data))
                data_file.write(" ")
            else:
                data_file.write(str(data))
                data_file.write("\n")
                data_file.close()
            '''


'''
if (counter > 100):
                for x in range(len(array)):
                    if (x % 2 == 0):
                        y = int(0.5 * x)
                        print(y, x)
                        humidities.append(array[x]) 
                        print(array[x])
                    else:
                        y = int(0.5 * x + 0.5)
                        temps[y] = array[x]
                        # print(temps[y])
                        # for x in range(100):
                        # print(humidities[x], temps[x])
                print("Done!")
                break
'''

























# import serial
# from datetime import datetime

# today = str(datetime.today().date())
# print("today is " +  today)

'''
sensor = "AHT10"
serial_port = '/dev/ttyACM0'
baud_rate = 9600
path = "%s_LOG_%s.txt" % (str(datetime.now()), sensor)
ser = serial.Serial(serial_port, baud_rate)
with open(path, 'w+') as f:
    while True:
        line = ser.readline()
        f.writelines([line.strip(), " t = %s \n " % (datetime.now())])
'''




        # if data and timestamp:
        #    timestamp = time.strftime('%H:%M:%S')
        #    print(timestamp > data)
        # elif data:




# converted_string = re.split("[%+F\xb0]", res.text)
            # converted_string = re.sub("[^%d]", "", res.text)
            # converted_string = res.text.translate({ord("\xb0"): None})
            # converted_string = re.translate({ord("[\xb0+%F]"): None})
            
