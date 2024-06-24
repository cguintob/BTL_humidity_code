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
import numpy as np                    # This allows me to perform complex calculations on Pandas objects.

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

# These two variables are simply shorthand for "True" and "False" so that the organization of my comments for each variable below is retained more easily.
T = True
F = False

lower_hum_bound = 35                 # Lower bound on humidity (cannot be greater than upper_hum_bound, lower bound (realistically): 0)
upper_hum_bound = 65                 # Upper bound on humidity (cannot be less than lower_hum_bound, upper bound (realistically): 100)
lower_temp_bound = 0                 # Lower bound on temperature (cannot be greater than upper_temp_bound)
upper_temp_bound = 40                # Upper bound on temperature (cannot be less than lower_temp_bound)
assigned_start = T                   # Boolean that determines whether the user wants to specify the start date for plotting
assigned_end = T                     # Boolean that determines whether the user wants to specify the end date for plotting
start_date = "2024-06-17 10:00:00"   # Assigned start date for plotting (this is a placeholder date; will get reassigned if assigned_start == False)
end_date = "2024-06-17 12:00:00"     # Assigned end date for plotting (same as above; wil get reassigned if assigned_end == False)
assign_stat_start = T                # Boolean like "assigned_start," but for calculating statistics
assign_stat_end = T                  # Boolean like "assigned_end," but for calculating statistics
stat_start = "2024-06-17 11:00:00"   # Assigned start date for statistics (will get reassigned if assign_stat_start == False)
stat_end = "2024-06-17 15:00:00"     # Assigned end date for statistics (will get reassigned if assign_stat_end == False)
update_stats = F                     # Boolean telling the program whether to continue printing statistics to the screen (used mainly for updating/non-updating files)

n_desired_ticks = 10                              # Sometimes there are 11 ticks shown on the x-axis, but ultimately, we want constant and evenly-spaced ticks
colors = ["cyan", "green", "yellow", "magenta"]   # List of colors for plotting
markers = ["x", "v", "^", ".", ","]               # List of markers for plotting
markersize = 5                                    # Size of markers plotted
linewidth = 2                                     # Width of lines plotted

''' ================================================================================================================== '''
''' =========================================== PART ii: HELPER FUNCTIONS ============================================ '''
''' ================================================================================================================== '''

''' This is the "initialization" section, where I define a few helper functions 
(defined in order of appearance in the program) that execute things that I need 
to execute multiple times in the program. They will become more apparent later 
in the program. '''

''' ================================================================================================================== '''

