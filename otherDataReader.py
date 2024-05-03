''' This script is exactly like dataReader.py, but for the merged data.
There is no Charlottsville weather data for this macro. '''

import matplotlib.pyplot as plt
import numpy as np
import sys

# Only one data file now.
try:
    if (sys.argv[1].endswith(".txt")):
        file1 = sys.argv[1]
    else:
        print("Use the following format: python dataReader.py [datafile1].txt\n")
        sys.exit(1)
except IndexError:
    print("Use the following format: npython dataReader.py [datafile1].txt\n")
    sys.exit(1)

index = []
dates_and_times = []
humidities = []
temps = []

for line in open(file1, "r"):
    lines = [i for i in line.split()]
    index.append(lines[0])
    dates_and_times.append(lines[1] + "\n" + lines[2])
    humidities.append(lines[3])
    temps.append(lines[4])
        
for i in range(len(index) - 1):
    if int(index[i + 1]) < int(index[i]):
        index[i + 1] = int(index[i]) + 1
    else:
        continue
        
indexed_times = []
n = 0
n_desired_ticks = 10
step = len(index) / n_desired_ticks

while n < n_desired_ticks:
    indexed_times.append(dates_and_times[n * step])
    n += 1

n_optimal = 0
for i in range(len(humidities)):
    if float(humidities[i]) > 40 and float(humidities[i]) < 60:
        n_optimal += 1
    else:
        continue
print("Percent of humidities in optimal range: " + str(float(n_optimal)/float(len(humidities)) * 100))
        
hum = plt.figure(1)
plt.title("Humidities at Various Times")
plt.xlabel("Date and Time")
plt.ylabel("Relative Humidity (%)")
plt.ylim([0, 100])
plt.xticks(np.arange(len(index), step = len(index) / n_desired_ticks), indexed_times, fontsize = 8, rotation = 45)
plt.plot(index, humidities, marker = "+", c = "g", label = "Assembly Room")
plt.plot([0, len(index)], [40, 40], c = "y", linewidth = 3.0)
plt.plot([0, len(index)], [60, 60], c = "y", linewidth = 3.0, label = "Optimal Range")
plt.legend(loc = "upper right")
plt.text(0.375 * step, 90, str(float(n_optimal)/float(len(humidities)) * 100) + "% of humidities in optimal range", fontsize = 10) 
hum.show()
        
temp = plt.figure(2)
plt.title("Temperatures at Various Times")
plt.xlabel("Date and Time")
plt.ylabel("Temperature (C)")
plt.ylim([0, 50])
plt.xticks(np.arange(len(index), step = len(index) / n_desired_ticks), indexed_times, fontsize = 8, rotation = 45)
plt.plot(index, temps, marker = "+", c = "g")
temp.show()

input()




# Code written by Christian Guinto-Brody for Professor Chris Neu's research group.
