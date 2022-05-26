from scipy.stats import gaussian_kde
from numpy import linspace
from rich.jupyter import print
from rich.markdown import Markdown
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import plotly.graph_objects as go
import re
from statistics import *

from matplotlib.pyplot import figure
from matplotlib.lines import Line2D

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

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

def pretty_paths(filepaths):
    """
      Prettify filepaths from a test.
    
      Parameters:
        filepaths ([strings]): List of filepaths.
    
      Returns:
        new_filepaths ( [strings] ): List of new filepaths.
    """
    new_filepaths = []
    for file in filepaths:
        if 'set_1' in file:
            split_file = file.split('/')
            if 'unicast' in file:
                comm_type = 'unicast'
            else:
                comm_type = 'multicast'
            new_path = comm_type.title() + " " + split_file[3]
            new_filepaths.append(new_path)
    return new_filepaths

def get_test_names(file_paths):
    """
        Produces a nicely formatted test name from a list of file paths.
    
        Parameters:
            file_paths ([strings]): List of file paths.
    
        Returns:
            test_names ([strings]): List of test names.
    """
    
    test_names = []

    for file in file_paths:
        if 'set_1' in file:
            if 'unicast' in file:
                comm_type = 'unicast'
            else:
                comm_type = 'multicast'

            test_names.append("%s 3P + 3S" %comm_type.title())
        elif 'set_2' in file:
            if 'unicast' in file:
                comm_type = 'unicast'
            else:
                comm_type = 'multicast'
            
            if '_1_' in file:
                pub_count = 10
                sub_count = 10
            elif '_2_' in file:
                pub_count = 25
                sub_count = 25
            elif '_3_' in file:
                pub_count = 50
                sub_count = 50
            elif '_5_' in file or '75_participants' in file:
                pub_count = 75
                sub_count = 75
            else:
                pub_count = 100
                sub_count = 100

            new_test_name = str(pub_count) + "P/" + str(sub_count) + "S " + comm_type.title() + " (100B)"
            test_names.append(new_test_name)
        elif 'set_3' in file:
            if 'unicast' in file:
                comm_type = 'unicast'
            else:
                comm_type = 'multicast'

            if '_2_' in file:
                pub_count = 25
                mal_pub_count = 25
                sub_count = 25
                mal_sub_count = 25
            elif '_3_' in file:
                pub_count = 50
                mal_pub_count = 50
                sub_count = 50
                mal_sub_count = 50

            if '300_bytes' in file:
                data_length = '300B'
            elif '500_bytes' in file:
                data_length = '500B'
            elif '1_kilobyte' in file:
                data_length = '1KB'
            elif '16_kilobytes' in file:
                data_length = '16KB'
            elif '64_kilobytes' in file:
                data_length = '64KB'
            elif '128_kilobytes' in file:
                data_length = '128KB'
            elif '512_kilobytes' in file:
                data_length = '512KB'
            elif '1024_kilobytes' in file:
                data_length = '1024KB'

            new_test_name = "%dP + %dS %s %s" %(pub_count + mal_pub_count, sub_count + mal_sub_count, comm_type.title(), data_length)
            test_names.append(new_test_name)
        elif 'set_4' in file:
            if 'unicast' in file:
                comm_type = 'unicast'
            else:
                comm_type = 'multicast'
            
            if '_1_' in file:
                pub_count = 10
                sub_count = 20
            elif '_2_' in file:
                pub_count = 25
                sub_count = 50
            elif '_3_' in file:
                pub_count = 50
                sub_count = 100
            elif '_4_' in file:
                pub_count = 100
                sub_count = 200
            else:
                raise Exception("Error getting clean test names for set 4.")

            new_test_name = str(pub_count) + "P/" + str(sub_count) + "S " + comm_type.title() + " (100B)"
            test_names.append(new_test_name)
        else:
            raise Exception('Error getting test names for set with number greater than 4.')

    return test_names

def format_numbers(numbers):
    """
      Format numbers to include commas every 3 digits and no decimals.
    
      Parameters:
        numbers ([ ints ]): List of numbers to format.
    
      Returns:
        formatted_numbers ( [ints] ): List of formatted numbers
    """
    formatted_numbers = []
    
    for number in numbers:
        formatted_numbers.append(format_number(number))
    
    return formatted_numbers

def format_number(number):
    """
      Format number to include commas every 3 digits and no decimals.
    
      Parameters:
        number (int): Number to format.
    
      Returns:
        number (int): Formatted number 
    """
    return "{0:,.0f}".format(number)

def get_double(string):
    """
      Converts a string representation of a double to it's numeric format.
    
      Parameters:
        string (string): String representation of number.
    
      Returns:
        number (float): Decimal representation of number. 
    """
    if len(re.findall("\d+\.\d+", string)) > 0:
        return float(re.findall("\d+\.\d+", string)[0])
    else:
        return float(string)

def parse_data_lens(data, format):
    """
      Convert array of data length strings into numeric representation as bits by default or specified format.
    
      Parameters:
        data ( [strings] ): Array of data length as strings.
        format (string): Specified format. e.g. 'megabytes', 'megabits', etc.
    
      Returns:
        data ( [floats] ): Array of data lengths as numbers.
    """
    new_data = []

    for item in data:
        if 'K' in item:
            value = get_double(item[:-2]) * 1000
        elif 'M' in item:
            value = get_double(item[:-2]) * 1000000
        elif 'b' in item:
            value = get_double(item[:-1])

        new_data.append(value)
    
    if format is None:
        return new_data
    else:
        format = format.lower()
        if 'bytes' in format:
            new_data = [data / 8 for data in new_data]
        
        if 'kilo' in format:
            new_data = [data / 1000 for data in new_data] 
        elif 'mega' in format:
            new_data = [data / 1000000 for data in new_data]
        elif 'giga' in format:
            new_data = [data / 1000000000 for data in new_data] 

        return new_data

def interpolate_network_data(input):
    """
      Interpolates the network data to produce values every second rather than every two seconds.
    
      Parameters:
        input ([int]): Array of values.
    
      Returns:
        output ([int]): Array of interpolated values. 
    """
    input = pd.Series(input)                                        # Convert to pandas series
    output = input.to_numpy()                                       # Convert to numpy array
    output = np.insert(output, np.arange(1, len(output), 1), 0)     # Insert 0 after every second item
    output = np.where(output == 0, np.NaN, output)                  # Replace 0 with NaN
    output = pd.Series(output).interpolate()                        # Interpolate values of NaN
    return output

def get_network_data(file, format):
    """
      Get the send and receive rates from an output file of the iftop command and parse data into required `format`.
    
      Parameters:
        file (string): Path to file containing output of iftop command.
        format (string): Data format. e.g. 'megabits', 'kilobytes', etc.
    
      Returns:
        data ( { [floats], [floats] } ): dictionary containing array of send_rates and another array of receive_rates.
    """
    data = {
        'send_rates': [],
        'receive_rates': []
    }

    with open(file) as f:
        for line in f.readlines():
            if 'Total send rate' in line:
                split_line = line.split(" ")
                try:
                    send_rate = [word for word in split_line if len(word) > 0][3]
                except:
                    None
                data['send_rates'].append(send_rate)
            elif 'Total receive rate' in line:
                split_line = line.split(" ")
                receive_rate = [word for word in split_line if len(word) > 0][3]
                data['receive_rates'].append(receive_rate)

    try:
        if format is not None:
            data['send_rates'] = parse_data_lens(data['send_rates'], format)
            data['receive_rates'] = parse_data_lens(data['receive_rates'], format)
        else:
            data['send_rates'] = parse_data_lens(data['send_rates'], None)
            data['receive_rates'] = parse_data_lens(data['receive_rates'], None)
    except:
        None

    data['send_rates'] = interpolate_network_data(data['send_rates'])
    data['receive_rates'] = interpolate_network_data(data['receive_rates'])

    return data

def plot_table(ax, headings, rows):
    """
        Plot a table using matplotlib. Plots the table one row at a time starting with the headings.
        
        Parameters:
            ax (Axes): Axes to plot table on.
            headings ( [strings] ): List of headings for first row.
            rows ( [ [strings] ] ): List of rows.
        
        Returns:
            table (Table): Table created.
    """
    cellText = []
    for row in rows:
        cellText.append(row)

    return ax.table(
        cellText=cellText,
        colLabels=headings,
        loc='center', 
        colLoc='center',
        cellLoc='center')

def plot_lat_summary_table(latency_files):
    """
      Creates metric summary tables for latency files.append
    
      Parameters:
        latency_files ([files]): Array of file paths of latency files.
    
      Returns:
        None 
    """
    for file in latency_files:
        fig, ax = plt.subplots()

        df = pd.read_csv(file)

        stats = {
            "counts": [],
            "means": [],
            "stds": [],
            "mins": [],
            "25s": [],
            "50s": [],
            "75s": [],
            "maxs": []
        }

        run_columns = (df.columns[1:len(df.columns) - 3])
        run_text = []

        colours = [greens[0], oranges[0], reds[0], blues[0]]
        cellColour = []

        for i in range(len(run_columns)):
            col = run_columns[i]
            run_text.append("Run " + str(i + 1))
            cellColour.append(colours[i])
            stats["counts"].append(format_number(df[col].count()))
            stats["means"].append(format_number(df[col].mean()))
            stats["stds"].append(format_number(df[col].std()))
            stats["mins"].append(format_number(df[col].min()))
            stats["25s"].append(format_number(df[col].quantile(.25)))
            stats["50s"].append(format_number(df[col].quantile(.5)))
            stats["75s"].append(format_number(df[col].quantile(.75)))
            stats["maxs"].append(format_number(df[col].max()))

        cellColours = [cellColour, cellColour, cellColour, cellColour, cellColour, cellColour, cellColour, cellColour, cellColour]

        table = ax.table(
            cellText=[ run_text, stats["counts"], stats["means"], stats["stds"], stats["mins"], stats["25s"], stats["50s"], stats["75s"], stats["maxs"],],
            cellColours = cellColours,
            cellLoc='center',
            rowLabels=["Run", "Count", "Mean", "Standard Deviation", "Min.", "25%", "50%", "75%", "Max"],
            rowLoc='center',
            colLoc='center',
            loc='center'
        )
        ax.set_title(get_test_names([file])[0] + " Latency Summary", fontsize=15)
        table.scale(1, 2)
        table.auto_set_font_size(False)
        table.set_fontsize(15)
        table.auto_set_column_width(range(len(stats)))
        ax.axis("off")
        _ = ax.axis("tight")
        
        fig.patch.set_visible(False)

def plot_plotly_table(titles, columns):
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

def remove_list_duplicates(a_list):
    """
      Remove duplicates from a list.
    
      Parameters:
        a_list ( [list] ): A list.
    
      Returns:
        a_list ( [list] ): A list without duplicate values.
    """
    return list(dict.fromkeys(a_list))

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

def plot_cdf(title, df, ax, color, type):
    """
      Plot a CDF from a given DataFrame.
    
      Parameters:
        title (string): Label of x-axis.
        df (DataFrame): Data to plot cdf from.
        ax (Axis): Axis to plot on.
        color (string): Colour of cdf line.
        type (string): Whether it's an average plot (dashed lines) or normal (solid line).
    
      Returns:
        None
    """
    cdf = df.value_counts().sort_index().cumsum() / df.shape[0]
    if 'average' in type:
        cdf.plot(ax = ax, label=title, color=color, ls="--")
    else:
        cdf.plot(ax = ax, label=title, color=color)

def plot_pdf(df, ax, color, label):
    """
      Plot a PDF from a given DataFrame.
    
      Parameters:
        df (DataFrame): Data to plot cdf from.
        ax (Axis): Axis to plot on.
        color (string): Colour of cdf line.
        label (string): Label of x-axis.
    
      Returns:
        None
    """
    kde = gaussian_kde(df)
    dist_space = linspace(min(df), max(df), 1000)
    ax.plot(dist_space, kde(dist_space), color=color, label=label)

def set2_plot_latency_cdfs():
    set2_avgs = [file for file in get_files("data/set_2") if 'average' in file and 'forced_transport' in file]
    set2_lats = [file for file in set2_avgs if 'latencies' in file]

    ucast_lats = [file for file in set2_lats if 'unicast' in file]
    mcast_lats = [file for file in set2_lats if 'multicast' in file]
    mcast_lats.append(mcast_lats.pop(0))
    
    fig, ax = plt.subplots(figsize=(25, 10))

    lats = {
        "ucast_names": get_test_names(ucast_lats),
        "ucast_files": ucast_lats,
        "mcast_names": get_test_names(mcast_lats),
        "mcast_files": mcast_lats
    }

    for i in range(len(lats["ucast_files"])):
        if i < len(lats["ucast_files"]):
            # print(i)
            # print(lats["ucast_names"][i])
            if "100P" not in lats["ucast_names"][i]:
                df = pd.read_csv(lats["ucast_files"][i])
                try:
                    combined_df = pd.concat([ df['run_1_latency'], df['run_2_latency'], df['run_3_latency'] ])
                    plot_cdf( lats["ucast_names"][i] , combined_df, ax, greens[0], 'average')
                except:
                    print("Didn't work for " + lats["ucast_names"][i])

            if "100P" not in lats["mcast_names"][i]:
                df = pd.read_csv(lats["mcast_files"][i])
                try:
                    combined_df = pd.concat([ df['run_1_latency'], df['run_2_latency'], df['run_3_latency'] ])
                    plot_cdf( lats["mcast_names"][i] , combined_df, ax, reds[0], 'average')
                except:
                    print("Didn't work for " + lats["mcast_names"][i])
    
    ax.set_xlim(xmin=0, xmax=300000)
    ax.set_ylim(ymin=0, ymax=1)
    ax.set_xlabel("Latency ($\mu$s)")
    ax.set_xticks(list(ax.get_xticks()) + [8000, ])
    # ax.set_yticks(list(ax.get_yticks()) + [.25, .5, .75])
    ax.text(8000, 0.9, "10P/10S", color="black", backgroundcolor=greens[6], fontsize=12)
    ax.text(30000, 0.5, "25P/25S", color="black", backgroundcolor=greens[6], fontsize=12)
    ax.text(85000, 0.53, "50P/50S", color="black", backgroundcolor=greens[6], fontsize=12)
    # ax.text(140000, 0.3, "75P/75S", color="black", backgroundcolor=greens[6], fontsize=12)
    ax.grid()
    ax.legend()

    fig.suptitle("Latency CDFs (Unicast vs Multicast for Increasing Participants)", fontsize=15, fontweight='bold')

    plt.tight_layout()

def set2_plot_latency_cdfs_per_participant():

    fig, axes = plt.subplots(nrows=4, ncols=1, figsize=(35, 60))
    fig.suptitle("Latency CDFs Per Participant (Unicast vs Multicast)", fontsize=20, fontweight='bold')

    s2_lats = [file for file in get_files('data/set_2') if 'average_latencies' in file and '_4_' not in file and 'forced_transport' in file]

    s2_ucast_lats = [file for file in s2_lats if 'unicast' in file]
    s2_ucast_lats.sort()

    for file in s2_ucast_lats:
        i = s2_ucast_lats.index(file)
        df = pd.read_csv(file)
        combined_df = pd.concat([df['run_1_latency'], df['run_2_latency'], df['run_3_latency']])
        ax = axes[i]
        
        ax.set_ylim(ymin=0)
        ax.set_xlabel("Latency ($\mu$s)")

        if i == 0:
            ax.set_xlim(xmin=0, xmax=15000)
            ax.set_title("10P + 10S", fontsize=15, fontweight='bold')
        elif i == 1:
            ax.set_xlim(xmin=0, xmax=100000)
            ax.set_title("25P + 25S", fontsize=15, fontweight='bold')
        elif i == 2:
            ax.set_xlim(xmin=0, xmax=300000)
            ax.set_title("50P + 50S", fontsize=15, fontweight='bold')
        elif i == 3:
            ax.set_xlim(xmin=0, xmax=600000)
            ax.set_title("75P + 75S", fontsize=15, fontweight='bold')

        plot_cdf("", df['run_1_latency'], ax, greens[0], 'normal')
        plot_cdf("", df['run_2_latency'], ax, greens[0], 'normal')
        plot_cdf("", df['run_3_latency'], ax, greens[0], 'normal')
        plot_cdf(get_test_names([file])[0] + " Average", combined_df, ax, greens[0], 'average')

    s2_mcast_lats = [file for file in s2_lats if 'multicast' in file]
    s2_mcast_lats.sort()
    s2_mcast_lats.append(s2_mcast_lats.pop(0))

    for file in s2_mcast_lats:
        i = s2_mcast_lats.index(file)
        df = pd.read_csv(file)
        combined_df = pd.concat([df['run_1_latency'], df['run_2_latency'], df['run_3_latency']])
        ax = axes[i]
        
        ax.set_ylim(ymin=0)
        ax.set_xlabel("Latency ($\mu$s)")

        if i == 0:
            ax.set_xlim(xmin=0, xmax=15000)
            # ax.set_title("10P + 10S (Multicast)", fontsize=15, fontweight='bold', color=reds[0])
        elif i == 1:
            ax.set_xlim(xmin=0, xmax=120000)
            # ax.set_title("25P + 25S (Multicast)", fontsize=15, fontweight='bold', color=reds[0])
        elif i == 2:
            ax.set_xlim(xmin=0, xmax=300000)
            # ax.set_title("50P + 50S (Multicast)", fontsize=15, fontweight='bold', color=reds[0])
        elif i == 3:
            ax.set_xlim(xmin=0, xmax=600000)
            # ax.set_title("75P + 75S", fontsize=15, fontweight='bold')

        plot_cdf("", df['run_1_latency'], ax, reds[0], 'normal')
        plot_cdf("", df['run_2_latency'], ax, reds[0], 'normal')
        plot_cdf("", df['run_3_latency'], ax, reds[0], 'normal')
        plot_cdf(get_test_names([file])[0] + " Average", combined_df, ax, reds[0], 'average')

    for ax in axes:
        ax.grid()
        ax.legend(loc=2)

    plt.tight_layout(pad=5)

