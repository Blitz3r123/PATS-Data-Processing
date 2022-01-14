import csv
import inspect
import os
import pathlib
import re

from rich.markdown import Markdown
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

        # console.print(Markdown("# " + file), style="bold white")

        open_file = open(file)
        csvreader = csv.reader(open_file)

        new_output = []
        # Remove all empty cells
        for row in csvreader:
            new_row = []
            for cell in row:
                if cell != "":
                    new_row.append(cell.strip())
            new_output.append(new_row)

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
        
        open_file.close()

        # clean_numeric_output has all numeric data in it
        # clean_string_output has all string data in it

        # If there are no measurements (clean_numeric_output is empty) then get headers
        if clean_numeric_output:
            for line in clean_string_output:
                if len(line) > 1:
                    headers = line
        else:
            headers = []

        # 
        # Check headers and data have same number of columns
        #
        # if headers and clean_numeric_output:
        #     if len(headers) != len(clean_numeric_output[0]):
        #         console.print(file, style="red")
        #         console.print(len(headers), style="white")
        #         console.print(headers, style="blue")

        #         console.print(len(clean_numeric_output[0]), style="white")
        #         console.print(clean_numeric_output[0], style="blue")
        #         console.print(Markdown("---"), style="white")

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

with console.status("Collecting all files..."):
    all_files = get_files("data")
with console.status("Selecting csv files..."):
    csv_files = list(filter(lambda file: file.endswith(".csv"), all_files))
with console.status("Deleting any previous clean data..."):
    delete_clean_files(csv_files)
with console.status("Collecting all files again..."):
    all_files = get_files("data")
with console.status("Selecting csv files again..."):
    csv_files = list(filter(lambda file: file.endswith(".csv"), all_files))
with console.status("Cleaning data..."):
    clean_data(csv_files)