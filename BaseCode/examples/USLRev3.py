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
##import RPi.GPIO as gpio
import pandas as pd
import logging
logging.basicConfig(format='%(asctime)s - %(message)s',level=logging.INFO,filename='Triggered.log')
logging.info("Recorded info")
clasifier = "Cosine"

##gpio.setmode(gpio.BCM)
##gpio.setup(13,gpio.OUT)#Status 1 RED LED
##gpio.setup(19,gpio.OUT)#Status 2 GREED LED
##gpio.setup(5,gpio.IN)#SW 1
##gpio.setup(6,gpio.IN)#SW 2
##gpio.output(13,0)
##gpio.output(19,0)
###gpio.output(13,1)
###i = gpio.input(5)
### Import the ADS1x15 module.
##import Adafruit_ADS1x15


# Create an ADS1115 ADC (16-bit) instance.
##adc = Adafruit_ADS1x15.ADS1115()

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
##GAIN = 1
##if gpio.input(5) == 1:
##    print("Run")
##else:
##    print("Stop")
##if gpio.input(6) == 1:
##    print("Should Collect New Data")
##else:
##    print("Load Old Data")
##print('Reading ADS1x15 values, press Ctrl-C to quit...')
# Print nice channel column headers.
print('| {0:>6} | {1:>6} | {2:>6} | {3:>6} |'.format(*range(4)))
print('-' * 37)
# Main loop.
datatotrain = []
iteration = 500
j=0
Flag = 1
collectdataformodelcreation = 1
splitter = 100
#Flags
MainFlag = 1
CollectdataFlag = 1
TrainClasifierFlag = 0
TestFlag = 0
CollectdataFlag2 = 0
kfolding = 10


