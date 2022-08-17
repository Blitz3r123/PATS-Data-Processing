from rich.console import Console
console = Console()

import os
import re
import sys

"""
  Checks a string (to_match) with a regex (match).

  Parameters:
    to_match (string): String to check.
    match (regex string): Regex to search for.

  Returns:
    Boolean: True if there is a match and False if there isn't 
"""
def has_match(match, to_match):
    return re.search(match, to_match) != None