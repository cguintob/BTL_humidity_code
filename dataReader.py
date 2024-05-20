''' This script takes the data from the Arduino that was put
into a data file by sensorData.py and plots it. When running
this script, we do "python dataReader.py," and it will plot
humidity and temperature graphs over time to the screen. '''

# These packages are useful for plotting and for math.
import matplotlib.pyplot as plt
import numpy as np
import sys

'''--------------------------------------------------------------------------'''
'''--------------------------------------------------------------------------'''
'''--------------------------------------------------------------------------'''

def plotting_from_outside_macro(file1, file2):
    
    # These lists will adopt the appropriate values from our data files.
    index = []
    dates_and_times = []
    humidities = []
    temps = []
    
    weather_data_index = []
    weather_data_temps = []
    weather_data_hums = []
    weather_data_precips = []
    
    ''' This for loop puts the appropriate data into the appropriate lists.
    Note that times[] contains both the data from the second column and the
    data from the third column, separated by a newline character. This will
    be useful for plotting the labels along the x-axis. '''
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
            
    for line in open(file2, "r"):
        lines = [i for i in line.split()]
        
        ''' I intended to leave my code running for about five days in between
        my Thursday work and Tuesday research meeting and then show a plot of
        my measurements at the meeting, but at about 6 pm after I left, my code
        "crashed," leaving the WTTR data incomplete (i.e. the index and date
        were printed to the data file but the humidity and temperature were not).
        As a result, when I tried plotting what data I did have, the range of
        values for lines[3] and lines[4] (i.e. humidities and temperatures) was
        smaller than that of lines[0] (i.e. indices), so I was running into a 
        "list index out of range" error. By only using data where the list (i.e.
        row in the dataset) has a length equal to the expected length (i.e. 6),
        I was able to circumnavigate this issue. This simple code was implemented
        4/30/2024 and was a very significant change. '''
        if (len(lines) == 6):
            weather_data_index.append(lines[0])
            weather_data_hums.append(lines[3])
            weather_data_temps.append(lines[4])
            weather_data_precips.append(lines[5])
        else:
            continue
            
    for i in range(len(weather_data_temps)):
        weather_data_temps[i] = (int(weather_data_temps[i]) - 32) / 1.8
        
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
        indexed_times.append(dates_and_times[n * step])
        n += 1
        
    ''' Originally, when I plotted the x-ticks, I had the following:
    
    plt.xticks(np.arange(len(index), step = len(index) / 10), times, ...).
    
    By using times as my list, only the first 10 data points displayed as the
    x-tick labels, not the data point at each step. To correct this, I introduced
    the new list indexed_times, which was explained above. I also changed 10 to
    n_desired_ticks in case I want to change the number of ticks. ''' 
    
    weather_data_points = np.linspace(0, len(index), len(weather_data_index))
    precip_points = np.linspace(0, len(index), len(weather_data_precips))
    
    ''' This section of code plots the humidities. I used "superposition" with my
    plotting because I had to plot 1) two different graphs at the same time on
    different canvases, 2) two different graphs on the same canvas with the same
    x-axis but different numbers of data points, and 3) a third graph that uses a 
    different y-axis in addition to different numbers of data points on the same
    x-axis. To do this, I defined the plot and the x-axis as two different subplots
    then defined the y-axis of the third graph as a twin axis that uses the x-axis
    of the first two graphs (if that made any sense). Then, I plotted the points
    and set the characteristics of the graphs. '''
    hum, ax1 = plt.subplots()
    ax2 = ax1.twinx()
    
    ax1.plot(index, humidities, marker = "+", c = "g", label = "Assembly Room")
    ax1.plot(weather_data_points, weather_data_hums, marker = "+", c = "r", label = "Charlottesville")
    ax2.plot(precip_points, weather_data_precips, marker = "o", c = "b")

    # These denote the lower and upper bounds for the humidity graph.
    lower_hum_range_limit = 0
    upper_hum_range_limit = 100
    
    ax1.set_xlabel("Date and Time")
    ax1.set_ylabel("Relative Humidity (%)", color = "g")
    ax1.tick_params(axis = "x", labelsize = 8)
    ax1.tick_params(axis = "y", labelcolor = "r")
    ax1.set_ylim([lower_hum_range_limit, upper_hum_range_limit])
    ax2.set_ylabel("Precipitation (mm/3hr)", color = "b")
    ax2.tick_params(axis = "y", labelcolor = "b")
    ax2.set_ylim([0, None])
    
    plt.xticks(np.arange(len(index), step = len(index) / n_desired_ticks), indexed_times)
    hum.suptitle("Humidities at Various Times")
    hum.autofmt_xdate(ha = "center")
    
    # These lines show the optimal range of humidities.
    ax1.plot([0, len(index)], [40, 40], c = "y", linewidth = 3.0)
    ax1.plot([0, len(index)], [60, 60], c = "y", linewidth = 3.0, label = "Optimal Range")
    ax1.legend(loc = "upper right")
    hum.show()
    
    ''' This section of code finds and displays the percent of 
    humidities in the optimal range. '''
    n_optimal = 0
    for i in range(len(humidities)):
        if float(humidities[i]) > 40 and float(humidities[i]) < 60:
            n_optimal += 1
        else:
            continue
    print("Percent of humidities in optimal range:", float(n_optimal)/float(len(humidities)) * 100)

    # These denote the lower and upper bounds for the temperature graph.
    lower_temp_range_limit = 0
    upper_temp_range_limit = 50

    # This section of code plots the temperatures.
    temp = plt.figure(2)
    plt.title("Temperatures at Various Times")
    plt.xlabel("Date and Time")
    plt.ylabel("Temperature (C)")
    plt.ylim([lower_temp_range_limit, upper_temp_range_limit])
    plt.xticks(np.arange(len(index), step = len(index) / n_desired_ticks), indexed_times, fontsize = 8, rotation = 45)
    plt.plot(index, temps, marker = "+", c = "g", label = "Assembly Room")
    plt.plot(weather_data_points, weather_data_temps, marker = "+", c = "r", label = "Charlottesville")
    plt.legend(loc = "upper right")
    temp.show()
    
    # This command is necessary for showing the plots separately, for some reason.
    input()