def set2_plot_tp_cdfs():
    set2_tps = [file for file in get_files('data/set_2') if 'average_throughput' in file and '_4_' not in file and 'forced_transport' in file]

    ucast_tps = [file for file in set2_tps if 'unicast' in file]
    mcast_tps = [file for file in set2_tps if 'multicast' in file]

    fig = plt.figure(figsize=(30, 15))

    tps = {
        "ucast_names": get_test_names(ucast_tps),
        "ucast_files": ucast_tps,
        "mcast_names": get_test_names(mcast_tps),
        "mcast_files": mcast_tps
    }

    grid = plt.GridSpec(2, 4, wspace=0.1, hspace=0.2)

    top_ax = plt.subplot(grid[0, :])
    bot_axes = {
        "1": plt.subplot(grid[1, 0]),
        "2": plt.subplot(grid[1, 1]),
        "3": plt.subplot(grid[1, 2]),
        "4": plt.subplot(grid[1, 3])
    }

    for i in range(len(tps["ucast_names"])):
        ucast_file = tps["ucast_files"][i]
        ucast_name = tps["ucast_names"][i]
        
        df = pd.read_csv(ucast_file)
        try:
            combined_df = pd.concat( [ df["run_1_throughput"], df["run_2_throughput"], df["run_3_throughput"] ] )
            if "_1_forced" in ucast_file:
                if 'sub_0' in ucast_file:
                    label = "10P + 10S"
                else:
                    label = ""
                plot_cdf(label, combined_df, top_ax, greens[0], 'average')
                plot_cdf(label, combined_df, bot_axes["1"], greens[0], 'average')
            elif "_2_forced" in ucast_file:
                if 'sub_0' in ucast_file:
                    label = "25P + 25S"
                else:
                    label = ""
                plot_cdf(label, combined_df, top_ax, greens[0], 'average')
                plot_cdf(label, combined_df, bot_axes["2"], greens[0], 'average')
            elif "_3_forced" in ucast_file:
                if 'sub_0' in ucast_file:
                    label = "50P + 50S"
                else:
                    label = ""
                plot_cdf(label, combined_df, top_ax, greens[0], 'average')
                plot_cdf(label, combined_df, bot_axes["3"], greens[0], 'average')
            elif "_5_75_participants" in ucast_file:
                if 'sub_0' in ucast_file:
                    label = "75P + 75S"
                else:
                    label = ""
                plot_cdf(label, combined_df, top_ax, greens[0], 'average')
                plot_cdf(label, combined_df, bot_axes["4"], greens[0], 'average')
        except:
            None

        mcast_file = tps["mcast_files"][i]
        mcast_name = tps["mcast_names"][i]
        try:
            df = pd.read_csv(mcast_file)
            combined_df = pd.concat( [ df["run_1_throughput"], df["run_2_throughput"], df["run_3_throughput"] ] )
            if "_1_forced" in mcast_file:
                if 'sub_0' in mcast_file:
                    label = "10P + 10S"
                else:
                    label = ""
                plot_cdf(label, combined_df, top_ax, reds[0], 'average')
                plot_cdf(label, combined_df, bot_axes["1"], reds[0], 'average')
                bot_axes["1"].title.set_text("10P + 10S")
            elif "_2_forced" in mcast_file:
                if 'sub_0' in mcast_file:
                    label = "25P + 25S"
                else:
                    label = ""
                plot_cdf(label, combined_df, top_ax, reds[0], 'average')
                plot_cdf(label, combined_df, bot_axes["2"], reds[0], 'average')
                bot_axes["2"].title.set_text("25P + 25S")
            elif "_3_forced" in mcast_file:
                if 'sub_0' in mcast_file:
                    label = "50P + 50S"
                else:
                    label = ""
                plot_cdf(label, combined_df, top_ax, reds[0], 'average')
                plot_cdf(label, combined_df, bot_axes["3"], reds[0], 'average')
                bot_axes["3"].title.set_text("50P + 50S")
            elif "_5_75_participants" in mcast_file:
                if 'sub_0' in mcast_file:
                    label = "75P + 75S"
                else:
                    label = ""
                plot_cdf(label, combined_df, top_ax, reds[0], 'average')
                plot_cdf(label, combined_df, bot_axes["4"], reds[0], 'average')
                bot_axes["4"].title.set_text("75P + 75S")
        except:
            None

    top_ax.set_ylim(ymin=0, ymax=1)
    top_ax.set_xlim(xmin=0, xmax=35)
    top_ax.set_xlabel("Throughput (mbps)")
    # ax.set_xticks( list(ax.get_xticks()) + [2, ] )
    # ax.legend()
    top_ax.grid()

    top_ax.text(28, 0.6, "10P + 10S", fontweight='bold', fontsize=12)
    top_ax.text(9, 0.6, "25P + 25S", fontweight='bold', fontsize=12)
    top_ax.text(4.5, 0.6, "50P + 50S", fontweight='bold', fontsize=12)
    top_ax.text(0.5, 0.6, "75P + 75S", fontweight='bold', fontsize=12)

    for ax in bot_axes:
        bot_axes[str(ax)].grid()
        bot_axes[str(ax)].set_xlabel("Throughput (mbps)")

    plt.subplot(grid[0, :]).title.set_text("Throughput CDFs (Unicast vs Multicast for Increasing Participants)")

def s2_plot_latency_avg_per_participant():
    fig, ax = plt.subplots(figsize=(35, 10))
    fig.suptitle("Latency Averages Per Participant Amount", fontsize=25, fontweight='bold')

    lats = [file for file in get_files("data/set_2") if 'average_latencies' in file and 'forced_transport' in file and '_4_' not in file]
    ucast_lats = [file for file in lats if 'unicast' in file]
    ucast_lats.sort()
    mcast_lats = [file for file in lats if 'multicast' in file]
    mcast_lats.sort()
    mcast_lats.append(mcast_lats.pop(0))

    ucast_names = []
    ucast_avg_lats = []

    for file in ucast_lats:
        ucast_names.append(get_test_names([file])[0])
        df = pd.read_csv(file)
        ucast_avg_lats.append(df['avg_run_latency'].mean())

    mcast_names = []
    mcast_avg_lats = []

    for file in mcast_lats:
        mcast_names.append(get_test_names([file])[0])
        df = pd.read_csv(file)
        mcast_avg_lats.append(df['avg_run_latency'].mean())

    udf = pd.DataFrame({
        "names": ucast_names,
        "avg_lats": ucast_avg_lats
    })

    mdf = pd.DataFrame({
        "names": mcast_names,
        "avg_lats": mcast_avg_lats
    })

    width = 0.15
    ucast_bars = ax.bar(udf.index - width / 2, udf['avg_lats'], width, color=greens[0], label="Unicast")
    ucast_bars = ax.bar(mdf.index + width / 2, mdf['avg_lats'], width, color=reds[0], label="Multicast")

    percent_diffs = []

    if len(udf['avg_lats']) == len(mdf['avg_lats']):
        for i in range(len(udf)):
            ucast_avg = udf['avg_lats'][i]
            mcast_avg = mdf['avg_lats'][i]
            if mcast_avg > ucast_avg:
                diff = mcast_avg - ucast_avg
                percent_diff = diff / ucast_avg
            else:
                diff = ucast_avg - mcast_avg
                percent_diff = diff / mcast_avg
            percent_diffs.append(percent_diff * 100)

    for i in range(len(udf['avg_lats'])):
        ax.text(i - width * 0.75, udf['avg_lats'][i] * 0.9, "{0:,.0f}".format(udf['avg_lats'][i]), color='white', fontweight='bold', backgroundcolor=greens[0])
        ax.text(i + width * 0.25, mdf['avg_lats'][i] * 0.9, "{0:,.0f}".format(mdf['avg_lats'][i]), color='white', fontweight='bold', backgroundcolor=reds[0])
        ax.text(i + width * 0.25, mdf['avg_lats'][i] * 1.1, "+" + format_number(percent_diffs[i]) + "%", color='black', backgroundcolor='white', fontweight='bold')

    u_mean = udf['avg_lats'].mean()
    ax.axhline(u_mean, 0, 1, ls='dashed', color=greens[0])
    ax.text(width * -1, u_mean * 1.05, "Unicast Avg.: " + format_number(u_mean) + "us", color=greens[0], fontweight='bold')

    m_mean = mdf['avg_lats'].mean()
    ax.axhline(m_mean, 0, 1, ls='dashed', color=reds[0])
    ax.text(width * -1, m_mean * 1.05, "Multicast Avg.: " + format_number(m_mean) + "us", color=reds[0], fontweight='bold')

    ax.annotate("+" + format_number(((m_mean - u_mean) / u_mean) * 100) + "%", xy=(width * 1.25, u_mean), xytext=(width * 1.25, m_mean * 1.05), arrowprops=dict(arrowstyle='<->'), fontweight='bold')

    ax.set_yscale('log')
    ax.set_ylabel("Latency ($\mu$s)")
    _ = ax.set_xticks(np.arange(len(udf['names'])), udf['names'])
    _ = ax.legend()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_color('#999')
    ax.spines['left'].set_color('#999')

def s2_rerun_plot_latency_variation_per_participant():
    files = [file for file in get_files('data/set_2') if 'forced_transport' in file and 'average_latencies' in file]

    ucast_files = [file for file in files if 'unicast' in file]
    mcast_files = [file for file in files if 'multicast' in file]
    mcast_files = mcast_files[1:] + [mcast_files[0]]

    data = {
        "ucast": {
            "run0": [],
            "run1": [],
            "run2": []
        },
        "mcast": {
            "run0": [],
            "run1": [],
            "run2": []
        }
    }

    for i in range(len(ucast_files)):
        ucast_file = ucast_files[i]
        mcast_file = mcast_files[i]

        udf = pd.read_csv(ucast_file)
        mdf = pd.read_csv(mcast_file)

        if '_1_forced' in ucast_file:
            to_append = data["ucast"]
            to_append["run0"].append(udf["run_1_latency"].mean())
            to_append["run1"].append(udf["run_2_latency"].mean())
            to_append["run2"].append(udf["run_3_latency"].mean())
            
            to_append = data["mcast"]
            to_append["run0"].append(mdf["run_1_latency"].mean())
            to_append["run1"].append(mdf["run_2_latency"].mean())
            to_append["run2"].append(mdf["run_3_latency"].mean())
        elif '_2_forced' in ucast_file:
            to_append = data["ucast"]
            to_append["run0"].append(udf["run_1_latency"].mean())
            to_append["run1"].append(udf["run_2_latency"].mean())
            to_append["run2"].append(udf["run_3_latency"].mean())
            
            to_append = data["mcast"]
            to_append["run0"].append(mdf["run_1_latency"].mean())
            to_append["run1"].append(mdf["run_2_latency"].mean())
            to_append["run2"].append(mdf["run_3_latency"].mean())
        elif '_3_forced' in ucast_file:
            to_append = data["ucast"]
            to_append["run0"].append(udf["run_1_latency"].mean())
            to_append["run1"].append(udf["run_2_latency"].mean())
            to_append["run2"].append(udf["run_3_latency"].mean())
            
            to_append = data["mcast"]
            to_append["run0"].append(mdf["run_1_latency"].mean())
            to_append["run1"].append(mdf["run_2_latency"].mean())
            to_append["run2"].append(mdf["run_3_latency"].mean())
        elif '_5_75_participants' in ucast_file:
            to_append = data["ucast"]
            to_append["run0"].append(udf["run_1_latency"].mean())
            to_append["run1"].append(udf["run_2_latency"].mean())
            to_append["run2"].append(udf["run_3_latency"].mean())
            
            to_append = data["mcast"]
            to_append["run0"].append(mdf["run_1_latency"].mean())
            to_append["run1"].append(mdf["run_2_latency"].mean())
            to_append["run2"].append(mdf["run_3_latency"].mean())

    df = pd.DataFrame(data)

    fig = plt.figure(figsize=(30, 15))
    grid = plt.GridSpec(2, 1, figure=fig, hspace=0.1, wspace=0.1)

    top_ax = plt.subplot(grid[0, 0])
    bot_ax = plt.subplot(grid[1, 0])

    width = 0.1

    # Plot top graph for unicast
    top_ax.title.set_text("Average Latencies Per Run Per Participant (Unicast)")
    top_ax.set_ylabel("Latency ($\mu$s)")
    top_ax.bar(np.array([0, 1, 2, 3]) - width, df["ucast"]["run0"], width, label="Run 1", color=yellows[0])
    top_ax.bar(np.array([0, 1, 2, 3]), df["ucast"]["run1"], width, label="Run 2", color=oranges[0])
    top_ax.bar(np.array([0, 1, 2, 3]) + width, df["ucast"]["run2"], width, label="Run 3", color=reds[0])
    top_ax.set_xticks(np.array([0, 1, 2,3 ]), ["10P + 10S", "25P + 25S", "50P + 50S", "75P + 75S"])

    # Add values on top of the bars for top plot
    for value in df["ucast"]["run0"]:
        index = df["ucast"]["run0"].index(value)
        top_ax.text(index - width * 1.5, value + 2000, format_number(value), fontweight='bold', color=greens[0])
    for value in df["ucast"]["run1"]:
        index = df["ucast"]["run1"].index(value)
        top_ax.text(index - width * 0.5, value + 2000, format_number(value), fontweight='bold', color=oranges[0])
    for value in df["ucast"]["run2"]:
        index = df["ucast"]["run2"].index(value)
        top_ax.text(index + width * 0.5, value + 2000, format_number(value), fontweight='bold', color=reds[0])

    # Plot bottom graph for multicast
    bot_ax.title.set_text("Average Latencies Per Run Per Participant (Multicast)")
    bot_ax.set_ylabel("Latency ($\mu$s)")
    bot_ax.bar(np.array([0, 1, 2, 3]) - width, df["mcast"]["run0"], width, label="Run 1", color=yellows[0])
    bot_ax.bar(np.array([0, 1, 2, 3]), df["mcast"]["run1"], width, label="Run 2", color=oranges[0])
    bot_ax.bar(np.array([0, 1, 2, 3]) + width, df["mcast"]["run2"], width, label="Run 3", color=reds[0])
    bot_ax.set_xticks(np.array([0, 1, 2,3 ]), ["10P + 10S", "25P + 25S", "50P + 50S", "75P + 75S"])

    # Add values on top of the bars for bottom plot
    for value in df["mcast"]["run0"]:
        index = df["mcast"]["run0"].index(value)
        bot_ax.text(index - width * 1.5, value + 2000, format_number(value), fontweight='bold', color=greens[0])
    for value in df["mcast"]["run1"]:
        index = df["mcast"]["run1"].index(value)
        bot_ax.text(index - width * 0.5, value + 2000, format_number(value), fontweight='bold', color=oranges[0])
    for value in df["mcast"]["run2"]:
        index = df["mcast"]["run2"].index(value)
        bot_ax.text(index + width * 0.5, value + 2000, format_number(value), fontweight='bold', color=reds[0])

    for ax in fig.get_axes():
        _ = ax.legend()
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

def s2_rerun_latency_cdf_vs_network_usage():
    lats = [file for file in get_files("data/set_2") if 'average_latencies' in file and ('network' in file or '75_participant' in file)]
    ucast_lats = [file for file in lats if 'unicast' in file]
    mcast_lats = [file for file in lats if 'multicast' in file]
    mcast_lats = mcast_lats[1:] + [mcast_lats[0]]

    net_logs = [file for file in get_files("data/set_2") if 'network_usage' in file and ('network' in file or '75_participant' in file)]
    net_logs.sort()
    net_logs = net_logs[12:] + [net_logs[:12]]
    ucast_logs = [file for file in net_logs if 'unicast' in file]
    mcast_logs = [file for file in net_logs if 'multicast' in file]

    fig = plt.figure(figsize=(30, 60))
    grid = plt.GridSpec(8, 2, figure=fig, hspace=0.25, wspace=0.1)

    left_ax = {
        "0": plt.subplot(grid[0:2, 0]),
        "1": plt.subplot(grid[2:4, 0]),
        "2": plt.subplot(grid[4:6, 0]),
        "3": plt.subplot(grid[6:8, 0])
    }

    right_ax = {
        "0": plt.subplot(grid[0, 1]),
        "1": plt.subplot(grid[1, 1]),
        "2": plt.subplot(grid[2, 1]),
        "3": plt.subplot(grid[3, 1]),
        "4": plt.subplot(grid[4, 1]),
        "5": plt.subplot(grid[5, 1]),
        "6": plt.subplot(grid[6, 1]),
        "7": plt.subplot(grid[7, 1])
    }

    left_ax["0"].title.set_text("10P + 10S")
    left_ax["1"].title.set_text("25P + 25S")
    left_ax["2"].title.set_text("50P + 50S")
    left_ax["3"].title.set_text("75P + 75S")

    for file in ucast_lats:
        i = ucast_lats.index(file)
        df = pd.read_csv(file)
        combined_df = pd.concat([df["run_1_latency"], df["run_2_latency"], df["run_3_latency"]])

        if i == 0:                  # 10P + 10S
            plot_cdf("", df["run_1_latency"], left_ax[str(i)], greens[0], 'normal')
            plot_cdf("", df["run_2_latency"], left_ax[str(i)], greens[0], 'normal')
            plot_cdf("", df["run_3_latency"], left_ax[str(i)], greens[0], 'normal')
            plot_cdf("Average", combined_df, left_ax[str(i)], greens[0], 'average')
            left_ax[str(i)].set_xlim(xmin=0, xmax=40000)
        elif i == 1:                  # 25P + 25S
            plot_cdf("", df["run_1_latency"], left_ax[str(i)], greens[0], 'normal')
            plot_cdf("", df["run_2_latency"], left_ax[str(i)], greens[0], 'normal')
            plot_cdf("", df["run_3_latency"], left_ax[str(i)], greens[0], 'normal')
            plot_cdf("Average", combined_df, left_ax[str(i)], greens[0], 'average')
            left_ax[str(i)].set_xlim(xmin=0, xmax=100000)
        elif i == 2:                  # 50P + 50S
            plot_cdf("", df["run_1_latency"], left_ax[str(i)], greens[0], 'normal')
            plot_cdf("", df["run_2_latency"], left_ax[str(i)], greens[0], 'normal')
            plot_cdf("", df["run_3_latency"], left_ax[str(i)], greens[0], 'normal')
            plot_cdf("Average", combined_df, left_ax[str(i)], greens[0], 'average')
            left_ax[str(i)].set_xlim(xmin=0, xmax=400000)
        elif i == 3:                  # 75P + 75S
            plot_cdf("", df["run_1_latency"], left_ax[str(i)], greens[0], 'normal')
            plot_cdf("", df["run_2_latency"], left_ax[str(i)], greens[0], 'normal')
            plot_cdf("", df["run_3_latency"], left_ax[str(i)], greens[0], 'normal')
            plot_cdf("Average", combined_df, left_ax[str(i)], greens[0], 'average')
            # left_ax[str(i)].set_xlim(xmin=0, xmax=4000)

    for file in mcast_lats:
        i = mcast_lats.index(file)
        df = pd.read_csv(file)
        combined_df = pd.concat([df["run_1_latency"], df["run_2_latency"], df["run_3_latency"]])

        if i == 0:                  # 10P + 10S
            plot_cdf("", df["run_1_latency"], left_ax[str(i)], reds[0], 'normal')
            plot_cdf("", df["run_2_latency"], left_ax[str(i)], reds[0], 'normal')
            plot_cdf("", df["run_3_latency"], left_ax[str(i)], reds[0], 'normal')
            plot_cdf("Average", combined_df, left_ax[str(i)], reds[0], 'average')
            left_ax[str(i)].set_xlim(xmin=0, xmax=40000)
        elif i == 1:                  # 25P + 25S
            plot_cdf("", df["run_1_latency"], left_ax[str(i)], reds[0], 'normal')
            plot_cdf("", df["run_2_latency"], left_ax[str(i)], reds[0], 'normal')
            plot_cdf("", df["run_3_latency"], left_ax[str(i)], reds[0], 'normal')
            plot_cdf("Average", combined_df, left_ax[str(i)], reds[0], 'average')
            left_ax[str(i)].set_xlim(xmin=0, xmax=100000)
        elif i == 2:                  # 50P + 50S
            plot_cdf("", df["run_1_latency"], left_ax[str(i)], reds[0], 'normal')
            plot_cdf("", df["run_2_latency"], left_ax[str(i)], reds[0], 'normal')
            plot_cdf("", df["run_3_latency"], left_ax[str(i)], reds[0], 'normal')
            plot_cdf("Average", combined_df, left_ax[str(i)], reds[0], 'average')
            left_ax[str(i)].set_xlim(xmin=0, xmax=400000)
        elif i == 3:                  # 75P + 75S
            plot_cdf("", df["run_1_latency"], left_ax[str(i)], reds[0], 'normal')
            plot_cdf("", df["run_2_latency"], left_ax[str(i)], reds[0], 'normal')
            plot_cdf("", df["run_3_latency"], left_ax[str(i)], reds[0], 'normal')
            plot_cdf("Average", combined_df, left_ax[str(i)], reds[0], 'average')
            # left_ax[str(i)].set_xlim(xmin=0, xmax=4000)

    for log in ucast_logs:
        i = ucast_logs.index(log)
        data = get_network_data(log, 'kilobytes')
        send_df = pd.DataFrame(data["send_rates"])
        receive_df = pd.DataFrame(data["receive_rates"])
        
        if "_1_" in log:
        
            right_ax[str(0)].title.set_text("10P + 10S Send Rate")
            right_ax[str(1)].title.set_text("10P + 10S Receive Rate")
        
            if "run_1" in log:
                if 'vm1' in log:
                    label="Run 1"
                else:
                    label=""
                right_ax[str(0)].plot(send_df, color=oranges[0], label=label)
                right_ax[str(1)].plot(receive_df, color=oranges[0], label=label)
            elif "run_2" in log:
                if 'vm1' in log:
                    label="Run 2"
                else:
                    label=""
                right_ax[str(0)].plot(send_df, color=blues[0], label=label)
                right_ax[str(1)].plot(receive_df, color=blues[0], label=label)
            elif "run_3" in log:
                if 'vm1' in log:
                    label="Run 3"
                else:
                    label=""
                right_ax[str(0)].plot(send_df, color=greens[0], label=label)
                right_ax[str(1)].plot(receive_df, color=greens[0], label=label)
        
        elif "_2_" in log:
        
            right_ax[str(2)].title.set_text("25P + 25S Send Rate")
            right_ax[str(3)].title.set_text("25P + 25S Receive Rate")

            if "run_1" in log:
                if 'vm1' in log:
                    label="Run 1"
                else:
                    label=""
                right_ax[str(2)].plot(send_df, color=oranges[0], label=label)
                right_ax[str(3)].plot(receive_df, color=oranges[0], label=label)
            elif "run_2" in log:
                if 'vm1' in log:
                    label="Run 2"
                else:
                    label=""
                right_ax[str(2)].plot(send_df, color=blues[0], label=label)
                right_ax[str(3)].plot(receive_df, color=blues[0], label=label)
            elif "run_3" in log:
                if 'vm1' in log:
                    label="Run 3"
                else:
                    label=""
                right_ax[str(2)].plot(send_df, color=greens[0], label=label)
                right_ax[str(3)].plot(receive_df, color=greens[0], label=label)

        elif "_3_" in log:

            right_ax[str(4)].title.set_text("50P + 50S Send Rate")
            right_ax[str(5)].title.set_text("50P + 50S Receive Rate")

            if "run_1" in log:
                if 'vm1' in log:
                    label="Run 1"
                else:
                    label=""
                right_ax[str(4)].plot(send_df, color=oranges[0], label=label)
                right_ax[str(5)].plot(receive_df, color=oranges[0], label=label)
            elif "run_2" in log:
                if 'vm1' in log:
                    label="Run 2"
                else:
                    label=""
                right_ax[str(4)].plot(send_df, color=blues[0], label=label)
                right_ax[str(5)].plot(receive_df, color=blues[0], label=label)
            elif "run_3" in log:
                if 'vm1' in log:
                    label="Run 3"
                else:
                    label=""
                right_ax[str(4)].plot(send_df, color=greens[0], label=label)
                right_ax[str(5)].plot(receive_df, color=greens[0], label=label)

        elif "_5_75_participants" in log:

            right_ax[str(6)].title.set_text("75P + 75S Send Rate")
            right_ax[str(7)].title.set_text("75P + 75S Receive Rate")

            if "run_1" in log:
                if 'vm1' in log:
                    label="Run 1"
                else:
                    label=""
                right_ax[str(6)].plot(send_df, color=oranges[0], label=label)
                right_ax[str(7)].plot(receive_df, color=oranges[0], label=label)
            elif "run_2" in log:
                if 'vm1' in log:
                    label="Run 2"
                else:
                    label=""
                right_ax[str(6)].plot(send_df, color=blues[0], label=label)
                right_ax[str(7)].plot(receive_df, color=blues[0], label=label)
            elif "run_3" in log:
                if 'vm1' in log:
                    label="Run 3"
                else:
                    label=""
                right_ax[str(6)].plot(send_df, color=greens[0], label=label)
                right_ax[str(7)].plot(receive_df, color=greens[0], label=label)

    for ax in left_ax:
        left_ax[str(ax)].set_xlabel("Latency ($\mu$s)")

    for ax in right_ax:
        right_ax[str(ax)].set_xlim(xmin=0)
        right_ax[str(ax)].set_ylabel("Rate (kbps)")
        right_ax[str(ax)].legend()

    for ax in fig.get_axes():
        ax.grid()
        # ax.legend(loc=4)
        ax.set_ylim(ymin=0)

