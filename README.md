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
`AHTxx.h`   --- Header file for Arduino library

### Python Scripts
`sensorData.py` --- Takes sensor data from serial port and writes it to data 
file; fetches weather data from Charlottesville using WTTR and writes it to 
separate data file  
`NEW_READER.py` --- An updated plotting script that uses pandas; can plot an 
arbitrary number of data files (in a new format) in any order and can plot 
updating data

### Data Files, Plots, and Other Results
`EXAMPLE_hums_graph.png` `EXAMPLE_temps_graph.png` --- Example graphs in the 
new format 
`2024-06-06---17:53:43_to_2024-06-08---06:52:38.png` --- Example graph in 
the revised format (both humidities and temperatures are plotted on the 
same graph  
`Guinto-Brody_BTL_Humidity_Sensor_Project_2024.pdf` --- Report about project  
`EXAMPLE_sensor_0.txt` `EXAMPLE_weather.txt` `EXAMPLE_sensor_1.txt` --- Data 
files taken between 5/24/2024 at 3:23.47 pm and 5/26/2024 at 1:28:29 am in 
the new format

### Miscellaneous/Housekeeping
`README.md` --- Contains information about project and how to use programs  
`.gitignore.txt` --- Contains files that are not tracked by Git (includes backup
 version `.gitignore.txt~`)  
`.gitattributes` --- Used for pushing files that are larger than the maximum 
allowed size for pushing


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
2. Define the variable "temperature" in the same way but pass through the 
respective function the opposite Boolean so that the measurements are separate.
3. Print the values to the serial monitor.
4. Get the next measurement after a certain number of ms (in our case, after
 1000 ms).

Depending on the PC used (i.e. an old Centos7 system, Geekom), different
commands must be used to execute the Arduino from the command line.

### Old CentOS7 System
To execute `aht10.ino`, use the following command: 

`arduino --upload --port [SERIAL PORT] [PROGRAM].ino`

The components of the command are the following:
1. `arduino` --- The executing function
2. `--upload` --- Builds and compiles the program for use
3. `--port` --- Signals to the program to print to the serial port. If it's not 
specified, it will use the last used port, so it's good to specify so we print
to the port we want
4. `[SERIAL PORT]` --- The serial port to which we print. We use `/dev/ttyACM0`,
but that only depends on which COM port is being used. For the machine being
used, we can change the number after "ACM" to switch the port
5. `[PROGRAM].ino` --- The Arduino program. Ours is `aht10.ino`

NOTE: When you execute this command, the sensor will *not* appear to be 
collecting measurements; however, it is. Check the serial monitor on the Arduino
 interface to be sure, or execute `sensorData.py` to see the values printed to 
the screen.

NOTE: `aht10.ino` can collect measurements indefinitely or after a set amount of
 time. This can be done by modifying the code so that the appropriate sections 
are or aren't commented out. The user can also modify how many points per second
 are collected and how long they want to collect data for, if this is how they 
want to use the program.

NOTE: This code can be executed using the Arduino IDE, as well. In fact, this 
may be the optimal method of running the Arduino. However, I like running it 
from the command line to keep everything in the command line. It is important to
 note that to do this, `aht10.ino`, `AHTxx.cpp`, and `AHT10xx.h` must be 
contained in a folder. Otherwise, the code will not work.

### Geekom PC
First, the Arduino client `arduino-cli` must be installed onto the PC and placed
 in the directory where the code will be run. Once it is installed, we can
compile and upload the Arduino script using the following commands:

`./arduino-cli compile -b [BOARD NAME] [FILE PATH]/[FILE NAME]`
`./arduino-cli upload -p [PORT] [FILE PATH]/[FILE NAME]`

The flag `-p` stands for "port," which is used above. The flag `-b` stands for
"board," which is the Arduino board recognized by the IDE (if the board isn't 
recognized, it must be installed). One can find the board name of the Arduino by
 running the following command:

`./arduino-cli board list`

The board name will be under the "FQBN" column, which stands for "Fully 
Qualified Board Name." The file path and name are self explanatory.


## USING `sensorData.py`
`sensorData.py` is used with the following command:

`python sensorData.py [INTEGER] [DATA FILE 1].txt [DATA FILE 2].txt`
1. `python` --- The executing function
2. `sensorData.py` --- The Python program
3. `[INTEGER]` --- A number telling the program which serial port to use
4. `[DATAFILE 1].txt` --- Includes measurements from the sensor
5. `[DATAFILE 2].txt` --- Includes measurements from Charlottesville using WTTR

After the program is run, it will print whatever is sent to the serial port by
`aht10.ino` to the screen. Those values, as well as the date and time of the 
measurement and an index used for plotting, are then written to the first data 
file (they're actually appended so no data is lost).

5/24/2024 UPDATE: Instead of plotting an index, `sensorData.py` now plots the 
serial port number in the first column. This is useful for using 
`NEW_READER.py`.

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
hit the spacebar. When the ALT button is hit, the program will terminate.

NOTE: Because `keyboard` only works with root access, the user must be logged in
 as a root user to execute the function. This can be accomplished by running the
 following command:

`sudo su`

The user will then be prompted to enter their password. After that is entered, 
the program should be freely usable.


## USING `NEW_READER.py`
This new program takes an arbitrary number of data files in any order and plots 
them all on graphs. It is used as follows:

`python NEW_READER.py [DATA FILE 1].txt [DATA FILE 2].txt [DATA FILE 3].txt ...`

The reasons it takes an arbitrary number of files are:
1. There are multiple sensors running at the same time.
2. There is data from multiple time periods.

`NEW_READER.py` can plot data from just one sensor, multiple sensors, just one
 file of weather data, or multple sensors with a file of weather data, across 
differing time periods for each. The files can be passed in any order to 
prevent mistakes in plotting.

The nice thing about `NEW_READER.py` is that it can display the data as it 
is being taken and will only stop plotting if all the data files have finished 
updating. This was implemented 6/8/2024 -- 6/10/2024 and allows the user to see 
the data as it is updating and make decisions about where to go from there.

NOTE: Multiple weather data files can be passed *if they are not on the same 
time interval*. Just make sure you know which files include weather data 
and which don't.


## SUMMARY
The following commands, in order, are how to run and plot the data from the 
sensor:
1. `arduino --upload --port [PORT] aht10.ino`
2. `sudo su`
3. `python sensorData.py [INTEGER] [DATA FILE 1].txt [DATA FILE 2].txt`
4. `alt`

If we are using a Geekom PC, switch command #1 with the following commands:

1. `./arduino-cli compile -b [BOARD NAME] [FILE PATH]/[FILE NAME]`
2. `./arduino-cli upload -p [PORT] [FILE PATH]/[FILE NAME]`

To plot the data, using the following command:

`python NEW_READER.py [DATA FILE 1].txt [DATA FILE 2].txt [DATA FILE 3].txt ...`

NOTE: You can also specify a file path to a data file in another directory. And 
if the files all have a common beginning, you can use the `*` method to use them 
all with the script. As an example:

`python NEW_READER.py data_runs/run000001*`

This example assumes you are in the directory where `NEW_READER.py` is 
located and that the directory `data_runs/` is a subdirectory of your current 
working directory.


## TROUBLESHOOTING
### Check Permissions on Files and Programs
If a program isn't working, check the permissions on it using the following 
command:

`ls -l(h)`

(The `-h` flag stands for "human-readable format" and displays everything in a
more comprehensible format.)

If the desired file has root permissions, use the following command to change it
 to user permissions:

`sudo chown [USER]:[USER] [FILE NAME]`

`[USER]` is the name of the user found if you execute `pwd` (or when looking at 
the current directory) while `[FILE NAME]` is the file for which you want to 
change permissions. This command works if you are not a root user at the moment,
 and it will ask you to enter your sudo password. If you are a root user at the 
moment, omit `sudo` from the command.

You can change the read (r), write (w) and execute (x) permissions on a file by
using the following command:

`sudo chmod +(-)r(w)(x) [FILE(DIRECTORY)]`

You can add "+" (or remove "-") any combination of r, w, and x on a file or
directory. If you're already acting as a root user, you can omit `sudo`.

### Humidity and Temperature Values Switch
Sometimes, when executing `sensorData.py`, the timing gets off with the sensor 
and the values that are listed as humidities are actually temperatures and vice 
versa. To fix this, simply use `Ctrl-C` or `Ctrl-Z` (the latter is slightly
nicer to the program) and rerun the command with different data files.

NOTE: This bug was fixed by editing `aht10.ino` to send `sensorData.py` a 
counter. `sensorData.py` will then determine whether that counter is odd or 
even, and depending on which it is, it will write temperature or humidity 
measurements to the data file.

### Can't Push Files to GitHub
Sometimes, changes to your files and those that appear on GitHub become out of 
sync. This can happen if you accidentally commit something but forget to push it
 or if you modify your files in GitHub when you usually do it on the command 
line. To check the status of Git, execute the following command:

`git status`

This command will let you know whether your changes are up to date. If they 
aren't, you'll be ahead or behind by a certain number of commits. To fix this, 
execute the following command:

`git reset --soft origin/[BRANCH NAME]`

You can determine the branch name by running `git branch --show-current`.

### Removing Files from GitHub but not Local Directory

Use the following commands:

`git rm --cached [FILES]`  
`git commit -m "[MESSAGE]"`  
`git push`

This series of commands is similar to adding files to GitHub, but instead 
of just saying `rm` in this case, you must include `--cached`; otherwise,
 your files will be deleted from your local directory, too.

### Getting Changes Pushed from One Local Repository to Another
If your GitHub repository is connected to several different local repositories
on different machines and you make changes to your files on one repository but
not another, you will first need to push your changes to GitHub from your
current local repository (call it R1 for our purposes) and then pull the
changes pushed to GitHub to the other local repository (call it R2).

In R2, run the following command:

`git pull`

You may be prompted to enter your sudo password. If so, enter it. The changes
you made in R1 will then be given to R2. It is important to note that if you
made changes to the files in R2, they will be overwritten by the changes you
made in R1. Either copy the files if you want to record those changes
somewhere or accept defeat.

### Initializing Repository and Connecting to GitHub
Check to see if git is installed on the machine you want to connect to
GitHub by running the following command:

`git --version`

If git is installed, it will return the version of git on the machine. If
not, install git using either a Debian/Ubuntu system installation (top) or
 a Fedora/CentOS system installation (bottom):

`sudo apt-get update` + `sudo apt-get install git-all`
`sudo dnf(yum) update` + `sudo dnf(yum) install git-all`

Create a directory where you want to initialize git and type the following
command:

`git init`

You must create a new SSH key and connect it to your GitHub repository. To
do this, run the following command:

`ssh-keygen -t ed25519 -C [GITHUB EMAIL]`

where your GitHub email is the email to which your GitHub is linked.

Next, start the ssh-agent in the background with the following command:

`eval "$(ssh-agent -s)"`

Then, add your key to the ssh-agent with the following command:

`ssh-add ~/.ssh/id_ed25519`

Once this is done, copy the SSH key to the clipboard. It can be found by
using the following command:

`cat ~/.ssh/id_ed25519.pub`

Then, go to your GitHub account and click "Settings." Under the "Access"
section of the sidebar, click "SSH and GPG Keys." Click "New SSH Key" and
title the key to fit your needs. After selecting the key type, paste the key
 to the field and click "Add SSH Key." The key should be ready for use now.

If you have a repository on GitHub already, you can clone that repository to
 your local directory with the following command:

`git clone git@github.com:[USERNAME]/[REPOSITORY].git`

where your username is your GitHub username and the repository is the
repository you want to clone.

If you don't have a repository on GitHub already, you can use the series of
 commands in the directory where you have the code you want to track with
git:

`git add [FILES]`  
`git commit -m "[MESSAGE"]`  
Click "New Repository" in GitHub, name it the same as your directory, and
click "Create Repository"  
`git remote add origin git@github.com:[USERNAME]/[REPOSITORY].git`  
`git push -u origin master`

The repositories should be linked now. Ideally, you'll create a `README.md` file
 and a `.gitignore.txt` file.

### Merging Data into One File
To merge different datasets into one file, simply use the following command:

`cat [DATA FILE 1].txt [DATA FILE 2].txt ... > [MERGED DATA FILE].txt`

### `NEW_READER` Gives Shaded Area instead of Line
This is a result of using multiple weather data files along the same time 
period. Use only one.

### `NEW_READER.py` Taking Long Time to Load
Just be patient. It's working, I promise.