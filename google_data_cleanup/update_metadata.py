import os
import platform
from pathlib import Path
import json
import sys
import logging
from GPSPhoto.gpsphoto import GPSInfo, GPSPhoto
from datetime import datetime
import re
from get_metadata import get_creation_date, check_metadata

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

image_ext = ['.jpg', '.png', '.jpeg', '.heic']
video_ext = ['.mp4','mv4', '.3ga', '.mov']
audio_ext = ['.mp3']

DST = '/Volumes/SSD1/Google_Data/phase1c/'
SRC = '/Volumes/SSD1/Google_Data/phase1/'

regex = re.compile(r'(20\d\d)([01]\d)([0123]\d)_([012]\d)([0-5]\d)(\d\d)')


def organize_file(file, dst=DST):
    create_time =  datetime.fromtimestamp(get_creation_date(file))
    dir_path = Path(f'{dst}/{create_time.year}')
    if not Path(dir_path).is_dir():
        os.makedirs(dir_path)
        logging.info(f'mkdir: {dir_path}')
    move_file(file, dir_path)


def rename_file(path, sep=" ", rep="_", root_dir=False, recursive=False):
    dir, dir_list, filenames = next(os.walk(path))
    for f in filenames:
        new_file_name = os.path.basename(f).replace(sep, rep)
        full_path = os.path.join(dir, f)
        new_path = os.path.join(dir, new_file_name)
        os.rename(full_path, new_path)
    if root_dir:
        level_up_path = os.path.dirname(dir)
        new_dir = os.path.join(level_up_path, os.path.basename(dir).replace(sep, rep))
        os.rename(dir, new_dir)


def update_time(file):
    if Path(file).is_file() and Path(f'{file}.json').is_file():
        with open(f'{file}.json') as f:
            metadata = json.load(f)
        m_time = int(metadata['creationTime']['timestamp'])
        c_time = int(metadata['modificationTime']['timestamp'])
        os.utime(f'{file}', (c_time, m_time))
        logging.info(f"Updated using json c_time:{c_time} and m_time :{m_time} for {file}")
        return True
    elif Path(file).is_file() and re.search(regex, Path(file).name):
        _find = re.findall(regex, Path(file).name)[0]
        y,m,d,h,mm,s = [int(_) for _ in _find]
        c_time = datetime(y,m,d,h,mm,s).timestamp()
        os.utime(f'{file}', (c_time, c_time))
        logging.info(f"Updated using filename c_time:{c_time} and m_time :{c_time} for {file}")
        return True


def update_image_gps(file):
    try:
        with open(f'{file}.json') as f:
            metadata = json.load(f)
        cordinates = ( float(metadata['geoDataExif']['latitude']), float(metadata['geoDataExif']['longitude']) )
        altitude = int(metadata['geoDataExif']['altitude'])
        timestamp = int(metadata['photoTakenTime']['timestamp'])
        timestamp = datetime.utcfromtimestamp(timestamp)
        info = GPSInfo(cordinates, alt=altitude, timeStamp=timestamp)
        photo = GPSPhoto(file)
        photo.modGPSData(info, file)
        logging.info(f'Update GPS info for file {file} coord:{cordinates}, alt:{altitude}, timestamp:{timestamp}')
        return True
    except FileNotFoundError as e:
        logging.error('FileNotFound', e)
    except Exception as e:
        logging.error(e)


def move_file(src, dst=DST, metadata=True):
    if Path(src).is_file():
        if metadata:
            metadata_file = Path(f'{src}.json')
            if metadata_file.is_file():
                new_metadata_file = Path(f'{dst}/{Path(src).name}.json')
                os.rename(metadata_file, new_metadata_file)
                logging.info(f'mv: src:{metadata_file}, dst:{new_metadata_file}')
        new_path = Path(f'{dst}/{Path(src).name}')
        os.rename(Path(src), new_path)
        logging.info(f'mv: src:{src}, dst:{new_path}')
        return new_path

def clean_up(file):
    if check_metadata(file):
        metadata_file = check_metadata(file)
        os.remove(metadata_file)
        logging.info(f'rm: {metadata_file}')
    else:
        logging.error(f'rm: no metadata file found')

def image_processing(image_files):
    for file in image_files:
        new_file_path = move_file(file)
        if check_metadata(new_file_path):
            update_image_gps(new_file_path)
            clean_up(new_file_path)
        else:
            logging.info(f'No .json metadata file found for file:{new_file_path}')
        update_time(new_file_path)
        organize_file(new_file_path)

def scan_dir(dir):
    for path, dir, filenames in os.walk(dir):
        image_files = [f'{path}/{file}' for file in filenames if Path(file).suffix in image_ext]
        video_files = [f'{path}/{file}' for file in filenames if Path(file).suffix in video_ext]
        audio_files = [f'{path}/{file}' for file in filenames if Path(file).suffix in audio_ext]

        all_filenames = image_files + video_files + audio_files
        # Update all the create time and modified time
        # for file in all_filenames:
        #     update_time(file)
        
        image_processing(image_files)
        # vidoe_processing(video_files)
        # organize_files(image_files)



scan_dir(SRC)