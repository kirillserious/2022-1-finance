#!/usr/bin/python3
from progress.bar import ChargingBar
import matplotlib.pyplot as plt
import numpy as np
import os

from model import get_price
from utils import parula_map

data_file_name = 'depends_on_strike.npy'
grid = np.linspace(80, 120, 40)

def get_data():
    prices = np.zeros((grid.size))
    bar = ChargingBar('Processing',
        max=grid.size,
        suffix='%(percent)d%% - eta %(eta_td)ss - elapced %(elapsed_td)ss')

    for i in range(grid.size):
        price = get_price([100,100], grid[i], [[0.97, 1.03], [0.99, 1.01]], 5)
        prices[i] = price
        bar.next()

    return prices

def draw(prices):
    plt.plot(grid, prices)
    plt.xlabel("$\chi$")
    plt.ylabel("$v_0^*$")
    plt.grid(True)
    
    plt.show()

if os.path.exists(data_file_name):
    prices = np.load(data_file_name)
else:
    prices = get_data()
    np.save(file=data_file_name, arr=prices)

draw(prices)
