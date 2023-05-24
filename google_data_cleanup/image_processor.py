import os
import platform
from pathlib import Path
import json
import sys
import logging
from GPSPhoto.gpsphoto import GPSInfo, GPSPhoto
from datetime import datetime

from get_metadata import check_metadata
from file_operations import rename_file, update_time, organize_file, move_file, clean_up

logging.basicConfig(stream=sys.stdout, level=logging.INFO)


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


def image_processing(image_files, dst):
    '''
    Move all the files to the destination
    Update GPS
    update time
    Organize files
    
    '''
    for file in image_files:
        new_file_path = move_file(file, dst)
        if check_metadata(new_file_path):
            update_image_gps(new_file_path)
            update_time(new_file_path)
            clean_up(new_file_path)
        else:
            logging.info(f'No .json metadata file found for file:{new_file_path}')
            logging.info("Updating Time using the file name")
            update_time(new_file_path)
        organize_file(new_file_path, dst)