import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import pandas as pd
import sys
from collections import OrderedDict
from datetime import datetime
import time

''' This macro functions similarly as dataReader.py, but using pandas. This nice
 thing about pandas is that you can treat data from files as dataframes, which 
make plotting a lot simpler because you don't need to split the data into lists 
and loop through them. It's also nice because the index isn't necessary---you 
can plot solely using the timestamp. '''

files = []
# This defines the files from command-line arguments in an efficient way.
for i in range(1, len(sys.argv)):
    if (sys.argv[i].endswith(".txt")):
        files.append(sys.argv[i])
    else:
        print("Use the following format: python NEW_READER.py [datafile1].txt [datafile2].txt [datafile3].txt ...\n")
        print("NOTE: One of the datafiles must be weather data; the other files must be from different sensors.")
        sys.exit(1)

''' This defines the dataframes from the command-line arguments. It allows the 
user to enter the files in whichever order they choose. '''
unsorted_df = {}
for f in files:
    df = pd.read_csv(f, sep = " ", header = None)
    if (len(df.columns) > 5):
        if ("df{0}".format(0) not in list(unsorted_df.keys())):
            unsorted_df["df{0}".format(0)] = pd.read_csv(f, sep = " ", header = None, names = ["Port", "Date", "Time", "Humidity", "Temperature", "Precipitation"])
        else:
            unsorted_df["df{0}".format(0)] = unsorted_df["df{0}".format(int(0.5 * (len(sys.argv) - 1)))].append(pd.read_csv(f, sep = " ", header = None, names = ["Port", "Date", "Time", "Humidity", "Temperature", "Precipitation"]), ignore_index = True)
    else:
        if ("df{0}".format(df.iloc[0][0] + 1) not in list(unsorted_df.keys())):
            unsorted_df["df{0}".format(df.iloc[0][0] + 1)] = pd.read_csv(f, sep = " ", header = None, names = ["Port", "Date", "Time", "Humidity", "Temperature"])
        else:
            unsorted_df["df{0}".format(df.iloc[0][0] + 1)] = unsorted_df["df{0}".format(df.iloc[0][0] + 1)].append(pd.read_csv(f, sep = " ", header = None, names = ["Port", "Date", "Time", "Humidity", "Temperature"]), ignore_index = True)

sorted_df = OrderedDict(sorted(unsorted_df.items()))
keys = list(sorted_df.keys())

# This sets the index (i.e. the x-axis) for plotting.
indexed_times = []
for i in range(len(keys)):
    sorted_df[keys[i]]["Date"] = sorted_df[keys[i]]["Date"].astype(str) + " " + sorted_df[keys[i]]["Time"].astype(str)
    sorted_df[keys[i]].rename(columns = {"Date": "Date and Time"}, inplace = True)
    sorted_df[keys[i]]["Date and Time"] = pd.to_datetime(sorted_df[keys[i]]["Date and Time"])
    sorted_df[keys[i]].drop("Time", axis = 1, inplace = True)
    sorted_df[keys[i]].sort_values(by = "Date and Time", inplace = True)
    sorted_df[keys[i]].set_index(["Date and Time"], inplace = True)

start_date = sorted_df[keys[0]].index.tolist()[0]
end_date = sorted_df[keys[len(keys) - 1]].index.tolist()[len(sorted_df[keys[len(keys) - 1]].index.tolist()) - 1]
date_list = pd.date_range(start_date, end_date, freq = "s")

lower_time_index = 0
upper_time_index = 1
lower_time_bound = int(lower_time_index * (len(date_list) - 1))
upper_time_bound = int(upper_time_index * (len(date_list) - 1))
lower_hum_bound = 48
upper_hum_bound = 55

n_desired_ticks = 10
colors = ["cyan", "green", "yellow", "magenta"]
markers = ["x", ".", ",", "v", "^"]

hums, ax_hum = plt.subplots()
hums = plt.figure(1)
for i in range(len(keys)):
    if (len(sorted_df[keys[i]].columns) < 4):
        color = colors[i]
        graph_label = "Sensor {0}".format(int(sorted_df[keys[i]]["Port"][0]) + 1)
    else:
        color = "red"
        graph_label = "CVille"
        ax_precip = sorted_df[keys[i]]["Precipitation"].plot(rot = 45, marker = "*", secondary_y = True, color = "blue")
        ax_precip.set_ylabel("Precipitation (mm/3hr)", color = "b")
        ax_precip.tick_params(axis = "y", labelcolor = "b")
        ax_precip.set_ylim([0, None])

    if (i == 0):
        ax_hum = sorted_df[keys[i]]["Humidity"].plot(rot = 45, color = color, marker = markers[i], label = graph_label)
    else:
        sorted_df[keys[i]]["Humidity"].plot(rot = 45, color = color, marker = markers[i], label = graph_label)
        
ax_hum.set_xlabel("Date and Time")
ax_hum.tick_params(axis = "x", labelsize = 8)
ax_hum.xaxis.set_major_locator(mdates.SecondLocator(interval = int(len(date_list) / n_desired_ticks)))
ax_hum.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d\n%H:%M:%S"))
ax_hum.set_ylabel("Relative Humidity (%)", color = "k")
ax_hum.tick_params(axis = "y", labelcolor = "k")
ax_hum.set_ylim([lower_hum_bound, upper_hum_bound])    
plt.xlim(date_list[lower_time_bound], date_list[upper_time_bound])
plt.title("Humidities at Various Times")
ax_hum.legend(loc = "best", prop = {"size": 10})
hums.autofmt_xdate(ha = "right")
hums.show()

lower_temp_bound = 0
upper_temp_bound = 30

temps, ax_temp = plt.subplots()
temps = plt.figure(2)
for i in range(len(keys)):
    if (len(sorted_df[keys[i]].columns) < 4):
        color = colors[i]
        graph_label = "Sensor {0}".format(int(sorted_df[keys[i]]["Port"][0]) + 1)
    else:
        color = "red"
        graph_label = "CVille"
        sorted_df[keys[i]]["Temperature"] = sorted_df[keys[i]]["Temperature"].apply(lambda x: (int(x) - 32) / 1.8)

    if (i == 0):
        ax_temp = sorted_df[keys[i]]["Temperature"].plot(rot = 45, color = color, marker = markers[i], label = graph_label)
    else:
        sorted_df[keys[i]]["Temperature"].plot(rot = 45, color = color, marker = markers[i], label = graph_label)
        
ax_temp.set_xlabel("Date and Time")
ax_temp.tick_params(axis = "x", labelsize = 8)
ax_temp.xaxis.set_major_locator(mdates.SecondLocator(interval = int(len(date_list) / n_desired_ticks)))
ax_temp.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d\n%H:%M:%S"))
ax_temp.set_ylabel("", color = "k")
ax_temp.tick_params(axis = "y", labelcolor = "k")
ax_temp.set_ylim([lower_temp_bound, upper_temp_bound])    
plt.xlim(date_list[lower_time_bound], date_list[upper_time_bound])
plt.title("Temperatures at Various Times")
ax_temp.legend(loc = "best", prop = {"size": 10})
temps.autofmt_xdate(ha = "right")
temps.show()

input()
