import sys                            # This allows the user to enter command-line arguments and shuts down the program if things go wrong. 
if (sys.version_info[0] == 3):        # If the machine has Python 3 and above, import tkinter; if not, import Tkinter (they changed the name).
    import tkinter as tk
else:
    import Tkinter as tk
import matplotlib                     # I messed up the program playing with (installing) backend services and now I must manually set the backend this way. Whoops.
matplotlib.use("tkagg")               # This is an interactive backend used with tkinter.
import matplotlib.pyplot as plt       # This creates the plots and their characteristics.
import matplotlib.dates as mdates     # This is used for plotting the x-ticks with datetimes.
from collections import OrderedDict   # This is necessary for ordering the dataframes chronologically.
import time                           # This is necessary for pausing the program before continuing its execution (see Part 8).
import datetime                       # This is necessary for determining whether the files are weather data or sensor data.
import warnings                       # This is used to disable warning messages, specifically FutureWarning and UserWarning messages.
warnings.simplefilter(action = "ignore", category = FutureWarning)
warnings.simplefilter(action = "ignore", category = UserWarning)
import pandas as pd                   # This creates the dataframes used for plotting and other functionalities.

''' ================================================================================================================== '''
''' ==================================================== OVERVIEW ==================================================== '''
''' ================================================================================================================== '''

''' This macro functions similarly as dataReader.py, but using pandas. The nice
 thing about pandas is that you can treat data from files as dataframes, which 
make plotting a lot simpler because you don't need to split the data into lists 
and loop through them. It's also nice because the index isn't necessary---you 
can plot solely using the timestamp. '''

''' ================================================================================================================== '''
''' ============================================= PART i: DEFINING BOUNDS ============================================ '''
''' ================================================================================================================== '''

''' These objects are simply simple ways to store the various bounds for the 
plots. It makes life easier when they are all 1) defined) and 2) put in the 
same place. I also defined the number of x-ticks I want as well as some 
colors and markers included in matplotlib.pyplot for ease of definition. '''

''' ================================================================================================================== '''

lower_time_index = 0    # Factor denoting what fraction from the start date we're including on the graph (cannot be greater than upper_time_index, lower bound: 0)
upper_time_index = 1    # Same as above, but for end date (cannot be less than lower_time_index, upper bound: 1)
lower_hum_bound = 40    # Lower bound on humidity (cannot be greater than upper_hum_bound, lower bound (realistically): 0)
upper_hum_bound = 60    # Upper bound on humidity (cannot be less than lower_hum_bound, upper bound (realistically): 100)
lower_temp_bound = 0    # Lower bound on temperature (cannot be greater than upper_temp_bound)
upper_temp_bound = 30   # Upper bound on temperature (cannot be less than lower_temp_bound)
stat_low_index = 0      # Factor denoting what fraction from the start date we're including in the statistics (cannot be greater than stat_high_index, lower bound: 0)
stat_high_index = 1     # Same as above, but for the end date (cannot be less than stat_low_index, upper bound = 1)
switcher = 0            # Number denoting whether we want unchanging or changing statistics (0 for changing, 1 for unchanging)

n_desired_ticks = 10   # Sometimes there are 11 ticks shown on the x-axis, but ultimately, we want constant and evenly-spaced ticks
colors = ["cyan", "green", "yellow", "magenta"]
markers = ["x", ".", ",", "v", "^"]

''' ================================================================================================================== '''
''' =========================================== PART ii: HELPER FUNCTIONS ============================================ '''
''' ================================================================================================================== '''

''' This is the "initialization" section, where I define a few helper functions 
(defined in order of appearance in the program) that execute things that I need 
to execute multiple times in the program. They will become more apparent later 
in the program. '''

''' ================================================================================================================== '''

