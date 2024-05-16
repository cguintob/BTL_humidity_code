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
`.giattributes` --- Used for pushing files that are larger than the maximum allowed size for pushing


## USING `aht10.ino`
`aht10.ino` must be opened outside the command line. The first section of code initializes the sensor to do the following:
1. Begin collecting data after 9600 ms
2. Print > Starting up...
3. Check to see if the sensor is running and, if not, delay the data collection by 5000 ms and print > Sensor not running.
4. If running, set the cycle mode and print > AHT10 runnning.