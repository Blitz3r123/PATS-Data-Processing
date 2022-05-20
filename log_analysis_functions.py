from pydoc import describe
from rich.jupyter import print
from rich.markdown import Markdown
from rich.console import Console

import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import plotly.graph_objects as go
import re
import datetime
from statistics import *

from matplotlib.pyplot import figure
from matplotlib.lines import Line2D

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

console = Console()

purples = ['#665191', '#76619e', '#8772ac', '#9782b9', '#a794c7', '#b8a5d5', '#c9b7e3', '#dac9f1', '#ebdcff']
blues = ['#003f5c', '#21526f', '#396582', '#507a96', '#668eaa', '#7ca4bf', '#93bad4', '#aad0e9', '#c2e7ff']
reds = ['#de425b', '#e4586a', '#ea6c79', '#ef7e88', '#f49097', '#f7a1a7', '#fbb3b7', '#fdc4c7', '#ffd5d7']
greens = ['#488f31', '#5b9a44', '#6ca556', '#7eb068', '#8fbc7b', '#9fc78d', '#b0d2a0', '#c1deb3', '#d2e9c6']
pinks = ['#d45087', '#da6393', '#e0749f', '#e685aa', '#ec95b6', '#f1a5c2', '#f6b5ce', '#fbc5d9', '#ffd5e5']
oranges = ['#ff7c43', '#ff8953', '#ff9562', '#ffa172', '#ffac82', '#ffb893', '#ffc3a3', '#ffceb5', '#ffd9c6']
yellows = ['#ffd200', '#ffd433', '#fed64d', '#fed762', '#fcd975', '#fbdb87', '#f8dd99', '#f5dfab', '#f2e1bc']

def get_files(dir_path):
    """
      Gets all the files from the folder stated - including files from subdirectories.
    
      Parameters:
        dir_path (string): Path of the folder from which to get the files from.
    
      Returns:
        all_files ( [strings] ): Paths of all files.
    """
    file_list = os.listdir(dir_path)
    all_files = list()
    # Iterate over all the entries
    for entry in file_list:
        # Create full path
        full_path = os.path.join(dir_path, entry)
        # If entry is a directory then get the list of files in this directory 
        if os.path.isdir(full_path):
            all_files = all_files + get_files(full_path)
        else:
            all_files.append(full_path)
                
    return all_files