# This function formats and sorts the columns in a dataframe. I must include "inplace = True" if I want the modifications to save.
def df_formatter(dataframe):
    dataframe["Date"] = dataframe["Date"].astype(str) + " " + dataframe["Time"].astype(str)   # Modify elements in "Date" column by combining elements in columns "Date" and "Time"
    dataframe.rename(columns = {"Date": "Date and Time"}, inplace = True)                     # Rename column "Date" to "Date and Time"
    dataframe["Date and Time"] = pd.to_datetime(dataframe["Date and Time"])                   # Change elements in "Date and Time" to Pandas datetime objects
    dataframe.drop("Time", axis = 1, inplace = True)                                          # Remove column "Time"
    dataframe.sort_values(by = "Date and Time", inplace = True)                               # Sort datetime objects chronologically
    dataframe.set_index(["Date and Time"], inplace = True)                                    # Make column "Date and Time" the new index of the dataframe
    dataframe.dropna(inplace = True)                                                          # Removes any row where NaN appears

# This function defines the start and end dates by comparing the corresponding indices in the dataframes in the dictionary.
def start_end(key_list, dictionary):
    cur_start = dictionary[key_list[0]].index.tolist()[0]                                               # These variables keep track of the first data files given
    cur_end = dictionary[key_list[0]].index.tolist()[len(dictionary[key_list[0]].index.tolist()) - 1]
    if (len(key_list) == 1):   # If there is only one data file given...
        start = dictionary[key_list[0]].index.tolist()[0] 
        end = dictionary[key_list[0]].index.tolist()[len(dictionary[key_list[0]].index.tolist()) - 1]
    else:
        for i in range(len(key_list) - 1):
            if (pd.Timestamp(dictionary[key_list[i]].index.tolist()[0]) < pd.Timestamp(dictionary[key_list[i + 1]].index.tolist()[0])):   # Check if date in 1st occurs before 2nd
                if (pd.Timestamp(cur_start) < pd.Timestamp(dictionary[key_list[i]].index.tolist()[0])):
                    start = cur_start
                else:
                    start = dictionary[key_list[i]].index.tolist()[0]
            else:
                if (pd.Timestamp(cur_start) < pd.Timestamp(dictionary[key_list[i + 1]].index.tolist()[0])):
                    start = cur_start
                else:
                    start = dictionary[key_list[i + 1]].index.tolist()[0]                                                         # If not, set the other equal to "start"
            if (pd.Timestamp(dictionary[key_list[i]].index.tolist()[len(dictionary[key_list[i]].index.tolist()) - 1]) > 
                pd.Timestamp(dictionary[key_list[i + 1]].index.tolist()[len(dictionary[key_list[i + 1]].index.tolist()) - 1])):   # Do the same with the last dates in dfs
                if (pd.Timestamp(cur_end) > pd.Timestamp(dictionary[key_list[i + 1]].index.tolist()[len(dictionary[key_list[i + 1]].index.tolist()) - 1])):
                    end = cur_end
                else:
                    end = dictionary[key_list[i]].index.tolist()[len(dictionary[key_list[i]].index.tolist()) - 1]
            else:
                if (pd.Timestamp(cur_end) > pd.Timestamp(dictionary[key_list[i + 1]].index.tolist()[len(dictionary[key_list[i + 1]].index.tolist()) - 1])):
                    end = cur_end
                else:
                    end = dictionary[key_list[i + 1]].index.tolist()[len(dictionary[key_list[i + 1]].index.tolist()) - 1]   # If the opposite, do the opposite
    return (start, end)   # Return both values

# This function makes sure all the bounds/bound indices are appropriate.
def bound_checker(low, high, num):
    if (low > high):
        print("At least one of your lower bounds is greater than its corresponding upper bound. This cannot occur.".format(bound))
        sys.exit(1)
    if (num == 0):
        if (low < 0):
            print("At least one of your lower indices is less than 0. This cannot occur.")
            sys.exit(1)
        if (high > 1):
            print("At least one of your upper indices is greater than 1. This cannot occur.")

