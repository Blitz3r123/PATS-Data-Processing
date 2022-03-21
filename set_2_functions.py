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

def get_test_name(file):
    run = os.path.dirname(file)
    run = os.path.basename(run).replace('_', ' ').title()

    folder_name = os.path.dirname(file)
    folder_name = os.path.dirname(folder_name)
    folder_name = os.path.basename(folder_name).replace('_', ' ').title()
    test_name = folder_name.replace(" Forced Transport", "").replace("Participant Measure ", "")
    test_name = re.sub('2 . ', '', test_name)
    return os.path.basename(test_name + " " + run)

def get_stat_from_file(stat, file):
    df = pd.read_csv(file)["Latency"]
    if 'measurement_amount' in stat:
        return df.size
    elif 'mean' in stat:
        return "{:0.0f}".format(df.mean())
    elif 'std' in stat:
        return "{:0.0f}".format(df.std())
    elif 'min' in stat:
        return df.min()
    elif 'max' in stat:
        return df.max()
    elif 'lower_quartile' in stat:
        return df.quantile(0.25)
    elif 'middle_quartile' in stat:
        return df.quantile(0.5)
    elif 'upper_quartile' in stat:
        return df.quantile(0.75)

def get_run_number(file):
    folder_name = os.path.dirname(file)
    run_number = os.path.basename(folder_name)[-1]
    return run_number

def plot_latency_summary_table(latency_files):
    figure, axes = plt.subplots()
    axes.axis('off')
    axes.axis('tight')

    test_names = []
    measurement_amounts = []
    means = []
    stds = []
    mins = []
    maxes = []
    lower_quartiles = []
    middle_quartiles = []
    upper_quartiles = []

    for file in latency_files:
        test_name, test_number = get_test_name(file)
        test_names.append(test_name + " Run " + str(get_run_number(file)))

        measurement_amount = get_stat_from_file('measurement_amount', file)
        measurement_amounts.append(measurement_amount)
        
        mean = get_stat_from_file('mean', file)
        means.append(mean)

        std = get_stat_from_file('std', file)
        stds.append(std)

        min = get_stat_from_file('min', file)
        mins.append(min)

        max = get_stat_from_file('max', file)
        maxes.append(max)

        lower_quartile = get_stat_from_file('lower_quartile', file)
        lower_quartiles.append(lower_quartile)

        middle_quartile = get_stat_from_file('middle_quartile', file)
        middle_quartiles.append(middle_quartile)

        upper_quartile = get_stat_from_file('upper_quartile', file)
        upper_quartiles.append(upper_quartile)

    row_even_colour = 'lightgrey'
    row_odd_colour = 'white'

    figure = go.Figure(data=[go.Table(
        header = dict(
            values=['Test', 'No. of Measurements', 'Mean Latency (us)', 'Standard Deviation', "Min", "Max", "25%", "50%", "75%"],
            fill_color = 'grey',
            font = dict(color='white', size=14)
        ),
        cells = dict(
            values=[test_names, measurement_amounts, means, stds, mins, maxes, lower_quartiles, middle_quartiles, upper_quartiles],
            fill_color = [[row_odd_colour, row_odd_colour, row_odd_colour, row_even_colour, row_even_colour, row_even_colour] * 5]
        )
    )])

    figure.show()

def get_test_name(file):
    test_number = os.path.dirname(os.path.dirname(file))
    test_number = os.path.basename(test_number).replace("_forced_transport", "")[-1:]
    test_number = int(test_number)
    
    if test_number == 1:
        test_name = '10P + 10S'
    elif test_number == 2:
        test_name = '25P + 25S'
    elif test_number == 3:
        test_name = '50P + 50S'
    elif test_number == 4:
        test_name = '100P + 100S'

    return test_name, test_number