def lat_tp_vs_net_per_vm_10p10s_unicast():
    lats = [file for file in get_files("data/set_2") if ('network_log_rerun' in file or '_5_75' in file) and 'average_latencies' in file]
    ulats = [file for file in lats if 'unicast' in file]
    mlats = [file for file in lats if 'multicast' in file]
    mlats.sort()
    mlats = mlats[1:] + mlats[:1]

    tps = [file for file in get_files("data/set_2") if 'average_throughput' in file and ('network_log_rerun' in file or '_5_75' in file)]
    tps.sort()

    logs = [file for file in get_files("data/set_2") if 'network_usage.log' in file and 'network' in file]
    logs.sort()
    ulogs = [file for file in logs if 'unicast' in file]
    mlogs = [file for file in logs if 'multicast' in file]
    mlogs = mlogs[12:] + mlogs[:12]

    fig = plt.figure(figsize=(30, 15))
    grid = plt.GridSpec(4, 4, figure=fig)

    row1 = {
        'lat': plt.subplot(grid[0:2, 0:2]),
        'tp': plt.subplot(grid[2:4, 0:2]),
        'vm1': plt.subplot(grid[0:2, 2]),
        'vm2': plt.subplot(grid[0:2, 3]),
        'vm3': plt.subplot(grid[2:4, 2]),
        'vm4': plt.subplot(grid[2:4, 3])
    }

    row1['lat'].title.set(text="10P + 10S Latency Measurements Over Increasing Time (Unicast)", fontsize=15, fontweight='bold')
    ulat = ulats[0]
    df = pd.read_csv(ulat)
    row1['lat'].plot(df["run_1_latency"], label="Run 1", color=greens[0])
    row1['lat'].plot(df["run_2_latency"], label="Run 2", color=blues[0])
    row1['lat'].plot(df["run_3_latency"], label="Run 3", color=reds[0])
    row1['lat'].set_xlim(xmin=0, xmax=3000)
    row1['lat'].set_ylim(ymin=0)
    row1['lat'].legend()
    row1['lat'].set_ylabel("Latency ($\mu$s)")
    row1['lat'].set_xlabel("Measurements Over Increasing Time")
    row1['lat'].spines['top'].set_visible(False)
    row1['lat'].spines['right'].set_visible(False)

    curr_tps = [file for file in tps if "unicast_1_" in file]
    for file in curr_tps:
        df = pd.read_csv(file)
        row1['tp'].plot(df["run_1_throughput"], color=greens[0])
        row1['tp'].plot(df["run_2_throughput"], color=blues[0])
        row1['tp'].plot(df["run_3_throughput"], color=reds[0])

    lines = [
        Line2D([0], [0], color=greens[0], lw=2),
        Line2D([0], [0], color=blues[0], lw=2),
        Line2D([0], [0], color=reds[0], lw=2)
    ]
    row1['tp'].title.set(text="10P + 10S Throughput Measurements Per Increasing Second (Unicast)", fontsize=15, fontweight='bold')
    row1['tp'].legend(lines, ['Run 1', 'Run 2', 'Run 3'])
    row1['tp'].set_xlim(xmin=0, xmax=900)
    row1['tp'].set_ylim(ymin=0)
    row1['tp'].set_ylabel("Throughput (MBps)")
    row1['tp'].set_xlabel("Increasing Time (s)")
    row1['tp'].spines['top'].set_visible(False)
    row1['tp'].spines['right'].set_visible(False)

    row1['vm1'].title.set(text="Network Send/Receive Rate for VM 1 \n Over Increasing Time Per Every 2 Seconds (3P + 2S)", fontsize=15, fontweight='bold')
    vm1_logs = [file for file in ulogs if 'vm1' in file and 'unicast_1_' in file]
    for log in vm1_logs:
        df = pd.DataFrame(get_network_data(log, 'megabytes'))
        if 'run_1' in log:  
            row1['vm1'].plot(df['send_rates'], color=greens[0], ls="--")
            # row1['vm1'].scatter(df['send_rates'].index, df['send_rates'], color=greens[0], ls="--", marker="_")
            row1['vm1'].plot(df['receive_rates'], color=greens[0])
            # row1['vm1'].scatter(df['receive_rates'].index, df['receive_rates'], color=greens[0], marker="|")
        elif 'run_2' in log:
            row1['vm1'].plot(df['send_rates'], color=blues[0], ls="--")
            # row1['vm1'].scatter(df['send_rates'].index, df['send_rates'], color=blues[0], ls="--", marker="_")
            row1['vm1'].plot(df['receive_rates'], color=blues[0])
            # row1['vm1'].scatter(df['receive_rates'].index, df['receive_rates'], color=blues[0], marker="|")
        elif 'run_3' in log:
            row1['vm1'].plot(df['send_rates'], color=reds[0], ls="--")
            # row1['vm1'].scatter(df['send_rates'].index, df['send_rates'], color=reds[0], ls="--", marker="_")
            row1['vm1'].plot(df['receive_rates'], color=reds[0])
            # row1['vm1'].scatter(df['receive_rates'].index, df['receive_rates'], color=reds[0], marker="|")
    lines = [
        Line2D([0], [0], linewidth=2, color=greens[0]),
        Line2D([0], [0], linewidth=2, color=blues[0]),
        Line2D([0], [0], linewidth=2, color=reds[0]),
        Line2D([0], [0], linewidth=2, ls="--", color='orange'),
        Line2D([0], [0], linewidth=2, color='orange')
    ]
    # row1['vm1'].legend(lines, ['Run 1', 'Run 2', 'Run 3', 'Send Rate', 'Receive Rate'])
    row1['vm1'].set_xlim(xmin=0, xmax=450)
    row1['vm1'].set_ylim(ymin=0)

    row1['vm2'].title.set(text="Network Send/Receive Rate for VM 2 \n Over Increasing Time Per Every 2 Seconds (2P + 3S)", fontsize=15, fontweight='bold')
    vm2_logs = [file for file in ulogs if 'vm2' in file and 'unicast_1_' in file]
    for log in vm2_logs:
        df = pd.DataFrame(get_network_data(log, 'megabytes'))
        if 'run_1' in log:  
            row1['vm2'].plot(df['send_rates'], color=greens[0], ls="--")
            # row1['vm2'].scatter(df['send_rates'].index, df['send_rates'], color=greens[0], ls="--", marker="_")
            row1['vm2'].plot(df['receive_rates'], color=greens[0])
            # row1['vm2'].scatter(df['receive_rates'].index, df['receive_rates'], color=greens[0], marker="|")
        elif 'run_2' in log:
            row1['vm2'].plot(df['send_rates'], color=blues[0], ls="--")
            # row1['vm2'].scatter(df['send_rates'].index, df['send_rates'], color=blues[0], ls="--", marker="_")
            row1['vm2'].plot(df['receive_rates'], color=blues[0])
            # row1['vm2'].scatter(df['receive_rates'].index, df['receive_rates'], color=blues[0], marker="|")
        elif 'run_3' in log:
            row1['vm2'].plot(df['send_rates'], color=reds[0], ls="--")
            # row1['vm2'].scatter(df['send_rates'].index, df['send_rates'], color=reds[0], ls="--", marker="_")
            row1['vm2'].plot(df['receive_rates'], color=reds[0])
            # row1['vm2'].scatter(df['receive_rates'].index, df['receive_rates'], color=reds[0], marker="|")
    lines = [
        Line2D([0], [0], linewidth=2, color=greens[0]),
        Line2D([0], [0], linewidth=2, color=blues[0]),
        Line2D([0], [0], linewidth=2, color=reds[0]),
        Line2D([0], [0], linewidth=2, ls="--", color='orange'),
        Line2D([0], [0], linewidth=2, color='orange')
    ]
    # row1['vm2'].legend(lines, ['Run 1', 'Run 2', 'Run 3', 'Send Rate', 'Receive Rate'])
    row1['vm2'].set_xlim(xmin=0, xmax=450)
    row1['vm2'].set_ylim(ymin=0)

    row1['vm3'].title.set(text="Network Send/Receive Rate for VM 3 \n Over Increasing Time Per Every 2 Seconds (3P + 2S)", fontsize=15, fontweight='bold')
    vm3_logs = [file for file in ulogs if 'vm3' in file and 'unicast_1_' in file]
    for log in vm3_logs:
        df = pd.DataFrame(get_network_data(log, 'megabytes'))
        if 'run_1' in log:  
            row1['vm3'].plot(df['send_rates'], color=greens[0], ls="--")
            # row1['vm3'].scatter(df['send_rates'].index, df['send_rates'], color=greens[0], ls="--", marker="_")
            row1['vm3'].plot(df['receive_rates'], color=greens[0])
            # row1['vm3'].scatter(df['receive_rates'].index, df['receive_rates'], color=greens[0], marker="|")
        elif 'run_2' in log:
            row1['vm3'].plot(df['send_rates'], color=blues[0], ls="--")
            # row1['vm3'].scatter(df['send_rates'].index, df['send_rates'], color=blues[0], ls="--", marker="_")
            row1['vm3'].plot(df['receive_rates'], color=blues[0])
            # row1['vm3'].scatter(df['receive_rates'].index, df['receive_rates'], color=blues[0], marker="|")
        elif 'run_3' in log:
            row1['vm3'].plot(df['send_rates'], color=reds[0], ls="--")
            # row1['vm3'].scatter(df['send_rates'].index, df['send_rates'], color=reds[0], ls="--", marker="_")
            row1['vm3'].plot(df['receive_rates'], color=reds[0])
            # row1['vm3'].scatter(df['receive_rates'].index, df['receive_rates'], color=reds[0], marker="|")
    lines = [
        Line2D([0], [0], linewidth=2, color=greens[0]),
        Line2D([0], [0], linewidth=2, color=blues[0]),
        Line2D([0], [0], linewidth=2, color=reds[0]),
        Line2D([0], [0], linewidth=2, ls="--", color='orange'),
        Line2D([0], [0], linewidth=2, color='orange')
    ]
    # row1['vm3'].legend(lines, ['Run 1', 'Run 2', 'Run 3', 'Send Rate', 'Receive Rate'])
    row1['vm3'].set_xlim(xmin=0, xmax=450)
    row1['vm3'].set_ylim(ymin=0)

    row1['vm4'].title.set(text="Network Send/Receive Rate for VM 4 \n Over Increasing Time Per Every 2 Seconds (2P + 3S)", fontsize=15, fontweight='bold')
    vm4_logs = [file for file in ulogs if 'vm4' in file and 'unicast_1_' in file]
    for log in vm4_logs:
        df = pd.DataFrame(get_network_data(log, 'megabytes'))
        if 'run_1' in log:  
            row1['vm4'].plot(df['send_rates'], color=greens[0], ls="--")
            # row1['vm4'].scatter(df['send_rates'].index, df['send_rates'], color=greens[0], ls="--", marker="_")
            row1['vm4'].plot(df['receive_rates'], color=greens[0])
            # row1['vm4'].scatter(df['receive_rates'].index, df['receive_rates'], color=greens[0], marker="|")
        elif 'run_2' in log:
            row1['vm4'].plot(df['send_rates'], color=blues[0], ls="--")
            # row1['vm4'].scatter(df['send_rates'].index, df['send_rates'], color=blues[0], ls="--", marker="_")
            row1['vm4'].plot(df['receive_rates'], color=blues[0])
            # row1['vm4'].scatter(df['receive_rates'].index, df['receive_rates'], color=blues[0], marker="|")
        elif 'run_3' in log:
            row1['vm4'].plot(df['send_rates'], color=reds[0], ls="--")
            # row1['vm4'].scatter(df['send_rates'].index, df['send_rates'], color=reds[0], ls="--", marker="_")
            row1['vm4'].plot(df['receive_rates'], color=reds[0])
            # row1['vm4'].scatter(df['receive_rates'].index, df['receive_rates'], color=reds[0], marker="|")
    # row1['vm4'].legend(lines, ['Run 1', 'Run 2', 'Run 3', 'Send Rate', 'Receive Rate'])
    row1['vm4'].set_xlim(xmin=0, xmax=450)
    row1['vm4'].set_ylim(ymin=0)

    # lines = [
    #     Line2D([0], [0], linewidth=2, color=greens[0]),
    #     Line2D([0], [0], linewidth=2, color=blues[0]),
    #     Line2D([0], [0], linewidth=2, color=reds[0]),
    #     Line2D([0], [0], linewidth=0, marker="_", color='black'),
    #     Line2D([0], [0], linewidth=0, marker="|", color='black')
    # ]
    for row in row1:
        if 'vm' in row:
            row1[str(row)].set_xlabel("Increasing Time (s)")
            row1[str(row)].set_ylabel("Send/Receive Rate (MBps)")
            row1[str(row)].legend(lines, ['Run 1', 'Run 2', 'Run 3', 'Send Rate', 'Receive Rate'])

    plt.tight_layout(pad=3)

