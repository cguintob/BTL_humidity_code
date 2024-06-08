import matplotlib.pyplot as plt       # This creates the plots and their characteristics.
import matplotlib.dates as mdates     # This is used for plotting the x-ticks with datetimes.
import pandas as pd                   # This creates the dataframes used for plotting and other functionalities.
import sys                            # This allows the user to enter command-line arguments and shuts down the program if things go wrong.
from collections import OrderedDict   # This is necessary for ordering the dataframes chronologically.
import time                           # This is necessary for pausing the program before continuing its execution (see Part 8).

''' ================================================================================================================== '''
''' ==================================================== OVERVIEW ==================================================== '''
''' ================================================================================================================== '''

''' This macro functions similarly as dataReader.py, but using pandas. The nice
 thing about pandas is that you can treat data from files as dataframes, which 
make plotting a lot simpler because you don't need to split the data into lists 
and loop through them. It's also nice because the index isn't necessary---you 
can plot solely using the timestamp. '''

''' ================================================================================================================== '''
''' ============================================ PART 0: HELPER FUNCTIONS ============================================ '''
''' ================================================================================================================== '''

''' This is the "initialization" section, where I define a few helper functions
 that execute things that I need to execute multiple times in the program. They
 will become more apparent later in the program. '''

''' ================================================================================================================== '''

# This function formats and sorts the columns in a dataframe.
def df_formatter(dataframe):
    dataframe["Date"] = dataframe["Date"].astype(str) + " " + dataframe["Time"].astype(str)
    dataframe.rename(columns = {"Date": "Date and Time"}, inplace = True)
    dataframe["Date and Time"] = pd.to_datetime(dataframe["Date and Time"])
    dataframe.drop("Time", axis = 1, inplace = True)
    dataframe.sort_values(by = "Date and Time", inplace = True)
    dataframe.set_index(["Date and Time"], inplace = True)
    dataframe.dropna(inplace = True)   # This corrects for any missing values (i.e. removes any row where a NaN appears).

# This function defines some parameters for the axis on which I plot humidities.
def hums_axis(axis, low_hum, high_hum, low_time, high_time, title_low_time, title_high_time):
    axis.set_xlabel("")                                                                                    # Only want labels and ticks for the bottom subplot
    axis.tick_params(axis = "x", bottom = False, labelbottom = False)
    axis.set_ylabel("Relative Humidity (%)", color = "k")
    axis.tick_params(axis = "y", labelcolor = "k")
    axis.set_ylim([low_hum, high_hum])    
    axis.set_xlim(date_list[low_time], date_list[high_time])
    axis.set_title("Humidities from {0} to {1}".format(title_low_time, title_high_time), fontsize = 10)

# This function defines some parameters for the axis on which I plot temperatures.
def temps_axis(axis, low_temp, high_temp, low_time, high_time, title_low_time, title_high_time, x_list, num_ticks):
    axis.set_xlabel("Date and Time")
    axis.tick_params(axis = "x", labelsize = 8)
    axis.xaxis.set_major_locator(mdates.SecondLocator(interval = int(len(x_list) / num_ticks)))            # Frequency of x-ticks
    axis.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d\n%H:%M:%S"))                             # Format of x-ticks
    axis.set_ylabel("Temperature (C)", color = "k")
    axis.tick_params(axis = "y", labelcolor = "k")
    axis.set_ylim([low_temp, high_temp])    
    axis.set_xlim(date_list[low_time], date_list[high_time])
    axis.set_title("Temperatures from {0} to {1}".format(title_low_time, title_high_time), fontsize = 10)
    axis.legend(loc = "best", prop = {"size": 10})                                                          # Location of the legend based on data

# This function defines some parameters for axis on which I plot precipitation levels.
def precip_axis(axis):
    axis.set_ylabel("Precipitation (mm/3hr)", color = "b")
    axis.tick_params(axis = "y", labelcolor = "b")
    axis.set_ylim([0, None])

