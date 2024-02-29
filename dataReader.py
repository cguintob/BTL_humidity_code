import matplotlib.pyplot as plt
import numpy as np

file = "data_file5.txt"

index = []
times = []
humidities = []
temps = []

for line in open(file, "r"):
    lines = [i for i in line.split()]
    index.append(lines[0])
    times.append(lines[1] + "\n" + lines[2])
    humidities.append(lines[3])
    temps.append(lines[4])

hum = plt.figure(1)
plt.title("Humidities at Various Times")
plt.ylabel("Relative Humidity (%)")
plt.xticks(np.arange(len(index), step = len(index) / 10), times, fontsize = 8, rotation = 45)
plt.plot(index, humidities, marker = "o", c = "g")
hum.show()

temp = plt.figure(2)
plt.title("Temperatures at Various Times")
plt.ylabel("Temperature (C)")
plt.xticks(np.arange(len(index), step = len(index) / 10), times, fontsize = 8, rotation = 45)
plt.plot(index, temps, marker = "o", c = "g")
temp.show()

input()




# x = [dt.datetime.strptime(d, '%Y-%m-%d').date() for d in dates]

# plt.ylimit(0, 100)
# plt.gca().xaxis.set_major_formatter(dates.DateFormatter('%Y-%m-%d'))
# plt.gca().xaxis.set_major_locator(dates.DayLocator())
# plt.plot_date(timestamps, humidities, marker = "o", c = "g", linestyle = "solid")
