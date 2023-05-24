import os
import platform
from pathlib import Path
import json
import sys
import logging
from datetime import datetime
import re


def check_metadata(file):
    return Path(f'{file}.json') if Path(f'{file}.json').is_file() else False


def find_extensions(dir,  excluded = ['', '.txt', '.lnk']):
    '''
    Used this to get list of all the extenion and based on that update the *-ext variables
    ''' 
    extensions = set()
    for _, _, files in os.walk(dir):   
        for f in files:
            ext = Path(f).suffix.lower()
            if not ext in excluded:
                extensions.add(ext)
    return extensions 

def get_creation_date(path_to_file):
    """
    Try to get the date that a file was created, falling back to when it was
    last modified if that isn't possible.
    See http://stackoverflow.com/a/39501288/1709587 for explanation.
    """
    if platform.system() == 'Windows':
        return os.path.getctime(path_to_file)
    else:
        stat = os.stat(path_to_file)
        try:
            return stat.st_birthtime
        except AttributeError:
            # We're probably on Linux. No easy way to get creation dates here,
            # so we'll settle for when its content was last modified.
            return stat.st_mtime