# This function tells the user how to use the program.
def help_func():
    print("\nTips for Using Program\n")
    print("1) Must run with \"python NEW_READER [datafile1].txt [datafile2].txt ...\"")
    print("\ta) Can also run with \"python NEW_READER [path to file(s)]/*[keyword for file(s)]*\"")
    print("\tb) For help, run \"python NEW_READER HELP\"")
    print("\tc) If using Python3, replace \"python\" with \"python3\"")
    print("2) Plots data in updating or non-updating data files to screen")
    print("\ta) If updating data files, plot updates every 10 seconds")
    print("\tb) Saves plot as PNG every hour or so")
    print("\tc) Calculates statistics of data and prints to screen when plot updates")
    print("\td) Can change ranges of plot and statistics")
    print("3) User must go in and change variables if they please")
    print("\ta) \"lower_hum_bound\" and \"upper_hum_bound\" must be between 0 and 100, and the former cannot be larger than the latter")
    print("\tb) \"lower_temp_bound\" and \"upper_temp_bound\" can take any reasonable value, but the former cannot be larger than the latter")
    print("\tc) \"assigned_start\" and \"assigned_end\" tell the program the range for plotting")
    print("\t\ti) \"start_date\" and \"end_date\" denote that range")
    print("\t\tii) These variables have values already, but will be overwritten if \"assigned_start\" and/or \"assigned_end\" are \"False\"")
    print("\t\tiii) These variables do not have to be in the range the data were taken")
    print("\t\tiv) \"start_date\" cannot come after \"end_date\"")
    print("\td) \"assign_stat_start\" and \"assign_stat_end\" tell the program the range for calculating statistics")
    print("\t\ti) \"stat_start\" and \"stat_end\" denote that range")
    print("\t\tii) \"stat_end\" cannot occur before the start of data collection and \"stat_start\" cannot occur after the end of data collection, but both can be outside the range the data were taken")
    print("\t\t\t/) In this case, they will not take into account values not in the range")
    print("\t\t\t//) In the event where both values are outside the data range, the statistics for the object will be listed as \"NaN\"")
    print("\t\tiii) \"stat_start\" cannot come after \"stat_end\"")
    print("\te) \"update_stats\" tells the program whether it should expect an updating dataset")
    print("\t\ti) If the dataset is not updating but \"update_stats\" is set to true, the statistics will be printed to the screen every 10 seconds")
    print("\tf) \"n_desired_ticks\" is the number of x-ticks the user wants plotted on the graph")
    print("\t\ti) If there are fewer than \"n_desired_ticks\" points in the dataset, that number of ticks will be used")
    print("\tg) The lists colors and markers can be added to or changed as desired")
    print("\th) The markersize and linewidth can also be changed as desired, but for optimal presentation, they should be kept as they are")
    print("4) Plotting")
    print("\ta) Sensor data will take colors and markers give by the \"colors\" and \"markers\" lists, respectively; weather data will always be red and have \"*\" markers")
    print("\tb) Precipitation data will always be blue and plotted on the temperature graph")
    print("\tc) Absolute humidities will always be blue with a border color that is the same as its corresponding sensor data values")
    print("\t\ti) For example, relative humidities from sensor 1 will be green while absolute humidities from sensor 1 will be blue with a green border")
    print("5) Exit out of program by closing plot and typing \"Ctrl-c\"")
    print("\ta) Not closing plot before killing program will cause it to freeze on screen\n") 
    sys.exit(1)

''' This function, implemented 6/20/2024, is meant to calculate the absolute 
humidity in an environment based on the sensor's relative humidity and 
temperature readings. If we can find the absolute humidity given the relative 
humidity and temperature, then we might be able to see if the sensor is 
actually affecting the water levels in the air (i.e. if the absolute humidity 
plot is a straight line). "hum_ser" is the series of relative humidities as 
percents, first converted to decimals, while "temp_ser" is the series of 
temperatures, used in the calculation for saturated vapor pressure. Returned 
is the absolute humidity in g/m^3. '''
def abs_hum_calc(hum_ser, temp_ser):
    h = hum_ser.astype(float) / 100
    t = temp_ser.astype(float)
    A, B, C = 0.611, 17.502, 240.97                                       # These are constants, where [A] = kPa and [C] = degrees Celsius (B is dimensionless)
    sat_vapor_press = 1000 * (A * np.exp((B * t) / (C + t)))
    air_vapor_press = h.astype(float) * sat_vapor_press.astype(float)     # This is the vapor pressure of air
    m = 18.02                                                             # This is the molar mass of water, given in grams per mole
    R = 8.314                                                             # This is the universal gas constant, given in terms of Joules per mole-Kelvin
    T_K = t + 273.15                                                      # This is the temperature in Kelvin
    H_a = (m / (R * T_K.astype(float))) * air_vapor_press.astype(float)   # This is the absolute humidity
    return H_a.astype(float)