''' This function defines the bounds and some dates to be used for naming. The 
first two are the lower and upper time bounds, respectively, used for the 
x-axis and other things. The second two are the start and end dates and times 
for the plot titles, respectively. The third two are the start and end dates 
and times for the photo titles, respectively. They are all returned by the 
function. '''
def bounds(low_time, high_time, list_of_dates):
    lower_bound = int(low_time * (len(list_of_dates) - 1))
    upper_bound = int(high_time * (len(list_of_dates) - 1))
    start_for_title = str(list_of_dates[lower_bound])[:10] + " at " + str(list_of_dates[lower_bound])[(10 + 1):]
    end_for_title = str(list_of_dates[upper_bound])[:10] + " at " + str(list_of_dates[upper_bound])[(10 + 1):]
    start_for_photo = str(list_of_dates[lower_bound])[:10] + "_at_" + str(list_of_dates[lower_bound])[(10 + 1):] 
    end_for_photo = str(list_of_dates[upper_bound])[:10] + "_at_" + str(list_of_dates[upper_bound])[(10 + 1):]
    return (lower_bound, upper_bound, start_for_title, end_for_title, start_for_photo, end_for_photo)

# This function defines the bounds and the list of dates to use for displaying the statistics.
def stat_bounds(list_of_dates, lower_bound, upper_bound):
    stat_low = int(lower_bound * (len(list_of_dates) - 1))
    stat_high = int(upper_bound * (len(list_of_dates) - 1))
    title_start = str(list_of_dates[stat_low])[:10] + " at " + str(list_of_dates[stat_low])[(10 + 1):]
    title_end = str(list_of_dates[stat_high])[:10] + " at " + str(list_of_dates[stat_high])[(10 + 1):]
    return (stat_low, stat_high, title_start, title_end)

# This function defines some parameters for axis on which I plot precipitation levels.
def precip_axis(axis):
    axis.yaxis.set_label_position("right")
    axis.set_ylabel("Precipitation (mm/3hr)", color = "b")
    axis.tick_params(axis = "y", labelcolor = "b")
    axis.set_ylim([0, None])

# This function defines the elements of the statistics dataframe printed to the screen.
def statistics_placer(stat_df, num, index, series, lower_bound, upper_bound):
    stat_df.loc[stat_df.index.tolist()[num], stat_df.columns.tolist()[index]] = str(series[lower_bound:upper_bound].mean().round(4)) + " +/- " + str(series[lower_bound:upper_bound].std().round(4))

# This function defines some parameters for the axis on which I plot humidities.
def hums_axis(axis, low_hum, high_hum, low_time, high_time, title_low_time, title_high_time):
    axis.set_xlabel("")                                                                                   # Only want labels for bottom subplot
    axis.tick_params(axis = "x", bottom = False, labelbottom = False)                                     # Only want ticks for bottom subplot
    axis.set_ylabel("Relative Humidity (%)", color = "k")                                                 # Set y-axis label and color
    axis.tick_params(axis = "y", labelcolor = "k")                                                        # Set y-axis ticks and color
    axis.set_ylim([low_hum, high_hum])                                                                    # Set range (values are chosen in Part 5)
    axis.set_xlim(date_list[low_time], date_list[high_time])                                              # Set domain (based on range of dates found in Part 5)
    axis.set_title("Humidities from {0} to {1}".format(title_low_time, title_high_time), fontsize = 10)   # Set title using .format()

# This function defines some parameters for the axis on which I plot temperatures.
def temps_axis(axis, low_temp, high_temp, low_time, high_time, title_low_time, title_high_time, x_list, num_ticks):
    axis.set_xlabel("Date and Time")
    axis.tick_params(axis = "x", labelsize = 8)
    if (len(x_list) < (1.5 * num_ticks)):   # This is so that I can plot fewer than 10 points
        axis.xaxis.set_major_locator(mdates.SecondLocator(interval = 1))
    else:
        axis.xaxis.set_major_locator(mdates.SecondLocator(interval = int(len(x_list) / num_ticks)))         # Frequency of x-ticks
    axis.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d\n%H:%M:%S"))                              # Format of x-ticks
    axis.set_ylabel("Temperature (C)", color = "k")
    axis.tick_params(axis = "y", labelcolor = "k")
    axis.set_ylim([low_temp, high_temp])    
    axis.set_xlim(date_list[low_time], date_list[high_time])
    axis.set_title("Temperatures from {0} to {1}".format(title_low_time, title_high_time), fontsize = 10)   
    axis.legend(loc = "best", prop = {"size": 10})                                                          # Location of legend based on data

