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
import RPi.GPIO as gpio
import pandas as pd
clasifier = "Cosine"
from random import seed
from random import randrange

gpio.setmode(gpio.BCM)
gpio.setup(13,gpio.OUT)#Status 1 RED LED
gpio.setup(19,gpio.OUT)#Status 2 GREED LED
gpio.setup(5,gpio.IN)#SW 1
gpio.setup(6,gpio.IN)#SW 2
gpio.output(13,0)
gpio.output(19,0)
#gpio.output(13,1)
#i = gpio.input(5)
# Import the ADS1x15 module.
import Adafruit_ADS1x15


# Create an ADS1115 ADC (16-bit) instance.
adc = Adafruit_ADS1x15.ADS1115()

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
GAIN = 1
if gpio.input(5) == 1:
    print("Run")
else:
    print("Stop")
if gpio.input(6) == 1:
    print("Should Collect New Data")
else:
    print("Load Old Data") 
print('Reading ADS1x15 values, press Ctrl-C to quit...')
# Print nice channel column headers.
print('| {0:>6} | {1:>6} | {2:>6} | {3:>6} |'.format(*range(4)))
print('-' * 37)
# Main loop.
datatotrain = []
iteration = 1000
j=0
Flag = 1
collectdataformodelcreation = 1
splitter = 10
#Flags
MainFlag = 1
CollectdataFlag = 1
TrainClasifierFlag = 0
TestFlag = 0
CollectdataFlag2 = 0
kfolding = 100
# Split a dataset into k folds

def cross_validation_split(dataset, folds=3):
	dataset_split = list()
	dataset_copy = list(dataset)
	fold_size = int(len(dataset) / folds)
	for i in range(folds):
		fold = list()
		while len(fold) < fold_size:
			index = randrange(len(dataset_copy))
			fold.append(dataset_copy.pop(index))
		dataset_split.append(fold)
	return dataset_split
 

while True:
    #print("Mainloop")
    while CollectdataFlag:
        print("Collection")
        time.sleep(1)
        # Read all the ADC channel values in a list.
        while MainFlag:
            time.sleep(1)
            if gpio.input(5) == 1:
                if Flag ==1:
                    print("Start or Stop..")   
                    Flag = 0
                    MainFlag = 0
                    j = 0
                    CollectdataFlag2 = 1
                    gpio.output(13,0)
                    gpio.output(19,0)
        while CollectdataFlag2:
            
            if gpio.input(6) == 1:
                values = [0]*4
                gpio.output(13,1)
                gpio.output(19,1)
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
                gpio.output(13,0)
                gpio.output(19,0)
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
        
        
             
    Testval = 10
    Kfolds = 0
    Accuracymodel = []
    while TestFlag:
        # Read all the ADC channel values in a list.
        if Flag ==1:
            print("Performing Inferences %i" %Kfolds)
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
            if Kfolds == Testval:
                Acc = np.array(Accuracymodel)
                mean = np.mean(Acc)
                
                print("Test Accuracy of the data collected is at %f" %mean)
                TestFlag = 0
                #CollectdataFlag = 1
                #MainFlag = 1
                #Flag = 1
                time.sleep(0.1)
                gpio.output(19,0)
                
                #iterationtest = i
            # if gpio.input(5)==0:
                # print("Break")
                # TestFlag = 0
                # CollectdataFlag = 1
                # MainFlag = 1
                # Flag = 1
                # time.sleep(0.1)
                # gpio.output(19,0)
                # iterationtest = i
                
            print('Test Iteration status %i,%f,%f,%f,%f' %(j,values[0],values[1],values[2],values[3]))
            time.sleep(0.1)
        #print('| {0:>6} | {1:>6} | {2:>6} | {3:>6} |'.format(*values))
        # Pause for half a second.
        
        datatest = np.array(datatotest)
        #print(datatest.shape)
        a,b = datatest.shape 
        similiarityp2ptest = []
        ResultsTest = []
        ResultsTest2 = []
        entrophyrepotesttotal = []
        for j in range(len(centerpointinternal)):
            print("Doing for internal point %f" %centerpointinternal[j]) 
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
                entrophyrepotesttotal.append(entrophycompared)

            #print(entrophyrepotest)
            #lcl,lcl2std
            #lcl = ucl[j]
            lcl = twiceucl[j]
            print(lcl)
            #print(meanforentrophy,std,lcl,lcl2std)
            for i in (entrophyrepotest):
                if i < lcl:
                    ResultsTest.append(1)
                # if i >= lcl:
                    # ResultsTest.append(-1)
                # if i < lcl2std:
                    # ResultsTest2.append(1)
                # if i >= lcl2std:
                    # ResultsTest2.append(-1)
                    
            #print(ResultsTest)
        Totalpass = len(ResultsTest)
        Totaltest = len(entrophyrepotesttotal)
        Accuracysmall = float((Totalpass/Totaltest)*100)
        Accuracymodel.append(Accuracysmall)
        print(Totalpass,Totaltest,Accuracysmall)
            # print(ResultsTest)
            # print(ResultsTest2)
            # c = Counter(ResultsTest)
            # d = Counter(ResultsTest2)
            # value, count = c.most_common()[0]     
            # value2, count2 = d.most_common()[0]    
            # if value == 1:
                # print("Not Detect Humidity at 1 std")
                # gpio.output(19,1)
                # gpio.output(13,0)
            # if value == -1:
                # print("Detect Humidity at 1 std")
                # gpio.output(13,1)
                # gpio.output(19,0)
            # if value2 == 1:
                # print("Not Detect Humidity at 2 Std")
                # gpio.output(19,1)
                # gpio.output(13,0)
            # if value2 == -1:
                # print("Detect Humidity at 2 Std")   
                # gpio.output(13,1) 
                # gpio.output(19,0)    
        Flag = 1
        Kfolds=Kfolds+1
    print(Accuracymodel)        
        #print(clf.predict(data))
    