def plot_stats(file, ax):
    df = pd.read_csv(file)["Latency"]
    x_width = df.size

    min = "{:.0f}".format(df.min())
    max = "{:.0f}".format(df.max())
    std = "{:.0f}".format(df.std())
    mean = "{:.0f}".format(df.mean())
    
    if df.mean() > 0 and x_width > 0:
        if 'unicast' in file:
            ax.hlines(df.mean(), 0, x_width, colors='#de425b', linestyles='dashed')
            ax.text(x_width * 0.6, df.mean(), "Mean: " + mean + "$\mu$s", color='white', backgroundcolor='#de425b')
            ax.text(x_width * 0.2, df.min(), "Min: " + min + "$\mu$s", color='white', backgroundcolor='#de425b')
            ax.text(x_width * 0.2, df.max(), "Max: " + max + "$\mu$s", color='white', backgroundcolor='#de425b')
            ax.text(x_width, df.max(), "std: " + std, color='white', backgroundcolor='#de425b')
        else:
            ax.hlines(df.mean(), 0, x_width, colors='#488f31', linestyles='dashed')
            ax.text(x_width * 0.4, df.mean(), "Mean: " + mean + "$\mu$s", color='white', backgroundcolor='#488f31')
            ax.text(0, df.min(), "Min: " + min + "$\mu$s", color='white', backgroundcolor='#488f31')
            ax.text(0, df.max(), "Max: " + max + "$\mu$s", color='white', backgroundcolor='#488f31')
            ax.text(x_width * 0.8, df.max(), "std: " + std, color='white', backgroundcolor='#488f31')


def plot_data(title, file, col, axes, c):
    if 'unicast' in file:
        test_type = "Unicast"
    else:
        test_type = "Multicast"
    test_name, test_number = get_test_name(file)
    df = pd.read_csv(file)["Latency"]
    index = (test_number - 1, col)
    ax = axes[index]
    # ax.scatter(df.index, df, s=s, label=test_type + ": " + test_name, c=c)
    ax.plot(df, label=test_type + ": " + test_name, c=c)
    ax.set_title(title)
    ax.set_yscale('log')
    ax.set_xlim(xmin=0)
    ax.set_ylabel("Latency ($\mu$s)")
    ax.set_xlabel("Measurements over Time")
    ax.legend()
    plot_stats(file, ax)

def get_run_count(files):
    max = 0
    for file in files:
        folder_name = os.path.basename(os.path.dirname(file))
        run_count = int(folder_name[-1])
        if run_count > max:
            max = run_count
    return max

def plot_all_latency_cdf_on_one(title, files, ax, color):
    run_count = get_run_count(files)
    for i in range(0, run_count):
        curr_run = i + 1
        for file in files:
            if 'run_' + str(curr_run) in file and title.lower() in file:
                df = pd.read_csv(file)["Latency"]
                filename = os.path.basename(file)
                filename = filename.replace("_", ' ')[5:11]
                cdf = df.value_counts().sort_index().cumsum() / df.shape[0]
                cdf.plot(ax = ax, label=title + " " + filename + " Run " + str(curr_run), color=color)
                ax.set_xlabel("Latency (mbps)")
        
    ax.legend()  
    ax.grid()
    # ax.set_xlim(xmin=0, xmax=1250)

def plot_cdf(title, file, ax, color, type):
    if 'latency' in type:
        df = pd.read_csv(file)["Latency"]
        cdf = df.value_counts().sort_index().cumsum() / df.shape[0]
        cdf.plot(ax = ax, label=title, color=color)
        ax.set_xlabel(title)
        ax.set_xlim(xmin=0, xmax=1500)

def plot_cdf(title, file, ax, color, type, xmin, xmax):
    if xmin is None:
        xmin = 0
    if 'latency' in type:
        df = pd.read_csv(file)["Latency"]
        if xmax is None:
            xmax = df.max()
            if xmax != xmax:
                xmax = None
        cdf = df.value_counts().sort_index().cumsum() / df.shape[0]
        cdf.plot(ax = ax, label=title, color=color)
        ax.set_xlim(xmin=xmin, xmax=xmax)
        ax.grid()
        ax.legend()
        ax.set_xlabel("Latency ($\mu$s)")

