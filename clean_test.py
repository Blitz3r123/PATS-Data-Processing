from cProfile import run
from rich.console import Console
from rich.markdown import Markdown
from rich.progress import track
from pprint import pprint

from clean_test_functions import *

import csv
import pandas as pd
import os
import sys

console = Console()

args = sys.argv[1:]
# Check that only one argument has been passed.
if len(args) > 1:
    console.print("You have more than 1 command line argument.", style="bold red")
    sys.exit
else:
    test_path = args[0]

"""
This script should take the filepath to a test. The structure of the contents should follow this pattern:

- 📂 test_one
    - 📂 run_1
        - 📄 pub_0.csv
        - 📄 ...
        - 📄 pub_n.csv
        - 📄 sub_0.csv
        - 📄 ...
        - 📄 sub_n.csv
        - 📄 vm1_cpu_usage.log
        - 📄 vm1_network_usage.log
        - 📄 ...
        - 📄 vmn_cpu_usage.log
        - 📄 vmn_network_usage.log
    - 📂 ...
    - 📂 run_n    

After the script has finished the test should have the following pattern:

- 📂 summarised_test_one
    - 📄 latencies.csv
    - 📄 throughputs.csv
    - 📄 total_samples.csv
    - 📄 sample_rates.csv
    - 📄 lost_samples.csv
    - 📂 throughputs_per_sub
        - 📄 sub_0.csv
        - 📄 ...
        - 📄 sub_n.csv
    - 📂 total_samples_per_sub
        - 📄 sub_0.csv
        - 📄 ...
        - 📄 sub_n.csv
    - 📂 sample_rates_per_sub
        - 📄 sub_0.csv
        - 📄 ...
        - 📄 sub_n.csv
    - 📂 lost_samples_per_sub
        - 📄 sub_0.csv
        - 📄 ...
        - 📄 sub_n.csv

How should the script work?
1. Check that the test follows the above pattern (the first one) and that there are no extra files or missing files.
2. Summarise the latencies.
    - Basically create a list of each runs' latencies:
        - {
            "run_1": [...],
            "run_2": [...],
            "run_3": [...]
        }
    2.1. For each run:
        2.1.1. Get the run count and the latencies and push to a list
3. Summarise the throughputs.
    - Basically create a list of each runs' throughputs:
        - {
                "run_1": [...],
                "run_2": [...],
                "run_3": [...]
            }
    3.1. For each run:
        3.2. Add up all throughput values from each sub_n.csv file and push to a list alongside the run count.
    3.2. Create the throughputs_per_sub folder.
        3.3. For each subscriber:
            3.3.1. Gather the list of throughputs per run.
            3.3.2. Place the list of throughputs per run into a file with the subscriber name.
            
4. Summarise the total_samples.
    - Basically create a list of each runs' throughputs:
        - {
                "run_1": [...],
                "run_2": [...],
                "run_3": [...]
            }
    4.1. For each run:
        4.2. Add up all throughput values from each sub_n.csv file and push to a list alongside the run count.
5. Summarise the sample_rates.
    - Basically create a list of each runs' throughputs:
        - {
                "run_1": [...],
                "run_2": [...],
                "run_3": [...]
            }
    5.1. For each run:
        5.2. Add up all throughput values from each sub_n.csv file and push to a list alongside the run count.
6. Summarise the lost_samples.
    - Basically create a list of each runs' throughputs:
        - {
                "run_1": [...],
                "run_2": [...],
                "run_3": [...]
            }
    6.1. For each run:
        6.2. Add up all throughput values from each sub_n.csv file and push to a list alongside the run count.

"""

# 1. Check that the test follows the above pattern (the first one) and that there are no extra files or missing files.

# Check path exists
if not os.path.exists(test_path):
    console.print("Path doesn't exist: \n\t" + test_path, style="bold red")
    sys.exit()
    

# Check that the subfolders are all run_n folders
sub_dirs = [x for x in os.listdir(test_path) if os.path.isdir( os.path.join(test_path, x) )]
run_dirs = [dir for dir in sub_dirs if "run_" in dir]
run_dirs_count = len(run_dirs)
if run_dirs_count == 0:
    console.print("There are no run_n folders in " + test_path, style="bold red")
    sys.exit()
    
# Make sure that the test folder only consists of tests and their metatadata - delete everything else
sub_files = [x for x in os.listdir(test_path) if not os.path.isdir( os.path.join(test_path, x) )]
if len(sub_files) > 0:
    for i in track(range(len(sub_files)), description="Deleting extra files in " + os.path.basename(test_path) + "..."):
        os.remove(os.path.join(test_path, sub_files[i]))
    