# This function formats and sorts the columns in a dataframe. I must include "inplace = True" if I want the modifications to save.
def df_formatter(dataframe):
    dataframe["Date"] = dataframe["Date"].astype(str) + " " + dataframe["Time"].astype(str)   # Modify elements in "Date" column by combining elements in columns "Date" and "Time"
    dataframe.rename(columns = {"Date": "Date and Time"}, inplace = True)                     # Rename column "Date" to "Date and Time"
    dataframe["Date and Time"] = pd.to_datetime(dataframe["Date and Time"])                   # Change elements in "Date and Time" to Pandas datetime objects
    dataframe.drop("Time", axis = 1, inplace = True)                                          # Remove column "Time"
    dataframe.sort_values(by = "Date and Time", inplace = True)                               # Sort datetime objects chronologically
    dataframe.set_index(["Date and Time"], inplace = True)                                    # Make column "Date and Time" the new index of the dataframe
    dataframe.dropna(inplace = True)                                                          # Removes any row where NaN appears
    if ("Port" in dataframe.columns.tolist()):                                                # Defines a column called "Absolute Humidity" for sensor data only
        dataframe["Absolute Humidity"] = abs_hum_calc(dataframe["Relative Humidity"], dataframe["Temperature"])
    dataframe["Relative Humidity"] = dataframe["Relative Humidity"].astype(float)             # Typecasts all the relative humidity values as floats
    dataframe["Temperature"] = dataframe["Temperature"].astype(float)                         # Typecasts all the temperature values as floats
    if ("Precipitation" in dataframe.columns.tolist()):                                       # Defines a column called "Precipitation" for weather data only
        dataframe["Precipitation"] = dataframe["Precipitation"].astype(float)
    
# This function defines the start date for plotting by comparing the corresponding indices in the dataframes in the dictionary.
def start_func(key_list, dictionary):
    cur_start = dictionary[key_list[0]].index.tolist()[0]                   # These variables keep track of the first data files given
    if (len(key_list) == 1):                                                # If there is only one data file given...
        start = dictionary[key_list[0]].index.tolist()[0] 
    else:
        for i in range(len(key_list) - 1):                                  # Check if date in 1st occurs before 2nd
            if (pd.Timestamp(dictionary[key_list[i]].index.tolist()[0]) < pd.Timestamp(dictionary[key_list[i + 1]].index.tolist()[0])):   
                if (pd.Timestamp(cur_start) < pd.Timestamp(dictionary[key_list[i]].index.tolist()[0])):
                    start = cur_start
                else:
                    start = dictionary[key_list[i]].index.tolist()[0]
            else:
                if (pd.Timestamp(cur_start) < pd.Timestamp(dictionary[key_list[i + 1]].index.tolist()[0])):
                    start = cur_start
                else:
                    start = dictionary[key_list[i + 1]].index.tolist()[0]   # If not, set the other equal to "start"
    return start                                                            # Return "start" to make this the start date

# This is an analogous function to "start_func," just for the end date for plotting.
def end_func(key_list, dictionary):
    cur_end = dictionary[key_list[0]].index.tolist()[len(dictionary[key_list[0]].index.tolist()) - 1]
    if (len(key_list) == 1):
        end = dictionary[key_list[0]].index.tolist()[len(dictionary[key_list[0]].index.tolist()) - 1]
    else:
        for i in range(len(key_list) - 1):
            if (pd.Timestamp(dictionary[key_list[i]].index.tolist()[len(dictionary[key_list[i]].index.tolist()) - 1]) > 
                pd.Timestamp(dictionary[key_list[i + 1]].index.tolist()[len(dictionary[key_list[i + 1]].index.tolist()) - 1])): 
                if (pd.Timestamp(cur_end) > pd.Timestamp(dictionary[key_list[i + 1]].index.tolist()[len(dictionary[key_list[i + 1]].index.tolist()) - 1])):
                    end = cur_end
                else:
                    end = dictionary[key_list[i]].index.tolist()[len(dictionary[key_list[i]].index.tolist()) - 1]
            else:
                if (pd.Timestamp(cur_end) > pd.Timestamp(dictionary[key_list[i + 1]].index.tolist()[len(dictionary[key_list[i + 1]].index.tolist()) - 1])):
                    end = cur_end
                else:
                    end = dictionary[key_list[i + 1]].index.tolist()[len(dictionary[key_list[i + 1]].index.tolist()) - 1]
    return end

# This function makes sure that, if there are assigned dates, they are in the correct format.
def date_formatter(date):
    try:
        pd.Timestamp(date)
    except:
        print("Assigned dates must be strings in the form YYYY-MM-DD HH:mm:ss.")
        sys.exit(1)

