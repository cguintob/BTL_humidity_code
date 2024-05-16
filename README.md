## OVERVIEW
This is a side-project of the BTL research and development project. The aim is to measure the relative humidity and temperature in the assembly rooms where sensor modules are being cured to understand better the environment in which they're being cured.

We use an Elegoo MEGA2560 R3 Arduino board with a fully calibrated ASAIR AHT10 humidity and temperature sensor connected to it to gather the data. The Arduino code is written in C++ and, once run, sends its data to a script written in Python, which receives the data from the Arduino and organizes it into a text file. Then, we use another Python script to plot the data. A detailed description of the project can be found in `Guinto-Brody_BTL_Humidity_Sensor_Project_2024.pdf`.


## REPOSITORY CONTENTS
### Sensor Files
`aht10.ino` --- Initializes the sensor, measures humidity and temperature in room, and sends information to serial port  
`AHTxx.cpp` --- Arduino library  
`AHTxx.h`   --- Header file for arduino library

### Python Scripts
`sensorData.py` --- Takes sensor data from serial port and writes it to data file; fetches weather data from Charlottesville using WTTR and writes it to separate data file  
`dataReader.py` --- Reads data from files and plots it  
`otherDataReader.py` --- Used like `dataReader.py` but without weather data from Charlottesville  
`sensorData.py~` `dataReader.py~` `otherDataReader.py~` --- Backup versions of each script

### Data Files, Plots, and Other Results
`merged_data.txt` --- Contains all data taken since the start of the project; shows example of data format  
`all_humidities_until_5-2.png` `all_temperatures_until_5-2.png` --- Plots of all data (used `merged_data.txt` for data and `otherDataReader.py` for plotting)  
`humidities_apr-30_may-2.png` `temperatures_apr-30_may-2.png` --- Plots of local and Charlottesville data between 4/30/2024 and 5/2/2024 (used `dataReader.py` for plotting)  
`Guinto-Brody_BTL_Humidity_Sensor_Project_2024.pdf` --- Report about project that contains above plots

### Miscellaneous/Housekeeping
`README.md` --- Contains information about project and how to use programs  
`.gitignore.txt` --- Contains files that are not tracked by Git (includes backup version `.gitignore.txt~`)  
`.gitattributes` --- Used for pushing files that are larger than the maximum allowed size for pushing


## USING `aht10.ino`
The first section of `aht10.ino1` initializes the sensor to do the following:
1. Begin collecting data after 9600 ms
2. Print "Starting up..."
3. Check to see if the sensor is running and, if not, delay the data collection by 5000 ms and print > Sensor not running.
4. Print "AHT10 running" and set the cycle mode if the sensor is running.  
The second section of the program is an infinite loop that collects measurements indefinitely via the following:
1. Define the variable "humidity" to be the humidity measured by the sensor. The definition accesses a function in `aht10` that measures the humidity. 
2. Define the variable "temperature" in the same way, but pass through the respective function the opposite boolean so that the measurements are separate.
3. Print the values to the serial monitor.
4. Get the next measurement after 1000 ms.

To execute `aht10.ino`, use the following command: `arduino --upload --port [SERIAL PORT] [PROGRAM.ino]`

The components of the command are the following:
1. `arduino` --- The executing function
2. `--upload` --- Builds and compiles the program for use
3. `--port` --- Signals to the program to print to the serial port. If it's not specified, it will use the last used port, so it's good to specify so we print to the port we want.
4. `[SERIAL PORT]` --- The serial port to which we print. We use `/dev/ttyACM0`
5. `[PROGRAM.ino]` --- The Arduino program. Ours is `aht10.ino`

NOTE: When you execute this command, the sensor will NOT appear to be collecting measurements; however, it is. Check the serial monitor on the Arduino interface to be sure, or execture `sensorData.py` to see the values printed to the screen.