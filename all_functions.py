from pydoc import describe
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
                send_rate = [word for word in split_line if len(word) > 0][3]
                data['send_rates'].append(send_rate)
            elif 'Total receive rate' in line:
                split_line = line.split(" ")
                receive_rate = [word for word in split_line if len(word) > 0][3]
                data['receive_rates'].append(receive_rate)

    if format is not None:
        data['send_rates'] = parse_data_lens(data['send_rates'], format)
        data['receive_rates'] = parse_data_lens(data['receive_rates'], format)
    else:
        data['send_rates'] = parse_data_lens(data['send_rates'], None)
        data['receive_rates'] = parse_data_lens(data['receive_rates'], None)
    
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