# This function simply plots the statistics dataframe. It's included for organizational purposes.
def printing_stats(dataframe, title_start, title_end):
    print("Mean and Standard Deviation from {0} to {1}".format(title_start, title_end))
    print(dataframe)
    print("=================================================================================")

# This function saves the plot to a PNG.
def photo_saver(photo_start, photo_end):
    plt.savefig("data_graphs/{0}_to_{1}.png".format(photo_start, photo_end))
    print("Saved to ~/BTL_humidity_code/data_graphs as {0}_to_{1}.png".format(photo_start, photo_end))
    print("=================================================================================")
    
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
    for i in range(1, len(sys.argv)):         # I defined the range this way so that the i in the for loop and the i index for the system arguments matched.
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

lastLine = [None] * len(files)       # Initialize a list of length len(files), all with the value None. This list is used for collecting the last lines of each data file 
for i in range(len(files)):          # This for loop initizalizes lastLine to be the last lines of the data files before we do any updating
    with open(files[i], "r") as f:
        lines = f.readlines()
        lastLine[i] = lines[-1]
    
''' ================================================================================================================== '''
''' ================================================ PART 2: DATAFRAMES ============================================== '''
''' ================================================================================================================== '''

''' This defines the dataframes from the command-line arguments while allowing 
the user to enter the files in whichever order they choose. The new thing I 
used for this is a dictionary (defined as [DICTIONARY TITLE] = {}), which is 
like a list with, for lack of better terms, "unhidden" and "noninteger" 
indices. In this case, I define an unsorted dictionary that simply takes all 
the data from each system argument (stored in the list "files") and makes 
dataframes out of them based on which sensor took the data and whether the data 
was from wttr or the sensors. It ends up becoming a dictionary of dataframes. 

Some features of note here are the following:
1) pd.read_csv([file], [separator], [header], [header names], [index indicator]) --- Reads data from txt files into a dataframe
2) len(df.columns) --- Gets the number of columns in a dataframe
3) "[string]{0}".format([int]) --- Will replace the number in curly brackets with whatever number is in the "format" function. For more than one number, use {0}, {1}, ...
4) list(unsorted_df.keys()) --- Makes a list out of the keys in the dictionary
5) df.iloc[0][0] --- iloc means "integer locator" and finds the element at [0][0] in this case '''

''' ================================================================================================================== '''

unsorted_df = {}
for f in files:
    try:
        df = pd.read_csv(f, sep = " ", header = None)   # Create a dataframe by reading the contents of the file
        for i in range(len(df.index)):
            if ((len(df.loc[i, :].values.flatten().tolist()) > 5) or (len(df.loc[i, :].values.flatten().tolist()) < 5)):
                df.drop([i], inplace = True)
        ''' The if part of the if-else statement defines the weather data; the else part defines the sensor data. 
        Both parts contain if-else statements---if the dataframe doesn't already exist, define it; if it does, add to it. '''
        if (isinstance(df.iloc[0][0], str) == True):   # Denotes weather data
            if ("df{0}".format(0) not in list(unsorted_df.keys())):
                unsorted_df["df{0}".format(0)] = pd.read_csv(f, sep = " ", header = None, names = ["Date", "Time", "Humidity", "Temperature", "Precipitation"])
            else:
                unsorted_df["df{0}".format(0)] = pd.concat([unsorted_df["df{0}".format(0)], pd.read_csv(f, sep = " ", header = None, names = ["Date", "Time", "Humidity", "Temperature", "Precipitation"])])
        else:
            if ("df{0}".format(df.iloc[0][0] + 1) not in list(unsorted_df.keys())):
                unsorted_df["df{0}".format(df.iloc[0][0] + 1)] = pd.read_csv(f, sep = " ", header = None, names = ["Port", "Date", "Time", "Humidity", "Temperature"])
            else:
                unsorted_df["df{0}".format(df.iloc[0][0] + 1)] = pd.concat([unsorted_df["df{0}".format(df.iloc[0][0] + 1)], pd.read_csv(f, sep = " ", header = None, names = ["Port", "Date", "Time", "Humidity", "Temperature"])])
    except FileNotFoundError:
        print("Couldn't find file. Choose a file that is in the directory and has data in it.")
        sys.exit(1)
        
