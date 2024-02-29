''' This script takes the data from the Arduino that was put
into a data file by sensorData.py and plots it. When running
this script, we do "python dataReader.py," and it will plot
humidity and temperature graphs over time to the screen. '''

# These packages are useful for plotting and for math.
import matplotlib.pyplot as plt
import numpy as np

# Like in sensorData.py, this variable prevents us from changing too much code.
file = "data_one-sec_1.txt"

# These lists will adopt the appropriate values from our data file.
index = []
times = []
humidities = []
temps = []

''' This for loop puts the appropriate data into the appropriate lists.
Note that times[] contains both the data from the second column and the
data from the third column, separated by a newline character. This will
be useful for plotting the labels along the x-axis. '''
for line in open(file, "r"):
    lines = [i for i in line.split()]
    index.append(lines[0])
    times.append(lines[1] + "\n" + lines[2])
    humidities.append(lines[3])
    temps.append(lines[4])

# This section of code plots the humidities.
hum = plt.figure(1)
plt.title("Humidities at Various Times")
plt.ylabel("Relative Humidity (%)")
plt.xticks(np.arange(len(index), step = len(index) / 10), times, fontsize = 8, rotation = 45)
plt.plot(index, humidities, marker = "o", c = "g")
hum.show()

# This section of code plots the temperatures.
temp = plt.figure(2)
plt.title("Temperatures at Various Times")
plt.ylabel("Temperature (C)")
plt.xticks(np.arange(len(index), step = len(index) / 10), times, fontsize = 8, rotation = 45)
plt.plot(index, temps, marker = "o", c = "g")
temp.show()

# This command is necessary for showing the plots separately, for some reason.
input()






'''-----------------------------------------------------------'''



''' Like in sensorData.py, the code from here on are ideas I was testing. '''

# x = [dt.datetime.strptime(d, '%Y-%m-%d').date() for d in dates]

# plt.ylimit(0, 100)
# plt.gca().xaxis.set_major_formatter(dates.DateFormatter('%Y-%m-%d'))
# plt.gca().xaxis.set_major_locator(dates.DayLocator())
# plt.plot_date(timestamps, humidities, marker = "o", c = "g", linestyle = "solid")