'''--------------------------------------------------------------------------------------------------------------------------------------------'''
'''--------------------------------------------------------------------------------------------------------------------------------------------'''
'''--------------------------------------------------------------------------------------------------------------------------------------------'''

def plotting_from_command_line(file1, file2):

    ''' Like in sensorData.py, these variables prevents us 
    from changing too much code. The first file gives us the
    actual measured data from our Arduino while the second
    file gives us the data from wttr. Of course, we test
    to see if the argument is given. '''
    try:
        if (sys.argv[1].endswith(".txt")):
            file1 = sys.argv[1]
        else:
            print("Use the following format: python dataReader.py [datafile1].txt [datafile2].txt [number1] [number2]\n")
            sys.exit(1)
    except IndexError:
        print("Use the following format: npython dataReader.py [number] [datafile1].txt [datafile2].txt [number1] [number2]\n")
        sys.exit(1)
        
    try:
        if (sys.argv[2].endswith(".txt")):
            file2 = sys.argv[2]
        else:
            print("Use the following format: python dataReader.py [datafile1].txt [datafile2].txt [number]\n")
            sys.exit(1)
    except IndexError:
        print("Use the following format: python dataReader.py [datafile1].txt [datafile2].txt [number]\n")
        sys.exit(1)

    # The remaining code is exactly the same as in plotting_from_outside_macro().
    index = []
    dates_and_times = []
    humidities = []
    temps = []
    
    weather_data_index = []
    weather_data_temps = []
    weather_data_hums = []
    weather_data_precips = []

    for line in open(file1, "r"):
        lines = [i for i in line.split()]
        index.append(lines[0])
        dates_and_times.append(lines[1] + "\n" + lines[2])
        humidities.append(lines[3])
        temps.append(lines[4])
        
    for i in range(len(index) - 1):
        if int(index[i + 1]) <= int(index[i]):
            index[i + 1] = int(index[i]) + 1
        else:
            continue
            
    for line in open(file2, "r"):
        lines = [i for i in line.split()]
        if (len(lines) == 6):
            weather_data_index.append(lines[0])
            weather_data_hums.append(lines[3])
            weather_data_temps.append(lines[4])
            weather_data_precips.append(lines[5])
        else:
            continue
            
    for i in range(len(weather_data_temps)):
        weather_data_temps[i] = (int(weather_data_temps[i]) - 32) / 1.8

    indexed_times = []
    n = 0
    n_desired_ticks = 10
    step = len(index) / n_desired_ticks
    
    while n < n_desired_ticks:
        indexed_times.append(dates_and_times[n * step])
        n += 1
        
    weather_data_points = np.linspace(0, len(index), len(weather_data_index))
    precip_points = np.linspace(0, len(index), len(weather_data_precips))

    hum, ax1 = plt.subplots()
    ax2 = ax1.twinx()
    
    ax1.plot(index, humidities, marker = "+", c = "g", label = "Assembly Room")
    ax1.plot(weather_data_points, weather_data_hums, marker = "+", c = "r", label = "Charlottesville")
    ax2.plot(precip_points, weather_data_precips, marker = "o", c = "b")
    
    # These denote the lower and upper bounds for the humidity graph.
    lower_hum_range_limit = 0
    upper_hum_range_limit = 100

    ax1.set_xlabel("Date and Time")
    ax1.set_ylabel("Relative Humidity (%)", color = "g")
    ax1.tick_params(axis = "x", labelsize = 8)
    ax1.tick_params(axis = "y", labelcolor = "r")
    ax1.set_ylim([lower_hum_range_limit, upper_hum_range_limit])
    ax2.set_ylabel("Precipitation (mm/3hr)", color = "b")
    ax2.tick_params(axis = "y", labelcolor = "b")
    ax2.set_ylim([0, None])
    
    plt.xticks(np.arange(len(index), step = len(index) / n_desired_ticks), indexed_times)
    hum.suptitle("Humidities at Various Times")
    hum.autofmt_xdate(ha = "center")
    
    ax1.plot([0, len(index)], [40, 40], c = "y", linewidth = 3.0)
    ax1.plot([0, len(index)], [60, 60], c = "y", linewidth = 3.0, label = "Optimal Range")
    ax1.legend(loc = "upper right")
    hum.show()
    
    n_optimal = 0
    for i in range(len(humidities)):
        if float(humidities[i]) > 40 and float(humidities[i]) < 60:
            n_optimal += 1
        else:
            continue
    print("Percent of humidities in optimal range:", float(n_optimal)/float(len(humidities)) * 100)

    # These denote the lower and upper bounds for the temperature graph.
    lower_temp_range_limit = 0
    upper_temp_range_limit = 50

    temp = plt.figure(2)
    plt.title("Temperatures at Various Times")
    plt.xlabel("Date and Time")
    plt.ylabel("Temperature (C)")
    plt.ylim([lower_temp_range_limit, upper_temp_range_limit])
    plt.xticks(np.arange(len(index), step = len(index) / n_desired_ticks), indexed_times, fontsize = 8, rotation = 45)
    plt.plot(index, temps, marker = "+", c = "g", label = "Assembly Room")
    plt.plot(weather_data_points, weather_data_temps, marker = "+", c = "r", label = "Charlottesville")
    plt.legend(loc = "upper right")
    temp.show()
    
    input()

