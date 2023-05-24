import sys
import re
import os
import shutil
import logging
import requests
from sys import stdout
from pathlib import Path


# Create and configure logger
handlers = [
    logging.FileHandler(os.path.expanduser('~/.script.log')),
    logging.StreamHandler(stdout),
    ]
logging.basicConfig(level=logging.DEBUG,handlers=handlers, format="%(asctime)s;%(levelname)s;%(message)s")

ONE_DRIVE = '/Users/mittalmak/Library/CloudStorage/OneDrive-Personal'
VIDEO_DRIVE = '/Volumes/SSD1/Videos/'
IMG_EXT = ['.jpg', '.png', '.jpeg']
VIDEO_EXT = ['.mp4', '.mkv']

API_KEY = '428798c163a4628d3ce00c9964f304fc'
VIDEO_DRIVE = '/Volumes/SSD1/Videos/'
TV_SHOW_FOLDER = "/Volumes/SSD1/Videos/TV_Shows/"
MOVIES_FOLDER = "/Volumes/SSD1/Videos/Movies/"

def sanitize_filename(filename):
    """Saniatize file name used mostly for serching in the api"""
    filename = filename.replace("_", " ")
    filename = filename.replace(".", " ")
    filename = re.sub(r"(\(.*\))", "", filename)
    filename = re.sub(r"S\d\d(E\d\d)?", "", filename)
    return filename

def subfolder_tv(metadata):
    """For TV show create a new Dir if the tv show dir is not present"""
    year = metadata['first_air_date'].split("-")[0]
    name = re.sub(r"[:\\]", "", metadata['name'])
    DIR_PATH = f"{TV_SHOW_FOLDER}{name}({year})"
    if not os.path.isdir(DIR_PATH):
        os.makedirs(DIR_PATH)
        logging.info(f"Createing a dir at {DIR_PATH}")
    return DIR_PATH

def rchop(s, suffix='\n'):
    if suffix and s.endswith(suffix):
        return s[:-len(suffix)]
    return s

def get_media_metadata(search):
    """Search the and only get the first result"""
    url = f"https://api.themoviedb.org/3/search/multi?query={sanitize_filename(search)}&api_key={API_KEY}"
    response = requests.request("GET", url)
    if response.ok:
        return response.json()['results'][0]
    logging.debug(f"No metadata found for {sanitize_filename(search)}")

def new_filename(name):
    import re
    regex_dict ={
        'movie_9x':{
            'regex': re.compile(r"((?P<name>.*?)\s+)((?P<dt>\((?:(?P<day>\d+)\s(?P<month>.+)\s)?(?P<yr>\d\d\d\d)\))\s+)((?P<web>(?P<host>(?:[A-Za-z0-9](?:[A-Za-z0-9-]{0,61})?)(\.))+(?P<tld>[a-z0-9][a-z0-9-]{0,61}[a-z0-9]))\s+)((?P<eposide>(?:S\d\d(E\d\d)?)?)\s)?(.*)(\[(?P<file_size>.*)\])$"),
            'replace': f"\g<name> \g<eposide>\g<dt>"
        },
    } 
    
    for source, pattern in regex_dict.items():
        if re.match(pattern['regex'], name):
            return re.sub(pattern['regex'], pattern['replace'], name)
    return name

for file in sys.stdin:
    file = Path(rchop(file))
    dir, file_name, extension = file.parent, file.stem, file.suffix
    if extension.lower() in IMG_EXT:
        if 'Screenshot' in file_name:
            dst = f'{ONE_DRIVE}/Documents/Pictures/ScreenShots'
        elif 'WhatsApp' in file_name:
            dst = f'{ONE_DRIVE}/Documents/Pictures/WhatsApp'
        else:
            dst = f'{ONE_DRIVE}/Documents/Pictures'
        logging.info(f'mv: {file} --> {dst}')
        shutil.move(file, dst)
    elif extension.lower() in VIDEO_EXT:
        newname = new_filename(file_name)
        if newname == file_name:
            # the new_filename will return the original name if there is not regex match so just move the file to Temp dir
            dst = f'{VIDEO_DRIVE}/temp/'
        else:
            metadata = get_media_metadata(newname)
            if metadata:
                if metadata['media_type'] == 'tv':
                    dst = subfolder_tv(metadata) + "/" + newname + extension
                elif metadata['media_type'] == 'movie':
                    # todo movie sort
                    dst = MOVIES_FOLDER + "/" + newname + extension
            else:
                logging.info(f'No Metadata found for {file_name}')
        logging.info(f'mv: {file} --> {dst}')
        shutil.move(file, dst)