def lat_tp_vs_net_per_vm_10p10s_multicast():
    lats = [file for file in get_files("data/set_2") if ('network_log_rerun' in file or '_5_75' in file) and 'average_latencies' in file]
    ulats = [file for file in lats if 'unicast' in file]
    mlats = [file for file in lats if 'multicast' in file]
    mlats.sort()
    mlats = mlats[1:] + mlats[:1]

    tps = [file for file in get_files("data/set_2") if 'average_throughput' in file and ('network_log_rerun' in file or '_5_75' in file)]
    tps.sort()

    logs = [file for file in get_files("data/set_2") if 'network_usage.log' in file and 'network' in file]
    logs.sort()
    ulogs = [file for file in logs if 'unicast' in file]
    mlogs = [file for file in logs if 'multicast' in file]
    mlogs = mlogs[12:] + mlogs[:12]

    fig = plt.figure(figsize=(30, 15))
    grid = plt.GridSpec(4, 4, figure=fig)

    row1 = {
        'lat': plt.subplot(grid[0:2, 0:2]),
        'tp': plt.subplot(grid[2:4, 0:2]),
        'vm1': plt.subplot(grid[0:2, 2]),
        'vm2': plt.subplot(grid[0:2, 3]),
        'vm3': plt.subplot(grid[2:4, 2]),
        'vm4': plt.subplot(grid[2:4, 3])
    }

    row1['lat'].title.set(text="10P + 10S Latency Measurements Over Increasing Time (Multicast)", fontsize=15, fontweight='bold')
    mlat = mlats[0]
    df = pd.read_csv(mlat)
    row1['lat'].plot(df["run_1_latency"], label="Run 1", color=greens[0])
    row1['lat'].plot(df["run_2_latency"], label="Run 2", color=blues[0])
    row1['lat'].plot(df["run_3_latency"], label="Run 3", color=reds[0])
    row1['lat'].set_xlim(xmin=0, xmax=3000)
    row1['lat'].set_ylim(ymin=0)
    row1['lat'].legend()
    row1['lat'].set_ylabel("Latency ($\mu$s)")
    row1['lat'].set_xlabel("Measurements Over Increasing Time")
    row1['lat'].spines['top'].set_visible(False)
    row1['lat'].spines['right'].set_visible(False)

    curr_tps = [file for file in tps if "multicast_1_" in file]
    for file in curr_tps:
        df = pd.read_csv(file)
        row1['tp'].plot(df["run_1_throughput"], color=greens[0])
        row1['tp'].plot(df["run_2_throughput"], color=blues[0])
        row1['tp'].plot(df["run_3_throughput"], color=reds[0])

    lines = [
        Line2D([0], [0], color=greens[0], lw=2),
        Line2D([0], [0], color=blues[0], lw=2),
        Line2D([0], [0], color=reds[0], lw=2)
    ]
    row1['tp'].title.set(text="10P + 10S Throughput Measurements Per Increasing Second (Multicast)", fontsize=15, fontweight='bold')
    row1['tp'].legend(lines, ['Run 1', 'Run 2', 'Run 3'])
    row1['tp'].set_xlim(xmin=0, xmax=900)
    row1['tp'].set_ylim(ymin=0)
    row1['tp'].set_ylabel("Throughput (mbps)")
    row1['tp'].set_xlabel("Increasing Time (s)")
    row1['tp'].spines['top'].set_visible(False)
    row1['tp'].spines['right'].set_visible(False)

    row1['vm1'].title.set(text="Network Send/Receive Rate for VM 1 \n Over Increasing Time Per Every 2 Seconds (12P + 13S)", fontsize=15, fontweight='bold')
    vm1_logs = [file for file in mlogs if 'vm1' in file and 'multicast_1_' in file]
    for log in vm1_logs:
        df = pd.DataFrame(get_network_data(log, 'megabytes'))
        if 'run_1' in log:  
            row1['vm1'].plot(df['send_rates'], color=greens[0], ls="--")
            # row1['vm1'].scatter(df['send_rates'].index, df['send_rates'], color=greens[0], ls="--", marker="_")
            row1['vm1'].plot(df['receive_rates'], color=greens[0])
            # row1['vm1'].scatter(df['receive_rates'].index, df['receive_rates'], color=greens[0], marker="|")
        elif 'run_2' in log:
            row1['vm1'].plot(df['send_rates'], color=blues[0], ls="--")
            # row1['vm1'].scatter(df['send_rates'].index, df['send_rates'], color=blues[0], ls="--", marker="_")
            row1['vm1'].plot(df['receive_rates'], color=blues[0])
            # row1['vm1'].scatter(df['receive_rates'].index, df['receive_rates'], color=blues[0], marker="|")
        elif 'run_3' in log:
            row1['vm1'].plot(df['send_rates'], color=reds[0], ls="--")
            # row1['vm1'].scatter(df['send_rates'].index, df['send_rates'], color=reds[0], ls="--", marker="_")
            row1['vm1'].plot(df['receive_rates'], color=reds[0])
            # row1['vm1'].scatter(df['receive_rates'].index, df['receive_rates'], color=reds[0], marker="|")
    lines = [
        Line2D([0], [0], linewidth=2, color=greens[0]),
        Line2D([0], [0], linewidth=2, color=blues[0]),
        Line2D([0], [0], linewidth=2, color=reds[0]),
        Line2D([0], [0], linewidth=2, ls="--", color='orange'),
        Line2D([0], [0], linewidth=2, color='orange')
    ]
    # row1['vm1'].legend(lines, ['Run 1', 'Run 2', 'Run 3', 'Send Rate', 'Receive Rate'])
    row1['vm1'].set_xlim(xmin=0, xmax=450)
    row1['vm1'].set_ylim(ymin=0)

    row1['vm2'].title.set(text="Network Send/Receive Rate for VM 2 \n Over Increasing Time Per Every 2 Seconds (13P + 12S)", fontsize=15, fontweight='bold')
    vm2_logs = [file for file in mlogs if 'vm2' in file and 'multicast_1_' in file]
    for log in vm2_logs:
        df = pd.DataFrame(get_network_data(log, 'megabytes'))
        if 'run_1' in log:  
            row1['vm2'].plot(df['send_rates'], color=greens[0], ls="--")
            # row1['vm2'].scatter(df['send_rates'].index, df['send_rates'], color=greens[0], ls="--", marker="_")
            row1['vm2'].plot(df['receive_rates'], color=greens[0])
            # row1['vm2'].scatter(df['receive_rates'].index, df['receive_rates'], color=greens[0], marker="|")
        elif 'run_2' in log:
            row1['vm2'].plot(df['send_rates'], color=blues[0], ls="--")
            # row1['vm2'].scatter(df['send_rates'].index, df['send_rates'], color=blues[0], ls="--", marker="_")
            row1['vm2'].plot(df['receive_rates'], color=blues[0])
            # row1['vm2'].scatter(df['receive_rates'].index, df['receive_rates'], color=blues[0], marker="|")
        elif 'run_3' in log:
            row1['vm2'].plot(df['send_rates'], color=reds[0], ls="--")
            # row1['vm2'].scatter(df['send_rates'].index, df['send_rates'], color=reds[0], ls="--", marker="_")
            row1['vm2'].plot(df['receive_rates'], color=reds[0])
            # row1['vm2'].scatter(df['receive_rates'].index, df['receive_rates'], color=reds[0], marker="|")
    lines = [
        Line2D([0], [0], linewidth=2, color=greens[0]),
        Line2D([0], [0], linewidth=2, color=blues[0]),
        Line2D([0], [0], linewidth=2, color=reds[0]),
        Line2D([0], [0], linewidth=2, ls="--", color='orange'),
        Line2D([0], [0], linewidth=2, color='orange')
    ]
    # row1['vm2'].legend(lines, ['Run 1', 'Run 2', 'Run 3', 'Send Rate', 'Receive Rate'])
    row1['vm2'].set_xlim(xmin=0, xmax=450)
    row1['vm2'].set_ylim(ymin=0)

    row1['vm3'].title.set(text="Network Send/Receive Rate for VM 3 \n Over Increasing Time Per Every 2 Seconds (12P + 13S)", fontsize=15, fontweight='bold')
    vm3_logs = [file for file in mlogs if 'vm3' in file and 'multicast_1_' in file]
    for log in vm3_logs:
        df = pd.DataFrame(get_network_data(log, 'megabytes'))
        if 'run_1' in log:  
            row1['vm3'].plot(df['send_rates'], color=greens[0], ls="--")
            # row1['vm3'].scatter(df['send_rates'].index, df['send_rates'], color=greens[0], ls="--", marker="_")
            row1['vm3'].plot(df['receive_rates'], color=greens[0])
            # row1['vm3'].scatter(df['receive_rates'].index, df['receive_rates'], color=greens[0], marker="|")
        elif 'run_2' in log:
            row1['vm3'].plot(df['send_rates'], color=blues[0], ls="--")
            # row1['vm3'].scatter(df['send_rates'].index, df['send_rates'], color=blues[0], ls="--", marker="_")
            row1['vm3'].plot(df['receive_rates'], color=blues[0])
            # row1['vm3'].scatter(df['receive_rates'].index, df['receive_rates'], color=blues[0], marker="|")
        elif 'run_3' in log:
            row1['vm3'].plot(df['send_rates'], color=reds[0], ls="--")
            # row1['vm3'].scatter(df['send_rates'].index, df['send_rates'], color=reds[0], ls="--", marker="_")
            row1['vm3'].plot(df['receive_rates'], color=reds[0])
            # row1['vm3'].scatter(df['receive_rates'].index, df['receive_rates'], color=reds[0], marker="|")
    lines = [
        Line2D([0], [0], linewidth=2, color=greens[0]),
        Line2D([0], [0], linewidth=2, color=blues[0]),
        Line2D([0], [0], linewidth=2, color=reds[0]),
        Line2D([0], [0], linewidth=2, ls="--", color='orange'),
        Line2D([0], [0], linewidth=2, color='orange')
    ]
    # row1['vm3'].legend(lines, ['Run 1', 'Run 2', 'Run 3', 'Send Rate', 'Receive Rate'])
    row1['vm3'].set_xlim(xmin=0, xmax=450)
    row1['vm3'].set_ylim(ymin=0)

    row1['vm4'].title.set(text="Network Send/Receive Rate for VM 4 \n Over Increasing Time Per Every 2 Seconds (13P + 12S)", fontsize=15, fontweight='bold')
    vm4_logs = [file for file in mlogs if 'vm4' in file and 'multicast_1_' in file]
    for log in vm4_logs:
        df = pd.DataFrame(get_network_data(log, 'megabytes'))
        if 'run_1' in log:  
            row1['vm4'].plot(df['send_rates'], color=greens[0], ls="--")
            # row1['vm4'].scatter(df['send_rates'].index, df['send_rates'], color=greens[0], ls="--", marker="_")
            row1['vm4'].plot(df['receive_rates'], color=greens[0])
            # row1['vm4'].scatter(df['receive_rates'].index, df['receive_rates'], color=greens[0], marker="|")
        elif 'run_2' in log:
            row1['vm4'].plot(df['send_rates'], color=blues[0], ls="--")
            # row1['vm4'].scatter(df['send_rates'].index, df['send_rates'], color=blues[0], ls="--", marker="_")
            row1['vm4'].plot(df['receive_rates'], color=blues[0])
            # row1['vm4'].scatter(df['receive_rates'].index, df['receive_rates'], color=blues[0], marker="|")
        elif 'run_3' in log:
            row1['vm4'].plot(df['send_rates'], color=reds[0], ls="--")
            # row1['vm4'].scatter(df['send_rates'].index, df['send_rates'], color=reds[0], ls="--", marker="_")
            row1['vm4'].plot(df['receive_rates'], color=reds[0])
            # row1['vm4'].scatter(df['receive_rates'].index, df['receive_rates'], color=reds[0], marker="|")
    # row1['vm4'].legend(lines, ['Run 1', 'Run 2', 'Run 3', 'Send Rate', 'Receive Rate'])
    row1['vm4'].set_xlim(xmin=0, xmax=450)
    row1['vm4'].set_ylim(ymin=0)

    # lines = [
    #     Line2D([0], [0], linewidth=2, color=greens[0]),
    #     Line2D([0], [0], linewidth=2, color=blues[0]),
    #     Line2D([0], [0], linewidth=2, color=reds[0]),
    #     Line2D([0], [0], linewidth=0, marker="_", color='black'),
    #     Line2D([0], [0], linewidth=0, marker="|", color='black')
    # ]
    for row in row1:
        if 'vm' in row:
            row1[str(row)].set_xlabel("Increasing Time (s)")
            row1[str(row)].set_ylabel("Send/Receive Rate (MBps)")
            row1[str(row)].legend(lines, ['Run 1', 'Run 2', 'Run 3', 'Send Rate', 'Receive Rate'])

    plt.tight_layout(pad=3)

def lat_tp_vs_net_per_vm_25p25s_unicast():
    lats = [file for file in get_files("data/set_2") if ('network_log_rerun' in file or '_5_75' in file) and 'average_latencies' in file]
    ulats = [file for file in lats if 'unicast' in file]
    mlats = [file for file in lats if 'multicast' in file]
    mlats.sort()
    mlats = mlats[1:] + mlats[:1]

    tps = [file for file in get_files("data/set_2") if 'average_throughput' in file and ('network_log_rerun' in file or '_5_75' in file)]
    tps.sort()

    logs = [file for file in get_files("data/set_2") if 'network_usage.log' in file and 'network' in file]
    logs.sort()
    ulogs = [file for file in logs if 'unicast' in file]
    mlogs = [file for file in logs if 'multicast' in file]
    mlogs = mlogs[12:] + mlogs[:12]

    fig = plt.figure(figsize=(30, 15))
    grid = plt.GridSpec(4, 4, figure=fig)

    row1 = {
        'lat': plt.subplot(grid[0:2, 0:2]),
        'tp': plt.subplot(grid[2:4, 0:2]),
        'vm1': plt.subplot(grid[0:2, 2]),
        'vm2': plt.subplot(grid[0:2, 3]),
        'vm3': plt.subplot(grid[2:4, 2]),
        'vm4': plt.subplot(grid[2:4, 3])
    }

    row1['lat'].title.set(text="25P + 25S Latency Measurements Over Increasing Time (Unicast)", fontsize=15, fontweight='bold')
    ulat = ulats[1]
    df = pd.read_csv(ulat)
    row1['lat'].plot(df["run_1_latency"], label="Run 1", color=greens[0])
    row1['lat'].plot(df["run_2_latency"], label="Run 2", color=blues[0])
    row1['lat'].plot(df["run_3_latency"], label="Run 3", color=reds[0])
    row1['lat'].set_xlim(xmin=0)
    row1['lat'].set_ylim(ymin=0)
    row1['lat'].legend()
    row1['lat'].set_ylabel("Latency ($\mu$s)")
    row1['lat'].set_xlabel("Measurements Over Increasing Time")
    row1['lat'].spines['top'].set_visible(False)
    row1['lat'].spines['right'].set_visible(False)

    curr_tps = [file for file in tps if "unicast_2_" in file]
    for file in curr_tps:
        df = pd.read_csv(file)
        row1['tp'].plot(df["run_1_throughput"], color=greens[0])
        row1['tp'].plot(df["run_2_throughput"], color=blues[0])
        row1['tp'].plot(df["run_3_throughput"], color=reds[0])

    lines = [
        Line2D([0], [0], color=greens[0], lw=2),
        Line2D([0], [0], color=blues[0], lw=2),
        Line2D([0], [0], color=reds[0], lw=2)
    ]
    row1['tp'].title.set(text="25P + 25S Throughput Measurements Per Increasing Second (Unicast)", fontsize=15, fontweight='bold')
    row1['tp'].legend(lines, ['Run 1', 'Run 2', 'Run 3'])
    row1['tp'].set_xlim(xmin=0, xmax=900)
    row1['tp'].set_ylim(ymin=0)
    row1['tp'].set_ylabel("Throughput (mbps)")
    row1['tp'].set_xlabel("Increasing Time (s)")
    row1['tp'].spines['top'].set_visible(False)
    row1['tp'].spines['right'].set_visible(False)

    row1['vm1'].title.set(text="Network Send/Receive Rate for VM 1 \n Over Increasing Time Per Every 2 Seconds (6P + 6S)", fontsize=15, fontweight='bold')
    vm1_logs = [file for file in ulogs if 'vm1' in file and 'unicast_2_' in file]
    for log in vm1_logs:
        df = pd.DataFrame(get_network_data(log, 'megabytes'))
        if 'run_1' in log:  
            row1['vm1'].plot(df['send_rates'], color=greens[0], ls="--")
            # row1['vm1'].scatter(df['send_rates'].index, df['send_rates'], color=greens[0], ls="--", marker="_")
            row1['vm1'].plot(df['receive_rates'], color=greens[0])
            # row1['vm1'].scatter(df['receive_rates'].index, df['receive_rates'], color=greens[0], marker="|")
        elif 'run_2' in log:
            row1['vm1'].plot(df['send_rates'], color=blues[0], ls="--")
            # row1['vm1'].scatter(df['send_rates'].index, df['send_rates'], color=blues[0], ls="--", marker="_")
            row1['vm1'].plot(df['receive_rates'], color=blues[0])
            # row1['vm1'].scatter(df['receive_rates'].index, df['receive_rates'], color=blues[0], marker="|")
        elif 'run_3' in log:
            row1['vm1'].plot(df['send_rates'], color=reds[0], ls="--")
            # row1['vm1'].scatter(df['send_rates'].index, df['send_rates'], color=reds[0], ls="--", marker="_")
            row1['vm1'].plot(df['receive_rates'], color=reds[0])
            # row1['vm1'].scatter(df['receive_rates'].index, df['receive_rates'], color=reds[0], marker="|")
    lines = [
        Line2D([0], [0], linewidth=2, color=greens[0]),
        Line2D([0], [0], linewidth=2, color=blues[0]),
        Line2D([0], [0], linewidth=2, color=reds[0]),
        Line2D([0], [0], linewidth=2, ls="--", color='orange'),
        Line2D([0], [0], linewidth=2, color='orange')
    ]
    # row1['vm1'].legend(lines, ['Run 1', 'Run 2', 'Run 3', 'Send Rate', 'Receive Rate'])
    row1['vm1'].set_xlim(xmin=0, xmax=450)
    row1['vm1'].set_ylim(ymin=0)

    row1['vm2'].title.set(text="Network Send/Receive Rate for VM 2 \n Over Increasing Time Per Every 2 Seconds (7P + 6S)", fontsize=15, fontweight='bold')
    vm2_logs = [file for file in ulogs if 'vm2' in file and 'unicast_2_' in file]
    for log in vm2_logs:
        df = pd.DataFrame(get_network_data(log, 'megabytes'))
        if 'run_1' in log:  
            row1['vm2'].plot(df['send_rates'], color=greens[0], ls="--")
            # row1['vm2'].scatter(df['send_rates'].index, df['send_rates'], color=greens[0], ls="--", marker="_")
            row1['vm2'].plot(df['receive_rates'], color=greens[0])
            # row1['vm2'].scatter(df['receive_rates'].index, df['receive_rates'], color=greens[0], marker="|")
        elif 'run_2' in log:
            row1['vm2'].plot(df['send_rates'], color=blues[0], ls="--")
            # row1['vm2'].scatter(df['send_rates'].index, df['send_rates'], color=blues[0], ls="--", marker="_")
            row1['vm2'].plot(df['receive_rates'], color=blues[0])
            # row1['vm2'].scatter(df['receive_rates'].index, df['receive_rates'], color=blues[0], marker="|")
        elif 'run_3' in log:
            row1['vm2'].plot(df['send_rates'], color=reds[0], ls="--")
            # row1['vm2'].scatter(df['send_rates'].index, df['send_rates'], color=reds[0], ls="--", marker="_")
            row1['vm2'].plot(df['receive_rates'], color=reds[0])
            # row1['vm2'].scatter(df['receive_rates'].index, df['receive_rates'], color=reds[0], marker="|")
    lines = [
        Line2D([0], [0], linewidth=2, color=greens[0]),
        Line2D([0], [0], linewidth=2, color=blues[0]),
        Line2D([0], [0], linewidth=2, color=reds[0]),
        Line2D([0], [0], linewidth=2, ls="--", color='orange'),
        Line2D([0], [0], linewidth=2, color='orange')
    ]
    # row1['vm2'].legend(lines, ['Run 1', 'Run 2', 'Run 3', 'Send Rate', 'Receive Rate'])
    row1['vm2'].set_xlim(xmin=0, xmax=450)
    row1['vm2'].set_ylim(ymin=0)

    row1['vm3'].title.set(text="Network Send/Receive Rate for VM 3 \n Over Increasing Time Per Every 2 Seconds (6P + 6S)", fontsize=15, fontweight='bold')
    vm3_logs = [file for file in ulogs if 'vm3' in file and 'unicast_2_' in file]
    for log in vm3_logs:
        df = pd.DataFrame(get_network_data(log, 'megabytes'))
        if 'run_1' in log:  
            row1['vm3'].plot(df['send_rates'], color=greens[0], ls="--")
            # row1['vm3'].scatter(df['send_rates'].index, df['send_rates'], color=greens[0], ls="--", marker="_")
            row1['vm3'].plot(df['receive_rates'], color=greens[0])
            # row1['vm3'].scatter(df['receive_rates'].index, df['receive_rates'], color=greens[0], marker="|")
        elif 'run_2' in log:
            row1['vm3'].plot(df['send_rates'], color=blues[0], ls="--")
            # row1['vm3'].scatter(df['send_rates'].index, df['send_rates'], color=blues[0], ls="--", marker="_")
            row1['vm3'].plot(df['receive_rates'], color=blues[0])
            # row1['vm3'].scatter(df['receive_rates'].index, df['receive_rates'], color=blues[0], marker="|")
        elif 'run_3' in log:
            row1['vm3'].plot(df['send_rates'], color=reds[0], ls="--")
            # row1['vm3'].scatter(df['send_rates'].index, df['send_rates'], color=reds[0], ls="--", marker="_")
            row1['vm3'].plot(df['receive_rates'], color=reds[0])
            # row1['vm3'].scatter(df['receive_rates'].index, df['receive_rates'], color=reds[0], marker="|")
    lines = [
        Line2D([0], [0], linewidth=2, color=greens[0]),
        Line2D([0], [0], linewidth=2, color=blues[0]),
        Line2D([0], [0], linewidth=2, color=reds[0]),
        Line2D([0], [0], linewidth=2, ls="--", color='orange'),
        Line2D([0], [0], linewidth=2, color='orange')
    ]
    # row1['vm3'].legend(lines, ['Run 1', 'Run 2', 'Run 3', 'Send Rate', 'Receive Rate'])
    row1['vm3'].set_xlim(xmin=0, xmax=450)
    row1['vm3'].set_ylim(ymin=0)

    row1['vm4'].title.set(text="Network Send/Receive Rate for VM 4 \n Over Increasing Time Per Every 2 Seconds (6P + 7S)", fontsize=15, fontweight='bold')
    vm4_logs = [file for file in ulogs if 'vm4' in file and 'unicast_2_' in file]
    for log in vm4_logs:
        df = pd.DataFrame(get_network_data(log, 'megabytes'))
        if 'run_1' in log:  
            row1['vm4'].plot(df['send_rates'], color=greens[0], ls="--")
            # row1['vm4'].scatter(df['send_rates'].index, df['send_rates'], color=greens[0], ls="--", marker="_")
            row1['vm4'].plot(df['receive_rates'], color=greens[0])
            # row1['vm4'].scatter(df['receive_rates'].index, df['receive_rates'], color=greens[0], marker="|")
        elif 'run_2' in log:
            row1['vm4'].plot(df['send_rates'], color=blues[0], ls="--")
            # row1['vm4'].scatter(df['send_rates'].index, df['send_rates'], color=blues[0], ls="--", marker="_")
            row1['vm4'].plot(df['receive_rates'], color=blues[0])
            # row1['vm4'].scatter(df['receive_rates'].index, df['receive_rates'], color=blues[0], marker="|")
        elif 'run_3' in log:
            row1['vm4'].plot(df['send_rates'], color=reds[0], ls="--")
            # row1['vm4'].scatter(df['send_rates'].index, df['send_rates'], color=reds[0], ls="--", marker="_")
            row1['vm4'].plot(df['receive_rates'], color=reds[0])
            # row1['vm4'].scatter(df['receive_rates'].index, df['receive_rates'], color=reds[0], marker="|")
    # row1['vm4'].legend(lines, ['Run 1', 'Run 2', 'Run 3', 'Send Rate', 'Receive Rate'])
    row1['vm4'].set_xlim(xmin=0, xmax=450)
    row1['vm4'].set_ylim(ymin=0)

    # lines = [
    #     Line2D([0], [0], linewidth=2, color=greens[0]),
    #     Line2D([0], [0], linewidth=2, color=blues[0]),
    #     Line2D([0], [0], linewidth=2, color=reds[0]),
    #     Line2D([0], [0], linewidth=0, marker="_", color='black'),
    #     Line2D([0], [0], linewidth=0, marker="|", color='black')
    # ]
    for row in row1:
        if 'vm' in row:
            row1[str(row)].set_xlabel("Increasing Time In 2s Increments(s)")
            row1[str(row)].set_ylabel("Send/Receive Rate (MBps)")
            row1[str(row)].legend(lines, ['Run 1', 'Run 2', 'Run 3', 'Send Rate', 'Receive Rate'])

    plt.tight_layout(pad=3)