'''--------------------------------------------------------------------------------------------------------------------------------------------'''
'''--------------------------------------------------------------------------------------------------------------------------------------------'''
'''--------------------------------------------------------------------------------------------------------------------------------------------'''

# This function is necessary for distinguishing between plotting from sensorData.py and from using the command line.
def number(num1, num2, file1, file2):
    if ((num1 == 1) and (num2 == 1)):
        plotting_from_outside_macro(file1, file2)
    else:
        plotting_from_command_line(file1, file2)

'''--------------------------------------------------------------------------------------------------------------------------------------------'''
'''--------------------------------------------------------------------------------------------------------------------------------------------'''
'''--------------------------------------------------------------------------------------------------------------------------------------------'''

# This checks to see if I'm plotting from sensorData.py or the command line.
if (len(sys.argv) > 4):
    number(sys.argv[3], sys.argv[4], sys.argv[1], sys.argv[2]) # Command line
else:
    print("Get ready...")




# Code written by Christian Guinto-Brody for Professor Chris Neu's research group.



















































'''-----------------------------------------------------------'''
''' Like in sensorData.py, the code from here on are ideas I was testing. '''







# x = [dt.datetime.strptime(d, '%Y-%m-%d').date() for d in dates]

# plt.ylimit(0, 100)
# plt.gca().xaxis.set_major_formatter(dates.DateFormatter('%Y-%m-%d'))
# plt.gca().xaxis.set_major_locator(dates.DayLocator())
# plt.plot_date(timestamps, humidities, marker = "o", c = "g", linestyle = "solid")