# This tells the program whether the user wants to assign dates or if they want to use the full range of the dataset.
def date_assigner(start, end, start_boolean, end_boolean, key_list, dictionary):
    if ((start_boolean == False) and (end_boolean == False)):    # If both booleans are "False," use the full range
        starter = start_func(key_list, dictionary)
        ender = end_func(key_list, dictionary)
    elif ((start_boolean == False) and (end_boolean == True)):   # If only start_boolean == False, assign it to the assigned start date
        starter = start_func(key_list, dictionary)
        date_formatter(end)
        ender = end
    elif ((start_boolean == True) and (end_boolean == False)):   # If only end_boolean == False, assign it to the assigned end date
        date_formatter(start)
        starter = start
        ender = end_func(key_list, dictionary)
    else:                                                        # If both booleans are "True," assign them to their appropriate assigned dates
        date_formatter(start)
        date_formatter(end)
        starter = start
        ender = end
    if (pd.Timestamp(starter) > pd.Timestamp(ender)):            # More so for assigned dates, are the dates in the correct order?
        print("Assigned start date must occur before assigned end date.")
        sys.exit(1)
    return (starter, ender)

# This function makes sure all the bounds/bound indices are appropriate and lets the user know if they aren't..
def bound_checker(low, high):
    if (low > high):
        print("At least one of your lower bounds is greater than its corresponding upper bound. This cannot occur.")
        sys.exit(1)

''' This function defines the bounds and some dates to be used for naming. The 
first two are the start and end dates and times for the plot titles, 
respectively. The second two are the start and end dates and times for the photo 
titles, respectively. They are all returned by the function. '''
def bounds(start, end):
    start_for_title = str(start)[:10] + " at " + str(start)[(10 + 1):]
    end_for_title = str(end)[:10] + " at " + str(end)[(10 + 1):]
    start_for_photo = str(start)[:10] + "_at_" + str(start)[(10 + 1):] 
    end_for_photo = str(end)[:10] + "_at_" + str(end)[(10 + 1):]
    return (start_for_title, end_for_title, start_for_photo, end_for_photo)

# This function defines the bounds to use for titling the displayed statistics.
def stat_bounds(start, end):
    title_start = str(start)[:10] + " at " + str(start)[(10 + 1):]
    title_end = str(end)[:10] + " at " + str(end)[(10 + 1):]
    return (title_start, title_end)

# This function defines some parameters for the axis on which I plot absolute humidity values.
def abs_axis(axis):
    axis.yaxis.set_label_position("right")
    axis.set_ylabel("Absolute Humidity (g/m\u00b3)", color = "b")
    axis.tick_params(axis = "y", labelcolor = "b")
    axis.set_ylim([0, None])

# This function corrects the dates given for calculating statistics if those dates weren't given in the range of the dataset.
def stat_date_formatter(start, end, dataframe):
    if ((start not in dataframe.index) and (end not in dataframe.index)):   # If the given statistics dates aren't in the dataset...
        start_indexer = dataframe.index.searchsorted(start)                 # ...search for the closest index to the given date...
        try:
            new_start = dataframe.index[start_indexer]                      # ...try to set the start date to be the date at that index
        except:
            new_start = dataframe.index[start_indexer - 1]                  # ...if the given date occurs after the final date in the dataframe, assign it to that
        end_indexer = dataframe.index.searchsorted(end)
        try:
            new_end = dataframe.index[end_indexer]
        except:
            new_end = dataframe.index[end_indexer - 1]
    elif (start not in dataframe.index):
        start_indexer = dataframe.index.searchsorted(start)
        try:
            new_start = dataframe.index[start_indexer]
        except:
            new_start = dataframe.index[start_indexer - 1]
        new_end = end
    elif (end not in dataframe.index):
        new_start = start
        end_indexer = dataframe.index.searchsorted(end)
        try:
            new_end = dataframe.index[end_indexer]
        except:
            new_end = dataframe.index[end_indexer - 1]
    else:                                                                   # If the dates are in the range, set them to the dates in the range
        new_start = start
        new_end = end
    return (new_start, new_end)

