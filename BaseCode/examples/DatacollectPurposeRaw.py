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
import time
import datetime
clasifier = "Cosine"

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
iteration = 10000
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
kfolding = 20


while True:
    while CollectdataFlag:
        print("Collection")
        time.sleep(1)
        # Read all the ADC channel values in a list.
        while MainFlag:
            print("Hereee")
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
                values = [0]*5
                gpio.output(13,1)
                gpio.output(19,1)
                for i in range(4):
                    
                    # Read the specified ADC channel using the previously set gain value.
                    ts = time.time()
                    st = datetime.datetime.fromtimestamp(ts).strftime('%Y_%m-%d_%H_%M_%S')
                    val = adc.read_adc(i, gain=GAIN)
                    val2 = float(5.0*(val/65536))
                    #print(val2)
                    #z = 5
                    #m = 0.00636
                    #b = 0.1515
                    #v = b/m
                    #k = (1/(z*m))*val2
                    #val2 = v+k
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
                values[i+1] = st
                datatotrain.append(values)
                #print(values)


                j=j+1
                forth_of_data = int(iteration/4)
                if j >= forth_of_data:
                    print("COOOOOOOOLLEEECTT NOW...")
                if gpio.input(5) == 0 or j == iteration:
                    print("Here")
                    CollectdataFlag2 = 0
                    if collectdataformodelcreation == 1:
                        print("SAVED FILE...")
                        data1 = []
                        data2 = []
                        data3 = []
                        data4 = []
                        data5 = []
                        #print(len(datatotrain))
                        #print(datatotrain[0][0])
                        for j in range(len(datatotrain)):
                            data1.append(datatotrain[j][0])
                            data2.append(datatotrain[j][1])
                            data3.append(datatotrain[j][2])
                            data4.append(datatotrain[j][3])
                            data5.append(datatotrain[j][4])
                        #data = np.array(datatotrain)
                        df = pd.DataFrame({'Timestamp':data5,'A0':data1,'A1':data2,'A2':data3,'A3':data4})
                        writer = pd.ExcelWriter('MetaData.xlsx',engine='xlsxwriter')
                        df.to_excel(writer,sheet_name='Sheet1')
                        writer.save()
                    CollectdataFlag = 1
                    MainFlag = 1
                    Flag = 1
                    data = np.array(datatotrain)
                    datatotrain = []
                    
                    
                print('Iteration status %i,%f,%f,%f,%f' %(j,values[0],values[1],values[2],values[3]))
                #print('| {0:>6} | {1:>6} | {2:>6} | {3:>6} |'.format(*values))
                # Pause for half a second.
                gpio.output(13,0)
                gpio.output(19,0)
                time.sleep(0.1)
                TrainClasifierFlag = 1


            
  
