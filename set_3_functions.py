from rich.jupyter import print
from rich.markdown import Markdown

import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import plotly.graph_objects as go
import re

from matplotlib.pyplot import figure
from all_functions import *

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

def get_files(dir_path):
    """Get all files (including files from subfolders) from a directory. Takes in directory and returns array of file paths."""
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

def plot_attack(ax, files, title):
    for file in files:
        if 'unicast' in file:
            if '_1_' in file:
                color = '#a9b957'
                label = 'Unicast 10P + 10S'
            elif '_2_' in file:
                color = '#7ba441'
                label = 'Unicast 50P + 50S'
            else: 
                color = '#488f31'
                label = 'Unicast 100P + 100S'
        else:
            if '_1_' in file:
                color = '#f8975e'
                label = 'Multicast 10P + 10S'
            elif '_2_' in file:
                color = '#ee6e58'
                label = 'Multicast 50P + 50S'
            else: 
                color = '#de425b'
                label = 'Multicast 100P + 100S'

        df = pd.read_csv(file)
        ax.scatter(df["avg_run_latency"].index, df["avg_run_latency"], s=3, label=label, c=color)
        # ax.plot(df["avg_run_latency"], label=label, color=color)
        ax.set_yscale("log")
        ax.set_title(title)
        ax.set_xlim(xmin=0)
        ax.set_ylabel("Latency ($\mu$s)")
        ax.set_xlabel("Measurements over Time")
        plot_stats(file, df["avg_run_latency"], ax, color)
        ax.legend()
        ax.grid()

def s3_plot_table(titles, columns):
    row_even_colour = '#d0d8e0'
    row_odd_colour = 'white'

    figure = go.Figure(data=[go.Table(
        header = dict(
            values=titles,
            fill_color = 'grey',
            font = dict(color='white', size=14)
        ),
        cells = dict(
            # values=[total_samples, avg_samples_per_sec, avg_throughput, lost_samples],
            values=columns,
            fill_color = [[row_odd_colour, row_even_colour] * 5]
        )
    )])

    figure.show()

def plot_mean(ax, df, colour):
    mean = df.mean()
    formatted_mean = '{0:,.0f}'.format(mean)
    ax.hlines(mean, 0, df.size, colors=colour)
    ax.text(df.size / 2, mean, 'Mean: %s' %formatted_mean, color='white', backgroundcolor=colour)

def plot_data(ax, df, column, type, colour, label, size):
    if column is not None:
        df = df[column]
    
    if 'line' in type:
        ax.plot(df, c=colour, label=label)
    else:
        ax.scatter(df.index, df, c=colour, s=size, label=label)
    
    plot_mean(ax, df, colour)

def config_ax(ax, yscale, ylabel, xlabel, ylim, xlim, show_grid, show_legend):
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

def plot_ddos_attack(ax, set_files, u_length, m_length, u_colour, u_label, m_colour, m_label, use_mal):
    if use_mal:
        mal_type = 'avg_mal_run_latency'
    else:
        mal_type = 'avg_non_mal_run_latency'
    df_ucast = pd.read_csv(set_files[u_length])
    df_mcast = pd.read_csv(set_files[m_length])
    plot_data(ax, df_ucast, mal_type, 'line', u_colour, u_label, 50)
    plot_data(ax, df_mcast, mal_type, 'line', m_colour, m_label, 50)

def plot_ddos_subplot(set_2_files, set_3_files, u_index, m_index, u_colour, m_colour, u_label, m_label, data_title):
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(30, 10))
    fig.suptitle("Effects of %s DDOS Attack on DDS with 50 Participants" %data_title)
    axes[0].set_title("25P + 25S Unicast VS Multicast")
    plot_ddos_attack(axes[0], set_2_files, 'unicast', 'multicast', '#488f31', 'Unicast', '#de425b','Multicast', False)
    config_ax(axes[0], 'log', "Latency ($\mu$s)", "Measurements Over Time", None, True, True, False)
    axes[1].set_title("25P + 25S Unicast VS Multicast under DDOS")
    plot_ddos_attack(axes[1], set_3_files, u_index, m_index, u_colour, u_label, m_colour, m_label, False)
    config_ax(axes[1], 'log', "Latency ($\mu$s)", "Measurements Over Time", None, True, True, False)