''' ================================================================================================================== '''
''' ================================================ PART 3: ORDERING ================================================ '''
''' ================================================================================================================== '''

''' This part of the code simply defines an OrderedDict, which is a special 
kind of dictionary that retains the order in which key-value pairs are inserted 
into the dictionary. I take the items inside my unsorted dictionary and sort 
them. Then, I make an OrderedDict out of them. Lastly, I define a new 
dictionary that contains the ordered items. The idea behind this is to put all 
the items in each dataframe in chronological order so I can plot based on 
timestamp. I also define a list called "keys," which is a list of the keys of 
the sorted dictionary. '''

''' ================================================================================================================== '''

sorted_df = OrderedDict(sorted(unsorted_df.items()))   # Sort the items in unsorted_df and create an OrderedDict out of them
keys = list(sorted_df.keys())                          # List of sorted keys (used A LOT)

''' ================================================================================================================== '''
''' ============================================== PART 4: MORE SORTING ============================================== '''
''' ================================================================================================================== '''

''' This part of the code defines the index (i.e. the x-axis) for plotting. The 
data I collect contains two separate columns for the date and time (nicely 
named "Date" and "Time," respectfully). However, this is not ideal for plotting 
via timestamps. So, for each dataframe in my sorted dictionary, I modify the 
"Date" column to include both the date and time from the "Date" and "Time" 
columns (with a space between them) and then rename that column "Date and 
Time." Then, I change the elements in the "Date and Time" column to be pandas 
datetime objects, which can be plotted. Next, I delete the "Time" column and 
sort all the datetime objects in the new "Date and Time" column so that they 
are in chronological order. Lastly, I set the "Date and Time" column as the 
index of the dataframe. This is all done in the helper function "df_formatter," 
which takes a dataframe as its input.

After doing all this, I then define a new list called "date_list," which is a 
pandas object that creates a list of datetime objects between a start and end 
date at a given frequency (for this case, I used every second since I collect 
data every second). I defined the start and end dates using a functino called 
"start_end," which takes a list of keys and a dictionary and sorts finds the 
oldest and most recent dates in all the dataframes. The list "date_list" 
denotes the x-bounds and the x-ticks on the plots. '''

''' ================================================================================================================== '''

for i in range(len(keys)):
    df_formatter(sorted_df[keys[i]])   # Format all the dataframes in the dictionary

start_date, end_date = start_end(keys, sorted_df)             # See Part 0 for how I assign the start and end dates
date_list = pd.date_range(start_date, end_date, freq = "s")   # Pandas date range from start_date to end_date with a frequencty of every second

''' ================================================================================================================== '''
''' ============================================ PART 5: REVISTING BOUNDS ============================================ '''
''' ================================================================================================================== '''

''' This section does more with the bounds defined in Part i, namely making 
sure they're valid and also defining some more bounds that depend on the 
ones we defined above using the functions defined in Part ii. '''

''' ================================================================================================================== '''

bound_checker(lower_time_index, upper_time_index, 0)
bound_checker(lower_hum_bound, upper_hum_bound, 1)
bound_checker(lower_temp_bound, upper_temp_bound, 1)
bound_checker(stat_low_index, stat_high_index, 0)