def lat_tp_vs_net_per_vm_25p25s_multicast():
    lats = [file for file in get_files("data/set_2") if ('network_log_rerun' in file or '_5_75' in file) and 'average_latencies' in file]
    ulats = [file for file in lats if 'unicast' in file]
    mlats = [file for file in lats if 'multicast' in file]
    mlats.sort()
    mlats = mlats[1:] + mlats[:1]

    tps = [file for file in get_files("data/set_2") if 'average_throughput' in file and ('network_log_rerun' in file or '_5_75' in file)]
    tps.sort()

    logs = [file for file in get_files("data/set_2") if 'network_usage.log' in file and 'network' in file]
    logs.sort()
    ulogs = [file for file in logs if 'unicast' in file]
    mlogs = [file for file in logs if 'multicast' in file]
    mlogs = mlogs[12:] + mlogs[:12]

    fig = plt.figure(figsize=(30, 15))
    grid = plt.GridSpec(4, 4, figure=fig)

    row1 = {
        'lat': plt.subplot(grid[0:2, 0:2]),
        'tp': plt.subplot(grid[2:4, 0:2]),
        'vm1': plt.subplot(grid[0:2, 2]),
        'vm2': plt.subplot(grid[0:2, 3]),
        'vm3': plt.subplot(grid[2:4, 2]),
        'vm4': plt.subplot(grid[2:4, 3])
    }

    row1['lat'].title.set(text="25P + 25S Latency Measurements Over Increasing Time (Multicast)", fontsize=15, fontweight='bold')
    mlat = mlats[1]
    df = pd.read_csv(mlat)
    row1['lat'].plot(df["run_1_latency"], label="Run 1", color=greens[0])
    row1['lat'].plot(df["run_2_latency"], label="Run 2", color=blues[0])
    row1['lat'].plot(df["run_3_latency"], label="Run 3", color=reds[0])
    row1['lat'].set_xlim(xmin=0)
    row1['lat'].set_ylim(ymin=0)
    row1['lat'].legend()
    row1['lat'].set_ylabel("Latency ($\mu$s)")
    row1['lat'].set_xlabel("Measurements Over Increasing Time")
    row1['lat'].spines['top'].set_visible(False)
    row1['lat'].spines['right'].set_visible(False)

    curr_tps = [file for file in tps if "multicast_2_" in file]
    for file in curr_tps:
        df = pd.read_csv(file)
        row1['tp'].plot(df["run_1_throughput"], color=greens[0])
        row1['tp'].plot(df["run_2_throughput"], color=blues[0])
        row1['tp'].plot(df["run_3_throughput"], color=reds[0])

    lines = [
        Line2D([0], [0], color=greens[0], lw=2),
        Line2D([0], [0], color=blues[0], lw=2),
        Line2D([0], [0], color=reds[0], lw=2)
    ]
    row1['tp'].title.set(text="25P + 25S Throughput Measurements Per Increasing Second (Multicast)", fontsize=15, fontweight='bold')
    row1['tp'].legend(lines, ['Run 1', 'Run 2', 'Run 3'])
    row1['tp'].set_xlim(xmin=0, xmax=900)
    row1['tp'].set_ylim(ymin=0)
    row1['tp'].set_ylabel("Throughput (mbps)")
    row1['tp'].set_xlabel("Increasing Time (s)")
    row1['tp'].spines['top'].set_visible(False)
    row1['tp'].spines['right'].set_visible(False)

    row1['vm1'].title.set(text="Network Send/Receive Rate for VM 1 \n Over Increasing Time Per Every 2 Seconds (6P + 6S)", fontsize=15, fontweight='bold')
    vm1_logs = [file for file in mlogs if 'vm1' in file and 'multicast_2_' in file]
    for log in vm1_logs:
        df = pd.DataFrame.from_dict(get_network_data(log, 'megabytes'), orient='index')
        df = df.transpose()
        # df = pd.DataFrame(get_network_data(log, 'megabytes'))
        if 'run_1' in log:  
            row1['vm1'].plot(df['send_rates'], color=greens[0], ls="--")
            # row1['vm1'].scatter(df['send_rates'].index, df['send_rates'], color=greens[0], ls="--", marker="_")
            row1['vm1'].plot(df['receive_rates'], color=greens[0])
            # row1['vm1'].scatter(df['receive_rates'].index, df['receive_rates'], color=greens[0], marker="|")
        elif 'run_2' in log:
            row1['vm1'].plot(df['send_rates'], color=blues[0], ls="--")
            # row1['vm1'].scatter(df['send_rates'].index, df['send_rates'], color=blues[0], ls="--", marker="_")
            row1['vm1'].plot(df['receive_rates'], color=blues[0])
            # row1['vm1'].scatter(df['receive_rates'].index, df['receive_rates'], color=blues[0], marker="|")
        elif 'run_3' in log:
            row1['vm1'].plot(df['send_rates'], color=reds[0], ls="--")
            # row1['vm1'].scatter(df['send_rates'].index, df['send_rates'], color=reds[0], ls="--", marker="_")
            row1['vm1'].plot(df['receive_rates'], color=reds[0])
            # row1['vm1'].scatter(df['receive_rates'].index, df['receive_rates'], color=reds[0], marker="|")
    lines = [
        Line2D([0], [0], linewidth=2, color=greens[0]),
        Line2D([0], [0], linewidth=2, color=blues[0]),
        Line2D([0], [0], linewidth=2, color=reds[0]),
        Line2D([0], [0], linewidth=2, ls="--", color='orange'),
        Line2D([0], [0], linewidth=2, color='orange')
    ]
    # row1['vm1'].legend(lines, ['Run 1', 'Run 2', 'Run 3', 'Send Rate', 'Receive Rate'])
    row1['vm1'].set_xlim(xmin=0, xmax=450)
    row1['vm1'].set_ylim(ymin=0)

    row1['vm2'].title.set(text="Network Send/Receive Rate for VM 2 \n Over Increasing Time Per Every 2 Seconds (7P + 6S)", fontsize=15, fontweight='bold')
    vm2_logs = [file for file in mlogs if 'vm2' in file and 'multicast_2_' in file]
    for log in vm2_logs:
        df = pd.DataFrame(get_network_data(log, 'megabytes'))
        if 'run_1' in log:  
            row1['vm2'].plot(df['send_rates'], color=greens[0], ls="--")
            # row1['vm2'].scatter(df['send_rates'].index, df['send_rates'], color=greens[0], ls="--", marker="_")
            row1['vm2'].plot(df['receive_rates'], color=greens[0])
            # row1['vm2'].scatter(df['receive_rates'].index, df['receive_rates'], color=greens[0], marker="|")
        elif 'run_2' in log:
            row1['vm2'].plot(df['send_rates'], color=blues[0], ls="--")
            # row1['vm2'].scatter(df['send_rates'].index, df['send_rates'], color=blues[0], ls="--", marker="_")
            row1['vm2'].plot(df['receive_rates'], color=blues[0])
            # row1['vm2'].scatter(df['receive_rates'].index, df['receive_rates'], color=blues[0], marker="|")
        elif 'run_3' in log:
            row1['vm2'].plot(df['send_rates'], color=reds[0], ls="--")
            # row1['vm2'].scatter(df['send_rates'].index, df['send_rates'], color=reds[0], ls="--", marker="_")
            row1['vm2'].plot(df['receive_rates'], color=reds[0])
            # row1['vm2'].scatter(df['receive_rates'].index, df['receive_rates'], color=reds[0], marker="|")
    lines = [
        Line2D([0], [0], linewidth=2, color=greens[0]),
        Line2D([0], [0], linewidth=2, color=blues[0]),
        Line2D([0], [0], linewidth=2, color=reds[0]),
        Line2D([0], [0], linewidth=2, ls="--", color='orange'),
        Line2D([0], [0], linewidth=2, color='orange')
    ]
    # row1['vm2'].legend(lines, ['Run 1', 'Run 2', 'Run 3', 'Send Rate', 'Receive Rate'])
    row1['vm2'].set_xlim(xmin=0, xmax=450)
    row1['vm2'].set_ylim(ymin=0)

    row1['vm3'].title.set(text="Network Send/Receive Rate for VM 3 \n Over Increasing Time Per Every 2 Seconds (6P + 6S)", fontsize=15, fontweight='bold')
    vm3_logs = [file for file in mlogs if 'vm3' in file and 'multicast_2_' in file]
    for log in vm3_logs:
        df = pd.DataFrame(get_network_data(log, 'megabytes'))
        if 'run_1' in log:  
            row1['vm3'].plot(df['send_rates'], color=greens[0], ls="--")
            # row1['vm3'].scatter(df['send_rates'].index, df['send_rates'], color=greens[0], ls="--", marker="_")
            row1['vm3'].plot(df['receive_rates'], color=greens[0])
            # row1['vm3'].scatter(df['receive_rates'].index, df['receive_rates'], color=greens[0], marker="|")
        elif 'run_2' in log:
            row1['vm3'].plot(df['send_rates'], color=blues[0], ls="--")
            # row1['vm3'].scatter(df['send_rates'].index, df['send_rates'], color=blues[0], ls="--", marker="_")
            row1['vm3'].plot(df['receive_rates'], color=blues[0])
            # row1['vm3'].scatter(df['receive_rates'].index, df['receive_rates'], color=blues[0], marker="|")
        elif 'run_3' in log:
            row1['vm3'].plot(df['send_rates'], color=reds[0], ls="--")
            # row1['vm3'].scatter(df['send_rates'].index, df['send_rates'], color=reds[0], ls="--", marker="_")
            row1['vm3'].plot(df['receive_rates'], color=reds[0])
            # row1['vm3'].scatter(df['receive_rates'].index, df['receive_rates'], color=reds[0], marker="|")
    lines = [
        Line2D([0], [0], linewidth=2, color=greens[0]),
        Line2D([0], [0], linewidth=2, color=blues[0]),
        Line2D([0], [0], linewidth=2, color=reds[0]),
        Line2D([0], [0], linewidth=2, ls="--", color='orange'),
        Line2D([0], [0], linewidth=2, color='orange')
    ]
    # row1['vm3'].legend(lines, ['Run 1', 'Run 2', 'Run 3', 'Send Rate', 'Receive Rate'])
    row1['vm3'].set_xlim(xmin=0, xmax=450)
    row1['vm3'].set_ylim(ymin=0)

    row1['vm4'].title.set(text="Network Send/Receive Rate for VM 4 \n Over Increasing Time Per Every 2 Seconds (6P + 7S)", fontsize=15, fontweight='bold')
    vm4_logs = [file for file in mlogs if 'vm4' in file and 'multicast_2_' in file]
    for log in vm4_logs:
        df = pd.DataFrame(get_network_data(log, 'megabytes'))
        if 'run_1' in log:  
            row1['vm4'].plot(df['send_rates'], color=greens[0], ls="--")
            # row1['vm4'].scatter(df['send_rates'].index, df['send_rates'], color=greens[0], ls="--", marker="_")
            row1['vm4'].plot(df['receive_rates'], color=greens[0])
            # row1['vm4'].scatter(df['receive_rates'].index, df['receive_rates'], color=greens[0], marker="|")
        elif 'run_2' in log:
            row1['vm4'].plot(df['send_rates'], color=blues[0], ls="--")
            # row1['vm4'].scatter(df['send_rates'].index, df['send_rates'], color=blues[0], ls="--", marker="_")
            row1['vm4'].plot(df['receive_rates'], color=blues[0])
            # row1['vm4'].scatter(df['receive_rates'].index, df['receive_rates'], color=blues[0], marker="|")
        elif 'run_3' in log:
            row1['vm4'].plot(df['send_rates'], color=reds[0], ls="--")
            # row1['vm4'].scatter(df['send_rates'].index, df['send_rates'], color=reds[0], ls="--", marker="_")
            row1['vm4'].plot(df['receive_rates'], color=reds[0])
            # row1['vm4'].scatter(df['receive_rates'].index, df['receive_rates'], color=reds[0], marker="|")
    # row1['vm4'].legend(lines, ['Run 1', 'Run 2', 'Run 3', 'Send Rate', 'Receive Rate'])
    row1['vm4'].set_xlim(xmin=0, xmax=450)
    row1['vm4'].set_ylim(ymin=0)

    # lines = [
    #     Line2D([0], [0], linewidth=2, color=greens[0]),
    #     Line2D([0], [0], linewidth=2, color=blues[0]),
    #     Line2D([0], [0], linewidth=2, color=reds[0]),
    #     Line2D([0], [0], linewidth=0, marker="_", color='black'),
    #     Line2D([0], [0], linewidth=0, marker="|", color='black')
    # ]
    for row in row1:
        if 'vm' in row:
            row1[str(row)].set_xlabel("Increasing Time In 2s Increments(s)")
            row1[str(row)].set_ylabel("Send/Receive Rate (MBps)")
            row1[str(row)].legend(lines, ['Run 1', 'Run 2', 'Run 3', 'Send Rate', 'Receive Rate'])

    plt.tight_layout(pad=3)

def lat_tp_vs_net_per_vm_50p50s_unicast():
    lats = [file for file in get_files("data/set_2") if ('network_log_rerun' in file or '_5_75' in file) and 'average_latencies' in file]
    ulats = [file for file in lats if 'unicast' in file]
    mlats = [file for file in lats if 'multicast' in file]
    mlats.sort()
    mlats = mlats[1:] + mlats[:1]

    tps = [file for file in get_files("data/set_2") if 'average_throughput' in file and ('network_log_rerun' in file or '_5_75' in file)]
    tps.sort()

    logs = [file for file in get_files("data/set_2") if 'network_usage.log' in file and 'network' in file]
    logs.sort()
    ulogs = [file for file in logs if 'unicast' in file]
    mlogs = [file for file in logs if 'multicast' in file]
    mlogs = mlogs[12:] + mlogs[:12]

    fig = plt.figure(figsize=(30, 15))
    grid = plt.GridSpec(4, 4, figure=fig)

    row1 = {
        'lat': plt.subplot(grid[0:2, 0:2]),
        'tp': plt.subplot(grid[2:4, 0:2]),
        'vm1': plt.subplot(grid[0:2, 2]),
        'vm2': plt.subplot(grid[0:2, 3]),
        'vm3': plt.subplot(grid[2:4, 2]),
        'vm4': plt.subplot(grid[2:4, 3])
    }

    row1['lat'].title.set(text="50P + 50S Latency Measurements Over Increasing Time (Unicast)", fontsize=15, fontweight='bold')
    ulat = ulats[2]
    df = pd.read_csv(ulat)
    row1['lat'].plot(df["run_1_latency"], label="Run 1", color=greens[0])
    row1['lat'].plot(df["run_2_latency"], label="Run 2", color=blues[0])
    row1['lat'].plot(df["run_3_latency"], label="Run 3", color=reds[0])
    row1['lat'].set_xlim(xmin=0)
    # row1['lat'].set_ylim(ymin=0)
    row1['lat'].set_yscale('log')
    row1['lat'].legend()
    row1['lat'].set_ylabel("Latency ($\mu$s)")
    row1['lat'].set_xlabel("Measurements Over Increasing Time")
    row1['lat'].spines['top'].set_visible(False)
    row1['lat'].spines['right'].set_visible(False)

    curr_tps = [file for file in tps if "unicast_5_" in file]
    for file in curr_tps:
        df = pd.read_csv(file)
        row1['tp'].plot(df["run_1_throughput"], color=greens[0])
        row1['tp'].plot(df["run_2_throughput"], color=blues[0])
        row1['tp'].plot(df["run_3_throughput"], color=reds[0])

    lines = [
        Line2D([0], [0], color=greens[0], lw=2),
        Line2D([0], [0], color=blues[0], lw=2),
        Line2D([0], [0], color=reds[0], lw=2)
    ]
    row1['tp'].title.set(text="50P + 50S Throughput Measurements Per Increasing Second (Unicast)", fontsize=15, fontweight='bold')
    row1['tp'].legend(lines, ['Run 1', 'Run 2', 'Run 3'])
    row1['tp'].set_xlim(xmin=0, xmax=900)
    row1['tp'].set_ylim(ymin=0)
    row1['tp'].set_ylabel("Throughput (mbps)")
    row1['tp'].set_xlabel("Increasing Time (s)")
    row1['tp'].spines['top'].set_visible(False)
    row1['tp'].spines['right'].set_visible(False)

    row1['vm1'].title.set(text="Network Send/Receive Rate for VM 1 \n Over Increasing Time Per Every 2 Seconds (12P + 13S)", fontsize=15, fontweight='bold')
    vm1_logs = [file for file in ulogs if 'vm1' in file and 'unicast_5_' in file]
    for log in vm1_logs:
        df = pd.DataFrame(get_network_data(log, 'megabytes'))
        if 'run_1' in log:  
            row1['vm1'].plot(df['send_rates'], color=greens[0], ls="--")
            # row1['vm1'].scatter(df['send_rates'].index, df['send_rates'], color=greens[0], ls="--", marker="_")
            row1['vm1'].plot(df['receive_rates'], color=greens[0])
            # row1['vm1'].scatter(df['receive_rates'].index, df['receive_rates'], color=greens[0], marker="|")
        elif 'run_2' in log:
            row1['vm1'].plot(df['send_rates'], color=blues[0], ls="--")
            # row1['vm1'].scatter(df['send_rates'].index, df['send_rates'], color=blues[0], ls="--", marker="_")
            row1['vm1'].plot(df['receive_rates'], color=blues[0])
            # row1['vm1'].scatter(df['receive_rates'].index, df['receive_rates'], color=blues[0], marker="|")
        elif 'run_3' in log:
            row1['vm1'].plot(df['send_rates'], color=reds[0], ls="--")
            # row1['vm1'].scatter(df['send_rates'].index, df['send_rates'], color=reds[0], ls="--", marker="_")
            row1['vm1'].plot(df['receive_rates'], color=reds[0])
            # row1['vm1'].scatter(df['receive_rates'].index, df['receive_rates'], color=reds[0], marker="|")
    lines = [
        Line2D([0], [0], linewidth=2, color=greens[0]),
        Line2D([0], [0], linewidth=2, color=blues[0]),
        Line2D([0], [0], linewidth=2, color=reds[0]),
        Line2D([0], [0], linewidth=2, ls="--", color='orange'),
        Line2D([0], [0], linewidth=2, color='orange')
    ]
    # row1['vm1'].legend(lines, ['Run 1', 'Run 2', 'Run 3', 'Send Rate', 'Receive Rate'])
    row1['vm1'].set_xlim(xmin=0, xmax=450)
    row1['vm1'].set_ylim(ymin=0)

    row1['vm2'].title.set(text="Network Send/Receive Rate for VM 2 \n Over Increasing Time Per Every 2 Seconds (13P + 12S)", fontsize=15, fontweight='bold')
    vm2_logs = [file for file in ulogs if 'vm2' in file and 'unicast_5_' in file]
    for log in vm2_logs:
        # df = pd.DataFrame(get_network_data(log, 'megabytes'))
        df = pd.DataFrame.from_dict(get_network_data(log, 'megabytes'), orient='index')
        df = df.transpose()
        if 'run_1' in log:  
            row1['vm2'].plot(df['send_rates'], color=greens[0], ls="--")
            # row1['vm2'].scatter(df['send_rates'].index, df['send_rates'], color=greens[0], ls="--", marker="_")
            row1['vm2'].plot(df['receive_rates'], color=greens[0])
            # row1['vm2'].scatter(df['receive_rates'].index, df['receive_rates'], color=greens[0], marker="|")
        elif 'run_2' in log:
            row1['vm2'].plot(df['send_rates'], color=blues[0], ls="--")
            # row1['vm2'].scatter(df['send_rates'].index, df['send_rates'], color=blues[0], ls="--", marker="_")
            row1['vm2'].plot(df['receive_rates'], color=blues[0])
            # row1['vm2'].scatter(df['receive_rates'].index, df['receive_rates'], color=blues[0], marker="|")
        elif 'run_3' in log:
            row1['vm2'].plot(df['send_rates'], color=reds[0], ls="--")
            # row1['vm2'].scatter(df['send_rates'].index, df['send_rates'], color=reds[0], ls="--", marker="_")
            row1['vm2'].plot(df['receive_rates'], color=reds[0])
            # row1['vm2'].scatter(df['receive_rates'].index, df['receive_rates'], color=reds[0], marker="|")
    lines = [
        Line2D([0], [0], linewidth=2, color=greens[0]),
        Line2D([0], [0], linewidth=2, color=blues[0]),
        Line2D([0], [0], linewidth=2, color=reds[0]),
        Line2D([0], [0], linewidth=2, ls="--", color='orange'),
        Line2D([0], [0], linewidth=2, color='orange')
    ]
    # row1['vm2'].legend(lines, ['Run 1', 'Run 2', 'Run 3', 'Send Rate', 'Receive Rate'])
    row1['vm2'].set_xlim(xmin=0, xmax=450)
    row1['vm2'].set_ylim(ymin=0)

    row1['vm3'].title.set(text="Network Send/Receive Rate for VM 3 \n Over Increasing Time Per Every 2 Seconds (12P + 13S)", fontsize=15, fontweight='bold')
    vm3_logs = [file for file in ulogs if 'vm3' in file and 'unicast_5_' in file]
    for log in vm3_logs:
        df = pd.DataFrame(get_network_data(log, 'megabytes'))
        if 'run_1' in log:  
            row1['vm3'].plot(df['send_rates'], color=greens[0], ls="--")
            # row1['vm3'].scatter(df['send_rates'].index, df['send_rates'], color=greens[0], ls="--", marker="_")
            row1['vm3'].plot(df['receive_rates'], color=greens[0])
            # row1['vm3'].scatter(df['receive_rates'].index, df['receive_rates'], color=greens[0], marker="|")
        elif 'run_2' in log:
            row1['vm3'].plot(df['send_rates'], color=blues[0], ls="--")
            # row1['vm3'].scatter(df['send_rates'].index, df['send_rates'], color=blues[0], ls="--", marker="_")
            row1['vm3'].plot(df['receive_rates'], color=blues[0])
            # row1['vm3'].scatter(df['receive_rates'].index, df['receive_rates'], color=blues[0], marker="|")
        elif 'run_3' in log:
            row1['vm3'].plot(df['send_rates'], color=reds[0], ls="--")
            # row1['vm3'].scatter(df['send_rates'].index, df['send_rates'], color=reds[0], ls="--", marker="_")
            row1['vm3'].plot(df['receive_rates'], color=reds[0])
            # row1['vm3'].scatter(df['receive_rates'].index, df['receive_rates'], color=reds[0], marker="|")
    lines = [
        Line2D([0], [0], linewidth=2, color=greens[0]),
        Line2D([0], [0], linewidth=2, color=blues[0]),
        Line2D([0], [0], linewidth=2, color=reds[0]),
        Line2D([0], [0], linewidth=2, ls="--", color='orange'),
        Line2D([0], [0], linewidth=2, color='orange')
    ]
    # row1['vm3'].legend(lines, ['Run 1', 'Run 2', 'Run 3', 'Send Rate', 'Receive Rate'])
    row1['vm3'].set_xlim(xmin=0, xmax=450)
    row1['vm3'].set_ylim(ymin=0)

    row1['vm4'].title.set(text="Network Send/Receive Rate for VM 4 \n Over Increasing Time Per Every 2 Seconds (13P + 12S)", fontsize=15, fontweight='bold')
    vm4_logs = [file for file in ulogs if 'vm4' in file and 'unicast_5_' in file]
    for log in vm4_logs:
        df = pd.DataFrame(get_network_data(log, 'megabytes'))
        if 'run_1' in log:  
            row1['vm4'].plot(df['send_rates'], color=greens[0], ls="--")
            # row1['vm4'].scatter(df['send_rates'].index, df['send_rates'], color=greens[0], ls="--", marker="_")
            row1['vm4'].plot(df['receive_rates'], color=greens[0])
            # row1['vm4'].scatter(df['receive_rates'].index, df['receive_rates'], color=greens[0], marker="|")
        elif 'run_2' in log:
            row1['vm4'].plot(df['send_rates'], color=blues[0], ls="--")
            # row1['vm4'].scatter(df['send_rates'].index, df['send_rates'], color=blues[0], ls="--", marker="_")
            row1['vm4'].plot(df['receive_rates'], color=blues[0])
            # row1['vm4'].scatter(df['receive_rates'].index, df['receive_rates'], color=blues[0], marker="|")
        elif 'run_3' in log:
            row1['vm4'].plot(df['send_rates'], color=reds[0], ls="--")
            # row1['vm4'].scatter(df['send_rates'].index, df['send_rates'], color=reds[0], ls="--", marker="_")
            row1['vm4'].plot(df['receive_rates'], color=reds[0])
            # row1['vm4'].scatter(df['receive_rates'].index, df['receive_rates'], color=reds[0], marker="|")
    # row1['vm4'].legend(lines, ['Run 1', 'Run 2', 'Run 3', 'Send Rate', 'Receive Rate'])
    row1['vm4'].set_xlim(xmin=0, xmax=450)
    row1['vm4'].set_ylim(ymin=0)

    # lines = [
    #     Line2D([0], [0], linewidth=2, color=greens[0]),
    #     Line2D([0], [0], linewidth=2, color=blues[0]),
    #     Line2D([0], [0], linewidth=2, color=reds[0]),
    #     Line2D([0], [0], linewidth=0, marker="_", color='black'),
    #     Line2D([0], [0], linewidth=0, marker="|", color='black')
    # ]
    for row in row1:
        if 'vm' in row:
            row1[str(row)].set_xlabel("Increasing Time In 2s Increments(s)")
            row1[str(row)].set_ylabel("Send/Receive Rate (MBps)")
            row1[str(row)].legend(lines, ['Run 1', 'Run 2', 'Run 3', 'Send Rate', 'Receive Rate'])

    plt.tight_layout(pad=3)