"""
Check that each run_n folder has the following at least (and delete all the rest of files):
    - pub_0.csv
    - sub_0.csv
    - vm1_cpu_usage.log
    - vm1_network_usage.log
    - vm2_cpu_usage.log
    - vm2_network_usage.log
    - vm3_cpu_usage.log
    - vm3_network_usage.log
    - vm4_cpu_usage.log
    - vm4_network_usage.log
"""
for dir in run_dirs:
    dir_path = os.path.join(test_path, dir)
    must_have_files = []
    to_delete_files = []
    for file in os.listdir(dir_path):
        # Look for files that start with e.g. pub_ and end with .csv
        pub_files_match = has_match("^pub_.*.csv$", file)
        sub_files_match = has_match("^sub_.*.csv$", file)
        cpu_files_match = has_match("^vm[0-9]_cpu_usage.log$", file)
        network_files_match = has_match("^vm[0-9]_network_usage.log$", file)
    
        if pub_files_match or sub_files_match or cpu_files_match or network_files_match:
            # Keep the required files
            must_have_files.append(file)
        else:
            # Delete all other files
            to_delete_files.append(file)

    if len(to_delete_files) > 0:
        for i in track(range(len(to_delete_files)), description="Deleting extra files in " + os.path.basename(dir_path) + "..."):
            file = to_delete_files[i]
            filepath = os.path.join(dir_path, file)
            os.remove(filepath)
        
# Summarise the latencies
for dir in run_dirs:
    dir_path = os.path.join(test_path, dir)
    pub_path = os.path.join(dir_path, "pub_0_output.csv")

    # Measurements start from row 35 onwards
    df = pd.read_csv(pub_path, skiprows=34, skip_blank_lines=True, on_bad_lines='skip')[" Latency (us)"]
    # Remove non-numeric values
    df.dropna(inplace=True)
    df.name = dir
    
    latencies_csv_path = os.path.join(test_path, "latencies.csv")
    
    if os.path.exists(latencies_csv_path):
        # Read the csv
        df_csv = pd.read_csv(latencies_csv_path)
        # Append to the csv values
        df_merged = pd.concat([df, df_csv], axis=1)
        # Sort columns alphabetically
        df_merged = df_merged.reindex(sorted(df_merged.columns), axis=1)
        # Remove any empty slots
        df_merged.dropna(inplace=True)
        # Write to csv again
        df_merged.to_csv(latencies_csv_path, index=False, mode="w")
    else:
        df.to_csv(latencies_csv_path, index=False, mode="w", header=[dir])
        
# Summarise the throughputs
#   For each run get the nth row of all subs and add them up together.
for dir in run_dirs:
    dir_path = os.path.join(test_path, dir)
    
    # Collect all the sub files
    dir_files = os.listdir(os.path.join(test_path, dir))
    sub_files = []
    for file in dir_files:
        sub_files_match = has_match("^sub_.*.csv$", file)
        if sub_files_match:
            sub_files.append(file)
    
    run_throughputs_df = pd.DataFrame()
    
    for file in sub_files:
        df = pd.read_csv(os.path.join(dir_path, file), skip_blank_lines=True, on_bad_lines='skip', skiprows=24)["  Ave Mbps"]
        df.dropna(inplace=True)
        header = file.split("_output.csv")[0]
        df.name = header
        run_throughputs_df = pd.concat([run_throughputs_df, df], axis=1)
        # run_throughputs_df["total"] = run_throughputs_df.sum(axis=1)
        
    # Convert all columns to float
    for col in run_throughputs_df.columns.to_list():
        # run_throughputs_df[col].astype(float, errors="ignore").notnull()
        run_throughputs_df[col] = pd.to_numeric(run_throughputs_df[col], errors="coerce")
    
    run_throughputs_df.dropna(inplace=True)
    
    run_throughputs_df[dir] = run_throughputs_df.sum(axis = 1)
    
    throughputs_csv_path = os.path.join(test_path, "throughputs.csv")
    
    if os.path.exists(throughputs_csv_path):
        # Read the csv
        df_csv = pd.read_csv(throughputs_csv_path)
        # Append to the csv values
        df_merged = pd.concat([run_throughputs_df[dir], df_csv], axis=1)
        # Sort columns alphabetically
        df_merged = df_merged.reindex(sorted(df_merged.columns), axis=1)
        # Remove any empty slots
        df_merged.dropna(inplace=True)
        # Write to csv again
        df_merged.to_csv(throughputs_csv_path, index=False, mode="w")
    else:
        run_throughputs_df[dir].to_csv(throughputs_csv_path, index=False, mode="w", header=[dir])