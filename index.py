import csv
import inspect
import os

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
def read_dir(dir_path):
    dir_contents = os.listdir(dir_path)
    for dir_content in dir_contents:

        dir_content_path = os.path.join(dir_path, dir_content)
        
        if os.path.isdir(dir_content_path):
            read_dir(dir_content_path)
        else:
            all_files.append(dir_content_path)
            return dir_content_path

read_dir("data")

csv_files = list(filter(lambda file: file.endswith(".csv"), all_files))

#
# Clean data
#
"""
    Find the first appearance of a number
    Find the first appereance of a letter after the first number
    Everything in between is the data
    The row before first appearance of number contains the headings
"""
# for csv_file in csv_files:
file = open(csv_files[0])

csvreader = csv.reader(file)

# Get all rows where first position is a number (this includes the final row being the summary row)
numeric_rows = []
for row in csvreader:
    if row[0].isdigit():
       numeric_rows.append(row)

# Remove the final summary row
del numeric_rows[-1]

console.print(numeric_rows, style="green")