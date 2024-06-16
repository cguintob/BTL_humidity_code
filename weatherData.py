import datetime             # Contains information about the date and time of either current moments or moments in the past and future
from datetime import date   # Module in "datetime" that specifically accesses the date
import sys                  # Allows the user to use command line arguments
import requests             # Allows the user to get information from a url
import random               # Necessary for changing the user-agent used for fetching WTTR data
import time                 # Necessary for addressing requests.exceptions.ConnectionErrors

''' ================================================================================================================== '''
''' ==================================================== OVERVIEW ==================================================== '''
''' ================================================================================================================== '''

''' This script solely collects weather data using WTTR. Since it kept timing 
out, we thought it was a good idea to decouple the weather-data collection 
from the sensor-data collection. '''

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
three days, which is longer than before, but not optimal. 

UPDATE 6/14/2024: My code was STILL timing out (specifically refusing to 
connect), so I added a list of User_Agents that are chosen by the session at 
random (using random.choice()) from which the request will appear to have been. 
Some of the User-Agents in the list are duplicated at random so that some sites 
are visited more often than others. '''

''' ================================================================================================================== '''

user_agents = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
               "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0",
               "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_4_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Safari/605.1.15",
               "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.2420.81",
               "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
               "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
               "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0",
               "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 OPR/109.0.0.0",
               "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
               "Mozilla/5.0 (X11; Linux i686; rv:124.0) Gecko/20100101 Firefox/124.0",
               "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0",
               "Mozilla/5.0 (Macintosh; Intel Mac OS X 14.4; rv:124.0) Gecko/20100101 Firefox/124.0",
               "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0",
               "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_4_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Safari/605.1.15",
               "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_4_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 OPR/109.0.0.0",
               "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
               "Mozilla/5.0 (X11; Linux i686; rv:124.0) Gecko/20100101 Firefox/124.0",
               "Mozilla/5.0 (X11; Linux i686; rv:124.0) Gecko/20100101 Firefox/124.0"]
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
from being lost. '''

''' ================================================================================================================== '''

# This variable tells us how often we want to get weather data.
rest_time = 10

while True:
    try:
        day = date.today()
        cur_time = datetime.datetime.now().strftime("%H:%M:%S")   # Named "cur_time" for "current time" so it didn't conflict with time module
        url = "http://wttr.in/Charlottesville?format=%h+%t+%p"
        sess.headers.update({"User-Agent": random.choice(user_agents)})
        try:
            res = sess.get(url)
            converted_string = res.text.translate({ord(i): None for i in "%+F\xb0mm"})   # Replaces all these delimiters with ""
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
            print("Humidity (%), Temperature (F), Precipitation (mm/3hr)")
            print(converted_string)
            print("\n")
        except requests.exceptions.ConnectionError:
            print("Raising requests.exceptions.ConnectionError")
            time.sleep(2 * rest_time)
            print("Ready after 20 seconds of rest.")
            print("\n")
            sess.headers.update({"User-Agent": random.choice(user_agents)})
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