while True:
    print("Mainloop")
    while CollectdataFlag:
        print("Collection")
        time.sleep(1)
        # Read all the ADC channel values in a list.
        while MainFlag:
            time.sleep(1)
            checit = 1
            if checit == 1:
                if Flag ==1:
                    print("Start or Stop..")
                    Flag = 0
                    MainFlag = 0
                    j = 0
                    CollectdataFlag2 = 1
                    #gpio.output(13,0)
                    #gpio.output(19,0)
        while CollectdataFlag2:
            runit = 1
            if runit == 1:
                values = [0]*4
                #gpio.output(13,1)
                #gpio.output(19,1)
                for i in range(4):

                    # Read the specified ADC channel using the previously set gain value.
                    val = adc.read_adc(i, gain=GAIN)
                    val2 = float(5.0*(val/65536))
                    #print(val2)
                    values[i] = val2
                    # Note you can also pass in an optional data_rate parameter that controls
                    # the ADC conversion time (in samples/second). Each chip has a different
                    # set of allowed data rate values, see datasheet Table 9 config register
                    # DR bit values.
                    #values[i] = adc.read_adc(i, gain=GAIN, data_rate=128)
                    # Each value will be a 12 or 16 bit signed integer value depending on the
                    # ADC (ADS1015 = 12-bit, ADS1115 = 16-bit).
                # Print the ADC values.
                #print(values)
                datatotrain.append(values)

                j=j+1
                if j == iteration:
                    print("Here")
                    CollectdataFlag2 = 0
                    if collectdataformodelcreation == 1:
                        print("SAVED FILE...")
                        data1 = []
                        data2 = []
                        data3 = []
                        data4 = []
                        #print(len(datatotrain))
                        #print(datatotrain[0][0])
                        for j in range(len(datatotrain)):
                            data1.append(datatotrain[j][0])
                            data2.append(datatotrain[j][1])
                            data3.append(datatotrain[j][2])
                            data4.append(datatotrain[j][3])
                        #data = np.array(datatotrain)
                        df = pd.DataFrame({'A0':data1,'A1':data2,'A2':data3,'A3':data4})
                        writer = pd.ExcelWriter('MetaData.xlsx',engine='xlsxwriter')
                        df.to_excel(writer,sheet_name='Sheet1')
                        writer.save()
                    CollectdataFlag = 0
                    data = np.array(datatotrain)

                print('Iteration status %i,%f,%f,%f,%f' %(j,values[0],values[1],values[2],values[3]))
                #print('| {0:>6} | {1:>6} | {2:>6} | {3:>6} |'.format(*values))
                # Pause for half a second.
                #gpio.output(13,0)
                #gpio.output(19,0)
                time.sleep(0.1)
                TrainClasifierFlag = 1


            else:
                gpio.output(13,1)
                gpio.output(19,1)
                time.sleep(1)
                print("This is load previous data loop..")
                df = pd.read_excel('MetaData.xlsx')
                print(df.columns)
                A0 = df['A0']
                A1 = df['A1']
                A2 = df['A2']
                A3 = df['A3']

                A0P = A0.tolist()
                A1P = A1.tolist()
                A2P = A2.tolist()
                A3P = A3.tolist()

                datatotrain = []
                for i in range(len(A0P)):
                    datatotrain.append([A0P[i],A1P[i],A2P[i],A3P[i]])
                #print(datatotrain)

                clasifier = "Dothis"
                data = np.array(datatotrain)
                #Testloop = 1
                TrainClasifierFlag = 1
                CollectdataFlag2 =0
                CollectdataFlag = 0
                gpio.output(13,0)
                gpio.output(19,0)
                time.sleep(1)


    while TrainClasifierFlag:
        print("Inside Trainer")
        centerpointinternal = []
        #kfold = int(len(datatotrain)/kfolding)
        centerpointrain = int(len(datatotrain)/kfolding)
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

        # Read all the ADC channel values in a list.
        if Flag ==1:
            print("Performing Inferences")
            Flag = 0
            time.sleep(1)
            #gpio.output(13,0)
            #gpio.output(19,0)

        iterationtest = 100
        j=0
        datatotest = []
        for i in range(iterationtest):
            values = [0]*4
            for i in range(4):
                # Read the specified ADC channel using the previously set gain value.
                val = adc.read_adc(i, gain=GAIN)
                val2 = float(5.0*(val/65536))
                #print(val2)
                values[i] = val2
                # Note you can also pass in an optional data_rate parameter that controls
                # the ADC conversion time (in samples/second). Each chip has a different
                # set of allowed data rate values, see datasheet Table 9 config register
                # DR bit values.
                #values[i] = adc.read_adc(i, gain=GAIN, data_rate=128)
                # Each value will be a 12 or 16 bit signed integer value depending on the
                # ADC (ADS1015 = 12-bit, ADS1115 = 16-bit).
            # Print the ADC values.
            #print(values)
            datatotest.append(values)
            j=j+1
            #if j == iteration:
            #    break
            if gpio.input(5)==0:
                print("Break")
                TestFlag = 0
                CollectdataFlag = 1
                MainFlag = 1
                Flag = 1
                time.sleep(0.1)
                gpio.output(19,0)
                iterationtest = i

            #print('Iteration status %i,%f,%f,%f,%f' %(j,values[0],values[1],values[2],values[3]))
            time.sleep(0.1)
        #print('| {0:>6} | {1:>6} | {2:>6} | {3:>6} |'.format(*values))
        # Pause for half a second.

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
        #value2td,count2std = d.most_common()[0]
        try:
            valuemin, countmin = c.most_common()[1]
        except:
            valuemin, countmin = 0,0
        #value2, count2 = d.most_common()[0]

        value2, count2 = d.most_common()[0]
        try:
            valuemin2std, countmin2std = d.most_common()[1]
        except:
            valuemin2std, countmin2std = 0,0
        print(c,d)
        print(value,count)
        print(valuemin,countmin)
        if NoiseCounter<=AnomoliesThreshold:
            if valuemin == -1:
                NoiseCounter=NoiseCounter+1
                print("Collecting Anamolies data %i out of %i"%(NoiseCounter,AnomoliesThreshold))
                Anomoliesrepo.append(countmin)
                Anomoliesrepo2std.append(countmin2std)
                logging.info("Collecting Spec Anomolies for 1st STD:%i , 2nd STD:%i"%(countmin,countmin2std))
        if AnamoliesFlags  == 1:
            if len(Anomoliesrepo) == AnomoliesThreshold:
                print("Achieving the Anamolies Threshold...Calculating the Mean and Std...")
                logging.info("Achieving the Anamolies Threshold...Calculating the Mean and Std...")
                AnamoliesMean = np.mean(Anomoliesrepo)
                AnamoliesStd = np.std(Anomoliesrepo)
                UCLAnamolies = AnamoliesMean+AnamoliesStd
                TUCLAnamolies = AnamoliesMean+AnamoliesStd+AnamoliesStd

                AnamoliesMean2STD = np.mean(Anomoliesrepo2std)
                AnamoliesStd2STD = np.std(Anomoliesrepo2std)
                UCLAnamolies2STD = AnamoliesMean2STD+AnamoliesStd2STD
                TUCLAnamolies2STD = AnamoliesMean2STD+AnamoliesStd2STD+AnamoliesStd2STD
                print("Generated Anamolies Spec is at %f" %UCLAnamolies)
                #logging.info("Generated STD Anamolies Spec is at %f" %AnamoliesStd)
                logging.info("Spec for 1st MX at 1STD %f and 2nd STD %f" %(UCLAnamolies,TUCLAnamolies))
                logging.info("Spec for 2st MX at 1STD %f and 2nd STD %f" %(UCLAnamolies2STD,TUCLAnamolies2STD))
                AnamoliesFlags = 0


        #rs = np.array(ResultsTest)
        #rs2 = np.array(ResultsTest2)
        #rsmax = rs.max()
        #rsmax2 = rs2.max()
        # if value == 1:
            # print("Not Detect Humidity at 1 std")
            # gpio.output(19,1)
            # gpio.output(13,0)
        # if value == -1:
            # print("Detect Humidity at 1 std")
            # gpio.output(13,1)
            # gpio.output(19,0)
        if AnamoliesFlags == 1:
            if value2 == 1 and value == 1:
                print("*****XXDETECT HUMIDITY*****")
                gpio.output(19,1)
                gpio.output(13,0)
            if value2 == -1 and value == -1:
                print(">>>>DETECT SOLID HUMIDITY @ 1&2 STD")
                gpio.output(13,1)
                gpio.output(19,0)
            if value == -1 and value2 == 1:
                print(">>>>MINOR SOLID HUMIDITY @ 1&2 STD")
                gpio.output(13,1)
                gpio.output(19,0)
        if AnamoliesFlags == 0:
            print("INSIDE NEW SPEC...1st MX level is %f, 2nd level is %f" %(UCLAnamolies,TUCLAnamolies))
            print("INSIDE NEW SPEC...2nd MX level is %f, 2nd level is %f" %(UCLAnamolies2STD,TUCLAnamolies2STD))
            if value == -1:
                print(">>>>DETECT 1ST LEVEL SOLID HUMIDITY @ 1&2 STD")
                gpio.output(13,1)
                gpio.output(19,0)
                logging.info(">>>>DETECT 1ST LEVEL SOLID HUMIDITY @ 1&2 STD -> %i Neg spec is %f" %(count,TUCLAnamolies))
            if value2 == -1:
                print(">>>>DETECT 2ND LEVEL SOLID HUMIDITY @ 1&2 STD")
                gpio.output(13,1)
                gpio.output(19,0)
                logging.info(">>>>DETECT 2ND LEVEL SOLID HUMIDITY @ 1&2 STD -> %i Neg spec is %f" %(count,TUCLAnamolies))
            if countmin >= TUCLAnamolies:
                print(">>>>1ST MX 2ND LEVEL MINOR SOLID HUMIDITY @ 2 STD")
                gpio.output(13,1)
                gpio.output(19,1)
                logging.info(">>>>>>>>1ST MX 2ND LEVEL MINOR SOLID HUMIDITY @ 2 STD -> %i spec is %f" %(countmin,TUCLAnamolies))
            if countmin >= UCLAnamolies:
                print(">>>>1ST MX 1ST LEVEL MINOR SOLID HUMIDITY @ 1 STD")
                gpio.output(13,1)
                gpio.output(19,1)
                logging.info(">>>>>>>>1ST MX 1ST LEVEL MINOR SOLID HUMIDITY @ 2 STD -> %i spec is %f" %(countmin,UCLAnamolies))
            if value == 1 and countmin < UCLAnamolies:
                print(">>>>1ST MX NO HUMIDITY @ 1 STD")
                logging.info(">>>>>1ST MX - NO HUMIDITY @ 1 STD: %i , %i " %(count,countmin))
                gpio.output(13,0)
                gpio.output(19,1)
            if value == 1 and countmin2std < UCLAnamolies2STD:
                print(">>>>2ND MX NO HUMIDITY @ 2 STD")
                logging.info(">>>>>2ND MX NO HUMIDITY @ 1 STD: %i , %i " %(count2,countmin2std))
                gpio.output(13,0)
                gpio.output(19,1)
            if value == 1 and countmin < TUCLAnamolies:
                print(">>>>1ST MX NO HUMIDITY @ 2 STD")
                logging.info(">>>>>1ST MX - NO HUMIDITY @ 2 STD: %i , %i " %(count,countmin))
                gpio.output(13,0)
                gpio.output(19,1)
            if value == 1 and countmin2std < TUCLAnamolies2STD:
                print(">>>>2ND MX NO HUMIDITY @ 2 STD")
                logging.info(">>>>>2ND MX NO HUMIDITY @ 2 STD: %i , %i " %(count2,countmin2std))
                gpio.output(13,0)
                gpio.output(19,1)

        #if rsmax2 == 1 and rsmax == 1:
        #    print("****Not detect Humidity at 1 & 2 Std*****")
        #    gpio.output(19,1)
        #    gpio.output(13,0)
        #if rsmax2 == -1 and rsmax == -1:
        #    print("****Detect Humidity at 1 & 2 Std*****")
        #    gpio.output(19,1)
        #    gpio.output(13,0)
        Flag = 1
        #print(value,value2)

        #print(clf.predict(data))

