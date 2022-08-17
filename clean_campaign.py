from rich.console import Console
console = Console()

import sys
import os
args = sys.argv[1:]

"""
How should the script work?
1. Call `python clean_test.py [test_folder_path]` for each test lol
"""
# Check that only one argument has been passed.
if len(args) > 1:
    console.print("You have more than 1 command line argument.", style="bold red")
    sys.exit
else:
    camp_path = args[0]

# Check path is legit and is a folder
if not (os.path.exists(camp_path)):
    console.print("The path does not exist: \n\t" + camp_path, style="bold red")
if not (os.path.isdir(camp_path)):
    console.print("The path is not a directory: \n\t" + camp_path, style="bold red")
    
# Get all folders inside
sub_dirs = [x for x in os.listdir(camp_path) if os.path.isdir( os.path.join(camp_path, x) )]
# for dir in sub_dirs:
for i in range(len(sub_dirs)):
    os.system('python clean_test.py ' + os.path.join(camp_path, sub_dirs[i]) + " " + str(i + 1) + " " + str(len(sub_dirs)))