''' comparison_temps = []
comparison_hums = []
m = 0
k = 0
while k < len(weather_data_times):
    print(m, k)
    if times[m] != weather_data_times[k]:
        comparison_temps.append(0)
        comparison_hums.append(0)
    else:
        if weather_data_times[k] != "NaN":
            comparison_temps.append(0)
            comparison_hums.append(0)
        else:
            comparison_temps.append(weather_data_temps[k])
            comparison_hums.append(weather_data_hums[k])

    k += 1
    m += int(len(index)/len(weather_data_times))

print(len(comparison_temps), len(comparison_hums))
'''
'''
for m in range(len(index)):
    print(m)
    for k in range(len(weather_data_times)):
        if times[m] != weather_data_times[k]:
            comparison_temps.append(0)
            comparison_hums.append(0)
        else:
            if weather_data_times[k] != "NaN":
                comparison_temps.append(0)
                comparison_hums.append(0)
            else:
                comparison_temps.append(weather_data_temps[k])
                comparison_hums.append(weather_data_hums[k])
'''



''' This code specifically was how I originally plotted the humidities
before adding the third axis for precipitation. '''

'''
hum = plt.figure(1)
plt.title("Humidities at Various Times")
plt.xlabel("Date and Time")
plt.ylabel("Relative Humidity (%)")
plt.xticks(np.arange(len(index), step = len(index) / n_desired_ticks), indexed_times, fontsize = 8, rotation = 45)
plt.plot(index, humidities, marker = "o", c = "g")
# plt.plot(index, pred_humidity, marker = "o", c = "r")
plt.plot(weather_data_points, weather_data_hums, marker = "o", c = "r")
plt.plot(precip_points, precips, marker = "o", c = "b")
hum.show()
'''






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




'''
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

data = ''
delay = 800

options = webdriver.ChromeOptions()
options.add_experimental_option('useAutomationExtension', False)
driver = webdriver.Chrome(options=options, executable_path="/home/aang/BTL_humidity_code/chromedriver")
driver.set_page_load_timeout(1000)
url = 'http://www.mfinante.gov.ro/patrims.html?adbAdbId=30'
driver.get(url)

try:
    myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'patrims')))
    print("Page is ready!")

except TimeoutException:
        print("Loading took too much time!")

rows = driver.find_elements_by_xpath("//table[@id='patrims']/tbody/tr")
print(len(rows))

listofdicts = []

def builder(outputlist, inputlist):
    #i =0
    for row in inputlist:
        #i+=1
        #print(i)
        soup = BeautifulSoup(row.get_attribute('innerHTML')  , 'html.parser')
        td= soup.find_all('td')
        d = {   "Legend" : soup.find("legend").get_text().strip(),
                "Localitatea" : td[2].get_text().strip(),
                "Strada" : td[4].get_text().strip(),
                "Descriere Tehnica" : td[6].get_text().strip(),
                "Cod de identificare" : td[-7].get_text().strip(),
                "Anul dobandirii sau darii in folosinta " : td[-6].get_text().strip(),
                "Valoare" : td[-5].get_text().strip(),
                "Situatie juridica" : td[-4].get_text().strip(),
                "Situatie juridica actuala" : td[-3].get_text().strip(),
                "Tip bun" : td[-2].get_text().strip(),
                "Stare bun" : td[-1].get_text().strip(),
            }
        outputlist.append(d)
    print('done!')

builder(listofdicts, rows)

print('writing result')
frame = pd.DataFrame(listofdicts)

# import urllib.request
# from pprint import pprint
# from html_table_parser.parser import HTMLTableParser
# import pandas as pd
'''