''' This function defines the bounds and some dates to be used for naming. The 
first two are the lower and upper time bounds, respectively, used for the x-axis
 and other things. The second two are the start and end dates and times for the 
plot titles, respectively. The third two are the start and end dates and times 
for the photo titles, respectively. They are all returned by the function. '''
def bounds(low_time, high_time, list_of_dates):
    lower_bound = int(low_time * (len(list_of_dates) - 1))
    upper_bound = int(high_time * (len(list_of_dates) - 1))
    start_for_title = str(list_of_dates[lower_bound])[:10] + ", " + str(list_of_dates[lower_bound])[(10 + 1):]
    end_for_title = str(list_of_dates[upper_bound])[:10] + ", " + str(list_of_dates[upper_bound])[(10 + 1):]
    start_for_photo = str(list_of_dates[lower_bound])[:10] + "---" + str(list_of_dates[lower_bound])[(10 + 1):] 
    end_for_photo = str(list_of_dates[upper_bound])[:10] + "---" + str(list_of_dates[upper_bound])[(10 + 1):]
    return (lower_bound, upper_bound, start_for_title, end_for_title, start_for_photo, end_for_photo)

# This function saves the figure and closes the program at the end of its functioning.
def save_exit(photo_start, photo_end):
    plt.savefig("data_graphs/{0}_to_{1}.png".format(photo_start, photo_end))
    print("Saved to ~/BTL_humidity_code/data_graphs as {0}_to_{1}.png".format(photo_start, photo_end))
    sys.exit(1)

''' ================================================================================================================== '''
''' ============================================= PART 1: GATHERING FILES ============================================ '''
''' ================================================================================================================== '''

''' This defines the files from command-line arguments in an efficient way: for
each system argument, if the argument is a txt file, add it to the list "files";
otherwise, tell the user that they should send the program txt files and exit. 
If no files are given, the program will exit and tell the user its usage. ''' 

''' ================================================================================================================== '''

files = []
if (len(sys.argv) != 1):
    for i in range(1, len(sys.argv)):        # I defined the range this way so that the i in the for loop and the i index for the system arguments matched.
        if (sys.argv[i].endswith(".txt")):
            files.append(sys.argv[i])
        else:
            print("Use the following format: python NEW_READER.py [datafile1].txt [datafile2].txt [datafile3].txt ...\n")
            print("Can also be used like this: python NEW_READER.py path_to_datafiles/[filename]*")
            sys.exit(1)
else:
    print("Use the following format: python NEW_READER.py [datafile1].txt [datafile2].txt [datafile3].txt ...\n")
    print("Can also be used like this: python NEW_READER.py path_to_datafiles/[filename]*")
    sys.exit(1)

''' ================================================================================================================== '''
''' ================================================ PART 2: DATAFRAMES ============================================== '''
''' ================================================================================================================== '''

''' This defines the dataframes from the command-line arguments while allowing 
the user to enter the files in whichever order they choose. The new thing I 
used for this is a dictionary (defined as [DICTIONARY TITLE] = {}), which is 
like a list with, for lack of better terms, "unhidden" and "noninteger" indices.
 In this case, I define an unsorted dictionary that simply takes all the data 
from each system argument (stored in the list "files") and makes dataframes out 
of them based on which sensor took the data and whether the data was from wttr 
or the sensors. It ends up becoming a dictionary of dataframes. 

Some features of note here are the following:
1) pd.read_csv([file], [separator], [header], [header names], [index indicator]) --- Reads data from txt files into a dataframe
2) len(df.columns) --- Gets the number of columns in a dataframe
3) "[string]{0}".format([int]) --- Will replace the number in curly brackets with whatever number is in the "format" function. For more than one number, use {0}, {1}, ...
4) list(unsorted_df.keys()) --- Makes a list out of the keys in the dictionary
5) df.iloc[0][0] --- iloc means "integer locator" and finds the element at [0][0] in this case '''

''' ================================================================================================================== '''

unsorted_df = {}
for f in files:
    df = pd.read_csv(f, sep = " ", header = None)
    ''' The if part of the if-else statement defines the weather data; the else part defines the sensor data. 
    Both parts contain if-else statements---if the dataframe doesn't already exist, define it; if it does, add to it. '''
    if (len(df.columns) > 5):
        if ("df{0}".format(0) not in list(unsorted_df.keys())):
            unsorted_df["df{0}".format(0)] = pd.read_csv(f, sep = " ", header = None, names = ["Port", "Date", "Time", "Humidity", "Temperature", "Precipitation"])
        else:
            unsorted_df["df{0}".format(0)] = unsorted_df["df{0}".format(0)].append(pd.read_csv(f, sep = " ", header = None, names = ["Port", "Date", "Time", "Humidity", "Temperature", "Precipitation"]), ignore_index = True)
    else:
        if ("df{0}".format(df.iloc[0][0] + 1) not in list(unsorted_df.keys())):
            unsorted_df["df{0}".format(df.iloc[0][0] + 1)] = pd.read_csv(f, sep = " ", header = None, names = ["Port", "Date", "Time", "Humidity", "Temperature"])
        else:
            unsorted_df["df{0}".format(df.iloc[0][0] + 1)] = unsorted_df["df{0}".format(df.iloc[0][0] + 1)].append(pd.read_csv(f, sep = " ", header = None, names = ["Port", "Date", "Time", "Humidity", "Temperature"]), ignore_index = True)

