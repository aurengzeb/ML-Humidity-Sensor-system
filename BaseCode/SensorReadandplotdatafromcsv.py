import random
from itertools import count
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

plt.style.use('fivethirtyeight')
fig, axes = plt.subplots(2)
def animate(i):
    data = pd.read_csv('data.csv')
    x = data['x_value']
    y1 = data['Humidity_1']
    y2 = data['Humidity_2']
    y3 = data['HD']
    y4 = data['HT']
    axes[0].cla()
    axes[1].cla()
    #x2 = x
    axes[0].plot(x,y1,label='Humidity_1',linewidth=2)
    axes[0].plot(x,y2,label='Humidity_2',linewidth=2)
    axes[1].plot(x,y3,label='HD',linewidth=2)

    #plt.plot(x,y3,label='Channel 3')
    axes[0].legend(loc='upper left')
    axes[1].legend(loc='upper left')
    plt.tight_layout()

ani = FuncAnimation(plt.gcf(), animate,interval=50)
plt.tight_layout()
plt.show()
