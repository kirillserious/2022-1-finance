from progress.bar import ChargingBar
import matplotlib.pyplot as plt
import numpy as np
from model import get_price
from robustfpm.pricing import *
from utils import parula_map

class SemiplaneHandler(ISetHandler):
    def __init__(self, restricted_direction):
        self.direction = restricted_direction
        pass

    def project(self, lattice):
        raise Exception('No mapping for unbounded set')

    def support_function(self, x):
        x = np.atleast_2d(x)
        if x[0] == 0 and self.direction == 1:
            return 0
        if x[1] == 0 and self.direction == 0:
            return 0
        return np.Inf

    def iscompact(self):
        return False
    def multiply(self, x):
        raise NotImplementedError('Multiplication is not implemented.')

    def add(self, x):
        raise NotImplementedError('Addition is not implemented.')

    @property
    def dim(self):
        return np.inf

    def contains(self, x, is_interior=False):
        x = np.atleast_2d(x)
        if self.direction == 0:
            return x[0] > 0.0 if is_interior else x[0] >=0.0
        if self.direction == 1:
            return x[1] > 0.0 if is_interior else x[1] >= 0.0
        return False

def get_data(constraint):
    prices = np.zeros((grid.size, grid.size))
    bar = ChargingBar('Processing',
        max=grid.size**2,
        suffix='%(percent)d%% - eta %(eta_td)ss - elapced %(elapsed_td)ss')

    for i in range(grid.size):
        for j in range(grid.size):
            price = get_price([mesh[0][i][j], mesh[1][i][j]], 100, rectangle, 5)
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
    ax.set_xlabel("$x_0^1$")
    ax.set_ylabel("$x_0^2$")
    ax.set_title("$v_0^∗$")
    fig.colorbar(im, shrink=1)
    plt.show()

grid = np.linspace(90, 110, 5)
mesh = np.meshgrid(grid, grid)
rectangle = [[0.97, 1.03], [0.99, 1.01]]
LongOnlyMoreVolatileConstraints = IdenticalMap(SemiplaneHandler(0))
LongOnlyLessVolatileConstraints = IdenticalMap(SemiplaneHandler(1))

price = get_data(LongOnlyLessVolatileConstraints)
draw(price)