def lat_tp_vs_net_per_vm_50p50s_multicast():
    lats = [file for file in get_files("data/set_2") if ('network_log_rerun' in file or '_5_75' in file) and 'average_latencies' in file]
    ulats = [file for file in lats if 'unicast' in file]
    mlats = [file for file in lats if 'multicast' in file]
    mlats.sort()
    mlats = mlats[1:] + mlats[:1]

    tps = [file for file in get_files("data/set_2") if 'average_throughput' in file and ('network_log_rerun' in file or '_5_75' in file)]
    tps.sort()

    logs = [file for file in get_files("data/set_2") if 'network_usage.log' in file and 'network' in file]
    logs.sort()
    ulogs = [file for file in logs if 'unicast' in file]
    mlogs = [file for file in logs if 'multicast' in file]
    mlogs = mlogs[12:] + mlogs[:12]

    fig = plt.figure(figsize=(30, 15))
    grid = plt.GridSpec(4, 4, figure=fig)

    row1 = {
        'lat': plt.subplot(grid[0:2, 0:2]),
        'tp': plt.subplot(grid[2:4, 0:2]),
        'vm1': plt.subplot(grid[0:2, 2]),
        'vm2': plt.subplot(grid[0:2, 3]),
        'vm3': plt.subplot(grid[2:4, 2]),
        'vm4': plt.subplot(grid[2:4, 3])
    }

    row1['lat'].title.set(text="50P + 50S Latency Measurements Over Increasing Time (Multicast)", fontsize=15, fontweight='bold')
    mlat = mlats[2]
    df = pd.read_csv(mlat)
    row1['lat'].plot(df["run_1_latency"], label="Run 1", color=greens[0])
    row1['lat'].plot(df["run_2_latency"], label="Run 2", color=blues[0])
    row1['lat'].plot(df["run_3_latency"], label="Run 3", color=reds[0])
    row1['lat'].set_xlim(xmin=0)
    # row1['lat'].set_ylim(ymin=0)
    row1['lat'].set_yscale('log')
    row1['lat'].legend()
    row1['lat'].set_ylabel("Latency ($\mu$s)")
    row1['lat'].set_xlabel("Measurements Over Increasing Time")
    row1['lat'].spines['top'].set_visible(False)
    row1['lat'].spines['right'].set_visible(False)

    curr_tps = [file for file in tps if "multicast_3_" in file]
    for file in curr_tps:
        df = pd.read_csv(file)
        row1['tp'].plot(df["run_1_throughput"], color=greens[0])
        row1['tp'].plot(df["run_2_throughput"], color=blues[0])
        row1['tp'].plot(df["run_3_throughput"], color=reds[0])

    lines = [
        Line2D([0], [0], color=greens[0], lw=2),
        Line2D([0], [0], color=blues[0], lw=2),
        Line2D([0], [0], color=reds[0], lw=2)
    ]
    row1['tp'].title.set(text="50P + 50S Throughput Measurements Per Increasing Second (Multicast)", fontsize=15, fontweight='bold')
    row1['tp'].legend(lines, ['Run 1', 'Run 2', 'Run 3'])
    row1['tp'].set_xlim(xmin=0, xmax=900)
    row1['tp'].set_ylim(ymin=0)
    row1['tp'].set_ylabel("Throughput (mbps)")
    row1['tp'].set_xlabel("Increasing Time (s)")
    row1['tp'].spines['top'].set_visible(False)
    row1['tp'].spines['right'].set_visible(False)

    row1['vm1'].title.set(text="Network Send/Receive Rate for VM 1 \n Over Increasing Time Per Every 2 Seconds (12P + 13S)", fontsize=15, fontweight='bold')
    vm1_logs = [file for file in mlogs if 'vm1' in file and 'multicast_3_' in file]
    for log in vm1_logs:
        df = pd.DataFrame(get_network_data(log, 'megabytes'))
        if 'run_1' in log:  
            row1['vm1'].plot(df['send_rates'], color=greens[0], ls="--")
            # row1['vm1'].scatter(df['send_rates'].index, df['send_rates'], color=greens[0], ls="--", marker="_")
            row1['vm1'].plot(df['receive_rates'], color=greens[0])
            # row1['vm1'].scatter(df['receive_rates'].index, df['receive_rates'], color=greens[0], marker="|")
        elif 'run_2' in log:
            row1['vm1'].plot(df['send_rates'], color=blues[0], ls="--")
            # row1['vm1'].scatter(df['send_rates'].index, df['send_rates'], color=blues[0], ls="--", marker="_")
            row1['vm1'].plot(df['receive_rates'], color=blues[0])
            # row1['vm1'].scatter(df['receive_rates'].index, df['receive_rates'], color=blues[0], marker="|")
        elif 'run_3' in log:
            row1['vm1'].plot(df['send_rates'], color=reds[0], ls="--")
            # row1['vm1'].scatter(df['send_rates'].index, df['send_rates'], color=reds[0], ls="--", marker="_")
            row1['vm1'].plot(df['receive_rates'], color=reds[0])
            # row1['vm1'].scatter(df['receive_rates'].index, df['receive_rates'], color=reds[0], marker="|")
    lines = [
        Line2D([0], [0], linewidth=2, color=greens[0]),
        Line2D([0], [0], linewidth=2, color=blues[0]),
        Line2D([0], [0], linewidth=2, color=reds[0]),
        Line2D([0], [0], linewidth=2, ls="--", color='orange'),
        Line2D([0], [0], linewidth=2, color='orange')
    ]
    # row1['vm1'].legend(lines, ['Run 1', 'Run 2', 'Run 3', 'Send Rate', 'Receive Rate'])
    row1['vm1'].set_xlim(xmin=0, xmax=450)
    row1['vm1'].set_ylim(ymin=0)

    row1['vm2'].title.set(text="Network Send/Receive Rate for VM 2 \n Over Increasing Time Per Every 2 Seconds (13P + 12S)", fontsize=15, fontweight='bold')
    vm2_logs = [file for file in mlogs if 'vm2' in file and 'multicast_3_' in file]
    for log in vm2_logs:
        # df = pd.DataFrame(get_network_data(log, 'megabytes'))
        df = pd.DataFrame.from_dict(get_network_data(log, 'megabytes'), orient='index')
        df = df.transpose()
        if 'run_1' in log:  
            row1['vm2'].plot(df['send_rates'], color=greens[0], ls="--")
            # row1['vm2'].scatter(df['send_rates'].index, df['send_rates'], color=greens[0], ls="--", marker="_")
            row1['vm2'].plot(df['receive_rates'], color=greens[0])
            # row1['vm2'].scatter(df['receive_rates'].index, df['receive_rates'], color=greens[0], marker="|")
        elif 'run_2' in log:
            row1['vm2'].plot(df['send_rates'], color=blues[0], ls="--")
            # row1['vm2'].scatter(df['send_rates'].index, df['send_rates'], color=blues[0], ls="--", marker="_")
            row1['vm2'].plot(df['receive_rates'], color=blues[0])
            # row1['vm2'].scatter(df['receive_rates'].index, df['receive_rates'], color=blues[0], marker="|")
        elif 'run_3' in log:
            row1['vm2'].plot(df['send_rates'], color=reds[0], ls="--")
            # row1['vm2'].scatter(df['send_rates'].index, df['send_rates'], color=reds[0], ls="--", marker="_")
            row1['vm2'].plot(df['receive_rates'], color=reds[0])
            # row1['vm2'].scatter(df['receive_rates'].index, df['receive_rates'], color=reds[0], marker="|")
    lines = [
        Line2D([0], [0], linewidth=2, color=greens[0]),
        Line2D([0], [0], linewidth=2, color=blues[0]),
        Line2D([0], [0], linewidth=2, color=reds[0]),
        Line2D([0], [0], linewidth=2, ls="--", color='orange'),
        Line2D([0], [0], linewidth=2, color='orange')
    ]
    # row1['vm2'].legend(lines, ['Run 1', 'Run 2', 'Run 3', 'Send Rate', 'Receive Rate'])
    row1['vm2'].set_xlim(xmin=0, xmax=450)
    row1['vm2'].set_ylim(ymin=0)

    row1['vm3'].title.set(text="Network Send/Receive Rate for VM 3 \n Over Increasing Time Per Every 2 Seconds (12P + 13S)", fontsize=15, fontweight='bold')
    vm3_logs = [file for file in mlogs if 'vm3' in file and 'multicast_3_' in file]
    for log in vm3_logs:
        df = pd.DataFrame(get_network_data(log, 'megabytes'))
        if 'run_1' in log:  
            row1['vm3'].plot(df['send_rates'], color=greens[0], ls="--")
            # row1['vm3'].scatter(df['send_rates'].index, df['send_rates'], color=greens[0], ls="--", marker="_")
            row1['vm3'].plot(df['receive_rates'], color=greens[0])
            # row1['vm3'].scatter(df['receive_rates'].index, df['receive_rates'], color=greens[0], marker="|")
        elif 'run_2' in log:
            row1['vm3'].plot(df['send_rates'], color=blues[0], ls="--")
            # row1['vm3'].scatter(df['send_rates'].index, df['send_rates'], color=blues[0], ls="--", marker="_")
            row1['vm3'].plot(df['receive_rates'], color=blues[0])
            # row1['vm3'].scatter(df['receive_rates'].index, df['receive_rates'], color=blues[0], marker="|")
        elif 'run_3' in log:
            row1['vm3'].plot(df['send_rates'], color=reds[0], ls="--")
            # row1['vm3'].scatter(df['send_rates'].index, df['send_rates'], color=reds[0], ls="--", marker="_")
            row1['vm3'].plot(df['receive_rates'], color=reds[0])
            # row1['vm3'].scatter(df['receive_rates'].index, df['receive_rates'], color=reds[0], marker="|")
    lines = [
        Line2D([0], [0], linewidth=2, color=greens[0]),
        Line2D([0], [0], linewidth=2, color=blues[0]),
        Line2D([0], [0], linewidth=2, color=reds[0]),
        Line2D([0], [0], linewidth=2, ls="--", color='orange'),
        Line2D([0], [0], linewidth=2, color='orange')
    ]
    # row1['vm3'].legend(lines, ['Run 1', 'Run 2', 'Run 3', 'Send Rate', 'Receive Rate'])
    row1['vm3'].set_xlim(xmin=0, xmax=450)
    row1['vm3'].set_ylim(ymin=0)

    row1['vm4'].title.set(text="Network Send/Receive Rate for VM 4 \n Over Increasing Time Per Every 2 Seconds (13P + 12S)", fontsize=15, fontweight='bold')
    vm4_logs = [file for file in mlogs if 'vm4' in file and 'multicast_3_' in file]
    for log in vm4_logs:
        df = pd.DataFrame(get_network_data(log, 'megabytes'))
        if 'run_1' in log:  
            row1['vm4'].plot(df['send_rates'], color=greens[0], ls="--")
            # row1['vm4'].scatter(df['send_rates'].index, df['send_rates'], color=greens[0], ls="--", marker="_")
            row1['vm4'].plot(df['receive_rates'], color=greens[0])
            # row1['vm4'].scatter(df['receive_rates'].index, df['receive_rates'], color=greens[0], marker="|")
        elif 'run_2' in log:
            row1['vm4'].plot(df['send_rates'], color=blues[0], ls="--")
            # row1['vm4'].scatter(df['send_rates'].index, df['send_rates'], color=blues[0], ls="--", marker="_")
            row1['vm4'].plot(df['receive_rates'], color=blues[0])
            # row1['vm4'].scatter(df['receive_rates'].index, df['receive_rates'], color=blues[0], marker="|")
        elif 'run_3' in log:
            row1['vm4'].plot(df['send_rates'], color=reds[0], ls="--")
            # row1['vm4'].scatter(df['send_rates'].index, df['send_rates'], color=reds[0], ls="--", marker="_")
            row1['vm4'].plot(df['receive_rates'], color=reds[0])
            # row1['vm4'].scatter(df['receive_rates'].index, df['receive_rates'], color=reds[0], marker="|")
    # row1['vm4'].legend(lines, ['Run 1', 'Run 2', 'Run 3', 'Send Rate', 'Receive Rate'])
    row1['vm4'].set_xlim(xmin=0, xmax=450)
    row1['vm4'].set_ylim(ymin=0)

    # lines = [
    #     Line2D([0], [0], linewidth=2, color=greens[0]),
    #     Line2D([0], [0], linewidth=2, color=blues[0]),
    #     Line2D([0], [0], linewidth=2, color=reds[0]),
    #     Line2D([0], [0], linewidth=0, marker="_", color='black'),
    #     Line2D([0], [0], linewidth=0, marker="|", color='black')
    # ]
    for row in row1:
        if 'vm' in row:
            row1[str(row)].set_xlabel("Increasing Time In 2s Increments(s)")
            row1[str(row)].set_ylabel("Send/Receive Rate (MBps)")
            row1[str(row)].legend(lines, ['Run 1', 'Run 2', 'Run 3', 'Send Rate', 'Receive Rate'])

    plt.tight_layout(pad=3)

