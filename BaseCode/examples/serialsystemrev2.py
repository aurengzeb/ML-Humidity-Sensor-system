import time
import pandas as pd
import datetime
import serial
ser = serial.Serial("/dev/ttyACM0",9600)
ser1 = serial.Serial("/dev/ttyACM1",9600)
print(ser)
for i in range(3):
	jj = 0
	threshold = 100000
	TimeTemperatureHUmidity = []
	TimeTemperatureHUmidity2 = []
	while True:
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
				TimeTemperatureHUmidity.append([st,float(temphum[0]),float(temphum[1]),float(temphum1[0]),float(temphum1[1])])
				jj = jj+1
				print(jj,st,float(temphum[0]),float(temphum[1]),float(temphum1[0]),float(temphum1[1]))
				if jj>=threshold:
					break
			
		except:
			pass
	#df = pd.DataFrame({'Timestamp':data3,'A0':data2,'A1'})
	ts = time.time()
	st = datetime.datetime.fromtimestamp(ts).strftime('%Y_%m-%d_%H_%M_%S')
	df = pd.DataFrame(data = TimeTemperatureHUmidity, columns=["Time","Temperature", "Humidity","TemperatureOutside","HumidityOutside"])
	writer = pd.ExcelWriter(st+'_MetaData.xlsx',engine='xlsxwriter')
	df.to_excel(writer,sheet_name='Sheet1')
	writer.save()	
ser.close()		
#print(TimeTemperatureHUmidity)
	
