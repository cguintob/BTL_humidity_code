## OVERVIEW
This is a side-project of the BTL research and development project. The aim is 
to measure the relative humidity and temperature in the assembly rooms where
sensor modules are being cured to understand better the environment in which
they're being cured.

We use an Elegoo MEGA2560 R3 Arduino board with a fully calibrated ASAIR AHT10
humidity and temperature sensor connected to it to gather the data. The Arduino
code is written in C++ and, once run, sends its data to a script written in 
Python, which receives the data from the Arduino and organizes it into a text
file. Then, we use another Python script to plot the data. A detailed
description of the project can be found in
`Guinto-Brody_BTL_Humidity_Sensor_Project_2024.pdf`.


## REPOSITORY CONTENTS
### Sensor Files
`aht10.ino` --- Initializes the sensor, measures humidity and temperature in 
room, and sends information to serial port  
`AHTxx.cpp` --- Arduino library  
`AHTxx.h`   --- Header file for arduino library

### Python Scripts
`sensorData.py` --- Takes sensor data from serial port and writes it to data 
file; fetches weather data from Charlottesville using WTTR and writes it to 
separate data file  
`dataReader.py` --- Reads data from files and plots it  
`otherDataReader.py` --- Used like `dataReader.py` but without weather data from
Charlottesville  
`sensorData.py~` `dataReader.py~` `otherDataReader.py~` --- Backup versions of 
each script

### Data Files, Plots, and Other Results
`merged_data.txt` --- Contains all data taken since the start of the project; 
shows example of data format  
`all_humidities_until_5-2.png` `all_temperatures_until_5-2.png` --- Plots of all
 data (used `merged_data.txt` for data and `otherDataReader.py` for plotting)  
`humidities_apr-30_may-2.png` `temperatures_apr-30_may-2.png` --- Plots of local
 and Charlottesville data between 4/30/2024 and 5/2/2024 (used `dataReader.py` 
for plotting)  
`Guinto-Brody_BTL_Humidity_Sensor_Project_2024.pdf` --- Report about project 
that contains above plots

### Miscellaneous/Housekeeping
`README.md` --- Contains information about project and how to use programs  
`.gitignore.txt` --- Contains files that are not tracked by Git (includes backup version `.gitignore.txt~`)  
`.gitattributes` --- Used for pushing files that are larger than the maximum allowed size for pushing


## USING `aht10.ino`
The first section of `aht10.ino` initializes the sensor to do the following:
1. Begin collecting data after 9600 ms
2. Print "Starting up..."
3. Check to see if the sensor is running and, if not, delay the data collection 
by 5000 ms and print "Sensor not running."
4. Print "AHT10 running" and set the cycle mode if the sensor is running.  

The second section of the program is an infinite loop that collects measurements
 indefinitely via the following:
1. Define the variable "humidity" to be the humidity measured by the sensor. The
 definition accesses a function in `aht10` that measures the humidity. 
2. Define the variable "temperature" in the same way, but pass through the 
respective function the opposite boolean so that the measurements are separate.
3. Print the values to the serial monitor.
4. Get the next measurement after 1000 ms.

To execute `aht10.ino`, use the following command: 

`arduino --upload --port [SERIAL PORT] [PROGRAM].ino`

The components of the command are the following:
1. `arduino` --- The executing function
2. `--upload` --- Builds and compiles the program for use
3. `--port` --- Signals to the program to print to the serial port. If it's not 
specified, it will use the last used port, so it's good to specify so we print
to the port we want.
4. `[SERIAL PORT]` --- The serial port to which we print. We use `/dev/ttyACM0`
5. `[PROGRAM].ino` --- The Arduino program. Ours is `aht10.ino`

NOTE: When you execute this command, the sensor will *not* appear to be 
collecting measurements; however, it is. Check the serial monitor on the Arduino
 interface to be sure, or execture `sensorData.py` to see the values printed to 
the screen.


## USING `sensorData.py`
`sensorData.py` is used with the following command:

`python sensorData.py [DATA FILE 1].txt [DATA FILE 2].txt`
1. `python` --- The executing function
2. `sensorData.py` --- The Python program
3. `[DATAFILE 1].txt` --- The necessary data file. Includes measurements from 
the sensor.
4. `[DATAFILE 2].txt` --- The *optional* data file. includes measurements from 
Charlottesville usign WTTR. When nothing is passed, `default_weather_data.txt` 
is used.