# This function defines the elements of the statistics dataframe printed to the screen.
def statistics_placer(stat_df, num, index, series, start, end):
    stat_df.loc[stat_df.index.tolist()[num], stat_df.columns.tolist()[index]] = str(series[str(start):str(end)].mean().round(4)) + " +/- " + str(series[str(start):str(end)].std().round(4))
    
# This function defines some parameters for the axis on which I plot precipitation levels from WTTR.
def precip_axis(axis):
    axis.yaxis.set_label_position("right")
    axis.set_ylabel("Precipitation (mm/3hr)", color = "b")
    axis.tick_params(axis = "y", labelcolor = "b")
    axis.set_ylim([0, None])

# This function defines some parameters for the axis on which I plot humidities.
def hums_axis(axis, low_hum, high_hum, start, end, title_low_time, title_high_time):
    axis.set_xlabel("")                                                                                   # Only want labels for bottom subplot
    axis.tick_params(axis = "x", bottom = False, labelbottom = False)                                     # Only want ticks for bottom subplot
    axis.set_ylabel("Relative Humidity (%)", color = "k")                                                 # Set y-axis label and color
    axis.tick_params(axis = "y", labelcolor = "k")                                                        # Set y-axis ticks and color
    axis.set_ylim([low_hum, high_hum])                                                                    # Set range (values are chosen in Part 5)
    axis.set_xlim(start, end)                                                                             # Set domain (based on range of dates found in Part 5)
    axis.set_title("Humidities from {0} to {1}".format(title_low_time, title_high_time), fontsize = 10)   # Set title using .format()

# This function defines some parameters for the axis on which I plot temperatures.
def temps_axis(axis, low_temp, high_temp, start, end, title_low_time, title_high_time, x_list, num_ticks):
    axis.set_xlabel("Date and Time")
    axis.tick_params(axis = "x", labelsize = 8)
    axis.xaxis.set_major_locator(mdates.SecondLocator(interval = int(len(x_list) / num_ticks)))             # Frequency of x-ticks
    axis.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d\n%H:%M:%S"))                              # Format of x-ticks
    axis.set_ylabel("Temperature (\u00b0C)", color = "k")
    axis.tick_params(axis = "y", labelcolor = "k")
    axis.set_ylim([low_temp, high_temp])    
    axis.set_xlim(start, end)
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
    if ((len(sys.argv) == 2) and (sys.argv[1] == "HELP")):
        help_func()
    for i in range(1, len(sys.argv)):         # I defined the range this way so that the i in the for loop and the i index for the system arguments matched.
        if (sys.argv[i].endswith(".txt")):
            files.append(sys.argv[i])
        else:
            print("Use the following format: python NEW_READER.py [datafile1].txt [datafile2].txt [datafile3].txt ...")
            print("Can also be used like this: python NEW_READER.py path_to_datafiles/[filename]*")
            print("If you need help in using this program or are running into issues, type \"python NEW_READER.py HELP\" for usage.")
            sys.exit(1)
else:
    print("Use the following format: python NEW_READER.py [datafile1].txt [datafile2].txt [datafile3].txt ...")
    print("Can also be used like this: python NEW_READER.py path_to_datafiles/[filename]*")
    print("If you need help in using this program or are running into issues, type \"python NEW_READER.py HELP\" for usage.")
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
5) df.iloc[0][0] --- iloc means "integer locator" and finds the element at [0][0] in this case

The if part of the if-else statement defines the weather data; the else part 
defines the sensor data. Both parts contain if-else statements---if the dataframe 
doesn't already exist, define it; if it does, add to it. '''

''' ================================================================================================================== '''

