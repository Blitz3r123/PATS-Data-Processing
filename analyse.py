from contextlib import contextmanager
from pydoc import describe
from socket import errorTab
from matplotlib.style import context
from inspect import currentframe, getframeinfo
from rich.jupyter import print
from rich.markdown import Markdown
from rich.align import Align
from rich.panel import Panel

import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import plotly.graph_objects as go
import re
import sys
import time
import datetime
from statistics import *

from rich.console import Console
from rich.table import Table
from rich.emoji import Emoji
from rich.live import Live
console = Console(record = True)

from matplotlib.pyplot import figure
from matplotlib.lines import Line2D

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

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

def convert_to_secs(time_string):
    """
      Converts hh:mm:ss to seconds.
    
      Parameters:
        time_string (string): String value of the time in the format hh:mm:ss.
    
      Returns:
        time_in_seconds (int): Number of seconds 
    """
    x = time.strptime(time_string,'%H:%M:%S')
    return int(datetime.timedelta(hours=x.tm_hour,minutes=x.tm_min,seconds=x.tm_sec).total_seconds())

def get_nums_from_string(text):
    """
      Gets numbers from a string.
    
      Parameters:
        text (string): string to take numbers from.
    
      Returns:
        number_list [int]: list of numbers inside of string. 
    """
    return [int(s) for s in re.findall(r'\d+', text)]

# with console.status("Checking given file path..."):
if len(sys.argv) > 1 and sys.argv[1] and isinstance(sys.argv[1], str):
    file_path = sys.argv[1]
else:
    console.print("Path for data folder not specified. Using /data.", style="bold red")
    file_path = "data"

# Check if file_path exists
if not os.path.exists(file_path):
    console.print("??? The path \n[white]" + file_path + "[/white]\ndoes not exist.", style="bold red")
    sys.exit()

def get_test_folders():
    """
      Scans a directory for all folders and returns the name of these folders
    
      Parameters:
        None
    
      Returns:
        test_folders [string]: Array containing all folder names.
    """
    test_folders = []
    all_files = os.listdir(file_path)
    for file in all_files:
        full_path = os.path.join(file_path, file)
        if os.path.isdir(full_path):
            test_folders.append(full_path)
    test_folders.sort()
    return test_folders

def format_test_titles(test_folders):
    """
      Takes folder names and formats them into titles.
    
      Parameters:
        test_folders [string]: Array of all folder names.
    
      Returns:
        new_files_names [string]: Array of new formatted folder names. 
    """
    new_file_names = []

    for file in test_folders:
        new_file_name = file.split("\\")[1]
        split_new_file_name = new_file_name.split("_")
        has_single_digit = len(split_new_file_name[1]) == 1
        
        if has_single_digit:
            split_new_file_name[1] = "0" + split_new_file_name[1]
            new_file_names.append((" ").join(split_new_file_name).replace("\\", " ").replace("/", " ").replace("data ", "").title())    
        else:
            new_file_names.append(new_file_name.replace("_", " ").replace("\\", " ").replace("/", " ").replace("data ", "").title())

    return new_file_names

def get_configs(test_folders, config_files, data):
    """
      Checks if config file is present, if so then appends True and config_file location, if not, it appends False and empty string to data['config_file']
    
      Parameters:
        test_folders [string]: Array of test_folders
        config_files [string]: Array of config_files
        data [too advanced]: Huge data structure containing all information
    
      Returns:
        None 
    """
    for file in test_folders:
        if file + "_metadata.txt" in config_files:
            data['has_config'].append(True)
            data["config_files"].append(file + "_metadata.txt")
        else:
            data['has_config'].append(False)
            data["config_files"].append("")

def get_data_runs(test_folders):
    """
      Returns the amount of run_n folders within the test folders for each test.
    
      Parameters:
        test_folders [string]: Array of test_folders.
    
      Returns:
         runs_per_test [int]: Array containing the numbers of run_n folders for each test within test_folders.
    """
    return [len([file for file in os.listdir(file) if '.csv' not in file and 'run_' in file]) for file in test_folders]

