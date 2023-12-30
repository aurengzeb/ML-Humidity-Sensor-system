import random
from itertools import count
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

plt.style.use('fivethirtyeight')
fig, axes = plt.subplots(3)
def animate(i):
    data = pd.read_csv('data.csv')
    x = data['x_value']
    y1 = data['Humidity_1']
    y2 = data['Humidity_2']
    y3 = data['HD']
    y4 = data['HT']
    y5 = data['Temperature_1']
    y6 = data['Temperature_2']
    y7 = data['Humidity_3']
    y8 = data['HD2']
    y9 = data['HT2']
    y10 = data['Temperature_3']



    axes[0].cla()
    axes[1].cla()
    axes[2].cla()
    #x2 = x
    axes[0].plot(x,y1,label='Humidity_Ref',linewidth=2)
    axes[0].plot(x,y2,label='Humidity_Inside',linewidth=2)
    axes[0].plot(x,y7,label='Humidity_Inside2',linewidth=2)

    axes[1].plot(x,y5,label='Temperature_Ref',linewidth=2)
    axes[1].plot(x,y6,label='Temperature_Inside',linewidth=2)
    axes[1].plot(x,y10,label='Temperature_Inside2',linewidth=2)

    axes[2].plot(x,y3,label='HD',linewidth=2)
    axes[2].plot(x,y8,label='HD2',linewidth=2)

    #plt.plot(x,y3,label='Channel 3')
    axes[0].legend(loc='upper left')
    axes[1].legend(loc='upper left')
    axes[2].legend(loc='upper left')
    plt.tight_layout()

ani = FuncAnimation(plt.gcf(), animate,interval=50)
plt.tight_layout()
plt.show()
