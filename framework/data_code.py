import pandas as pd
from IPython.display import display
use = pd.DataFrame(
    {'x0': [60, 46],
     'x1': [55, 15],
     'x2': [30, 64],
     'x3': [65, 10]},
    index=['K', 'L']
)
xdem = pd.DataFrame(
    {'HOU1': [60, 15, 40, 10],
     'HOU2': [26, 25, 40, 55],
     'GOVR': [20, 30, 14, 10]},
    index=['x0', 'x1', 'x2', 'x3']
)
enfac = pd.DataFrame(
    {'K': [55, 155],
     'L': [100, 35]},
    index=['HOU1', 'HOU2']
)
taxrev = pd.DataFrame(
    {'HOU1': [30],
     'HOU2': [44]},
    index=['GOVR']
)
trans = pd.DataFrame(
    {'HOU1': [(0), 0],
     'HOU2': [0, (0)]},
    index=['HOU1', 'HOU2']
)