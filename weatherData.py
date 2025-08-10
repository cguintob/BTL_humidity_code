import datetime             # Contains information about the date and time of either current moments or moments in the past and future
from datetime import date   # Module in "datetime" that specifically accesses the date
import sys                  # Allows the user to use command line arguments
import requests             # Allows the user to get information from a url
import time                 # Necessary for addressing requests.exceptions.ConnectionErrors

''' ================================================================================================================== '''
''' ==================================================== OVERVIEW ==================================================== '''
''' ================================================================================================================== '''

''' This script solely collects weather data using WTTR. Since it kept timing 
out, we thought it was a good idea to decouple the weather-data collection 
from the sensor-data collection. '''

''' ================================================================================================================== '''
''' ================================================ PART i: VARIABLES =============================================== '''
''' ================================================================================================================== '''

''' The following are variables used in the program, planted here for easy
access in case they need to be changed. '''

''' ================================================================================================================== '''

rest_time = 10                                           # This variable tells us how often we want to get weather data. 
url = "http://wttr.in/Charlottesville?u&format=%h+%t+%p"   # This is the URL from which we're fetching data.

''' ================================================================================================================== '''
''' ========================================= PART 1: COMMAND-LINE ARGUMENTS ========================================= '''
''' ================================================================================================================== '''

''' Similar to sensorData.py, this section of the code lets you specify your 
data file and makes sure that it's viable. '''

''' ================================================================================================================== '''

try:
    if (sys.argv[1].endswith(".txt")):
        file1 = sys.argv[1]
    else:
        print("Use the following format: python weatherData.py [datafile].txt\n")
        sys.exit(1)
except IndexError:
    print("Use the following format: python weatherData.py [datafile].txt\n")
    sys.exit(1)

''' ================================================================================================================== '''
''' ====================================== PART 2: FETCHING DATA FROM WEBSITES ======================================= '''
''' ================================================================================================================== '''

''' I intended to leave my code running for about five days in between my 
Thursday work and Tuesday research meeting and then show a plot of my 
measurements at the meeting, but at about 6 pm after I left, my code "crashed," 
leaving the WTTR data incomplete (i.e. the index and date were printed to the 
data file but the humidity and temperature were not). The reason for the "crash"
was the following error: 

requests.exceptions.SSLError: EOF occurred in violation of protocol (_ssl.c:618)

This error, as I understand, is a result of the server and the website becoming 
out of sync, possibly due to overload (I was fetching data from the website 
every second for several hours before the "crash." So, I opened a session, which
allows for the persistence of certain parameters across requests. The first 
line defines a session opened by requests, the second line defines an adapter 
(used to define interaction methods for an HTTP service, and the third line 
defines a prefix for which the adapter is to be used (any website with this 
prefix will use the adapter. This code was implemented 4/30/2024.

UPDATE 5/3/2024: I added the retry line because my code timed out after about 
three days, which is longer than before, but not optimal. ''' 

''' ================================================================================================================== '''

sess = requests.Session()
retry = requests.packages.urllib3.util.retry.Retry(total = 5, backoff_factor = 0.1, status_forcelist = [500, 502, 503, 504])
adapter = requests.adapters.HTTPAdapter(max_retries = retry)
sess.mount("http://", adapter)

''' ================================================================================================================== '''
''' ============================================ PART 3: DATA COLLECTION ============================================= '''
''' ================================================================================================================== '''

''' First, I define the URL from which I'll be requesting to fetch data. Then, I 
use a try-except statement that will get a new request with a new User-Agent 
if there's no connection error (changing the User-Agent should prevent there 
from being connection errors caused by refusal from the website) and write 
the desired data to the desired data file. If there is a connection error, 
the program will pause for a bit, get a new User-Agent, and continue. 

It's important to note that I open and close the data file each time I add a
new set of measurements (hence why I use "a" instead of "w"). I did this in 
case we need to stop data collection but didn't want to lose our data. By 
continuously opening and closing the file, we save the data, preventing it 
from being lost. 

UPDATE: As of 6/24/2024, WTTR apparently received over 1M requests in one day, 
causing it to lose data storage. So, I implemented an if statement that will 
cause the program to sleep for an hour to let it reset. '''

''' ================================================================================================================== '''

while True:
    try:
        day = date.today()
        cur_time = datetime.datetime.now().strftime("%H:%M:%S")                          # Named "cur_time" for "current time" so it didn't conflict with time module
        try:
            res = sess.get(url)
            converted_string = res.text.translate({ord(i): None for i in "%+FC\xb0mm"})   # Replaces all these delimiters with ""
            if ("Unknown location" in converted_string):
                print("WTTR had too many requests. Let's let it reset. Check back in an hour.")
                time.sleep(3600)
                print("Ready after an hour of rest.")
                print("\n")
                continue
            weather_data = open(file1, "a")
            weather_data.write(str(day))
            weather_data.write(" ")
            weather_data.write(str(cur_time))
            weather_data.write(" ")
            weather_data.write(str(converted_string))
            weather_data.write("\n")
            weather_data.close()
            print(str(day) + " " + str(cur_time))
            print("Weather")
            print("Humidity (%), Temperature (\u00B0F), Precipitation (mm/3hr)")
            print(converted_string)
            print("\n")
        except requests.exceptions.ConnectionError:
            print("Raising requests.exceptions.ConnectionError")
            time.sleep(2 * rest_time)
            print("Ready after {0} seconds of rest.".format(2 * rest_time))
            print("\n")
            continue
    except KeyboardInterrupt:
        print("\nKeyboardInterrupt")
        sys.exit(1)
        print("Done!")
        sys.exit(1)
    time.sleep(rest_time)
        
''' ================================================================================================================== '''
''' ============================================ PART 4: ACKNOWLEDGEMENTS ============================================ '''
''' ================================================================================================================== '''

# Code written by Christian Guinto-Brody for Professor Chris Neu's research group.