unsorted_df = {}
for f in files:
    try:
        df = pd.read_csv(f, sep = "\r\n", header = None, engine = "python")         # Create a dataframe by reading the contents of the file
        df = df[0].str.split(" ", expand = True)
        while ((df.isnull().values.any() == True) and (df.shape[1] > 6)):           # This gets rid of any rows that are too long
            df.drop(df.index[df.notnull().all(axis = 1)].tolist(), inplace = True)
            df.dropna(axis = 1, how = "all", inplace = True)
        df.dropna(axis = 0, inplace = True)                                         # This drops all the rows that aren't complete
        if ((len(df.columns) == 6) and ("-" in str(df.iloc[0][1]))):                # This if statement removes the port from the old version of weather data files
            df.drop(columns = df.columns[0], axis = 1, inplace = True)
        df.columns = [0, 1, 2, 3, 4]
        if ("-" in str(df.iloc[0][0])):                                             # Denotes weather data
            df.rename(columns = {0: "Date", 1: "Time",  2: "Relative Humidity", 3: "Temperature", 4: "Precipitation"}, inplace = True)
            if ("df{0}".format(0) not in list(unsorted_df.keys())):
                unsorted_df["df{0}".format(0)] = df
            else:
                unsorted_df["df{0}".format(0)] = pd.concat([unsorted_df["df{0}".format(0)], df])
        else:
            df.rename(columns = {0: "Port", 1: "Date",  2: "Time", 3: "Relative Humidity", 4: "Temperature"}, inplace = True)
            df.drop(df[df["Relative Humidity"].astype(float) > 100].index, inplace = True)
            if ("df{0}".format(int(df.iloc[0][0]) + 1) not in list(unsorted_df.keys())):
                unsorted_df["df{0}".format(int(df.iloc[0][0]) + 1)] = df
            else:
                unsorted_df["df{0}".format(int(df.iloc[0][0]) + 1)] = pd.concat([unsorted_df["df{0}".format(int(df.iloc[0][0]) + 1)], df])
    except:
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
    
start_date, end_date = date_assigner(start_date, end_date, assigned_start, assigned_end, keys, sorted_df)
stat_start, stat_end = date_assigner(stat_start, stat_end, assign_stat_start, assign_stat_end, keys, sorted_df)

date_list = pd.date_range(start_date, end_date, freq = "s")       # Pandas date range from start_date to end_date with a frequencty of every second

''' ================================================================================================================== '''
''' ============================================ PART 5: REVISTING BOUNDS ============================================ '''
''' ================================================================================================================== '''

''' This section does more with the bounds defined in Part i, namely making 
sure they're valid and also defining some more bounds that depend on the 
ones we defined above using the functions defined in Part ii. '''

''' ================================================================================================================== '''

bound_checker(lower_hum_bound, upper_hum_bound)
bound_checker(lower_temp_bound, upper_temp_bound)

title_start_date, title_end_date, png_start_date, png_end_date = bounds(start_date, end_date)
stat_title_start, stat_title_end = stat_bounds(stat_start, stat_end)

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
stats = pd.DataFrame(index = ["Relative Humidity (%)", "Temperature (\u00b0C)"], columns = columns)

abs_hum_definer = False                                   # This boolean helps to define the absolute-humidity axis, acting similarly to the "if (i == 0):" statement
hums = plt.subplot(211)                                   # Define a subplot. "211" maps to "2 rows," "1 column," "1st subplot"
for i in range(len(keys)):
    if ("Port" in sorted_df[keys[i]].columns.tolist()):   # If we have sensor data...
        color = colors[i]
        marker = markers[i]
        graph_label = "Sensor {0}".format(int(sorted_df[keys[i]]["Port"][0]) + 1)
        sorted_df[keys[i]]["Absolute Humidity"] = sorted_df[keys[i]]["Absolute Humidity"].astype(float)
        if (abs_hum_definer == False):
            ax_abs = sorted_df[keys[i]]["Absolute Humidity"].plot(rot = 45, marker = marker, secondary_y = True, color = color, lw = linewidth + 4, markersize = markersize + 3)
            sorted_df[keys[i]]["Absolute Humidity"].plot(rot = 45, ax = ax_abs,  marker = marker, secondary_y = True, color = "blue", lw = linewidth, markersize = markersize)
            abs_hum_definer = True
        else:
            sorted_df[keys[i]]["Absolute Humidity"].plot(rot = 45, ax = ax_abs, marker = marker, secondary_y = True, color = color, lw = linewidth + 4, markersize = markersize + 3)
            sorted_df[keys[i]]["Absolute Humidity"].plot(rot = 45, ax = ax_abs,  marker = marker, secondary_y = True, color = "blue", lw = linewidth, markersize = markersize)
        abs_axis(ax_abs)
    else:                                                 # If we have weather data...
        color = "red"
        marker = "*"
        graph_label = "CVille"
    if (i == 0):                                          # This defines the axis regardless of whether only weather data or sensor data is fed to the program.
        ax_hum = sorted_df[keys[i]]["Relative Humidity"].plot(rot = 45, color = color, marker = marker, label = graph_label, lw = linewidth, markersize = markersize)
    else:
        sorted_df[keys[i]]["Relative Humidity"].plot(rot = 45, color = color, marker = marker, label = graph_label, lw = linewidth, markersize = markersize)
    new_stat_start, new_stat_end = stat_date_formatter(stat_start, stat_end, sorted_df[keys[i]])
    if (new_stat_start != new_stat_end):
        statistics_placer(stats, 0, i, sorted_df[keys[i]]["Relative Humidity"], new_stat_start, new_stat_end)

