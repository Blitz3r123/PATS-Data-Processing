import csv
import inspect
import os
import pathlib

from rich.markdown import Markdown
from rich.console import Console
console = Console()

all_files = []

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


def clean_data(files):
    for file in files[0:5]:
        console.print(Markdown("# " + file), style="bold white")
        # console.print(Markdown("## " + os.path.basename(file)), style="bold white")

        open_file = open(file)
        csvreader = csv.reader(open_file)

        new_output = []
        # Remove all empty cells
        for row in csvreader:
            new_row = []
            for cell in row:
                if cell != "":
                    new_row.append(cell)
            new_output.append(new_row)

        # Clean data into header and numbers
        
        
            
         

all_files = get_files("data")
csv_files = list(filter(lambda file: file.endswith(".csv"), all_files))
clean_data(csv_files)