from rich.jupyter import print
from rich.markdown import Markdown

import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import plotly.graph_objects as go
import re

from matplotlib.pyplot import figure

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

def get_files(dir_path):
    """
        Get all files (including files from subfolders) from a directory. Takes in directory and returns array of file paths.
        
        Parameters:
            dir_path (string): directory to grab files from.

        Returns:
            all_files (string array): array of all file paths.
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

def plot_stats(file, df, ax, color):
    """
        Plots min, max, std, and mean for a given dataframe.

        Parameters:
            file (string): file path to check for unicast/multicast.
            df (DataFrame): DataFrame of data to produce statistics from.
            ax (Axis): axis to plot the stats on.
            color (string): colour of backgrounds of the stats

        Returns:
            None
    """
    x_width = df.size

    min = "{:.0f}".format(df.min())
    max = "{:.0f}".format(df.max())
    std = "{:.0f}".format(df.std())
    mean = "{:.0f}".format(df.mean())
    
    if df.mean() > 0 and x_width > 0:
        if 'unicast' in file:
            ax.hlines(df.mean(), 0, x_width, colors=color, linestyles='dashed')
            ax.text(x_width * 0.6, df.mean(), "Mean: " + mean + "$\mu$s", color='white', backgroundcolor=color)
            ax.text(x_width * 0.2, df.min(), "Min: " + min + "$\mu$s", color='white', backgroundcolor=color)
            ax.text(x_width * 0.2, df.max(), "Max: " + max + "$\mu$s", color='white', backgroundcolor=color)
            ax.text(x_width, df.max(), "std: " + std, color='white', backgroundcolor=color)
        else:
            ax.hlines(df.mean(), 0, x_width, colors=color, linestyles='dashed')
            ax.text(x_width * 0.4, df.mean(), "Mean: " + mean + "$\mu$s", color='white', backgroundcolor=color)
            ax.text(0, df.min(), "Min: " + min + "$\mu$s", color='white', backgroundcolor=color)
            ax.text(0, df.max(), "Max: " + max + "$\mu$s", color='white', backgroundcolor=color)
            ax.text(x_width * 0.8, df.max(), "std: " + std, color='white', backgroundcolor=color)

def plot_table(titles, columns):
    """
        Plots a table.

        Parameters:
            titles ( [string] ): array of titles of the header row of the table.
            columns ( [ [], [], ... ] ): array of arrays of data to be plotted for each column in the table.

        Returns:
            None
    """
    row_even_colour = '#d0d8e0'
    row_odd_colour = 'white'

    figure = go.Figure(data=[go.Table(
        header = dict(
            values=titles,
            fill_color = '#007bff',
            font = dict(color='white', size=14)
        ),
        cells = dict(
            # values=[total_samples, avg_samples_per_sec, avg_throughput, lost_samples],
            values=columns,
            fill_color = [[row_odd_colour, row_even_colour] * 100]
        )
    )])

    figure.show()

def plot_mean(ax, df, colour):
    """
        Produces the mean from a DataFrame and plots it on an axis.

        Parameters:
            ax (Axis): Axi to plot the data on.
            df (DataFrame): DataFrame containing the data to produce the mean from.
            colour (string): Colour of the background of the text.

        Returns:
            None
    """
    mean = df.mean()
    formatted_mean = '{0:,.0f}'.format(mean)
    ax.hlines(mean, 0, df.size, colors=colour)
    ax.text(df.size / 2, mean, 'Mean: %s' %formatted_mean, color='white', backgroundcolor=colour)

def plot_data(ax, df, column, type, colour, label, size):
    """
        Plots the data from a DataFrame onto an Axis.

        Parameters:
            ax (Axis): Axis to plot the data on.
            df (DataFrame): Data to plot.
            column (string): Specific column from the DataFrame to plot.
            type (string): 'line' or 'scatter'. Decides if the plot will be a line graph or scatter plot.
            label (string): Label of the plot.
            size (int): Size of the dots produced on the scatter plot.
        
        Returns:
            None
    """
    if column is not None:
        df = df[column]
    
    if 'line' in type:
        ax.plot(df, c=colour, label=label)
    else:
        ax.scatter(df.index, df, c=colour, s=size, label=label)
    
    plot_mean(ax, df, colour)

def config_ax(ax, yscale, ylabel, xlabel, ylim, xlim, show_grid, show_legend):
    """
        Configure Axis options such as settings yscale to 'log', setting the y-label, x-label, ylim, xlim, etc.

        Parameters:
            ax (Axis): Axis to configure.
            yscale (Boolean): Set yscale to 'log'
            ylabel (string): y label value to set to.
            xlabel (string): x label value to set to.
            ylim (Boolean): Start y-axis from 0.
            xlim (Boolean): Start x-axis from 0.
            show_grid (Boolean): Show grid on the graph plot.
            show_legend (Boolean): Show legend on the graph plot.

        Returns:
            None
    """
    if yscale:
        ax.set_yscale('log')
    if ylabel:
        ax.set_ylabel(ylabel)
    if xlabel:
        ax.set_xlabel(xlabel)
    if ylim:
        ax.set_ylim(ymin=0)
    if xlim:
        ax.set_xlim(xmin=0)
    if show_grid:
        ax.grid()
    if show_legend:
        ax.legend()

def get_test_type(filepath):
    """
        Checks whether the file belongs to set 2 (normal) or set 4 (attack).

        Parameters:
            filepath (string): filepath to check.

        Returns:
            test_type (string): test type: 'Normal' or 'Attack.
    """
    if 'set_2' in filepath: 
        return 'Normal'
    else:
        return 'Attack'

def get_test_comm(filepath):
    """
        Checks whether the file path contains unicast or multicast.

        Parameters:
            filepath (string): filepath to check.

        Returns:
            test_comm (string): 'unicast' or 'multicast'
    """
    if 'unicast' in filepath: 
        return 'unicast'
    else:
        return 'multicast'

def get_participants(filepath):
    """
      Get number of participants per test.
    
      Parameters:
        filepath (string): filepath to check.
    
      Returns:
        participant_amount (string): number of participants in test. 
    """
    if 'unicast_1_' in filepath or 'multicast_1_' in filepath:
        if 'set_2' in filepath:
            return '10P + 10S'
        else:
            return '10P + 20S'
    elif 'unicast_2_' in filepath or 'multicast_2_' in filepath:
        if 'set_2' in filepath:
            return '25P + 25S'
        else:
            return '25P + 50S'
    else:
        if 'set_2' in filepath:
            return '50P + 50S'
        else:
            return '50P + 100S'

def get_stat(df, stat, formatted):
    """
      Get stat from DataFrame.
    
      Parameters:
        df (DataFrame): DataFrame to get mean from.
        stat (string): stat to produce from data. Can be 'mean', 'min', 'max' or 'std'
        formatted (Boolean): Option to format mean as string.
    
      Returns:
        mean (double): Value of the mean. 
    """

    if 'mean' in stat:
        val = df.mean()
    elif 'min' in stat:
        val = df.min()
    elif 'max' in stat:
        val = df.max()
    else:
        val = df.std()

    if formatted:
        return "{0:,.0f}".format(val)
    else:
        return val

def get_table_data(s2_lat_files, s4_lat_files):
    """
      Get data to populate the table.
    
      Parameters:
        s2_lat_files ( [string] ): Files from set 2.
        s4_lat_files ( [string] ): Files from set 4.
    
      Returns:
        (
            types ( [string] ): Test type. 'Attack' or 'Normal'.
            comm_types ( [string] ): Communication type. 'Unicast' or 'Multicast'.
            participants ( [string] ): Number of publishers and subscribers used in the test.
            means ( [string / int] ): Means produced from the test.
            mins ( [string / int] ): Mins produced from the test.
            maxes ( [string / int] ): Maxes produced from the test.
            stds ( [string / int] ): Standard deviations produced from the test.
        ) 
    """

    types = []
    comm_types = []
    participants = []
    means = []
    mins = []
    maxes = []
    stds = []

    for i in range(0, len(s2_lat_files)):
        s2_file = s2_lat_files[i]
        s4_file = s4_lat_files[i]

        types.append(get_test_type(s2_file))
        types.append(get_test_type(s4_file))

        comm_types.append(get_test_comm(s2_file))
        comm_types.append(get_test_comm(s4_file))

        participants.append(get_participants(s2_file))
        participants.append(get_participants(s4_file))

        means.append(get_stat(pd.read_csv(s2_file)['avg_non_mal_run_latency'], 'mean', True))
        means.append(get_stat(pd.read_csv(s4_file)['avg_non_mal_run_latency'], 'mean', True))

        mins.append(get_stat(pd.read_csv(s2_file)['avg_non_mal_run_latency'], 'min', True))
        mins.append(get_stat(pd.read_csv(s4_file)['avg_non_mal_run_latency'], 'min', True))

        maxes.append(get_stat(pd.read_csv(s2_file)['avg_non_mal_run_latency'], 'max', True))
        maxes.append(get_stat(pd.read_csv(s4_file)['avg_non_mal_run_latency'], 'max', True))

        stds.append(get_stat(pd.read_csv(s2_file)['avg_non_mal_run_latency'], 'std', True))
        stds.append(get_stat(pd.read_csv(s4_file)['avg_non_mal_run_latency'], 'std', True))

    return (types, comm_types, participants, means, mins, maxes, stds)