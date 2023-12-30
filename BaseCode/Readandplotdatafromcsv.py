import random
from itertools import count
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

plt.style.use('fivethirtyeight')

def animate(i):
    data = pd.read_csv('data.csv')
    x = data['x_value']
    y1 = data['total_1']
    y2 = data['total_2']
    y3 = data['Differential']
    plt.cla()

    plt.plot(x,y1,label='Channel 1')
    plt.plot(x,y2,label='Channel 2')
    plt.plot(x,y3,label='Channel 3')
    plt.legend(loc='upper left')
    plt.tight_layout()

ani = FuncAnimation(plt.gcf(), animate,interval=500)
plt.tight_layout()
plt.show()
