from image_processor import image_processing
from video_processor import video_processing
from file_operations import flatten, rename_file
import logging
import sys
import os
from pathlib import Path
import glob

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

IMG_EXT = ['.jpg', '.png', '.jpeg', '.heic']
VID_EXT = ['.mp4','mv4', '.3ga', '.mov']
AUD_EXT = ['.mp3']

DST = '/Volumes/SSD1/Google_Data/phase1c/'
SRC = '/Volumes/SSD1/Google_Data/final'



def scan_dir(dir):
    image_files, video_files, audio_files = [], [], []
    for root, dirs, files in os.walk(dir):
        for file in files:
            if Path(file).suffix.lower() in IMG_EXT:
                image_files.append(os.path.join(root, file))
            if Path(file).suffix.lower() in VID_EXT:
                video_files.append(os.path.join(root, file))
            if Path(file).suffix.lower() in AUD_EXT:
                audio_files.append(os.path.join(root, file))
    return(image_files, video_files, audio_files)

logging.info(f"Starting Renaming all the files in the : {SRC}")
rename_file(SRC)
logging.info(f"Scanning Dir:{SRC}")
image_files, video_files,audio_files= scan_dir(SRC)

logging.info("Processing image files")
# image_processing(image_files, DST)

logging.info("Processing Vidoes")
video_processing(video_files, DST)