''' ================================================================================================================== '''
''' ================================================ PART 3: ORDERING ================================================ '''
''' ================================================================================================================== '''

''' This part of the code simply defines an OrderedDict, which is a special kind
 of dictionary that retains the order in which key-value pairs are inserted into
 the dictionary. I take the items inside my unsorted dictionary and sort them. 
Then, I make an OrderedDict out of them. Lastly, I define a new dictionary that 
contains the ordered items. The idea behind this is to put all the items in each
 dataframe in chronological order so I can plot based on timestamp. I also 
define a list called "keys," which is a list of the keys of the sorted 
dictionary. '''

''' ================================================================================================================== '''

sorted_df = OrderedDict(sorted(unsorted_df.items()))
keys = list(sorted_df.keys())

''' ================================================================================================================== '''
''' ============================================== PART 4: MORE SORTING ============================================== '''
''' ================================================================================================================== '''

''' This part of the code defines the index (i.e. the x-axis) for plotting. The 
data I collect contains two separate columns for the date and time (nicely named
 "Date" and "Time," respectfully). However, this is not ideal for plotting via 
timestamps. So, for each dataframe in my sorted dictionary, I modify the "Date" 
column to include both the date and time from the "Date" and "Time" columns 
(with a space between them) and then rename that column "Date and Time." Then, 
I change the elements in the "Date and Time" column to be pandas datetime 
objects, which can be plotted. Next, I delete the "Time" column and sort all 
the datetime objects in the new "Date and Time" column so that they are in 
chronological order. Lastly, I set the "Date and Time" column as the index of 
the dataframe. This is all done in the helper function "df_formatter," which 
takes a dataframe as its input.

After doing all this, I then define a new list called "date_list," which is a 
pandas object that creates a list of datetime objects between a start and end 
date at a given frequency (for this case, I used every second since I collect 
data every second). I defined the start date to be the first date and time 
listed in my first dataframe and the end date to be the last date and time 
listed in my last dataframe (when I say "first" and "last" with respect to the 
dataframes, I mean that each frame is given an index, and the order of the index
 determines which is first and last). The list "date_list" denotes the x-bounds 
and the x-ticks on the plots. '''

''' ================================================================================================================== '''

for i in range(len(keys)):
    df_formatter(sorted_df[keys[i]])

start_date = sorted_df[keys[0]].index.tolist()[0]
end_date = sorted_df[keys[len(keys) - 1]].index.tolist()[len(sorted_df[keys[len(keys) - 1]].index.tolist()) - 1]
date_list = pd.date_range(start_date, end_date, freq = "s")

''' ================================================================================================================== '''
''' ============================================= PART 5: DEFINING BOUNDS ============================================ '''
''' ================================================================================================================== '''

''' These next objects are simply simple ways to store the various bounds for 
the plots. It makes life easier when they are all 1) defined) and 2) put in 
the same place. I also defined the number of x-ticks I want as well as some 
colors and markers included in matplotlib.pyplot for ease of definition. '''

''' ================================================================================================================== '''

lower_time_index = 0
upper_time_index = 1
lower_hum_bound = 0
upper_hum_bound = 100
lower_temp_bound = 0
upper_temp_bound = 30

n_desired_ticks = 10
colors = ["cyan", "green", "yellow", "magenta"]
markers = ["x", ".", ",", "v", "^"]

lower_time_bound, upper_time_bound, title_start_date, title_end_date, png_start_date, png_end_date = bounds(lower_time_index, upper_time_index, date_list)

''' ================================================================================================================== '''
''' =========================================== PART 6: PLOTTING HUMIDITIES ========================================== '''
''' ================================================================================================================== '''

