# Simple demo of reading each analog input from the ADS1x15 and printing it to
# the screen.
# Author: Tony DiCola
# License: Public Domain
import time
from sklearn.ensemble import IsolationForest
from sklearn.svm import OneClassSVM
from sklearn.metrics.pairwise import cosine_similarity
from scipy.stats import entropy
import numpy as np
from collections import Counter
import pandas as pd
clasifier = "Cosine"
import time
import datetime

#gpio.output(13,1)
#i = gpio.input(5)
# Import the ADS1x15 module.

# Or create an ADS1015 ADC (12-bit) instance.
#adc = Adafruit_ADS1x15.ADS1015()

# Note you can change the I2C address from its default (0x48), and/or the I2C
# bus by passing in these optional parameters:
#adc = Adafruit_ADS1x15.ADS1015(address=0x49, busnum=1)

# Choose a gain of 1 for reading voltages from 0 to 4.09V.
# Or pick a different gain to change the range of voltages that are read:
#  - 2/3 = +/-6.144V
#  -   1 = +/-4.096V
#  -   2 = +/-2.048V
#  -   4 = +/-1.024V
#  -   8 = +/-0.512V
#  -  16 = +/-0.256V
# See table 3 in the ADS1015/ADS1115 datasheet for more info on gain.
# Main loop.
datatotrain = []
iteration = 100
j=0
Flag = 1
collectdataformodelcreation = 1
splitter = 20
#Flags
MainFlag = 1
CollectdataFlag = 1
TrainClasifierFlag = 0
TestFlag = 0
CollectdataFlag2 = 0
import serial