def configure_cdf(file, index, xmin, xmax, run_colors, axes):
    run = os.path.basename(os.path.dirname(file))
    run_count = int(run[-1]) - 1
    if 'unicast' in file:
        title = "Unicast " + run
    else:
        title = "Multicast " + run
    plot_cdf(title, file, axes[index], run_colors[run_count], 'latency', xmin, xmax)

def plot_latency_cdf_per_amount(unicast_latency_files, multicast_latency_files, axes):

    for file in unicast_latency_files:
        run_colors = ['#488f31', '#83af70', '#bad0af']
        if 'unicast_1' in file:
            configure_cdf(file, 0, 0, 8000, run_colors, axes)
        elif 'unicast_2' in file:
            configure_cdf(file, 1, None, None, run_colors, axes)
        elif 'unicast_3' in file:
            configure_cdf(file, 2, None, 450000, run_colors, axes)
        
    for file in multicast_latency_files:
        run_colors = ['#f3babc', '#ec838a', '#de425b']
        if 'multicast_1' in file:
            configure_cdf(file, 0, 0, 8000, run_colors, axes)
        elif 'multicast_2' in file:
            configure_cdf(file, 1, None, None, run_colors, axes)
        elif 'multicast_3' in file:
            configure_cdf(file, 2, None, 450000, run_colors, axes)

def plot_throughput_summary_table(files, test_name):
    figure, axes = plt.subplots()
    axes.axis('off')
    axes.axis('tight')

    tests = []
    total_samples = []
    samples_per_secs = []
    average_throughputs = []
    average_lost_samples = []

    for file in files:
        run_name = os.path.basename(os.path.dirname(file)).replace("_", " ").title()
        
        tests.append(test_name + run_name + " " + os.path.basename(file).replace("clean_", "").replace("_output.csv", "").replace("_", " ").title())

        df = pd.read_csv(file)
        
        total_samples.append(   "{:,.0f}".format(  df["Total Samples"].max()  )   )
        samples_per_secs.append(   "{:,.0f}".format(  df["Samples Per Second"].mean()  )   )
        average_throughputs.append(   "{:,.0f}".format(  df["Throughput"].mean()  )   )
        average_lost_samples.append(   "{:,.0f}".format(  df["Lost Samples"].mean()  )   )
        
    row_even_colour = 'lightgrey'
    row_odd_colour = 'white'

    figure = go.Figure(data=[go.Table(
        header = dict(
            values=['Test', 'Total Samples', 'Average Samples/Sec', 'Average Throughput (mbps)', 'Average Samples Lost'],
            fill_color = 'grey',
            font = dict(color='white', size=14)
        ),
        cells = dict(
            # values=[total_samples, avg_samples_per_sec, avg_throughput, lost_samples],
            values=[tests, total_samples, samples_per_secs, average_throughputs, average_lost_samples],
            fill_color = [[row_odd_colour, row_odd_colour, row_odd_colour, row_even_colour, row_even_colour, row_even_colour] * 5]
        )
    )])

    figure.show()

def plot_throughput_summary_tables(unicast_1_throughput_files, unicast_2_throughput_files, unicast_3_throughput_files, unicast_4_throughput_files, multicast_1_throughput_files, multicast_2_throughput_files, multicast_3_throughput_files, multicast_4_throughput_files):
    plot_throughput_summary_table(unicast_1_throughput_files, "10P + 10S Unicast ")
    plot_throughput_summary_table(multicast_1_throughput_files, "10P + 10S Multicast ")

    plot_throughput_summary_table(unicast_2_throughput_files, "25P + 25S Unicast ")
    plot_throughput_summary_table(multicast_2_throughput_files, "25P + 25S Multicast ")

    plot_throughput_summary_table(unicast_3_throughput_files, "50P + 50S Unicast ")
    plot_throughput_summary_table(multicast_3_throughput_files, "50P + 50S Multicast ")

    plot_throughput_summary_table(unicast_4_throughput_files, "100P + 100S Unicast ")
    plot_throughput_summary_table(multicast_4_throughput_files, "100P + 100S Multicast ")