''' This section of code plots the humidities from each sensor and wttr. To do 
this, I first define the plot itself and an axis as subplots of each other. The 
plot ends up being defined as a figure (figure 1, specifically, becasue I'm 
plotting two different plots from the same graph). The axis, however, is the 
thing that takes the data. I loop over all the dataframes in my sorted 
dictionary and try to find the weather data because it contains an extra column 
for preciptation that I plot on the same graph with the humidities. (The weather
 data is found in the first dataframe (the 0th, if you will). I check whether 
the dataframe has more than four columns, and if it does, I know that this is 
the weather data. This is different from before when I checked if the data had 
more than five columns because I merged two of the columns and made it the 
index.) For the weather data, I set the color to "red" and the graph label to 
"CVille." I also define a separate axis for plotting the precipitation and 
define the color, marker, title, and limits of it. For the sensor data, I set 
the color equal to one of the elements in the list "color" and the graph label 
equal to the sensor that took the data. Then, I define the humidity axis. If 
the index in the for loop is zero, then I define the axis, but if it isn't, then
 I simply plot the data on that axis because it already exists. The nice thing 
about doing it this way is that no matter whether I have weather data or only 
sensor data, the axis is defined.

After defining the labels and axes, I configure a bunch of other things with the
 plots, including x- and y-labels, the x-ticks (which are defined as dates at an
 interval given by the length of "date_list" divided by the number of desired 
ticks (I end up getting one extra tick, but that is a least-concern worry)), 
bounds for the x- and y-axes, a legend, and a plot title (all done with the 
helper function "hums_axis." For data-specific configurations, I define things 
using the axis; for whole-plot configurations, I define things using "plt." '''

''' ================================================================================================================== '''

hums = plt.subplot(211)
for i in range(len(keys)):
    if (len(sorted_df[keys[i]].columns) < 4):
        color = colors[i]
        marker = markers[i]
        graph_label = "Sensor {0}".format(int(sorted_df[keys[i]]["Port"][0]) + 1)
    else:
        color = "red"
        marker = "*"
        graph_label = "CVille"
        ax_precip = sorted_df[keys[i]]["Precipitation"].plot(rot = 45, marker = "*", secondary_y = True, color = "blue")
        precip_axis(ax_precip)
    if (i == 0):
        ax_hum = sorted_df[keys[i]]["Humidity"].plot(rot = 45, color = color, marker = marker, label = graph_label)
    else:
        sorted_df[keys[i]]["Humidity"].plot(rot = 45, color = color, marker = marker, label = graph_label)

hums_axis(ax_hum, lower_hum_bound, upper_hum_bound, lower_time_bound, upper_time_bound, title_start_date, title_end_date)

''' ================================================================================================================== '''
''' ========================================== PART 7: PLOTTING TEMPERATURES ========================================= '''
''' ================================================================================================================== '''

''' This section is analogous to Parts 5 and 6, but for temperatures. The key 
differences here are that 1) I don't need to define a separate axis for 
precipitation data, since I'm not including that data on the plot, and 2) I must
 convert the wttr temperature data to degrees Celsius since they were collected 
in degrees Fahrenheit. To do the latter, I apply a "lambda" modification to each
 element in the columns containing the data. '''

''' ================================================================================================================== '''

temps = plt.subplot(212)
for i in range(len(keys)):
    if (len(sorted_df[keys[i]].columns) < 4):
        color = colors[i]
        marker = markers[i]
        graph_label = "Sensor {0}".format(int(sorted_df[keys[i]]["Port"][0]) + 1)
    else:
        color = "red"
        marker = "*"
        graph_label = "CVille"
        sorted_df[keys[i]]["Temperature"] = sorted_df[keys[i]]["Temperature"].apply(lambda x: (int(x) - 32) / 1.8)
    if (i == 0):
        ax_temp = sorted_df[keys[i]]["Temperature"].plot(rot = 45, color = color, marker = marker, label = graph_label)
    else:
        sorted_df[keys[i]]["Temperature"].plot(rot = 45, color = color, marker = marker, label = graph_label)
        
temps_axis(ax_temp, lower_temp_bound, upper_temp_bound, lower_time_bound, upper_time_bound, title_start_date, title_end_date, date_list, n_desired_ticks)

''' ================================================================================================================== '''
''' ============================================ PART 8: DISPLAYING PLOTS ============================================ '''
''' ================================================================================================================== '''

