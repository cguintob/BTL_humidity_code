import serial
import datetime
from datetime import date

def readserial(comport, baudrate, timestamp = False):
    ser = serial.Serial(comport, baudrate, timeout = 0.1)  
    # 1/timeout is the frequency at which the port is read

    counter = 0

    file = "data_file7.txt"

    init_file = open(file, "w")
    init_file.write("")
    init_file.close

    while True:
        data = ser.readline().decode().strip()
        if ((data == "Starting up...") or (data == "Sensor not running.") or (data == "AHT10 running")):
            print(data)
        elif ((data == "") or (data == "0.00") or (data == "-50.00") or (data == "..") or (data == "up..")):
            continue
        elif (data == "Done!"):
            print(data)
            break
        else:
            if (counter % 10 == 0):
                print("Gathering data. Please be patient. It's working, I promise.")
            day = date.today()
            time = datetime.datetime.now().strftime("%H:%M")
            if (counter % 2 == 0):
                data_file = open(file, "a")
                data_file.write(str(int(0.5 * counter)))
                data_file.write(" ")
                data_file.write(str(day))
                data_file.write(" ")
                data_file.write(str(time))
                data_file.write(" ")
                data_file.write(str(data))
                data_file.write(" ")
            else:
                data_file.write(str(data))
                data_file.write("\n")
                data_file.close()
            counter += 1

if __name__ == '__main__':
    readserial('/dev/ttyACM0', 9600, True)
    # COM port, Baudrate, Show timestamp
    






''' The code from here on are ideas I was testing and didn't work. '''

# import matplotlib.dates as dates
# time = dates.date2num(datetime.datetime.now())

# timestamps.append(str(time))
# array.append(data)

# array = []
# timestamps = []
# humidities = []
# temps = []
   

'''
  elif (data == "Done gathering data!"):
            print(data)
            for x in range(len(array)):
                if (x % 2 != 1):
                    humidities.append(array[x])
                else:
                    temps.append(array[x])
            print("Done!")
            break
      '''


'''
    data_file = open("data_filel.txt", "w")
    for x in range(int(0.5 * len(array))):
        # data_file = open("data_file.txt", "a")
        data_file.write(timestamps[x])
        data_file.write(" ")
        data_file.write(humidities[x])
        data_file.write(" ")
        data_file.write(temps[x])
        data_file.write("\n")
        # data_file.close()
    data_file.close()
'''
    

'''if (counter % 2 == 0):
                data_file = open("data_file.txt", "a")
                data_file.write(str(time))
                data_file.write(" ")
                data_file.write(str(data))
                data_file.write(" ")
            else:
                data_file.write(str(data))
                data_file.write("\n")
                data_file.close()
            '''


'''
if (counter > 100):
                for x in range(len(array)):
                    if (x % 2 == 0):
                        y = int(0.5 * x)
                        print(y, x)
                        humidities.append(array[x]) 
                        print(array[x])
                    else:
                        y = int(0.5 * x + 0.5)
                        temps[y] = array[x]
                        # print(temps[y])
                        # for x in range(100):
                        # print(humidities[x], temps[x])
                print("Done!")
                break
'''

























# import serial
# from datetime import datetime

# today = str(datetime.today().date())
# print("today is " +  today)

'''
sensor = "AHT10"
serial_port = '/dev/ttyACM0'
baud_rate = 9600
path = "%s_LOG_%s.txt" % (str(datetime.now()), sensor)
ser = serial.Serial(serial_port, baud_rate)
with open(path, 'w+') as f:
    while True:
        line = ser.readline()
        f.writelines([line.strip(), " t = %s \n " % (datetime.now())])
'''




        # if data and timestamp:
        #    timestamp = time.strftime('%H:%M:%S')
        #    print(timestamp > data)
        # elif data:
