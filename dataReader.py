''' This script takes the data from the Arduino that was put
into a data file by sensorData.py and plots it. When running
this script, we do "python dataReader.py," and it will plot
humidity and temperature graphs over time to the screen. '''

# These packages are useful for plotting and for math.
import matplotlib.pyplot as plt
import numpy as np

# Like in sensorData.py, this variable prevents us from changing too much code.
file = "data_one-sec_2.txt"

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

''' I implemented this list 3/14/2024. Originally, when I stopped my
two-week-long data collection and I plotted my data, each tick on the
x-axis displayed the same date and time. (I just realized, as I'm
writing this, that it was showing the same date and time because I collected
data every second but only used 10 x-ticks, meaning the 10 ticks were
the first 10 items in my list, which were all collected during the same minute.
This is different from it only showing the first item.) So, I made a new
list that is filled with the items in the time list at each step.'''
indexed_times = []

''' The variable n is a counter while the variable n_desired_ticks is the
number of ticks I want on my x-axis. By formatting my program this way, I can
easily change the number of ticks if I want to do so. The variable step denotes
the value of the ticks. '''
n = 0
n_desired_ticks = 10
step = len(index) / n_desired_ticks

# This while loop fills the new list with step values.
while n < n_desired_ticks:
    indexed_times.append(times[n * step])
    n += 1

''' Originally, when I plotted the x-ticks, I had the following:

plt.xticks(np.arange(len(index), step = len(index) / 10), times, ...).

By using times as my list, only the first 10 data points displayed as the
x-tick labels, not the data point at each step. To correct this, I introduced
the new list indexed_times, which was explained above. I also changed 10 to
n_desired_ticks in case I want to change the number of ticks. ''' 

'''
num = 0
pred_humidity = []
while num < len(index):
    A = 17.625
    B = 243.04
    C = (A * float(temps[num])) / (B + float(temps[num]))
    L = 2.45 * 10**6
    R = 461.5
    D = L / R
    K = 273.15
    T = float(temps[num]) + K
    a = (T / D) * (K - B)
    b = (B - ((B * T * C) / D) - K - ((K * A * T) / D) + ((K * T * C) / D)+ T)
    c = ((B * C) + (K * A) - (K * C) - (A * T) + (T * C))
    
    pred_humidity.append(100 * np.exp((-b + np.sqrt((b * b) - (4 * a * c))) / (2 * a)))
    # print((-b + np.sqrt((b * b) - (4 * a * c))) / (2 * a))
    # print(a, b, c)
    # print(b, 2 * a, np.sqrt((b * b) - (4 * a * c)))
    # print(pred_humidity[num])
    num += 1
'''

# This section of code plots the humidities.
hum = plt.figure(1)
plt.title("Humidities at Various Times")
plt.ylabel("Relative Humidity (%)")
plt.xticks(np.arange(len(index), step = len(index) / n_desired_ticks), indexed_times, fontsize = 8, rotation = 45)
plt.plot(index, humidities, marker = "o", c = "g")
# plt.plot(index, pred_humidity, marker = "o", c = "r")
hum.show()

# This section of code plots the temperatures.
temp = plt.figure(2)
plt.title("Temperatures at Various Times")
plt.ylabel("Temperature (C)")
plt.xticks(np.arange(len(index), step = len(index) / n_desired_ticks), indexed_times, fontsize = 8, rotation = 45)
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