def get_config_runs_and_participants(data):
    """
      Read the config file per test and store its pub/sub and mal_pub/mal_sub counts as well as how many runs there were.
    
      Parameters:
        data [too advanced]: Single huge data structure containing all information.
    
      Returns:
        None 
    """
    for file in data['config_files']:
        if len(file) > 0:
            with open(file.replace("[green]", "").replace("[/green]", ""), "r") as f:
                contents = f.readlines()
                
                pub_amounts = "".join([line for line in contents if '"pub_amount"' in line])
                mal_pub_amounts = "".join([line for line in contents if '"mal_pub_amount"' in line])
                sub_amounts = "".join([line for line in contents if '"sub_amount"' in line])
                mal_sub_amounts = "".join([line for line in contents if '"mal_sub_amount"' in line])

                data['pub_count'].append(sum(get_nums_from_string(pub_amounts)))
                data['mal_pub_count'].append(sum(get_nums_from_string(mal_pub_amounts)))
                data['sub_count'].append(sum(get_nums_from_string(sub_amounts)))
                data['mal_sub_count'].append(sum(get_nums_from_string(mal_sub_amounts)))
                
                restart_lines = [line for line in contents if 'Restart' in line]

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

            data['config_runs'].append(restart_counts[max(restart_counts, key=restart_counts.get)])
        else:
            data['config_runs'].append(0)
            data['pub_count'].append(0)
            data['mal_pub_count'].append(0)
            data['sub_count'].append(0)
            data['mal_sub_count'].append(0)

        data["errors"].append("")

def get_run_participants(data):
    for i in range(len(data['test_files'])):
        runs_arr = []
        filename = data['test_files'][i]
        runs = data['config_runs'][i]
        run_folders = int(data['data_runs'][i])

        if int(runs) == run_folders or run_folders > 0:
            for i in range(run_folders):
                run_obj = {
                    "run_n": 0,
                    "pub_count": 0,
                    "sub_count": 0,
                    "mal_pub_count": 0,
                    "mal_sub_count": 0
                }
                # Get path to run_n folder
                run_dir = os.path.join(filename, "run_" + str(i + 1))
                # Read run_n folder contents
                all_files = os.listdir(run_dir)
                all_raw_files = [file for file in all_files if '.csv' in file and 'clean_' not in file]

                pub_count = len([file for file in all_raw_files if 'pub_' in file and 'mal_' not in file])
                mal_pub_count = len([file for file in all_raw_files if 'pub_' in file and 'mal_' in file])
                sub_count = len([file for file in all_raw_files if 'sub_' in file and 'mal_' not in file])
                mal_sub_count = len([file for file in all_raw_files if 'sub_' in file and 'mal_' in file])
                
                run_obj['run_n'] = i + 1
                run_obj['pub_count'] = pub_count                
                run_obj['mal_pub_count'] = mal_pub_count                
                run_obj['sub_count'] = sub_count                
                run_obj['mal_sub_count'] = mal_sub_count
                
                runs_arr.append(run_obj)

                run_obj = {
                    "run_n": 0,
                    "pub_count": 0,
                    "sub_count": 0,
                    "mal_pub_count": 0,
                    "mal_sub_count": 0
                }

        data['run_participants'].append(runs_arr)

def get_total_test_durations(data):
    for i in range(len(data['config_files'])):
        config_file = data['config_files'][i]
        has_config = data['has_config'][i]

        if has_config:
            with open(config_file, "r") as f:
                file_contents = f.readlines()
                try:
                    test_duration = [line for line in file_contents if "Duration" in line]
                    if len(test_duration) > 0:
                        test_duration = test_duration[0]
                        test_duration = test_duration.replace("Test Duration: ", "")
                        test_duration = test_duration.split(".")[0]
                    else:
                        test_duration = "-"
                except Exception as e:
                    print("Error on line " + str(getframeinfo(currentframe()).lineno) + ": ")
                    print(e)
                    test_duration = "-"
        else:
            test_duration = "-"

        data['total_test_durations'].append(test_duration)