lower_time_bound, upper_time_bound, title_start_date, title_end_date, png_start_date, png_end_date = bounds(lower_time_index, upper_time_index, date_list)
stat_lower_bound, stat_upper_bound, stat_title_start, stat_title_end = stat_bounds(date_list, stat_low_index, stat_high_index)

''' ================================================================================================================== '''
''' =========================================== PART 6: PLOTTING HUMIDITIES ========================================== '''
''' ================================================================================================================== '''

''' This section of code plots the humidities from each sensor and wttr. To do 
this, I first define the plot itself and an axis as subplots of each other. The 
plot ends up being defined as a figure (figure 1, specifically, becasue I'm 
plotting two different plots from the same graph). The axis, however, is the 
thing that takes the data. I loop over all the dataframes in my sorted 
dictionary and try to find the weather data because it contains an extra column 
for preciptation that I plot on the same graph with the humidities. (The 
weather data is found in the first dataframe (the 0th, if you will). I check 
whether the dataframe has more than four columns, and if it does, I know that 
this is the weather data. This is different from before when I checked if the 
data had more than five columns because I merged two of the columns and made it
the index.) For the weather data, I set the color to "red" and the graph label 
to "CVille." I also define a separate axis for plotting the precipitation and 
define the color, marker, title, and limits of it. For the sensor data, I set 
the color equal to one of the elements in the list "color" and the graph label 
equal to the sensor that took the data. Then, I define the humidity axis. If 
the index in the for loop is zero, then I define the axis, but if it isn't, 
then I simply plot the data on that axis because it already exists. The nice 
thing about doing it this way is that no matter whether I have weather data or 
only sensor data, the axis is defined.

After defining the labels and axes, I configure a bunch of other things with 
the plots, including x- and y-labels, the x-ticks (which are defined as dates 
at an interval given by the length of "date_list" divided by the number of 
desired ticks (I end up getting one extra tick, but that is a least-concern 
worry)), bounds for the x- and y-axes, a legend, and a plot title (all done 
with the helper function "hums_axis." For data-specific configurations, I 
define things using the axis; for whole-plot configurations, I define things 
using "plt."

In addition to defining my graphs, I also define a new dataframe called 
"stats," in which I display the mean and standard deviation of every 
data file included for a given range.  '''

''' ================================================================================================================== '''

# This is a dataframe used for displaying the mean and standard deviation of the humidities and temperatures of the weather data and the data from each sensor.
columns = []
for i in range(len(keys)):
    if ("df{0}".format(0) in keys):
        if ("Weather" not in columns):
            columns.append("Weather")
    if ("df{0}".format(int(sorted_df[keys[i]].iloc[0][0]) + 1) in keys):
        if ("Sensor {0}".format(int(sorted_df[keys[i]].iloc[0][0]) + 1) not in columns):
            columns.append("Sensor {0}".format(int(sorted_df[keys[i]].iloc[0][0]) + 1))
stats = pd.DataFrame(index = ["Humidity", "Temperature"], columns = columns)

hums = plt.subplot(211)   # Define a subplot. "211" maps to "2 rows," "1 column," "1st subplot"
for i in range(len(keys)):
    if ("Port" in sorted_df[keys[i]].columns.tolist()):   # If we have sensor data...
        color = colors[i]
        marker = markers[i]
        graph_label = "Sensor {0}".format(int(sorted_df[keys[i]]["Port"][0]) + 1)
    else:   # If we have weather data...
        color = "red"
        marker = "*"
        graph_label = "CVille"
        ax_precip = sorted_df[keys[i]]["Precipitation"].plot(rot = 45, marker = "*", secondary_y = True, color = "blue")
        precip_axis(ax_precip)
    if (i == 0):   # This defines the axis regardless of whether only weather data or sensor data is fed to the program.
        ax_hum = sorted_df[keys[i]]["Humidity"].plot(rot = 45, color = color, marker = marker, label = graph_label)
    else:
        sorted_df[keys[i]]["Humidity"].plot(rot = 45, color = color, marker = marker, label = graph_label)
    statistics_placer(stats, 0, i, sorted_df[keys[i]]["Humidity"], stat_lower_bound, stat_upper_bound)