''' This section is used for continuously updating the plots with the updating 
code. I first plot the data from the initial dataframes and make the plot show 
in a nonblocking manner so code can be executed underneath it. I also pause the 
code for one second before continuing the program. I then define a list called 
"lastLine," which takes the value of the last line of each file. Next, I run an 
infinite while loop, in which I clear the plots' axes so I can plot anew, and 
open all the files given to the program from the command line. I then read each 
line of the files, and since we're in an infinite while loop, it constantly 
gathers any new data that was added to them. Next, I define the last line as a 
dataframe, give it header names based on whether it was sensor or weather data, 
and format it using "df_formatter." (Importantly, I use a try-except statement 
here, which checks to see if a line was added. If it was, then I do the above, 
but if it wasn't, then it's a static dataset, and I exit the program.) Lastly, I
 do all the things I did in Parts 6 and 7 with plotting and configuring the 
data. I then display the data on the already created plot. 

The complications with all this are the following:
1) I'm working with a VERY nested loop, so indentations are VERY important.
2) I had to redefine end_date and this date_list (and the subsequent variables depending on them) since I'm adding more data. 
3) I had to cast the values of the new dataframe as floats to use them. 
4) I'm working with different indices and keys for the appended dataframes since I'm looping over files, not keys in sorted_df.

All in all, it works. And I'm glad it does. '''

''' ================================================================================================================== '''

plt.show(block = False)
plt.pause(1)

lastLine = [None]*len(files)

while True:
    ax_hum.cla()
    ax_temp.cla()
    for i in range(len(files)):
        with open(files[i], "r") as f:
            lines = f.readlines()
            if lines[-1] != lastLine[i]:
                lastLine[i] = lines[-1]
                split_line = lastLine[i].rstrip("\n").split(" ")
                df = pd.DataFrame([split_line])
                try:
                    if (len(df.columns) > 5):
                        df.columns = ["Port", "Date", "Time", "Humidity", "Temperature", "Precipitation"]
                    elif (len(df.columns) > 4):
                        df.columns = ["Port", "Date", "Time", "Humidity", "Temperature"]
                    else:
                        save_exit(png_start_date, png_end_date)
                except ValueError or KeyboardInterrupt:
                    save_exit(png_start_date, png_end_date)
                df_formatter(df)
                if (len(df.columns) > 3):
                    ax_precip.cla()
                    color = "red"
                    marker = "*"
                    label = "CVille"
                    key = "df{0}".format(0)
                    df["Temperature"] = df["Temperature"].apply(lambda x: (int(x) - 32) / 1.8)
                    sorted_df[key]["Precipitation"] = sorted_df[key]["Precipitation"].astype(float)
                    sorted_df[key]["Precipitation"].plot(rot = 45, ax = ax_precip, marker = "*", secondary_y = True, color = "blue")
                    precip_axis(ax_precip)
                else:
                    color = colors[int(df.iloc[0][0]) + 1]
                    marker = markers[int(df.iloc[0][0]) + 1]
                    label = "Sensor {0}".format(int(df.iloc[0][0]) + 1)
                    key = "df{0}".format(int(df.iloc[0][0]) + 1)
                sorted_df[key] = sorted_df[key].append(df)
                sorted_df[key]["Humidity"] = sorted_df[key]["Humidity"].astype(float)
                sorted_df[key]["Temperature"] = sorted_df[key]["Temperature"].astype(float)
                sorted_df[key]["Humidity"].plot(rot = 45, ax = ax_hum, color = color, marker = marker, label = label)
                sorted_df[key]["Temperature"].plot(rot = 45, ax = ax_temp, color = color, marker = marker, label = label)
                end_date = sorted_df[key].index.tolist()[len(sorted_df[key].index.tolist()) - 1]
                end_date.strftime("%Y-%m-%d %H:%M:%S")
                date_list = pd.date_range(start_date, end_date, freq = "s")
                lower_time_bound, upper_time_bound, title_start_date, title_end_date, png_start_date, png_end_date = bounds(lower_time_index, upper_time_index, date_list)
            else:
                save_exit(png_start_date, png_end_date)
    hums_axis(ax_hum, lower_hum_bound, upper_hum_bound, lower_time_bound, upper_time_bound, title_start_date, title_end_date)
    temps_axis(ax_temp, lower_temp_bound, upper_temp_bound, lower_time_bound, upper_time_bound, title_start_date, title_end_date, date_list, n_desired_ticks)
    plt.show(block = False)
    plt.pause(1)
    time.sleep(1)

''' ================================================================================================================== '''
''' ============================================ PART 9: ACKNOWLEDGEMENTS ============================================ '''
''' ================================================================================================================== '''

# Code written by Christian Guinto-Brody for Professor Chris Neu's research group.