def main():
    """
    1. List tests in a table format
    2. Check how many runs were stated in the config
    3. Get sub, malsub, pub, and malpub count
    4. Get number of run folders
    5. Get participant amounts per run
    """

    data = {
        "test_files": [],
        "test_names": [],
        "has_config": [],
        "config_files": [],
        "config_runs": [],
        "data_runs": [],
        "sub_count": [],
        "mal_sub_count": [],
        "pub_count": [],
        "mal_pub_count": [],
        "run_participants": [],
        "total_test_durations": [],
        "errors": []
    }

    test_folders = get_test_folders()
    
    new_file_names = format_test_titles(test_folders)

    # Sort both in the same order
    new_file_names, test_folders = zip(*sorted(zip(new_file_names, test_folders)))

    config_files = [file for file in get_files(file_path) if '.txt' in file]

    get_configs(test_folders, config_files, data)

    data['test_files'] = test_folders
    
    data['test_names'] = new_file_names
    
    data['data_runs'] = get_data_runs(test_folders)

    get_config_runs_and_participants(data)

    get_run_participants(data)

    get_total_test_durations(data)

    """
    Identify all errors and add to data['errors'].
    Errors:
    1. Config not found.
        - Can't read any config data.
    2. 0 runs.
        - No restarts recorded in the config file.
        - Normally happens when test is interrupted before first restart.
    3. Config run and run_n folder amount mismatch.
        3.1. run_n < run
            - Hasn't completed all runs.
        3.2. run_n > run
            - HUH?!
    4. Can't read run amount from config.
        - Config file is corrupted/incomplete/something is wrong with it.
    5. Participant amount == 0 from config.
        - Either error with analysis.py or for some reason there are no participants in the config file.
    6. Config participants and test result participant amount mismatch.
        - Test results haven't been downloaded properly.
        6.1. Config participants > test result participants
            - Missing test data
        6.2. Config participants < test result participants
            - HUH?!
    7. Test duration hasn't been calculated in the config file.
        - Test has probably been interrupted and there is no test end
        7.1. Test Start exists but Test End doesn't
            - Test has been interrupted and didn't complete properly
        7.2. Test End exists but Test Start doesn't
            - HUH?!
    8. Test duration doesn't match duration set in config
        - Very weird...
    """
    for i in range(len(data['test_files'])):
        error = ""
        # 1. Config not found.
        if data["has_config"][i] == False:
            error = "Config file not found."
        else:
            # 2. 0 runs.
            if int(data["config_runs"][i]) == 0:
                error = error + "\n0 runs recorded from config file. It's probably the case that no restarts have been recorded."
                # error = error + "\n\tConfig file can be found at:"
                # error = error + "\n\t" + data["config_files"][i]
            
            # 3. Config run and run_n folder mismatch.
            if not (data["config_runs"][i] == data["data_runs"][i]):
                error = error + "\nMismatch between config run amount and run_n folders."
                if data["data_runs"][i] < data["config_runs"][i]:
                    error = error + "\n\tTest hasn't completed all runs. Missing run_n folders."
                    error = error + "\n\tResults contain " +str(data["data_runs"][i])+ "/" +str(data["config_runs"][i])+ " runs."
                else:
                    error = error + "\n\tHUH?! What happened here? How has this happened???"
                    error = error + "\n\tResults contain " +str(data["data_runs"][i])+ "/" +str(data["config_runs"][i])+ " runs."
                    error = error + "\n\tYeah...somehow...there is more run data than configured runs...."

            # 4. Can't read run amount from config.
            if data["config_runs"][i] == 0:
                error = error + "\nCouldn't read run amount from config."
                error = error + "\n\tConfig file is corrupted or incomplete or something else is wrong with it:"
                # error = error + "\n\t" + data["config_files"][i]

            # 5. Participant amount == 0 from config.
            if data["pub_count"][i] == 0 and data["sub_count"][i] == 0 and data["mal_pub_count"][i] == 0 and data["mal_sub_count"][i] == 0:
                error = error + "\nParticipant amount is 0 according to the config file."
                error = error + "\n\tEither there is a bug in analysis.py (the code behind this) or it's actually set to 0 in the config file..."

            # 6. Config participant and test results participant amount mismatch.
            runs_arr = data["run_participants"][i]
            for run in runs_arr:
                if len(run) > 0:
                    if not (run['pub_count'] + run['mal_pub_count'] == data['pub_count'][i] + data['mal_pub_count'][i]):
                        error = error + "\nPublisher amount mismatch for Run " + str(runs_arr.index(run) + 1)  + " results."

                    if not (run['sub_count'] + run['mal_sub_count'] == data['sub_count'][i] + data['mal_sub_count'][i]):
                        error = error + "\nSubscriber amount mismatch for Run " + str(runs_arr.index(run) + 1)  + " results."

            # 7. Test duration hasn't been calculated in the config file
            test_duration = data['total_test_durations'][i]
            config_file = data['config_files'][i]
            
            if test_duration == "-":
                error = error + "\nTest Duration not seen in config file."

            with open(config_file, "r") as f:
                file_contents = f.readlines()
                test_start_lines = [line for line in file_contents if "Test Start" in line]
                test_end_lines = [line for line in file_contents if "Test End" in line]
                # 7.1. Test Start exists but Test End doesn't
                if len(test_start_lines) > 0 and len(test_end_lines) == 0:
                    test_start = test_start_lines[0].split(" ")[3]
                    error = error + "\n\tTest Start found to be " + str(test_start) + " \tbut there is no Test End..."

                    restart_lines = [line for line in file_contents if "Restart VM" in line]

                    error = error + "\n\t\tVM 1 restarted " + str(len([line for line in restart_lines if "10.200.51.21" in line])) + " time(s)."
                    error = error + "\n\t\tVM 2 restarted " + str(len([line for line in restart_lines if "10.200.51.22" in line])) + " time(s)."
                    error = error + "\n\t\tVM 3 restarted " + str(len([line for line in restart_lines if "10.200.51.23" in line])) + " time(s)."
                    error = error + "\n\t\tVM 4 restarted " + str(len([line for line in restart_lines if "10.200.51.24" in line])) + " time(s)."

                elif len(test_start_lines) == 0 and len(test_end_lines) > 0:
                    error = error + "\n\tHUH?! There is a Test End but no Test Start in the config file. How has that happened?!"

            # 8. Test duration doesn't match duration set in config
            with open(config_file, 'r') as f:
                content = f.readlines()
                execution_times = []
                for line in content:
                    if '-executionTime' in line:
                        for time in [item for item in line.split(" -") if "executionTime" in item]:
                            execution_times.append(get_nums_from_string(time)[0])

            # Make sure all execution_times match
            no_dupe_execution_times = list(dict.fromkeys(execution_times))
            if len(no_dupe_execution_times) > 1:
                error = error + "\nThe -executionTime amounts do NOT match."
                error = error + "\n\t" + str(len(no_dupe_execution_times)) + " values have been seen: "
                error = error + "\n\t"
                for time in no_dupe_execution_times:
                    error = error + str(time) + " "
            else:
                config_duration = no_dupe_execution_times[0]
                actual_duration = convert_to_secs(test_duration)
                config_duration_hours = config_duration // 3600
                actual_duration_hours = actual_duration // 3600

                if config_duration_hours != actual_duration_hours:
                    error = error + "\nConfig duration and actual test duration do NOT match:"
                    error = error + "\n\tConfig Duration: " + str(datetime.timedelta(seconds=config_duration))
                    error = error + "\n\tActual Duration: " + str(datetime.timedelta(seconds=actual_duration))

            execution_times = []

        data['errors'][i] = error

    """
    Create errors table
    """
    error_table = Table(show_header = True, header_style = "bold red", show_lines = True)
    error_table.add_column("Test", no_wrap=False)
    error_table.add_column("Errors", no_wrap=False)
    for i in range(len(data['test_files'])):
        test_name = data['test_names'][i]
        error = data['errors'][i]
        if not error == "":
            error_table.add_row(test_name, error)

    """
    Construct the table
    """
    table = Table(show_header = True, header_style = "bold white", show_lines = True)
    table.add_column("Test", no_wrap=False)
    table.add_column("Has\nConfig", no_wrap=False)
    table.add_column("Config\nRuns", no_wrap=False)
    table.add_column("Data\nRuns", no_wrap=False)
    table.add_column("Config\nParticipants", no_wrap=False)
    table.add_column("Data\nParticipants", no_wrap=False)
    table.add_column("Total\nTest\nDurations\nhr : m : s", no_wrap=False)
    
    # with Live(table_centered, console=console, screen=False, refresh_per_second=20):
    for i in range(len(data['test_files'])):
        error = data["errors"][i]

        test_name = data['test_names'][i]
        has_config = data["has_config"][i]
        has_config = "[green]Yes[/green]" if has_config else "-"

        if error == "":
            # test_file = data['test_files'][i]
            runs = str(data['config_runs'][i])
            
            run_folder_count = str(data['data_runs'][i])
            if "-" not in runs and int(runs) == int(run_folder_count):
                run_folder_count = "[green]" + run_folder_count + "[/green]"
            
            pub_count = data['pub_count'][i]
            mal_pub_count = data['mal_pub_count'][i]
            sub_count = data['sub_count'][i]
            mal_sub_count = data['mal_sub_count'][i]
            
            participants = "[green]" +str(sub_count)+ "S[/green]\t[green]" +str(pub_count)+ "P[/green]\n[red]" +str(mal_sub_count)+ "S[/red]\t[red]" +str(mal_pub_count)+ "P[/red]\n------------\n" + str(sub_count + mal_sub_count) + "S\t" + str(pub_count + mal_pub_count) + "P"

            runs_arr = data["run_participants"][i]
            participants_data = ""
            for run in runs_arr:
                if run['pub_count'] + run['mal_pub_count'] == data['pub_count'][i] + data['mal_pub_count'][i]:
                    total_pub_count_output = "[black on green]" + str(run['pub_count'] + run['mal_pub_count']) + "P[/black on green]"
                else:
                    has_error = True
                    comments = comments + "\n Publisher amount mismatch for Run " + str(runs_arr.index(run) + 1)  + " results."
                    total_pub_count_output = "[white on red]" + str(run['pub_count'] + run['mal_pub_count']) + "P[/white on red]"

                if run['sub_count'] + run['mal_sub_count'] == data['sub_count'][i] + data['mal_sub_count'][i]:
                    total_sub_count_output = "[black on green]" + str(run['sub_count'] + run['mal_sub_count']) + "S[/black on green]"
                else:
                    has_error = True
                    comments = comments + "\n Subscriber amount mismatch for Run " + str(runs_arr.index(run) + 1)  + " results."
                    total_sub_count_output = "[white on red]" + str(run['sub_count'] + run['mal_sub_count']) + "S[/white on red]"

                participants_data = participants_data + "[bold underline]Run " + str(run['run_n']) + ":[/bold underline]\n[green]" + str(run['sub_count']) + "S[/green]\t[green]" + str(run['pub_count']) + "P[/green]\n[red]" + str(run['mal_sub_count']) + "S[/red]\t[red]" + str(run['mal_pub_count']) + "P[/red]\n------------\n" + total_sub_count_output + "\t" +total_pub_count_output+ "\n\n"

            test_durations = data['total_test_durations'][i]

            table.add_row(test_name, has_config, runs, run_folder_count, participants, participants_data, test_durations)
        else:
            
            if "\n" in error[0:3]:
                error[0:3].replace("\n", "", 1)

            try:
                runs = str(data['config_runs'][i])
            except Exception as e:
                print("Error on line " + str(getframeinfo(currentframe()).lineno) + ": ")
                print(e)
                runs = "-"
            try:
                run_folder_count = str(data['data_runs'][i])
            except Exception as e:
                print("Error on line " + str(getframeinfo(currentframe()).lineno) + ": ")
                print(e)
                run_folder_count = "-"
            try:
                pub_count = data['pub_count'][i]
                mal_pub_count = data['mal_pub_count'][i]
                sub_count = data['sub_count'][i]
                mal_sub_count = data['mal_sub_count'][i]

                participants = "[green]" +str(sub_count)+ "S[/green]\t[red]" +str(pub_count)+ "P[/red]\n[green]" +str(mal_sub_count)+ "S[/green]\t[red]" +str(mal_pub_count)+ "P[/red]\n------------\n" + str(sub_count + mal_sub_count) + "S\t" + str(pub_count + mal_pub_count) + "P"
            except Exception as e:
                print("Error on line " + str(getframeinfo(currentframe()).lineno) + ": ")
                print(e)
                participants = "-"
            try:
                # comments = ""
                runs_arr = data["run_participants"][i]
                participants_data = ""
                for run in runs_arr:
                    if run['pub_count'] + run['mal_pub_count'] == data['pub_count'][i] + data['mal_pub_count'][i]:
                        total_pub_count_output = "[black on green]" + str(run['pub_count'] + run['mal_pub_count']) + "P[/black on green]"
                    else:
                        has_error = True
                        # comments = comments + "\nPublisher amount mismatch for Run " + str(runs_arr.index(run) + 1)  + " results."
                        total_pub_count_output = "[white on red]" + str(run['pub_count'] + run['mal_pub_count']) + "P[/white on red]"

                    if run['sub_count'] + run['mal_sub_count'] == data['sub_count'][i] + data['mal_sub_count'][i]:
                        total_sub_count_output = "[black on green]" + str(run['sub_count'] + run['mal_sub_count']) + "S[/black on green]"
                    else:
                        has_error = True
                        # comments = comments + "\nSubscriber amount mismatch for Run " + str(runs_arr.index(run) + 1)  + " results."
                        total_sub_count_output = "[white on red]" + str(run['sub_count'] + run['mal_sub_count']) + "S[/white on red]"

                    participants_data = participants_data + "[bold underline]Run " + str(run['run_n']) + ":[/bold underline]\n[green]" + str(run['sub_count']) + "S[/green]\t[green]" + str(run['pub_count']) + "P[/green]\n[red]" + str(run['mal_sub_count']) + "S[/red]\t[red]" + str(run['mal_pub_count']) + "P[/red]\n------------\n" + total_sub_count_output + "\t" +total_pub_count_output+ "\n\n"
            except Exception as e:
                print("Error on line " + str(getframeinfo(currentframe()).lineno) + ": ")    
                print(e)                        
                participants_data = "-"

            test_durations = data['total_test_durations'][i]

            comments = data["errors"][i]
            
            if i == 0:
                table.add_column("Comments", no_wrap=False)
            table.add_row(test_name, has_config, runs, run_folder_count, participants, participants_data, test_durations, comments, style="bold #003f5c on #ffa600")

    console.print(Markdown("# All Tests"), style="")
    console.print(table)
    console.print(Markdown("# All Errors"), style="")
    console.print(error_table)
    # console.print(data)

    # Output to analysis.html too
    with open("analysis.html", "w", encoding='utf-8') as f:
        f.write(console.export_html())

# with console.status("Analysing data..."):
main()