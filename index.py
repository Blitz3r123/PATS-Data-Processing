from rich.jupyter import print
from rich.markdown import Markdown

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
    for file in files:

        with console.status("Cleaning " + file):

            # console.print(Markdown("# " + file), style="bold white")

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
            else:
                # print("What file is this?! It ain't got 'pub' or 'sub' in it's name.")
                break

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
    for file in [file for file in files if "clean" in file]:
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

    for test in test_folders:
        test_files = get_files(test)

        with console.status("Creating average run latencies..."):
            latency_files = [file for file in test_files if 'clean_pub_0' in file]
            if len(latency_files) > 0:
                data = {}
                for file in latency_files:
                    series = pd.read_csv(file)["Latency"]
                    column = {os.path.basename(os.path.dirname(file)) + "_latency" : series}
                    data.update(column)        

                df = pd.DataFrame(data=data)
                df['avg_run_latency'] = df.mean(numeric_only=True, axis=1)

                # Create new .csv file in test_folder:
                df.to_csv(os.path.join(test, 'average_latencies.csv'))

        with console.status("Creating new average run throughputs..."):
            throughput_files = [file for file in test_files if 'clean_sub' in file]
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
                    df.to_csv(os.path.join(test, file.split("clean_")[1][0:5] + "_average_throughputs.csv"))

if len(sys.argv) > 1 and sys.argv[1] and isinstance(sys.argv[1], str):
    file_path = sys.argv[1]
else:
    console.print("Path for data folder not specified. Using /data.", style="bold red")
    file_path = "data"

# Check if file_path exists
if not os.path.exists(file_path):
    console.print("The path \n[white]" + file_path + "[/white]\ndoes not exist.", style="bold red")
    sys.exit()

with console.status("Collecting all files..."):
    all_files = get_files(file_path)
with console.status("Selecting csv files..."):
    csv_files = list(filter(lambda file: file.endswith(".csv"), all_files))
with console.status("Deleting any previous clean data..."):
    delete_clean_files(csv_files)
with console.status("Collecting all files again..."):
    all_files = get_files(file_path)
with console.status("Selecting csv files again..."):
    csv_files = list(filter(lambda file: file.endswith(".csv"), all_files))
clean_data(csv_files)
with console.status("Verifying files..."):
    verify_files(csv_files)
with console.status("Deleting old run average files..."):
    delete_old_run_averages(file_path)
create_run_averages(file_path)
console.print("Files cleaned in /[bold white]%s[/bold white]" % file_path, style="bold red")