import requests
import re
import os
import sys, shutil, logging
from sys import stdout
from pathlib import Path

# Create and configure logger
handlers = [
    logging.FileHandler(os.path.expanduser('~/.script.log')),
    logging.StreamHandler(stdout),
    ]
logging.basicConfig(level=logging.DEBUG,handlers=handlers, format="%(asctime)s;%(levelname)s;%(message)s")


# The API key is for the movie db api
API_KEY = '428798c163a4628d3ce00c9964f304fc'
VIDEO_DRIVE = '/Volumes/SSD1/Videos/'
TV_SHOW_FOLDER = "/Volumes/SSD1/Videos/TV_Shows/"
MOVIES_FOLDER = "/Volumes/SSD1/Videos/Movies/"

def sanitize_filename(filename):
    filename = filename.replace("_", " ")
    filename = filename.replace(".", " ")
    filename = re.sub(r"(\(.*\))", "", filename)
    filename = re.sub(r"S\d\d(E\d\d)?", "", filename)
    return filename

def subfolder_tv(metadata):
    year = metadata['first_air_date'].split("-")[0]
    DIR_PATH = f"{TV_SHOW_FOLDER}{metadata['name']}({year})"
    if not os.path.isdir(DIR_PATH):
        os.makedirs(DIR_PATH)
        logging.info(f"Create a dir at {DIR_PATH}")
    return DIR_PATH

    

def rchop(s, suffix='\n'):
    if suffix and s.endswith(suffix):
        return s[:-len(suffix)]
    return s

def get_media_metadata(search):
    url = f"https://api.themoviedb.org/3/search/multi?query={sanitize_filename(search)}&api_key={API_KEY}"
    response = requests.request("GET", url)
    if response.ok:
        return response.json()['results'][0]
    logging.debug(f"No metadata found for {sanitize_filename(search)}")

for file in sys.stdin:
    file = Path(rchop(file))
    logging.info(file)
    dir, file_name, extension = file.parent, file.stem, file.suffix
    metadata = get_media_metadata(file_name)
    category  = metadata['media_type']
    if metadata:
        if category == 'tv':
            dst = subfolder_tv(metadata)
        elif category == 'movie':
            dst = MOVIES_FOLDER
        logging.info(f'mv: {file} --> {dst}')
        shutil.move(file, dst)
    else:
        logging.info(f"No Metadata found for {file_name} so skipping")