hums_axis(ax_hum, lower_hum_bound, upper_hum_bound, lower_time_bound, upper_time_bound, title_start_date, title_end_date)

''' ================================================================================================================== '''
''' ========================================== PART 7: PLOTTING TEMPERATURES ========================================= '''
''' ================================================================================================================== '''

''' This section is analogous to Parts 5 and 6, but for temperatures. The key 
differences here are that 1) I don't need to define a separate axis for 
precipitation data, since I'm not including that data on the plot, and 2) I 
must convert the wttr temperature data to degrees Celsius since they were 
collected in degrees Fahrenheit. To do the latter, I apply a "lambda" 
modification to each element in the columns containing the data. '''

''' ================================================================================================================== '''

temps = plt.subplot(212)   # Second of two subplots. This displays below hums
for i in range(len(keys)):
    if ("Port" in sorted_df[keys[i]].columns.tolist()):
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
    statistics_placer(stats, 1, i, sorted_df[keys[i]]["Temperature"], stat_lower_bound, stat_upper_bound)
   
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
but if it wasn't, then it's a static dataset, and I exit the program.) Lastly, 
I do all the things I did in Parts 6 and 7 with plotting and configuring the 
data. I then display the data on the already created plot. 

The complications with all this are the following:
1) I'm working with a VERY nested loop, so indentations are VERY important.
2) I had to redefine end_date and this date_list (and the subsequent variables depending on them) since I'm adding more data. 
3) I had to cast the values of the new dataframe as floats to use them. 
4) I'm working with different indices and keys for the appended dataframes since I'm looping over files, not keys in sorted_df.

All in all, it works. And I'm glad it does. '''

''' ================================================================================================================== '''

printing_stats(stats, stat_title_start, stat_title_end)   # This just prints the statistics dataframe to the screen with nice formatting
photo_saver(png_start_date, png_end_date)                 # This saves the graph as a PNG
plt.show(block = False)                                   # Plot the graph with nonblocking behavior so code can run while it's plotted
try:
    plt.pause(10)                                         # Pause the program for 30 seconds before continuing
except KeyboardInterrupt:
    print("\nKeyboardInterrupt")
    sys.exit(1)
    
start_time = int(time.time())    # This gets the current time and will be used for saving a figure every hour