hums_axis(ax_hum, lower_hum_bound, upper_hum_bound, start_date, end_date, title_start_date, title_end_date)

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
        ax_precip = sorted_df[keys[i]]["Precipitation"].plot(rot = 45, marker = "*", secondary_y = True, color = "blue", lw = linewidth, markersize = markersize)
        precip_axis(ax_precip)
    if (i == 0):
        ax_temp = sorted_df[keys[i]]["Temperature"].plot(rot = 45, color = color, marker = marker, label = graph_label, lw = linewidth, markersize = markersize)
    else:
        sorted_df[keys[i]]["Temperature"].plot(rot = 45, color = color, marker = marker, label = graph_label, lw = linewidth, markersize = markersize)
    new_stat_start, new_stat_end = stat_date_formatter(stat_start, stat_end, sorted_df[keys[i]])
    if (new_stat_start != new_stat_end):
        statistics_placer(stats, 1, i, sorted_df[keys[i]]["Temperature"], new_stat_start, new_stat_end)
        
temps_axis(ax_temp, lower_temp_bound, upper_temp_bound, start_date, end_date, title_start_date, title_end_date, date_list, n_desired_ticks)
    
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
    plt.pause(10)                                         # Pause the program for 10 seconds before continuing
except KeyboardInterrupt:
    print("\nKeyboardInterrupt")
    sys.exit(1)
    
start_time = int(time.time())    # This gets the current time and will be used for saving a figure every hour

