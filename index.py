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