def plot_run(label, file, color, title, column_index, data_type, plot_type, axes):
    if 'throughput' in data_type:
        if 'sub_0' in file:
            label=label
        else:
            label = None
        df = pd.read_csv(file)["Throughput"]
        test_name, test_number = get_test_name(file)
        index = (test_number - 1, column_index)
        ax = axes[index]
        if "100P" in title:
            ax.scatter(df.index, df, s=2, label=label, c=color)
        else:
            if 'line' in plot_type:
                ax.plot(df, label=label, c=color)
            else:
                ax.scatter(df.index, df, s=5, label=label, c=color)
                
        ax.set_title(title)
        ax.set_xlim(xmin=0)
        ax.set_ylabel("Throughput (mbps)")
        ax.set_xlabel("Time (s)")
        # ax.legend()

def plot_throughput_test(test_files, test_type, test_title, axes):
    if 'unicast' in test_type:
        color = '#488f31'
    else:
        color = '#de425b'

    for file in test_files:
        if 'run_1' in file:
            plot_run(test_type.title(), file, color, test_title + " Run 1", 0, 'throughput', 'dots', axes)
        elif 'run_2' in file:
            plot_run(test_type.title(), file, color, test_title + " Run 2", 1, 'throughput', 'dots', axes)
        elif 'run_3' in file:
            plot_run(test_type.title(), file, color, test_title + " Run 3", 2, 'throughput', 'dots', axes)

def plot_test_cdfs(ax, files, color, label):
    for file in files:
        if 'sub_0' in file and 'run_1' in file:
            label = label
        else:
            label = ""
        df = pd.read_csv(file)["Throughput"]
        cdf = df.value_counts().sort_index().cumsum() / df.shape[0]
        cdf.plot(ax = ax, c = color, label=label)
        ax.grid()
        ax.legend()

def plot_tests_cdfs(axes, unicast_1_throughput_files, unicast_2_throughput_files, unicast_3_throughput_files, unicast_4_throughput_files, multicast_1_throughput_files, multicast_2_throughput_files, multicast_3_throughput_files, multicast_4_throughput_files):
    plot_test_cdfs(axes[0], unicast_1_throughput_files, '#488f31', "Unicast")
    plot_test_cdfs(axes[0], multicast_1_throughput_files, '#de425b', "Multicast")
    axes[0].set_title("10P + 10S Unicast VS Multicast CDF")
    axes[0].set_xlabel("Throughput (mbps)")

    plot_test_cdfs(axes[1], unicast_2_throughput_files, '#488f31', "Unicast")
    plot_test_cdfs(axes[1], multicast_2_throughput_files, '#de425b', "Multicast")
    axes[1].set_title("25P + 25S Unicast VS Multicast CDF")
    axes[1].set_xlabel("Throughput (mbps)")

    plot_test_cdfs(axes[2], unicast_3_throughput_files, '#488f31', "Unicast")
    plot_test_cdfs(axes[2], multicast_3_throughput_files, '#de425b', "Multicast")
    axes[2].set_title("50P + 50S Unicast VS Multicast CDF")
    axes[2].set_xlabel("Throughput (mbps)")

    plot_test_cdfs(axes[3], unicast_4_throughput_files, '#488f31', "Unicast")
    plot_test_cdfs(axes[3], multicast_4_throughput_files, '#de425b', "Multicast")
    axes[3].set_title("100P + 100S Unicast VS Multicast CDF")
    axes[3].set_xlabel("Throughput (mbps)")