while True:
    try:
        for i in range(len(files)):
            with open(files[i], "r") as f:                             # Open the files...
                lines = f.readlines()                                  # Read their lines...
                if (lines[-1] != lastLine[i]):                         # If the last line is not equal to whatever was collected to be the last line from before...
                    lastLine[i] = lines[-1]                            # ...set it equal to that line...
                    split_line = lastLine[i].rstrip("\n").split(" ")   # ...format the line by eliminating the newline character and splitting between spaces...
                    df = pd.DataFrame([split_line])                    # ...and create a new dataframe out of that line as a list
                    try:
                        if (len(df.columns) == 5):                     # If there are the appropriate number of columns... (there will no longer be six columns)
                            if ("-" in str(df.iloc[0][0])):            # ...and we have weather data...
                                df.columns = ["Date", "Time", "Relative Humidity", "Temperature", "Precipitation"]
                                df["Temperature"] = df["Temperature"].apply(lambda x: (int(x) - 32) / 1.8)
                                key = "df{0}".format(0)
                            else:                                      # ...otherwise, we have sensor data
                                df.columns = ["Port", "Date", "Time", "Relative Humidity", "Temperature"]
                                key = "df{0}".format(int(df.iloc[0][0]) + 1)
                            df_formatter(df)                           # Format the dataframe as before and then add it to the appropriate dataframe in sorted_df
                            sorted_df[key] = pd.concat([sorted_df[key], df])
                        else:                                          # If we don't have the appropriate number of columns (i.e. there was a timeout)...
                            continue                                   # ...do nothing
                    except ValueError:                                 # If there are NO columns, then we do nothing
                        continue
                else:                                                  # Likewise, if the last line of the file is nonexistent, do nothing
                    continue
        ax_hum.cla()                                                   # Now that we've made updates to sorted_df, we can replot by clearing the plots' axes
        ax_temp.cla()
        start_date, end_date = date_assigner(start_date, end_date, assigned_start, assigned_end, keys, sorted_df)         # Recalculate the dates if unassigned
        stat_start, stat_end = date_assigner(stat_start, stat_end, assign_stat_start, assign_stat_end, keys, sorted_df)   # Same for the statistics dates
        if (assigned_end == False):
            end_date.strftime("%Y-%m-%d %H:%M:%S")                     # This is for formatting. I ran into an issue for some reason
        date_list = pd.date_range(start_date, end_date, freq = "s")    # We must also recalculate the date range as well as our bounds
        title_start_date, title_end_date, png_start_date, png_end_date = bounds(start_date, end_date)
        if (update_stats == True):
            stat_title_start, stat_title_end = stat_bounds(stat_start, stat_end)
        for i in range(len(keys)):                                     # This part is basically Parts 6 and 7, just written a little differently
            if ("Precipitation" in sorted_df[keys[i]].columns.tolist()):
                ax_precip.cla()                                        # Clear the secondary precipitation axis, too (don't clear ax_abs, though)
                color = "red"
                marker = "*"
                label = "CVille"
                sorted_df[keys[i]]["Precipitation"] = sorted_df[keys[i]]["Precipitation"].astype(float)
                sorted_df[keys[i]]["Precipitation"].plot(rot = 45, ax = ax_precip, marker = "*", secondary_y = True, color = "blue", lw = linewidth, markersize = markersize)
                precip_axis(ax_precip)
            else:
                color = colors[i]
                marker = markers[i]
                label = "Sensor {0}".format(int(sorted_df[keys[i]]["Port"][0]) + 1)
                sorted_df[keys[i]]["Absolute Humidity"] = sorted_df[keys[i]]["Absolute Humidity"].astype(float)
                sorted_df[keys[i]]["Absolute Humidity"].plot(rot = 45, ax = ax_abs, marker = marker, secondary_y = True, color = color, lw = linewidth + 3, markersize = markersize + 3)
                sorted_df[keys[i]]["Absolute Humidity"].plot(rot = 45, ax = ax_abs, marker = marker, secondary_y = True, color = "blue", lw = linewidth, markersize = markersize)
                abs_axis(ax_abs)
            sorted_df[keys[i]]["Relative Humidity"] = sorted_df[keys[i]]["Relative Humidity"].astype(float)
            sorted_df[keys[i]]["Temperature"] = sorted_df[keys[i]]["Temperature"].astype(float)
            sorted_df[keys[i]]["Relative Humidity"].plot(rot = 45, ax = ax_hum, color = color, marker = marker, label = label, lw = linewidth, markersize = markersize)
            sorted_df[keys[i]]["Temperature"].plot(rot = 45, ax = ax_temp, color = color, marker = marker, label = label, lw = linewidth, markersize = markersize)
            if (update_stats == True):
                new_stat_start, new_stat_end = stat_date_formatter(stat_start, stat_end, sorted_df[keys[i]])
                if (new_stat_start != new_stat_end):
                    statistics_placer(stats, 0, i, sorted_df[keys[i]]["Relative Humidity"], new_stat_start, new_stat_end)
                    statistics_placer(stats, 1, i, sorted_df[keys[i]]["Temperature"], new_stat_start, new_stat_end)
        hums_axis(ax_hum, lower_hum_bound, upper_hum_bound, start_date, end_date, title_start_date, title_end_date)
        temps_axis(ax_temp, lower_temp_bound, upper_temp_bound, start_date, end_date, title_start_date, title_end_date, date_list, n_desired_ticks)
        if (update_stats == True):
            printing_stats(stats, stat_title_start, stat_title_end)
        end_time = int(time.time())                                    # Current time after the loop runs
        if ((end_time - start_time) > 3600):                           # Every hour (in seconds), save the plot
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