def lat_tp_vs_net_per_vm_75p75s_unicast():
    lats = [file for file in get_files("data/set_2") if ('network_log_rerun' in file or '_5_75' in file) and 'average_latencies' in file]
    ulats = [file for file in lats if 'unicast' in file]
    mlats = [file for file in lats if 'multicast' in file]
    mlats.sort()
    mlats = mlats[1:] + mlats[:1]

    tps = [file for file in get_files("data/set_2") if 'average_throughput' in file and ('network_log_rerun' in file or '_5_75' in file)]
    tps.sort()

    logs = [file for file in get_files("data/set_2") if 'network_usage.log' in file and 'network' in file]
    logs.sort()
    ulogs = [file for file in logs if 'unicast' in file]
    mlogs = [file for file in logs if 'multicast' in file]
    mlogs = mlogs[12:] + mlogs[:12]

    fig = plt.figure(figsize=(30, 15))
    grid = plt.GridSpec(4, 4, figure=fig)

    row1 = {
        'lat': plt.subplot(grid[0:2, 0:2]),
        'tp': plt.subplot(grid[2:4, 0:2]),
        'vm1': plt.subplot(grid[0:2, 2]),
        'vm2': plt.subplot(grid[0:2, 3]),
        'vm3': plt.subplot(grid[2:4, 2]),
        'vm4': plt.subplot(grid[2:4, 3])
    }

    row1['lat'].title.set(text="75P + 75S Latency Measurements Over Increasing Time (Unicast)", fontsize=15, fontweight='bold')
    ulat = ulats[3]
    df = pd.read_csv(ulat)
    row1['lat'].plot(df["run_1_latency"], label="Run 1", color=greens[0])
    row1['lat'].plot(df["run_2_latency"], label="Run 2", color=blues[0])
    row1['lat'].plot(df["run_3_latency"], label="Run 3", color=reds[0])
    row1['lat'].set_xlim(xmin=0)
    # row1['lat'].set_ylim(ymin=0)
    row1['lat'].set_yscale('log')
    row1['lat'].legend()
    row1['lat'].set_ylabel("Latency ($\mu$s)")
    row1['lat'].set_xlabel("Measurements Over Increasing Time")
    row1['lat'].spines['top'].set_visible(False)
    row1['lat'].spines['right'].set_visible(False)

    curr_tps = [file for file in tps if "unicast_5_" in file]
    for file in curr_tps:
        df = pd.read_csv(file)
        row1['tp'].plot(df["run_1_throughput"], color=greens[0])
        row1['tp'].plot(df["run_2_throughput"], color=blues[0])
        row1['tp'].plot(df["run_3_throughput"], color=reds[0])

    lines = [
        Line2D([0], [0], color=greens[0], lw=2),
        Line2D([0], [0], color=blues[0], lw=2),
        Line2D([0], [0], color=reds[0], lw=2)
    ]
    row1['tp'].title.set(text="75P + 75S Throughput Measurements Per Increasing Second (Unicast)", fontsize=15, fontweight='bold')
    row1['tp'].legend(lines, ['Run 1', 'Run 2', 'Run 3'])
    row1['tp'].set_xlim(xmin=0, xmax=900)
    row1['tp'].set_ylim(ymin=0)
    row1['tp'].set_ylabel("Throughput (mbps)")
    row1['tp'].set_xlabel("Increasing Time (s)")
    row1['tp'].spines['top'].set_visible(False)
    row1['tp'].spines['right'].set_visible(False)

    row1['vm1'].title.set(text="Network Send/Receive Rate for VM 1 \n Over Increasing Time Per Every 2 Seconds (19P + 18S)", fontsize=15, fontweight='bold')
    vm1_logs = [file for file in ulogs if 'vm1' in file and 'unicast_5_' in file]
    for log in vm1_logs:
        df = pd.DataFrame(get_network_data(log, 'megabytes'))
        if 'run_1' in log:  
            row1['vm1'].plot(df['send_rates'], color=greens[0], ls="--")
            # row1['vm1'].scatter(df['send_rates'].index, df['send_rates'], color=greens[0], ls="--", marker="_")
            row1['vm1'].plot(df['receive_rates'], color=greens[0])
            # row1['vm1'].scatter(df['receive_rates'].index, df['receive_rates'], color=greens[0], marker="|")
        elif 'run_2' in log:
            row1['vm1'].plot(df['send_rates'], color=blues[0], ls="--")
            # row1['vm1'].scatter(df['send_rates'].index, df['send_rates'], color=blues[0], ls="--", marker="_")
            row1['vm1'].plot(df['receive_rates'], color=blues[0])
            # row1['vm1'].scatter(df['receive_rates'].index, df['receive_rates'], color=blues[0], marker="|")
        elif 'run_3' in log:
            row1['vm1'].plot(df['send_rates'], color=reds[0], ls="--")
            # row1['vm1'].scatter(df['send_rates'].index, df['send_rates'], color=reds[0], ls="--", marker="_")
            row1['vm1'].plot(df['receive_rates'], color=reds[0])
            # row1['vm1'].scatter(df['receive_rates'].index, df['receive_rates'], color=reds[0], marker="|")
    lines = [
        Line2D([0], [0], linewidth=2, color=greens[0]),
        Line2D([0], [0], linewidth=2, color=blues[0]),
        Line2D([0], [0], linewidth=2, color=reds[0]),
        Line2D([0], [0], linewidth=2, ls="--", color='orange'),
        Line2D([0], [0], linewidth=2, color='orange')
    ]
    # row1['vm1'].legend(lines, ['Run 1', 'Run 2', 'Run 3', 'Send Rate', 'Receive Rate'])
    row1['vm1'].set_xlim(xmin=0, xmax=450)
    row1['vm1'].set_ylim(ymin=0)

    row1['vm2'].title.set(text="Network Send/Receive Rate for VM 2 \n Over Increasing Time Per Every 2 Seconds (19P + 19S)", fontsize=15, fontweight='bold')
    vm2_logs = [file for file in ulogs if 'vm2' in file and 'unicast_5_' in file]
    for log in vm2_logs:
        # df = pd.DataFrame(get_network_data(log, 'megabytes'))
        df = pd.DataFrame.from_dict(get_network_data(log, 'megabytes'), orient='index')
        df = df.transpose()
        if 'run_1' in log:  
            row1['vm2'].plot(df['send_rates'], color=greens[0], ls="--")
            # row1['vm2'].scatter(df['send_rates'].index, df['send_rates'], color=greens[0], ls="--", marker="_")
            row1['vm2'].plot(df['receive_rates'], color=greens[0])
            # row1['vm2'].scatter(df['receive_rates'].index, df['receive_rates'], color=greens[0], marker="|")
        elif 'run_2' in log:
            row1['vm2'].plot(df['send_rates'], color=blues[0], ls="--")
            # row1['vm2'].scatter(df['send_rates'].index, df['send_rates'], color=blues[0], ls="--", marker="_")
            row1['vm2'].plot(df['receive_rates'], color=blues[0])
            # row1['vm2'].scatter(df['receive_rates'].index, df['receive_rates'], color=blues[0], marker="|")
        elif 'run_3' in log:
            row1['vm2'].plot(df['send_rates'], color=reds[0], ls="--")
            # row1['vm2'].scatter(df['send_rates'].index, df['send_rates'], color=reds[0], ls="--", marker="_")
            row1['vm2'].plot(df['receive_rates'], color=reds[0])
            # row1['vm2'].scatter(df['receive_rates'].index, df['receive_rates'], color=reds[0], marker="|")
    lines = [
        Line2D([0], [0], linewidth=2, color=greens[0]),
        Line2D([0], [0], linewidth=2, color=blues[0]),
        Line2D([0], [0], linewidth=2, color=reds[0]),
        Line2D([0], [0], linewidth=2, ls="--", color='orange'),
        Line2D([0], [0], linewidth=2, color='orange')
    ]
    # row1['vm2'].legend(lines, ['Run 1', 'Run 2', 'Run 3', 'Send Rate', 'Receive Rate'])
    row1['vm2'].set_xlim(xmin=0, xmax=450)
    row1['vm2'].set_ylim(ymin=0)

    row1['vm3'].title.set(text="Network Send/Receive Rate for VM 3 \n Over Increasing Time Per Every 2 Seconds (19P + 19S)", fontsize=15, fontweight='bold')
    vm3_logs = [file for file in ulogs if 'vm3' in file and 'unicast_5_' in file]
    for log in vm3_logs:
        df = pd.DataFrame(get_network_data(log, 'megabytes'))
        if 'run_1' in log:  
            row1['vm3'].plot(df['send_rates'], color=greens[0], ls="--")
            # row1['vm3'].scatter(df['send_rates'].index, df['send_rates'], color=greens[0], ls="--", marker="_")
            row1['vm3'].plot(df['receive_rates'], color=greens[0])
            # row1['vm3'].scatter(df['receive_rates'].index, df['receive_rates'], color=greens[0], marker="|")
        elif 'run_2' in log:
            row1['vm3'].plot(df['send_rates'], color=blues[0], ls="--")
            # row1['vm3'].scatter(df['send_rates'].index, df['send_rates'], color=blues[0], ls="--", marker="_")
            row1['vm3'].plot(df['receive_rates'], color=blues[0])
            # row1['vm3'].scatter(df['receive_rates'].index, df['receive_rates'], color=blues[0], marker="|")
        elif 'run_3' in log:
            row1['vm3'].plot(df['send_rates'], color=reds[0], ls="--")
            # row1['vm3'].scatter(df['send_rates'].index, df['send_rates'], color=reds[0], ls="--", marker="_")
            row1['vm3'].plot(df['receive_rates'], color=reds[0])
            # row1['vm3'].scatter(df['receive_rates'].index, df['receive_rates'], color=reds[0], marker="|")
    lines = [
        Line2D([0], [0], linewidth=2, color=greens[0]),
        Line2D([0], [0], linewidth=2, color=blues[0]),
        Line2D([0], [0], linewidth=2, color=reds[0]),
        Line2D([0], [0], linewidth=2, ls="--", color='orange'),
        Line2D([0], [0], linewidth=2, color='orange')
    ]
    # row1['vm3'].legend(lines, ['Run 1', 'Run 2', 'Run 3', 'Send Rate', 'Receive Rate'])
    row1['vm3'].set_xlim(xmin=0, xmax=450)
    row1['vm3'].set_ylim(ymin=0)

    row1['vm4'].title.set(text="Network Send/Receive Rate for VM 4 \n Over Increasing Time Per Every 2 Seconds (18P + 19S)", fontsize=15, fontweight='bold')
    vm4_logs = [file for file in ulogs if 'vm4' in file and 'unicast_5_' in file]
    for log in vm4_logs:
        df = pd.DataFrame(get_network_data(log, 'megabytes'))
        if 'run_1' in log:  
            row1['vm4'].plot(df['send_rates'], color=greens[0], ls="--")
            # row1['vm4'].scatter(df['send_rates'].index, df['send_rates'], color=greens[0], ls="--", marker="_")
            row1['vm4'].plot(df['receive_rates'], color=greens[0])
            # row1['vm4'].scatter(df['receive_rates'].index, df['receive_rates'], color=greens[0], marker="|")
        elif 'run_2' in log:
            row1['vm4'].plot(df['send_rates'], color=blues[0], ls="--")
            # row1['vm4'].scatter(df['send_rates'].index, df['send_rates'], color=blues[0], ls="--", marker="_")
            row1['vm4'].plot(df['receive_rates'], color=blues[0])
            # row1['vm4'].scatter(df['receive_rates'].index, df['receive_rates'], color=blues[0], marker="|")
        elif 'run_3' in log:
            row1['vm4'].plot(df['send_rates'], color=reds[0], ls="--")
            # row1['vm4'].scatter(df['send_rates'].index, df['send_rates'], color=reds[0], ls="--", marker="_")
            row1['vm4'].plot(df['receive_rates'], color=reds[0])
            # row1['vm4'].scatter(df['receive_rates'].index, df['receive_rates'], color=reds[0], marker="|")
    # row1['vm4'].legend(lines, ['Run 1', 'Run 2', 'Run 3', 'Send Rate', 'Receive Rate'])
    row1['vm4'].set_xlim(xmin=0, xmax=450)
    row1['vm4'].set_ylim(ymin=0)

    # lines = [
    #     Line2D([0], [0], linewidth=2, color=greens[0]),
    #     Line2D([0], [0], linewidth=2, color=blues[0]),
    #     Line2D([0], [0], linewidth=2, color=reds[0]),
    #     Line2D([0], [0], linewidth=0, marker="_", color='black'),
    #     Line2D([0], [0], linewidth=0, marker="|", color='black')
    # ]
    for row in row1:
        if 'vm' in row:
            row1[str(row)].set_xlabel("Increasing Time In 2s Increments(s)")
            row1[str(row)].set_ylabel("Send/Receive Rate (MBps)")
            row1[str(row)].legend(lines, ['Run 1', 'Run 2', 'Run 3', 'Send Rate', 'Receive Rate'])

    plt.tight_layout(pad=3)

def lat_tp_vs_net_per_vm_75p75s_multicast():
    lats = [file for file in get_files("data/set_2") if ('network_log_rerun' in file or '_5_75' in file) and 'average_latencies' in file]
    ulats = [file for file in lats if 'unicast' in file]
    mlats = [file for file in lats if 'multicast' in file]
    mlats.sort()
    mlats = mlats[1:] + mlats[:1]

    tps = [file for file in get_files("data/set_2") if 'average_throughput' in file and ('network_log_rerun' in file or '_5_75' in file)]
    tps.sort()

    logs = [file for file in get_files("data/set_2") if 'network_usage.log' in file and 'network' in file]
    logs.sort()
    ulogs = [file for file in logs if 'unicast' in file]
    mlogs = [file for file in logs if 'multicast' in file]
    mlogs = mlogs[12:] + mlogs[:12]

    fig = plt.figure(figsize=(30, 15))
    grid = plt.GridSpec(4, 4, figure=fig)

    row1 = {
        'lat': plt.subplot(grid[0:2, 0:2]),
        'tp': plt.subplot(grid[2:4, 0:2]),
        'vm1': plt.subplot(grid[0:2, 2]),
        'vm2': plt.subplot(grid[0:2, 3]),
        'vm3': plt.subplot(grid[2:4, 2]),
        'vm4': plt.subplot(grid[2:4, 3])
    }

    row1['lat'].title.set(text="75P + 75S Latency Measurements Over Increasing Time (Multicast)", fontsize=15, fontweight='bold')
    mlat = mlats[3]
    df = pd.read_csv(mlat)
    row1['lat'].plot(df["run_1_latency"], label="Run 1", color=greens[0])
    row1['lat'].plot(df["run_2_latency"], label="Run 2", color=blues[0])
    row1['lat'].plot(df["run_3_latency"], label="Run 3", color=reds[0])
    row1['lat'].set_xlim(xmin=0)
    # row1['lat'].set_ylim(ymin=0)
    row1['lat'].set_yscale('log')
    row1['lat'].legend()
    row1['lat'].set_ylabel("Latency ($\mu$s)")
    row1['lat'].set_xlabel("Measurements Over Increasing Time")
    row1['lat'].spines['top'].set_visible(False)
    row1['lat'].spines['right'].set_visible(False)

    curr_tps = [file for file in tps if "multicast_5_" in file]
    for file in curr_tps:
        df = pd.read_csv(file)
        row1['tp'].plot(df["run_1_throughput"], color=greens[0])
        row1['tp'].plot(df["run_2_throughput"], color=blues[0])
        row1['tp'].plot(df["run_3_throughput"], color=reds[0])

    lines = [
        Line2D([0], [0], color=greens[0], lw=2),
        Line2D([0], [0], color=blues[0], lw=2),
        Line2D([0], [0], color=reds[0], lw=2)
    ]
    row1['tp'].title.set(text="75P + 75S Throughput Measurements Per Increasing Second (Multicast)", fontsize=15, fontweight='bold')
    row1['tp'].legend(lines, ['Run 1', 'Run 2', 'Run 3'])
    row1['tp'].set_xlim(xmin=0, xmax=900)
    row1['tp'].set_ylim(ymin=0)
    row1['tp'].set_ylabel("Throughput (mbps)")
    row1['tp'].set_xlabel("Increasing Time (s)")
    row1['tp'].spines['top'].set_visible(False)
    row1['tp'].spines['right'].set_visible(False)

    row1['vm1'].title.set(text="Network Send/Receive Rate for VM 1 \n Over Increasing Time Per Every 2 Seconds (19P + 18S)", fontsize=15, fontweight='bold')
    vm1_logs = [file for file in mlogs if 'vm1' in file and 'multicast_5_' in file]
    for log in vm1_logs:
        df = pd.DataFrame(get_network_data(log, 'megabytes'))
        if 'run_1' in log:  
            row1['vm1'].plot(df['send_rates'], color=greens[0], ls="--")
            # row1['vm1'].scatter(df['send_rates'].index, df['send_rates'], color=greens[0], ls="--", marker="_")
            row1['vm1'].plot(df['receive_rates'], color=greens[0])
            # row1['vm1'].scatter(df['receive_rates'].index, df['receive_rates'], color=greens[0], marker="|")
        elif 'run_2' in log:
            row1['vm1'].plot(df['send_rates'], color=blues[0], ls="--")
            # row1['vm1'].scatter(df['send_rates'].index, df['send_rates'], color=blues[0], ls="--", marker="_")
            row1['vm1'].plot(df['receive_rates'], color=blues[0])
            # row1['vm1'].scatter(df['receive_rates'].index, df['receive_rates'], color=blues[0], marker="|")
        elif 'run_3' in log:
            row1['vm1'].plot(df['send_rates'], color=reds[0], ls="--")
            # row1['vm1'].scatter(df['send_rates'].index, df['send_rates'], color=reds[0], ls="--", marker="_")
            row1['vm1'].plot(df['receive_rates'], color=reds[0])
            # row1['vm1'].scatter(df['receive_rates'].index, df['receive_rates'], color=reds[0], marker="|")
    lines = [
        Line2D([0], [0], linewidth=2, color=greens[0]),
        Line2D([0], [0], linewidth=2, color=blues[0]),
        Line2D([0], [0], linewidth=2, color=reds[0]),
        Line2D([0], [0], linewidth=2, ls="--", color='orange'),
        Line2D([0], [0], linewidth=2, color='orange')
    ]
    # row1['vm1'].legend(lines, ['Run 1', 'Run 2', 'Run 3', 'Send Rate', 'Receive Rate'])
    row1['vm1'].set_xlim(xmin=0, xmax=450)
    row1['vm1'].set_ylim(ymin=0)

    row1['vm2'].title.set(text="Network Send/Receive Rate for VM 2 \n Over Increasing Time Per Every 2 Seconds (19P + 19S)", fontsize=15, fontweight='bold')
    vm2_logs = [file for file in mlogs if 'vm2' in file and 'multicast_5_' in file]
    for log in vm2_logs:
        # df = pd.DataFrame(get_network_data(log, 'megabytes'))
        df = pd.DataFrame.from_dict(get_network_data(log, 'megabytes'), orient='index')
        df = df.transpose()
        if 'run_1' in log:  
            row1['vm2'].plot(df['send_rates'], color=greens[0], ls="--")
            # row1['vm2'].scatter(df['send_rates'].index, df['send_rates'], color=greens[0], ls="--", marker="_")
            row1['vm2'].plot(df['receive_rates'], color=greens[0])
            # row1['vm2'].scatter(df['receive_rates'].index, df['receive_rates'], color=greens[0], marker="|")
        elif 'run_2' in log:
            row1['vm2'].plot(df['send_rates'], color=blues[0], ls="--")
            # row1['vm2'].scatter(df['send_rates'].index, df['send_rates'], color=blues[0], ls="--", marker="_")
            row1['vm2'].plot(df['receive_rates'], color=blues[0])
            # row1['vm2'].scatter(df['receive_rates'].index, df['receive_rates'], color=blues[0], marker="|")
        elif 'run_3' in log:
            row1['vm2'].plot(df['send_rates'], color=reds[0], ls="--")
            # row1['vm2'].scatter(df['send_rates'].index, df['send_rates'], color=reds[0], ls="--", marker="_")
            row1['vm2'].plot(df['receive_rates'], color=reds[0])
            # row1['vm2'].scatter(df['receive_rates'].index, df['receive_rates'], color=reds[0], marker="|")
    lines = [
        Line2D([0], [0], linewidth=2, color=greens[0]),
        Line2D([0], [0], linewidth=2, color=blues[0]),
        Line2D([0], [0], linewidth=2, color=reds[0]),
        Line2D([0], [0], linewidth=2, ls="--", color='orange'),
        Line2D([0], [0], linewidth=2, color='orange')
    ]
    # row1['vm2'].legend(lines, ['Run 1', 'Run 2', 'Run 3', 'Send Rate', 'Receive Rate'])
    row1['vm2'].set_xlim(xmin=0, xmax=450)
    row1['vm2'].set_ylim(ymin=0)

    row1['vm3'].title.set(text="Network Send/Receive Rate for VM 3 \n Over Increasing Time Per Every 2 Seconds (19P + 19S)", fontsize=15, fontweight='bold')
    vm3_logs = [file for file in mlogs if 'vm3' in file and 'multicast_5_' in file]
    for log in vm3_logs:
        df = pd.DataFrame(get_network_data(log, 'megabytes'))
        if 'run_1' in log:  
            row1['vm3'].plot(df['send_rates'], color=greens[0], ls="--")
            # row1['vm3'].scatter(df['send_rates'].index, df['send_rates'], color=greens[0], ls="--", marker="_")
            row1['vm3'].plot(df['receive_rates'], color=greens[0])
            # row1['vm3'].scatter(df['receive_rates'].index, df['receive_rates'], color=greens[0], marker="|")
        elif 'run_2' in log:
            row1['vm3'].plot(df['send_rates'], color=blues[0], ls="--")
            # row1['vm3'].scatter(df['send_rates'].index, df['send_rates'], color=blues[0], ls="--", marker="_")
            row1['vm3'].plot(df['receive_rates'], color=blues[0])
            # row1['vm3'].scatter(df['receive_rates'].index, df['receive_rates'], color=blues[0], marker="|")
        elif 'run_3' in log:
            row1['vm3'].plot(df['send_rates'], color=reds[0], ls="--")
            # row1['vm3'].scatter(df['send_rates'].index, df['send_rates'], color=reds[0], ls="--", marker="_")
            row1['vm3'].plot(df['receive_rates'], color=reds[0])
            # row1['vm3'].scatter(df['receive_rates'].index, df['receive_rates'], color=reds[0], marker="|")
    lines = [
        Line2D([0], [0], linewidth=2, color=greens[0]),
        Line2D([0], [0], linewidth=2, color=blues[0]),
        Line2D([0], [0], linewidth=2, color=reds[0]),
        Line2D([0], [0], linewidth=2, ls="--", color='orange'),
        Line2D([0], [0], linewidth=2, color='orange')
    ]
    # row1['vm3'].legend(lines, ['Run 1', 'Run 2', 'Run 3', 'Send Rate', 'Receive Rate'])
    row1['vm3'].set_xlim(xmin=0, xmax=450)
    row1['vm3'].set_ylim(ymin=0)

    row1['vm4'].title.set(text="Network Send/Receive Rate for VM 4 \n Over Increasing Time Per Every 2 Seconds (18P + 19S)", fontsize=15, fontweight='bold')
    vm4_logs = [file for file in mlogs if 'vm4' in file and 'multicast_5_' in file]
    for log in vm4_logs:
        # df = pd.DataFrame(get_network_data(log, 'megabytes'))
        df = pd.DataFrame.from_dict(get_network_data(log, 'megabytes'), orient='index')
        df = df.transpose()
        if 'run_1' in log:  
            row1['vm4'].plot(df['send_rates'], color=greens[0], ls="--")
            # row1['vm4'].scatter(df['send_rates'].index, df['send_rates'], color=greens[0], ls="--", marker="_")
            row1['vm4'].plot(df['receive_rates'], color=greens[0])
            # row1['vm4'].scatter(df['receive_rates'].index, df['receive_rates'], color=greens[0], marker="|")
        elif 'run_2' in log:
            row1['vm4'].plot(df['send_rates'], color=blues[0], ls="--")
            # row1['vm4'].scatter(df['send_rates'].index, df['send_rates'], color=blues[0], ls="--", marker="_")
            row1['vm4'].plot(df['receive_rates'], color=blues[0])
            # row1['vm4'].scatter(df['receive_rates'].index, df['receive_rates'], color=blues[0], marker="|")
        elif 'run_3' in log:
            row1['vm4'].plot(df['send_rates'], color=reds[0], ls="--")
            # row1['vm4'].scatter(df['send_rates'].index, df['send_rates'], color=reds[0], ls="--", marker="_")
            row1['vm4'].plot(df['receive_rates'], color=reds[0])
            # row1['vm4'].scatter(df['receive_rates'].index, df['receive_rates'], color=reds[0], marker="|")
    # row1['vm4'].legend(lines, ['Run 1', 'Run 2', 'Run 3', 'Send Rate', 'Receive Rate'])
    row1['vm4'].set_xlim(xmin=0, xmax=450)
    row1['vm4'].set_ylim(ymin=0)

    # lines = [
    #     Line2D([0], [0], linewidth=2, color=greens[0]),
    #     Line2D([0], [0], linewidth=2, color=blues[0]),
    #     Line2D([0], [0], linewidth=2, color=reds[0]),
    #     Line2D([0], [0], linewidth=0, marker="_", color='black'),
    #     Line2D([0], [0], linewidth=0, marker="|", color='black')
    # ]
    for row in row1:
        if 'vm' in row:
            row1[str(row)].set_xlabel("Increasing Time In 2s Increments(s)")
            row1[str(row)].set_ylabel("Send/Receive Rate (MBps)")
            row1[str(row)].legend(lines, ['Run 1', 'Run 2', 'Run 3', 'Send Rate', 'Receive Rate'])

    plt.tight_layout(pad=3)

