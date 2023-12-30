import csv
import random
import time
import datetime
import serial
x_value = 0.0
##Humidity_1 = 55.0
##Humidity_2 = 55.0
##HD = 0.0
##HT = 0.0
ser = serial.Serial("COM6",9600)
ser1 = serial.Serial("COM7",9600)
ts = time.time()
st = datetime.datetime.fromtimestamp(ts).strftime('%Y_%m-%d_%H_%M_%S')
fieldnames = ["x_value","Timestamp", "Humidity_1", "Humidity_2","HD","HT"]

with open('data.csv', 'w') as csv_file:
    csv_writer = csv.DictWriter(csv_file,fieldnames=fieldnames)
    csv_writer.writeheader()

while True:
    with open('data.csv', 'a') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)


        cc=str(ser.readline())
        dd=str(ser1.readline())
        #print(cc)
        ccc = cc.split("<")
        ddd = dd.split("<")
        try:
            #print(ccc[1])
            ccc = ccc[1].split(">")
            ddd = ddd[1].split(">")
            #print(ccc)
            temphum = ccc[0].split(",")
            temphum1 = ddd[0].split(",")

            if temphum !=[]:
                x_value +=1
                ts = time.time()
                st = datetime.datetime.fromtimestamp(ts).strftime('%Y_%m-%d_%H_%M_%S')
                #print(temphum)
                Whichitone = temphum[0]
                Whichitone2 = temphum1[0]
                if Whichitone == "1":
                    DTemperature = float(temphum1[1]) - float(temphum[1])
                    DHumidity = float(temphum1[2]) - float(temphum[2])
                    Humidity_1 = float(temphum[2])
                    Humidity_2 = float(temphum1[2])
                elif Whichitone == "2":
                    DTemperature = float(temphum[1]) - float(temphum1[1])
                    DHumidity = float(temphum[2]) - float(temphum1[2])
                    Humidity_1 = float(temphum1[2])
                    Humidity_2 = float(temphum[2])
                HD = DHumidity
                HT = DTemperature

        except:
            pass


        info = {
        "x_value": x_value,
        "Timestamp":st,
        "Humidity_1": Humidity_1,
        "Humidity_2": Humidity_2,
        "HD":HD,
        "HT":HT
        }

        csv_writer.writerow(info)
        print(x_value,Humidity_1,Humidity_2,HD,HT)

##        total_1 = total_1 + random.randint(-6,8)
##        total_2 = total_2 + random.randint(-5,6)
        #total_1 = random.randint(-6,8)
        #total_2 = random.randint(-5,6)
        #Differential = total_1-total_2
    time.sleep(0.05)


