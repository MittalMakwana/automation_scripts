from file_operations import move_file, update_time, clean_up
from get_metadata import check_metadata

import logging, sys
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

def video_processing(video_files, dst):
    for file in video_files:
        new_file_path = move_file(file, dst)
        update_time(new_file_path)
    if check_metadata(new_file_path):
        clean_up(new_file_path)
    else:
        logging.info(f'No .json metadata file found for file:{new_file_path}')

    organize_file(new_file_path, dst)