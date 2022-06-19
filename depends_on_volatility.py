#!/usr/bin/python3
from progress.bar import ChargingBar
import matplotlib.pyplot as plt
import numpy as np
import os

from model import get_price
from utils import parula_map

data_file_name = 'depends_on_volatility_1.npy'
grid = np.linspace(0, 0.1, 10)
mesh = np.meshgrid(grid, grid)

def get_data():
    prices = np.zeros((grid.size, grid.size))
    bar = ChargingBar('Processing',
        max=grid.size**2,
        suffix='%(percent)d%% - eta %(eta_td)ss - elapced %(elapsed_td)ss')

    for i in range(grid.size):
        for j in range(grid.size):
            price = get_price([90, 110], 100, [[1-grid[i], 1+grid[i]], [1-grid[j], 1+grid[j]]], 5)
            prices[i][j] = price
            bar.next()

    return prices

def draw(prices):
    fig = plt.figure()

    ax = fig.add_subplot(111)
    im = ax.imshow(prices, interpolation='bilinear', origin='lower',
               cmap=parula_map, extent=(grid[0], grid[-1], grid[0], grid[-1]))
    cs = ax.contour(grid, grid, prices, 6, colors='k')
    ax.clabel(cs, inline=True)
    ax.set_xlabel("$\Delta_1$")
    ax.set_ylabel("$\Delta_2$")
    ax.set_title("$v_0^∗$")
    fig.colorbar(im, shrink=1)
    plt.show()

if os.path.exists(data_file_name):
    prices = np.load(data_file_name)
else:
    prices = get_data()
    np.save(file=data_file_name, arr=prices)
draw(prices)