##
TrainClasifierFlag = 0
TestFlag = 0
CollectdataFlag2 = 0
kfolding = 10
collectdataformodelcreation = 1
splitter = 10
ser = serial.Serial("COM6",9600)
ser1 = serial.Serial("COM7",9600)
print(ser)
while True:
    print("Data Collection")
    jj = 0
    threshold = 10000
    datatotrain = []
    TimeTemperatureHUmidity2 = []
    CollectdataFlag2 = 1
    while CollectdataFlag2:
        cc=str(ser.readline())
        dd=str(ser1.readline())
        #print(cc)
        ccc = cc.split("<")
        ddd = dd.split("<")
        #ccc = ccc[1].split(">")
        try:
            #print(ccc[1])
            ccc = ccc[1].split(">")
            ddd = ddd[1].split(">")
            #print(ccc)
            temphum = ccc[0].split(",")
            temphum1 = ddd[0].split(",")
            ts = time.time()
            st = datetime.datetime.fromtimestamp(ts).strftime('%Y_%m-%d_%H_%M_%S')
            if temphum !=[]:
                #print(temphum)
                Whichitone = temphum[0]
                Whichitone2 = temphum1[0]
                if Whichitone == "1":
                    DTemperature = float(temphum1[1]) - float(temphum[1])
                    DHumidity = float(temphum1[2]) - float(temphum[2])
                elif Whichitone == "2":
                    DTemperature = float(temphum[1]) - float(temphum1[1])
                    DHumidity = float(temphum[2]) - float(temphum1[2])
                #datatotrain.append([float(temphum[1]),float(temphum[2]),float(temphum1[1]),float(temphum1[2])])
                datatotrain.append([abs(DTemperature),abs(DHumidity)])
                jj = jj+1
                print(jj,threshold,abs(DTemperature),abs(DHumidity))
                #print(jj,float(temphum[1]),float(temphum[2]),float(temphum1[1]),float(temphum1[2]))
                if jj>=threshold:
                    CollectdataFlag2 = 0
                    TrainClasifierFlag = 1
                    break
        except:
            pass
    ser.close()
    ser1.close()

    while TrainClasifierFlag:
        print("Inside Trainer")
        centerpointinternal = []
        #kfold = int(len(datatotrain)/kfolding)
        centerpointrain = int(len(datatotrain)/kfolding)
        data = np.array(datatotrain)
        print(kfolding,centerpointrain)
        kpoint = []
        x,y = data.shape
        for k in range(0,x,kfolding):
            before = k
            after = k + kfolding
            #print(before,after)
            smallcenter = int((after-before)/2)
            newcentroid = k+smallcenter
            centerpointinternal.append(newcentroid)
        #folds = cross_validation_split(datatotrain, 10)
        #print(centerpointinternal)
        #print(len(folds))
        centerpoint = int(len(datatotrain)/2)
        #print(centerpoint)
        similiarityp2p = []

        #data = data.reshape(1,-1)
        print(data.shape)
        x,y = data.shape
        ucl = []
        twiceucl = []
        for j in range(len(centerpointinternal)):
            for i in range(x):
                datacenter = data[centerpointinternal[j]]
                datacenter = datacenter.reshape(1,-1)
                datacompared = data[i]
                datacompared = datacompared.reshape(1,-1)
                similiairyofp2pdata = cosine_similarity(datacenter,datacompared)
                #print(similiairyofp2pdata[0][0])
                similiarityp2p.append(similiairyofp2pdata[0][0])
            #splitter = 10
            reshapetocomply = int(len(similiarityp2p)/splitter)
            similiarityprocess = np.array(similiarityp2p)
            similiarityprocess = similiarityprocess.reshape([reshapetocomply,splitter])
            #print(similiarityprocess.shape)
            xx,yy = similiarityprocess.shape
            centerfornewxx = int(xx/2)
            entrophyrepo = []
            for i in range(xx):
                datacenter = similiarityprocess[centerfornewxx]
                datacompared = similiarityprocess[i]
                entrophycompared = entropy(datacenter, qk=datacompared)
                #print(entrophycompared)
                entrophyrepo.append(entrophycompared)
            #print(entrophyrepo)
            entrophyrepoprocess = np.array(entrophyrepo)
            meanforentrophy = np.mean(entrophyrepoprocess)
            std = np.std(entrophyrepoprocess)
            lcl = meanforentrophy + std
            lcl2std =  meanforentrophy + (2*std)
            print(meanforentrophy,std,lcl,lcl2std)
            ucl.append(lcl)
            twiceucl.append(lcl2std)
            TrainClasifierFlag = 0
            TestFlag = 1
            Flag = 1
            NoiseCounter = 0
            AnomoliesThreshold = 20
            Anomoliesrepo = []
            Anomoliesrepo2std = []
            AnamoliesFlags = 1

    while TestFlag:
        threshold = 100
        howmanytimes = 10
        majorityvoting = []
        majorityvoting2std = []
        for ccd in range (int(threshold/howmanytimes)):
            print("Inferences Modes running for %i out of %i" %(ccd+1,int(threshold/howmanytimes)))
            ser = serial.Serial("COM6",9600)
            ser1 = serial.Serial("COM7",9600)
            datatotest = []
            CollectdataFlag2 = 1
            jj = 0
            while CollectdataFlag2:
                cc=str(ser.readline())
                dd=str(ser1.readline())
                #print(cc)
                ccc = cc.split("<")
                ddd = dd.split("<")
                #ccc = ccc[1].split(">")
                try:
                    #print(ccc[1])
                    ccc = ccc[1].split(">")
                    ddd = ddd[1].split(">")
                    #print(ccc)
                    temphum = ccc[0].split(",")
                    temphum1 = ddd[0].split(",")
                    if temphum !=[]:
                        #print(temphum)
                        Whichitone = temphum[0]
                        Whichitone2 = temphum1[0]
                        if Whichitone == "1":
                            DTemperature = float(temphum1[1]) - float(temphum[1])
                            DHumidity = float(temphum1[2]) - float(temphum[2])
                        elif Whichitone == "2":
                            DTemperature = float(temphum[1]) - float(temphum1[1])
                            DHumidity = float(temphum[2]) - float(temphum1[2])
                        #datatotrain.append([float(temphum[1]),float(temphum[2]),float(temphum1[1]),float(temphum1[2])])
                        datatotest.append([abs(DTemperature),abs(DHumidity)])
                        jj = jj+1
                        #print(jj,float(temphum[0]),float(temphum[1]),float(temphum1[0]),float(temphum1[1]))
                        if jj>=threshold:
                            CollectdataFlag2 = 0
                            TrainClasifierFlag = 1
                            ser.close()
                            ser1.close()
                            break
                except:
                    pass


            datatest = np.array(datatotest)
            #print(datatest.shape)
            a,b = datatest.shape
            similiarityp2ptest = []
            ResultsTest = []
            ResultsTest2 = []
            for j in range(len(centerpointinternal)):
                for i in range(a):
                    datacenter = data[centerpointinternal[j]]
                    datacenter = datacenter.reshape(1,-1)
                    datacompared = datatest[i]
                    datacompared = datacompared.reshape(1,-1)
                    similiairyofp2pdata = cosine_similarity(datacenter,datacompared)
                    #print(similiairyofp2pdata[0][0])
                    similiarityp2ptest.append(similiairyofp2pdata[0][0])
                reshapetocomplytest = int(len(similiarityp2ptest)/splitter)
                similiarityprocesstest = np.array(similiarityp2ptest)
                similiarityprocesstest = similiarityprocesstest.reshape([reshapetocomplytest,splitter])
                #print(similiarityprocesstest.shape)
                #centerfornewxx = int(xx/2)
                aa,bb = similiarityprocesstest.shape
                entrophyrepotest = []
                #print(similiarityprocesstest)
                for i in range(aa):
                    datacenter = similiarityprocess[centerfornewxx]
                    datacompared = similiarityprocesstest[i]
                    entrophycompared = entropy(datacenter, qk=datacompared)
                    #print(entrophycompared)
                    entrophyrepotest.append(entrophycompared)

                #print(entrophyrepotest)
                #lcl,lcl2std
                lcl = ucl[j]
                lcl2std = twiceucl[j]
                #print(lcl,lcl2std)
                #print(meanforentrophy,std,lcl,lcl2std)
                for i in (entrophyrepotest):
                    if i <= lcl:
                        ResultsTest.append(1)
                    if i > lcl:
                        ResultsTest.append(-1)
                    if i <= lcl2std:
                        ResultsTest2.append(1)
                    if i > lcl2std:
                        ResultsTest2.append(-1)
                #print(ResultsTest)
                #print(ResultsTest2)
            c = Counter(ResultsTest)
            d = Counter(ResultsTest2)
            value, count = c.most_common()[0]
            print(c,d)
            #value2td,count2std = d.most_common()[0]
            try:
                valuemin, countmin = c.most_common()[0]
            except:
                valuemin, countmin = 0,0
            #value2, count2 = d.most_common()[0]

            value2, count2 = d.most_common()[0]
            try:
                valuemin2std, countmin2std = d.most_common()[0]
            except:
                valuemin2std, countmin2std = 0,0
            majorityvoting.append(valuemin)
            majorityvoting2std.append(valuemin2std)
        maj = Counter(majorityvoting)
        maj2std = Counter(majorityvoting2std)
        majprocess = maj.most_common()[0]
        maj2stdprocess =  maj2std.most_common()[0]
        print(majprocess,maj2stdprocess)
        if majprocess[0] == 1:
            print("HUMIDITY NOT DETECT")
        else:
            print("ANAMOLIES OF HUMIDITY DETECT")