while True:
    try:
        for i in range(len(files)):
            with open(files[i], "r") as f:                                     # Open the files...
                lines = f.readlines()                                          # Read their lines...
                if (lines[-1] != lastLine[i]):                                 # If the last line is not equal to whatever was collected to be the last line from before...
                    lastLine[i] = lines[-1]                                    # ...set it equal to that line...
                    split_line = lastLine[i].rstrip("\n").split(" ")           # ...format the line by eliminating the newline character and splitting between spaces...
                    df = pd.DataFrame([split_line])                            # ...and create a new dataframe out of that line as a list
                    try:
                        if (len(df.columns) == 5):                             # If there are the appropriate number of columns...
                            if ("-" in str(df.iloc[0][0])):                    # ...and we have weather data...
                                df.columns = ["Date", "Time", "Humidity", "Temperature", "Precipitation"]
                                df["Temperature"] = df["Temperature"].apply(lambda x: (int(x) - 32) / 1.8)
                                key = "df{0}".format(0)
                            else:                                              # ...otherwise, we have sensor data
                                df.columns =["Port", "Date", "Time", "Humidity", "Temperature"]
                                key = "df{0}".format(int(df.iloc[0][0]) + 1)
                            df_formatter(df)                                   # Format the dataframe as before
                            sorted_df[key] = pd.concat([sorted_df[key], df])   # Add the dataframe to the appropriate dataframe in sorted_df
                        else:                                                  # If we don't have the appropriate number of columns (i.e. there was a timeout)...
                            continue                                           # ...do nothing
                    except ValueError:                                         # If there are NO columns, then we do nothing
                        continue
                else:                                                          # Likewise, if the last line of the file is nonexistent, do nothing
                    continue
        ax_hum.cla()                                                   # Now that we've made updates to sorted_df, we can replot by clearing the plots' axes
        ax_temp.cla()
        start_date, end_date = start_end(keys, sorted_df)              # Since new dates were added, we must recalculate the start and end dates
        end_date.strftime("%Y-%m-%d %H:%M:%S")                         # This is for formatting. I ran into an issue for some reason
        date_list = pd.date_range(start_date, end_date, freq = "s")    # We must also recalculate the date range (since the end date is presumably different) as well as our bounds
        lower_time_bound, upper_time_bound, title_start_date, title_end_date, png_start_date, png_end_date = bounds(lower_time_index, upper_time_index, date_list)
        if (switcher == 0):
            stat_lower_bound, stat_upper_bound, stat_title_start, stat_title_end = stat_bounds(date_list, stat_low_index, stat_high_index)
        for i in range(len(keys)):   # This part is basically Parts 6 and 7, just written a little differently
            if ("Precipitation" in sorted_df[keys[i]].columns.tolist()):
                ax_precip.cla()      # Clear the secondary precipitation axis, too
                color = "red"
                marker = "*"
                label = "CVille"
                sorted_df[keys[i]]["Precipitation"] = sorted_df[keys[i]]["Precipitation"].astype(float)
                sorted_df[keys[i]]["Precipitation"].plot(rot = 45, ax = ax_precip, marker = "*", secondary_y = True, color = "blue")
                precip_axis(ax_precip)
            else:
                color = colors[i]
                marker = markers[i]
                label = "Sensor {0}".format(int(sorted_df[keys[i]]["Port"][0]) + 1)
            sorted_df[keys[i]]["Humidity"] = sorted_df[keys[i]]["Humidity"].astype(float)
            sorted_df[keys[i]]["Temperature"] = sorted_df[keys[i]]["Temperature"].astype(float)
            sorted_df[keys[i]]["Humidity"].plot(rot = 45, ax = ax_hum, color = color, marker = marker, label = label)
            sorted_df[keys[i]]["Temperature"].plot(rot = 45, ax = ax_temp, color = color, marker = marker, label = label)
            if (switcher == 0):
                statistics_placer(stats, 0, i, sorted_df[keys[i]]["Humidity"], stat_lower_bound, stat_upper_bound)
                statistics_placer(stats, 1, i, sorted_df[keys[i]]["Temperature"], stat_lower_bound, stat_upper_bound)
        hums_axis(ax_hum, lower_hum_bound, upper_hum_bound, lower_time_bound, upper_time_bound, title_start_date, title_end_date)
        temps_axis(ax_temp, lower_temp_bound, upper_temp_bound, lower_time_bound, upper_time_bound, title_start_date, title_end_date, date_list, n_desired_ticks)
        if (switcher == 0):
            printing_stats(stats, stat_title_start, stat_title_end)
        end_time = int(time.time())            # Current time after the loop runs
        if ((end_time - start_time) > 3600):   # Every hour (3600 seconds since we're using the number of seconds since January 1, 1970), save the plot
            photo_saver(png_start_date, png_end_date)
            start_time = end_time
        plt.show(block = False)
        plt.pause(5)
        time.sleep(5)
    except KeyboardInterrupt:
        print("\nKeyboardInterrupt")
        sys.exit(1)

''' ================================================================================================================== '''
''' ============================================ PART 9: ACKNOWLEDGEMENTS ============================================ '''
''' ================================================================================================================== '''

# Code written by Christian Guinto-Brody for Professor Chris Neu's research group.
