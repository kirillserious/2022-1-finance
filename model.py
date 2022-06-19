#!/usr/bin/python3

import os, sys
import numpy as np

ROBUSTFPM_REPO_ENV = 'ROBUSTFPM_REPO'

def import_robustfmp():
    robustfpm_repo = os.environ[ROBUSTFPM_REPO_ENV] \
        if ROBUSTFPM_REPO_ENV in os.environ else 'robust-fpm-cmc-msu-edu-2021'
    sys.path.insert(0, os.path.abspath(robustfpm_repo))

import_robustfmp()
from robustfpm.finance import make_option
from robustfpm.pricing import *

# get_price returns the optimal option price for considered task
def get_price(starting_price:list[float],
    strike:float,
    dynamics_rectangle:list[list[float]],
    time_horizon:int,
    trading_constraints=NoConstraints,
) -> (float, []):
    # TODO: Add starting_price and dinamics_rectangle dimentions check
    option = make_option(option_type='callonmax', strike=np.float32(strike))
    problem = Problem(starting_price=np.array(starting_price),
        price_dynamics=MDAFDynamics(support=RectangularHandler(np.array(dynamics_rectangle))),
        trading_constraints=NoConstraints,
        option=option,
        lattice=Lattice(delta=np.ones_like(starting_price)),
        time_horizon=time_horizon)
    # TODO: Add progress bar to wrap this ugly behaviour with integer iter_tick. 
    solver = ConvhullSolver(ignore_warnings=True, iter_tick=100)
    solution = solver.solve(problem)
    # Lol: The documentation is lying: you can’t derive strategies here in any way.
    # There are two parameters and both are not used in the sources.
    return solution['Vf'][0][0] #, solution['hedge']