def plot_s3_latency_cdfs_unicast():
    # Get Set 2 25P + 25S latencies (test with _2_ in name)
    s2_lats = [file for file in get_files('data/set_2') if 'forced_transport' in file and 'average_latencies' in file and '_2_' in file]
    s2_lats = {
        'ucast': [file for file in s2_lats if 'unicast' in file][0],
        'mcast': [file for file in s2_lats if 'multicast' in file][0]
    }

    # Get Set 3 25P + 25MP + 25S + 25MS latencies (tests with _2_ in it)
    s3_lats = [file for file in get_files('data/set_3') if 'average_latencies' in file and '_2_' in file and 'kilobytes' in file]
    s3_lats = {
        'ucast': [file for file in s3_lats if 'unicast' in file],
        'mcast': [file for file in s3_lats if 'multicast' in file]
    }

    fig, ax = plt.subplots(figsize=(30, 15))
    s2df = pd.read_csv(s2_lats['ucast'])
    s2df_combined = pd.concat([ s2df['run_1_latency'], s2df['run_2_latency'], s2df['run_3_latency'] ])
    plot_cdf('100B Unicast DDS Usage', s2df_combined, ax, greens[0], 'average')

    for file in s3_lats['ucast']:
        colours = [purples[0], blues[0], reds[0], greens[0], pinks[0], oranges[0], yellows[0]]
        i = s3_lats['ucast'].index(file)
        df = pd.read_csv(file)
        combined_df = pd.concat( [ df['run_1_latency'], df['run_2_latency'], df['run_3_latency'] ] )
        plot_cdf(get_test_names([file])[0].replace("50P + 50S ", ""), combined_df, ax, colours[i], 'normal')
        average = format_number(combined_df.mean())
        ax.text((i * 30000) + 50000, (combined_df.mean() / 70000) * 0.5, get_test_names([file])[0].replace("50P + 50S", "").replace("unicast ", "") + " Avg.: " + average + "us", color='white', backgroundcolor=colours[i], fontsize=15)

    ax.set_ylim(ymin=0, ymax=1)
    ax.set_xlim(xmin=0, xmax=250000)
    ax.grid()
    ax.set_xlabel("Latency ($\mu$s)")
    _ = ax.legend()
    _ = ax.get_figure().suptitle("Latency CDFs Per Data Length (Unicast)", fontsize=15, fontweight='bold')

    plt.tight_layout()

def plot_s3_latency_cdfs_multicast():
    # Get Set 2 25P + 25S latencies (test with _2_ in name)
    s2_lats = [file for file in get_files('data/set_2') if 'forced_transport' in file and 'average_latencies' in file and '_2_' in file]
    s2_lats = {
        'ucast': [file for file in s2_lats if 'unicast' in file][0],
        'mcast': [file for file in s2_lats if 'multicast' in file][0]
    }

    # Get Set 3 25P + 25MP + 25S + 25MS latencies (tests with _2_ in it)
    s3_lats = [file for file in get_files('data/set_3') if 'average_latencies' in file and '_2_' in file and 'kilobytes' in file]
    s3_lats = {
        'ucast': [file for file in s3_lats if 'unicast' in file],
        'mcast': [file for file in s3_lats if 'multicast' in file]
    }
    fig, ax = plt.subplots(figsize=(30, 15))
    s2df = pd.read_csv(s2_lats['mcast'])
    s2df_combined = pd.concat([ s2df['run_1_latency'], s2df['run_2_latency'], s2df['run_3_latency'] ])
    plot_cdf('100B Multicast DDS Usage', s2df_combined, ax, greens[0], 'average')

    for file in s3_lats['mcast']:
        colours = [purples[0], blues[0], reds[0], greens[0], pinks[0], oranges[0], yellows[0]]
        i = s3_lats['mcast'].index(file)
        df = pd.read_csv(file)
        combined_df = pd.concat( [ df['run_1_latency'], df['run_2_latency'], df['run_3_latency'] ] )
        plot_cdf(get_test_names([file])[0].replace("50P + 50S ", ""), combined_df, ax, colours[i], 'normal')
        average = format_number(combined_df.mean())
        ax.text((i * 30000) + 50000, (combined_df.mean() / 70000) * 0.5, get_test_names([file])[0].replace("50P + 50S", "").replace("multicast ", "") + " Avg.: " + average + "us", color='white', backgroundcolor=colours[i], fontsize=15)

    ax.set_ylim(ymin=0, ymax=1)
    ax.set_xlim(xmin=0, xmax=250000)
    ax.grid()
    ax.set_xlabel("Latency ($\mu$s)")
    _ = ax.legend()
    _ = ax.get_figure().suptitle("Latency CDFs Per Data Length (Multicast)", fontsize=15, fontweight='bold')

    plt.tight_layout()