def s2_plot_summary_table(ax, ucast, mcast):
    # Get unicast latency files
    testname = ["", "", "", get_test_names([ucast])[0].replace("Unicast ", ""), "", "", ""]
    headings = ["", "", "Unicast", "", "", "Multicast", ""]
    runs = ["Runs", 1, 2, 3, 1, 2, 3]
    metric_count = ["No. of Measurements".title()]
    averages = ["averages".title()]
    stds = ["stds".title()]
    variances = ["variances".title()]
    mins = ["mins".title()]
    maxs = ["maxs".title()]
    lower_quartiles = ["lower_quartiles".title().replace("_", " ")]
    mid_quartiles = ["mid_quartiles".title().replace("_", " ")]
    upper_quartiles = ["upper_quartiles".title().replace("_", " ")]

    df = pd.read_csv(ucast)
    for col in df.columns[1:4]:
        metric_count.append(format_number(df[col].count()))
        averages.append(format_number(df[col].mean()))
        stds.append(format_number(df[col].std()))
        variances.append(format_number(df[col].var()))
        mins.append(format_number(df[col].min()))
        maxs.append(format_number(df[col].max()))
        lower_quartiles.append(format_number(df[col].quantile(.25)))
        mid_quartiles.append(format_number(df[col].quantile(.5)))
        upper_quartiles.append(format_number(df[col].quantile(.75)))

    df = pd.read_csv(mcast)
    for col in df.columns[1:4]:
        metric_count.append(format_number(df[col].count()))
        averages.append(format_number(df[col].mean()))
        stds.append(format_number(df[col].std()))
        variances.append(format_number(df[col].var()))
        mins.append(format_number(df[col].min()))
        maxs.append(format_number(df[col].max()))
        lower_quartiles.append(format_number(df[col].quantile(.25)))
        mid_quartiles.append(format_number(df[col].quantile(.5)))
        upper_quartiles.append(format_number(df[col].quantile(.75)))

    rows = [headings, runs, metric_count, averages, stds, variances, mins, maxs, lower_quartiles, mid_quartiles, upper_quartiles]

    # Get summary data for unicast per run
    
    table = plot_table(ax, testname, rows)
    table.auto_set_font_size(False)
    table.set_fontsize(4)
    for key, cell in table.get_celld().items():
        cell.set_linewidth(0)

def s2_plot_latency_summary_tables():
    ucast = [file for file in get_files('data/set_2') if 'average_latencies' in file and 'forced_transport' in file and 'unicast' in file]
    mcast = [file for file in get_files('data/set_2') if 'average_latencies' in file and 'forced_transport' in file and 'multicast' in file]
    ucast.sort()
    mcast.sort()
    mcast = mcast[1:] + mcast[:1]

    for i in range(0, len(ucast)):
        plot_lat_summary_table([ucast[i]])
        plot_lat_summary_table([mcast[i]])

def s2_24hr15m_cdf_comparison():
    avg_lat_24hr = [file for file in get_files("data/set_2") if '24_hours' in file and 'average_latencies' in file]
    avg_lat_15min = [file for file in get_files("data/set_2") if ('2_9_' in file or '2_10_' in file) and 'average_latencies' in file]

    fig = plt.figure(figsize=(30, 10))
    grid = plt.GridSpec(1, 2, figure=fig)

    left = plt.subplot(grid[0])
    right = plt.subplot(grid[1])

    fig.suptitle("Set 2 24-Hour vs 15-Minute Run Latency CDF Comparison", fontsize=15, fontweight="bold")
    left.set_title(label="15-Minute Run CDFs Per Run", fontsize=15, fontweight='bold')
    right.set_title(label="24-Hour Run CDFs Per Run", fontsize=15, fontweight='bold')

    for file in avg_lat_15min:
        df = pd.read_csv(file)
        color = greens[0] if 'unicast' in file else reds[0]
        title = "Unicast Average" if 'unicast' in file else "Multicast Average"
        try:
            plot_cdf("", df["run_1_latency"], left, color, "normal")
        except:
            print(df.head())
        plot_cdf("", df["run_2_latency"], left, color, "normal")
        plot_cdf("", df["run_3_latency"], left, color, "normal")
        try:
            plot_cdf(title, pd.concat([df["run_1_latency"], df["run_2_latency"], df["run_3_latency"]]), left, color, "average")
        except:
            print(df.head())

    for file in avg_lat_24hr:
        df = pd.read_csv(file)
        color = greens[0] if 'unicast' in file else reds[0]
        title = "Unicast Average" if 'unicast' in file else "Multicast Average"
        try:
            plot_cdf("", df["run_1_latency"], right, color, "normal")
        except:
            None
        plot_cdf("", df["run_2_latency"], right, color, "normal")
        plot_cdf("", df["run_3_latency"], right, color, "normal")
        try:
            plot_cdf(title, pd.concat([df["run_1_latency"], df["run_2_latency"], df["run_3_latency"]]), right, color, "average")
        except:
            plot_cdf(title, pd.concat([df["run_2_latency"], df["run_3_latency"]]), right, color, "average")

    left.set_ylim(ymin=0, ymax=1)
    right.set_ylim(ymin=0, ymax=1)

    left.set_xlim(xmin=0, xmax=500000)
    right.set_xlim(xmin=0, xmax=500000)

    left.set_xlabel("Latency ($\mu$s)", fontsize=12, fontweight="bold")
    right.set_xlabel("Latency ($\mu$s)", fontsize=12, fontweight="bold")

    left.grid()
    right.grid()

    left.legend()
    right.legend()

    plt.tight_layout(pad=2)

def s2_24hr15m_cdf_comparison_single_plot():
    avg_lat_24hr = [file for file in get_files("data/set_2") if '24_hours' in file and 'average_latencies' in file][0]
    avg_lat_15min = [file for file in get_files("data/set_2") if '2_9_' in file and 'average_latencies' in file][0]

    fig = plt.figure(figsize=(30, 10))
    grid = plt.GridSpec(1, 2, figure=fig)

    left = plt.subplot(grid[0])
    right = plt.subplot(grid[1])

    fig.suptitle("Set 2 24-Hour vs 15-Minute Average vs Run Latency CDF Comparison (Unicast)", fontsize=15, fontweight="bold")
    left.set_title(label="CDFs Of Averages of 15-Minute vs 24-Hour Runs", fontsize=15, fontweight='bold')
    right.set_title(label="CDFs Of All 6 Runs", fontsize=15, fontweight='bold')

    df_15 = pd.read_csv(avg_lat_15min)
    df_24 = pd.read_csv(avg_lat_24hr)

    plot_cdf("15-Minute Run Average", pd.concat([df_15["run_1_latency"], df_15["run_2_latency"], df_15["run_3_latency"]]), left, greens[0], "average")
    plot_cdf("24-Hour Run Average", pd.concat([df_24["run_1_latency"], df_24["run_2_latency"], df_24["run_3_latency"]]), left, reds[0], "average")

    plot_cdf("15-Minute Test", df_15["run_1_latency"], right, greens[0], "normal")
    plot_cdf("", df_15["run_2_latency"], right, greens[0], "normal")
    plot_cdf("", df_15["run_3_latency"], right, greens[0], "normal")
    plot_cdf("24-Hour Test", df_24["run_1_latency"], right, reds[0], "normal")
    plot_cdf("", df_24["run_2_latency"], right, reds[0], "normal")
    plot_cdf("", df_24["run_3_latency"], right, reds[0], "normal")

    left.set_ylim(ymin=0, ymax=1)
    right.set_ylim(ymin=0, ymax=1)

    left.set_xlim(xmin=0, xmax=500000)
    right.set_xlim(xmin=0, xmax=500000)

    left.set_xlabel("Latency ($\mu$s)", fontsize=12, fontweight="bold")
    right.set_xlabel("Latency ($\mu$s)", fontsize=12, fontweight="bold")

    left.grid()
    right.grid()

    left.legend()
    right.legend()

    plt.tight_layout(pad=2)

def get_percent_diff(current, previous):
    return ((float(current) - previous) / previous) * 100

def plot_mini_cdf(ax, title, ddos_size, normal_files, ddos_files):
    ax.set_title(label=title, fontsize=12, fontweight="bold")
    for file in ddos_files[ddos_size]:
        df = pd.read_csv(file)
        if 'run_1_latency' in df and 'run_2_latency' in df and 'run_3_latency' in df:
            combined_df = pd.concat([ df["run_1_latency"], df["run_2_latency"], df["run_3_latency"] ])
        else:
            combined_df = df['avg_run_latency']
        if 'unicast' in file:
            # plot_cdf('', df["run_1_latency"], ax, greens[0], 'normal')
            # plot_cdf('', df["run_2_latency"], ax, greens[0], 'normal')
            # plot_cdf('', df["run_3_latency"], ax, greens[0], 'normal')
            plot_cdf(ddos_size.upper() + " DDOS Unicast DDS Latency", combined_df, ax, greens[0], 'average')
            ax.text(50000, (combined_df.mean() / 200000), "Avg.: " + format_number(combined_df.mean()) + "$\mu$s", color=greens[0], backgroundcolor='white', fontweight='bold', fontsize=10)
            ax.annotate('', (60000, (combined_df.mean() / 200000)), (60000, 25934/200000), arrowprops={"arrowstyle": "->", "color": greens[0]})
            ax.text(40000, 0.2, "+" + format_number(get_percent_diff(combined_df.mean(), 25934)) + "%", fontweight='bold', color=greens[0])
        else:
            # plot_cdf('', df["run_1_latency"], ax, reds[0], 'normal')
            # plot_cdf('', df["run_2_latency"], ax, reds[0], 'normal')
            # plot_cdf('', df["run_3_latency"], ax, reds[0], 'normal')
            plot_cdf(ddos_size.upper() + " DDOS Multicast DDS Latency", combined_df, ax, reds[0], 'average')
            ax.text(90000, (combined_df.mean() / 200000), "Avg.: " + format_number(combined_df.mean()) + "$\mu$s", color=reds[0], backgroundcolor='white', fontweight='bold', fontsize=10)
            ax.annotate('', (100000, (combined_df.mean() / 200000)), (100000, 29149/200000), arrowprops={"arrowstyle": "->", "color": reds[0]})
            ax.text(80000, 0.2, "+" + format_number(get_percent_diff(combined_df.mean(), 29149)) + "%", fontweight='bold', color=reds[0])

    for file in normal_files:
        df = pd.read_csv(file)
        combined_df = pd.concat([ df["run_1_latency"], df["run_2_latency"], df["run_3_latency"] ])
        if 'unicast' in file:
            plot_cdf('Normal Unicast DDS Latency', combined_df, ax, blues[0], 'average')
            ax.text(50000, (combined_df.mean() / 200000), "Avg.: " + format_number(combined_df.mean()) + "$\mu$s", color=blues[0], backgroundcolor='white', fontweight='bold', fontsize=10)
        else:
            plot_cdf('Normal Multicast DDS Latency', combined_df, ax, oranges[0], 'average')
            ax.text(90000, (combined_df.mean() / 200000), "Avg.: " + format_number(combined_df.mean()) + "$\mu$s", color=oranges[0], backgroundcolor='white', fontweight='bold', fontsize=10)

def s3_plot_ddos_latency_cdf_comparison():
    """
    Get data for normal test (non-attack)
    """
    normal_files = [file for file in get_files("data/set_2") if 'average_latencies' in file and 'forced_transport' in file and ('unicast_2_' in file or 'multicast_2_' in file)]

    """
    Get data for ddos test
    """
    all_ddos_files = [file for file in get_files("data/set_3") if 'average_latencies' in file and ('unicast_2_' in file or 'multicast_2_' in file)]
    ddos_files = {
        "1mb": [file for file in all_ddos_files if '1024_kilobyte' in file],
        "512kb": [file for file in all_ddos_files if '512_kilobyte' in file],
        "128kb": [file for file in all_ddos_files if '128_kilobyte' in file],
        "64kb": [file for file in all_ddos_files if '64_kilobyte' in file],
        "16kb": [file for file in all_ddos_files if '16_kilobyte' in file]
    }

    fig = plt.figure(figsize=(30, 15))
    fig.suptitle("DDOS Latency CDF Comparison", fontsize=15, fontweight='bold')
    grid = plt.GridSpec(3, 3, figure=fig)

    combined = plt.subplot(grid[0:2,0:2])
    bot_left = plt.subplot(grid[2, 0])
    bot_mid = plt.subplot(grid[2, 1])
    top_right = plt.subplot(grid[0, 2])
    top_mid = plt.subplot(grid[1, 2])
    bot_right = plt.subplot(grid[2, 2])

    all = [combined, bot_left, bot_right, bot_mid, top_right, top_mid]

    """
    Plot combined latency graph
    """
    combined.set_title(label="Latency CDFs Combined", fontsize=12, fontweight='bold')
    combined.set_xlim(xmin=0, xmax=200000)
    for type in ddos_files:
        for file in ddos_files[type]:
            df = pd.read_csv(file)
            if '16_kilobyte' in file:
                title = "DDOS Latency"
            else:
                title = ""

            if 'unicast' in file:
                title = title + " Unicast" if len(title) > 0 else ""
                plot_cdf(title, pd.concat([ df["run_1_latency"], df["run_2_latency"], df["run_3_latency"] ]), combined, greens[0], 'average')
            else:
                title = title + " Multicast" if len(title) > 0 else ""
                plot_cdf(title, pd.concat([ df["run_1_latency"], df["run_2_latency"], df["run_3_latency"] ]), combined, reds[0], 'average')
    for file in normal_files:
        df = pd.read_csv(file)
        if 'unicast' in file:
            plot_cdf('Normal Unicast Latency', pd.concat([ df["run_1_latency"], df["run_2_latency"], df["run_3_latency"] ]), combined, blues[0], 'average')
        else:
            plot_cdf('Normal Multicast Latency', pd.concat([ df["run_1_latency"], df["run_2_latency"], df["run_3_latency"] ]), combined, oranges[0], 'average')

    plot_mini_cdf(bot_left, "16KB DDOS Latency CDFs Per Run", '16kb', normal_files, ddos_files)
    plot_mini_cdf(bot_mid, "64KB DDOS Latency CDFs Per Run", '64kb', normal_files, ddos_files)
    plot_mini_cdf(bot_right, "128KB DDOS Latency CDFs Per Run", '128kb', normal_files, ddos_files)
    plot_mini_cdf(top_mid, "512KB DDOS Latency CDFs Per Run", '512kb', normal_files, ddos_files)
    plot_mini_cdf(top_right, "1MB DDOS Latency CDFs Per Run", '1mb', normal_files, ddos_files)

    for ax in all:
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.set_ylim(ymin=0, ymax=1)
        ax.grid()
        ax.legend()
        ax.set_xlabel("Latency ($\mu$s)")
        ax.set_xlim(xmin=0, xmax=175000)

    plt.tight_layout()

def get_run_count(test):
  """
    Calculates how many runs were completed for a test by reading the metadata file.
  
    Parameters:
      test (string): Filepath of test.
  
    Returns:
      run_count (int): Number of runs that the test completed.
  """
  metadata_file_list = [f for f in get_files(os.path.dirname(os.path.dirname(test))) if 'metadata' in f and os.path.dirname(test) in f]
  if metadata_file_list == 0:
    print("No metadata files found for " + test, style="bold red")
  else:
    metadata_file = metadata_file_list[0]
    with open(metadata_file, 'r') as f:
      content = f.readlines()
      restart_lines = [line for line in content if 'Restart' in line]
      restart_counts = {
        "vm1": 0,
        "vm2": 0,
        "vm3": 0,
        "vm4": 0
      }
      for line in restart_lines:
        if "10.200.51.21" in line:
            restart_counts["vm1"] = restart_counts["vm1"] + 1
        elif "10.200.51.22" in line:
            restart_counts["vm2"] = restart_counts["vm2"] + 1
        elif "10.200.51.23" in line:
            restart_counts["vm3"] = restart_counts["vm3"] + 1
        elif "10.200.51.24" in line:
            restart_counts["vm4"] = restart_counts["vm4"] + 1

      return (restart_counts[max(restart_counts, key=restart_counts.get)])
  