After the program is run, it will print whatever is sent to the serial port by
`aht10.ino` to the screen. Those values, as well as the date and time of the 
measurement and an index used for plotting, are then written to the first data 
file (they're actually appended so no data is lost).

The unique features of this program are its use of `requests` and `keyboard`, 
two Python libraries that allow the program to fetch information from websites 
and allow the user keyboard functionality when operating the program. 

`requests` is used to get Charlottesville humidity, temperature, and 
precipitation values using WTTR, a "console-oriented weather forecast service" 
that allows users to collect meteorological data from anywhere in the world. 
The point of collecting this data for our purposes is to compare our measured 
values from the sensor with those outside in the city to see how the measured 
values fluctuate with the outside environment. This data is written to the 
second data file. `keyboard` allows the user to stop collecting data when they 
hit the spacebar. When the spacebar is hit, the program will terminate and plot 
the data using `dataReader.py`, which is imported into the program.

NOTE: Because `keyboard` only works with root access, the user must be logged in
 as a root user to execute the function. This can be accomplished by running the
 following command:

`sudo su`

The user will then be prompted to enter their password. After that is entered, 
the program should be freely usable.


## USING `dataReader.py` and `otherDataReader.py`
After the user hits the spacebar, `sensorData.py` will pass the two data files 
to which it was writing to `dataReader.py`, which will then plot them. 

`dataReader.py` contains a special function called `number`, which takes two 
data files and another extra value as inputs. When used with `sensorData.py`, 
the extra value is set to be 1, letting the program know that it is being used 
with `sensorData.py` and that the two data files are those written to. When not 
used with `sensorData.py`, the extra value must be set to a value *not* equal to
 1, letting the program know that it is being used *in the command line*. In 
this situation, the program is executed as follows:

`python dataReader.py [DATA FILE 1].txt [DATA FILE 2].txt [NUMBER]`

As before, `[DATA FILE 1].txt` contains measurements from the sensor while 
`[DATA FILE 2].txt` contains measurements from WTTR (that were previously 
collected). If nothing is passed for the latter file, `default_weather_data.txt`
 will be used.

A similar program is `otherDataReader.py` and is executed with the following 
command:

`python otherDataReader.py [DATA FILE].txt`

This program takes only one file *for sensor measurements*. It is not to be used
 with WTTR data.


## SUMMARY
The following commands, in order, are how to run and plot the data from the 
sensor:
1. `arduino --upload --port /dev/ttyACM0 aht10.ino`
2. `sudo su`
3. `python sensorData.py [DATA FILE 1].txt [DATA FILE 2].txt`
4. `space`

If there is already data available, use this command (can be run as a root user 
*or* not as a root user):

`python dataReader.py [DATA FILE 1].txt [DATA FILE 2].txt`

If the user wishes not to plot Charlottesville weather data, use this command:

`python otherDataReader.py [DATA FILE].txt`


## TROUBLESHOOTING
### Check Permissions on Files and Programs
If a program isn't working, check the permissions on it using the following 
command:

`ls -l`

If the desired file has root permissions, use the following command to change it
 to user permissions:

`sudo chown [USER]:[USER] [FILE NAME]`

`[USER]` is the name of the user found if you execute `pwd` (or when looking at 
the current directory) while `[FILE NAME]` is the file for which you want to 
change permissions. This command works if you are not a root user at the moment,
 and it will ask you to enter your sudo password. If you are a root user at the 
moment, omit `sudo` from the command.

### Humidity and Temperature Values Switch
Sometimes, when executing `sensorData.py`, the timing gets off with the sensor 
and the values that are listed as humidities are actually temperatures and vice 
versa. To fix this, simply use `Ctrl-C` or `Ctrl-Z` (the latter is slightly
nicer to the program) and rerun the command with different data files.

### Can't Push Files to GitHub
Sometimes changes to your files and those that appear on GitHub become out of 
sync. This can happen if you accidentally commit something but forget to push it
 or if you modify your files in GitHub when you usually do it on the command 
line. To check the status of Git, execute the following command:

`git status`

This command will let you know whether your changes are up to date. If they 
aren't, you'll be ahead or behind by a certain number of commits. To fix this, 
execute the following command:

`git reset --soft origin/[BRANCH NAME]`

You can determine the branch name by running `git branch --show-current`.