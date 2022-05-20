from rich.jupyter import print
from rich.markdown import Markdown
from rich.progress import track
from rich.table import Table

import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import plotly.graph_objects as go
import re
import codecs
import csv
import sys

from rich.console import Console
console = Console()

#
# List data
#
"""
    For each item in folder
        If folder
            Repeat this function
        If csv file
            Store the filepath
"""
def get_files(dir_path):
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

def is_number(str):
    try:
        float(str)
    except:
        return(False)
    else:
        return(True)

def delete_clean_files(files):
    for file in files:
        # Delete all files with clean_ at the start
        if "clean_" in file:
            os.remove(file)

def clean_data(files):
    for n in track(range(len(files)), description="Cleaning " +str(len(files))+ " Files", style="bold green"):
        file = files[n]

        # Check for NUL byte in csv:
        if '\0' in open(file).read():
            # print("NUL bytes found in \n" +file+ " \n")
            csvreader = csv.reader(x.replace('\0', '') for x in open(file))

        else:
            csvreader = csv.reader(codecs.open(file, 'rU', 'utf-8'))

        new_output = []
        # Remove all empty cells
        for row in csvreader:
            new_row = []
            for cell in row:
                if cell != "":
                    new_row.append(cell.strip())
            new_output.append(new_row)

        # Remove any rows with text in it
        for row in new_output:
            if re.search("[a-zA-Z]", str(row)):
                new_output.remove(row)

        # new_output has all data with empty cells removed

        clean_numeric_output = []
        clean_string_output = []
        # Parse any strings into integers
        for row in new_output:
            new_numeric_row = []
            new_string_row = []
            for cell in row:
                if is_number(cell):
                    new_numeric_row.append(float(cell))
                else:
                    new_string_row.append(cell)
            if new_numeric_row:
                clean_numeric_output.append(new_numeric_row)
            if new_string_row:
                clean_string_output.append(new_string_row)
        
        # open_file.close()

        # Remove last row because its the summary
        clean_numeric_output = clean_numeric_output[:-1]

        # clean_numeric_output has all numeric data in it
        # clean_string_output has all string data in it

        
        # Add custom headers depending on if file is pub or sub
        if "pub" in file:
            headers = ["Length", "Latency", "Average Latency", "Standard Deviation", "Minimum Latency", "Maximum Latency"]
        elif "sub" in file:
            headers = ["Length", "Total Samples", "Samples Per Second", "Average Samples Per Second", "Throughput", "Average Throughput", "Lost Samples", "Lost Samples Percentage"]
        elif "average" in file:
            continue
        else:
            console.print("Error: Couldn't find 'pub' or 'sub' in this file: " + str(file), style="bold red")
            continue
        
        clean_output = [headers, clean_numeric_output]

        #
        # Create new file
        #
        new_file_name = "clean_" + os.path.basename(file)
        old_folder_path = os.path.dirname(file)
        new_file_path = os.path.join(old_folder_path, new_file_name)

        # Delete any files with same name
        if os.path.exists(new_file_path):
            os.remove(new_file_path)
        else:
            with open(new_file_path, 'w', encoding='UTF8', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(headers)
                writer.writerows(clean_numeric_output)


def verify_files(files):
    for file in [file for file in files if "clean_" in file]:
        if '\0' in open(file).read():
            # print("NUL bytes found in \n" +file+ " \n")
            csvreader = csv.reader(x.replace('\0', '') for x in open(file))
        else:
            csvreader = csv.reader(codecs.open(file, 'rU', 'utf-8'))

        for row in csvreader:
            if csvreader.line_num > 1 and re.search("[a-zA-Z]", str(row)):
                console.print("No numeric value found on row " + str(csvreader.line_num) + " in file: \n" + str(file) + ":\n" + str(row) + "\n\n", style="red")


def get_test_folders(root_dir):
    """
        Gets the list of test folders containing multiple runs.

        Parameters:
            root_dir (string): root directory of all folders and subfolders

        Returns:
            test_folders (list): list of all test folders

    """
    test_folders = []
    for file in get_files(root_dir):
        test_folders.append(file.split("run_")[0][0:-1])
    test_folders = list(set(test_folders))
    test_folders.sort()
    test_folders = list(filter(lambda f: '.' not in f, test_folders))

    return test_folders

def delete_old_run_averages(file_path):
    for file in get_files(file_path):
        if 'average' in file:
            os.remove(file)

def clean_files_exist(files):
    return len([file for file in files if 'clean_' in file]) > 0

def average_files_exist(file_path):
    return len([file for file in get_files(file_path) if 'average' in file]) > 0

def create_run_averages(file_path):
    """
        Reads data from multiple run files, creates an average of each row and concatenates everything (including the data from each run) into a single .csv file. 
        Resulting .csv file example:
        
            run_1_latency   run_2_latency   run_3_latency   avg_run_latency
        0   120             120             120             120
        1   100             200             150             150

    """

    # Get test folders
    test_folders = get_test_folders(file_path)

    for n in track(range(len(test_folders)), description="Averaging Measurements"):
    # for test in test_folders:
        test = test_folders[n]
        try:
            test_files = get_files(test)
        except:
            continue

    # with console.status("Creating average run latencies for [green]%s[/green]" %test):
        latency_files = [file for file in test_files if 'clean_' in file and 'pub_0' in file]
        if len(latency_files) > 0:
            data = {}
            for file in latency_files:
                col_title = os.path.basename(os.path.dirname(file))
                if 'mal' in file:
                    col_title = col_title + "_mal_latency"
                else:
                    col_title = col_title + "_latency"
                series = pd.read_csv(file)["Latency"]
                column = {col_title : series}
                data.update(column)        

            df = pd.DataFrame(data=data)
            non_mal_cols = [col for col in df.columns if 'mal' not in col]
            mal_cols = [col for col in df.columns if 'mal' in col]
            df['avg_non_mal_run_latency'] = df[non_mal_cols].mean(numeric_only=True, axis=1)
            df['avg_mal_run_latency'] = df[mal_cols].mean(numeric_only=True, axis=1)
            df['avg_run_latency'] = df.mean(numeric_only=True, axis=1)

            # Create new .csv file in test_folder:
            df.to_csv(os.path.join(test, 'average_latencies.csv'))
        # else:
            # console.print("No latency files found for %s" % test, style="red")

    # with console.status("Creating new average run throughputs..."):
        throughput_files = [file for file in test_files if 'clean' in file and 'sub' in file]
        if len(throughput_files) > 0:
            sub_files = []
            for file in throughput_files:
                sub_files.append(os.path.basename(file))
            sub_files = list(set(sub_files))
            sub_files.sort()
            
            for file in sub_files:
                data = {}
                for tp_file in throughput_files:
                    if file in tp_file:
                        series = pd.read_csv(tp_file)["Throughput"]
                        column = {os.path.basename(os.path.dirname(tp_file)) + "_throughput" : series}
                        data.update(column)
                
                df = pd.DataFrame(data=data)
                df['avg_run_throughput'] = df.mean(numeric_only=True, axis=1)
                if 'mal' in file:
                    filename = os.path.join(test, file.split("clean_")[1].replace(".csv", "").replace("output_", "") + "_average_throughputs.csv")
                else:
                    filename = os.path.join(test, file.split("clean_")[1].replace(".csv", "").replace("output_", "") + "_average_throughputs.csv")
                # print(filename)
                df.to_csv(filename)
        # else:
            # console.print("No throughput files found for %s" % test, style="red")

"""
1. Get file_path
    1.1. Check if file_path exists
        1.1.1. If it does NOT, output error and exit code
2. Check if clean files already exist
    2.1. If they do
        2.1.1. Delete all clean files
        2.1.2. Clean the files
    2.2. If they do NOT
        2.2.1. Clean the files
3. Check if clean files exist
    3.1. If they do 
        3.1.1. Check if average measurements already exist
            3.1.1.1. If they do
                3.1.1.1.1. Delete all average files
                3.1.1.1.2. Average the files
            3.1.1.1.2. If they do NOT
                3.1.1.2.1 Average the files
        3.1.2. Check if average measurements exist
            3.1.2.1. If they do then exit successfully
            3.1.2.2. If they don't then exit with error
    3.2. If they don't then output error and exit code
"""

# 1. Get file_path
if len(sys.argv) > 1 and sys.argv[1] and isinstance(sys.argv[1], str):
    file_path = sys.argv[1]
    # 1.1. Check if file_path exists
    if not os.path.exists(file_path):
        # 1.1.1. If it does NOT, output error and exit code
        console.print("❎ The path \n[white]" + file_path + "[/white]\ndoes not exist.", style="bold red")
        sys.exit()
else:
    console.print("Path for data folder not specified. Using /data.", style="bold red")
    file_path = "data"

# 2. Check if clean files already exist
if clean_files_exist(get_files(file_path)):
    # 2.1.1. Delete all clean files
    delete_clean_files(get_files(file_path))
    # 2.1.2. Clean the files
    clean_data([file for file in get_files(file_path) if '.csv' in file])
else:
    # 2.2.1. Clean the files
    clean_data([file for file in get_files(file_path) if '.csv' in file])

# 3. Check if clean files exist
if clean_files_exist(get_files(file_path)):
    # 3.1.1. Cehck if average measurements already exist
    if average_files_exist(file_path):
        delete_old_run_averages(file_path)
        create_run_averages(file_path)
    else:
        create_run_averages(file_path)

    if average_files_exist(file_path):
        console.print("Completed successfully", style="bold green")
    else:
        console.print("Failed successfully", style="bold red")

else:
    console.print("Failed succesfully", style="bold red")
    table = Table(title="Failure Analysis", show_lines = True)    
    table.add_column("Description")
    table.add_column("Value")
    table.add_row("Total number of files", str(len(get_files(file_path))))
    table.add_row("Number of .csv files", str(len([file for file in get_files(file_path) if '.csv' in file])))
    table.add_row("Number of clean_ files", str(len([file for file in get_files(file_path) if 'clean_' in file])))
    console.print(table, style="")



# csv_files = [file for file in get_files(file_path) if '.csv' in file]

# if clean_files_exist(get_files(file_path)):
#     with console.status("Deleting any previous clean data..."):
#         delete_clean_files(get_files(file_path))
#         console.print("✅ Previous clean files deleted...", style="green")
#         csv_files = [file for file in get_files(file_path) if '.csv' in file]
# else:
#     with console.status("Selecting csv files again..."):
#         csv_files = [file for file in get_files(file_path) if '.csv' in file]
#         console.print('✅ Collected all csv files again...', style="green")

# clean_data(csv_files)
# console.print('✅ Cleaned all csv files...', style="green")

# with console.status("Verifying files..."):
#     verify_files(csv_files)
#     console.print('✅ Verified files...', style="green")

# if average_files_exist(file_path):
#     with console.status("Deleting old run average files..."):
#         delete_old_run_averages(file_path)

# create_run_averages(file_path)

# if not clean_files_exist(file_path):
#     console.print("❎ Something went wrong...I did all this work...and clean files don't exist....", style="bold red")
