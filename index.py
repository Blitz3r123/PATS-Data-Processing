import codecs
import csv
import os
import re
import sys

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
                print("What file is this?! It ain't got 'pub' or 'sub' in it's name.")

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