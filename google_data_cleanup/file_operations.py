import os
import platform
import shutil
import json
import sys
import logging
import re

from GPSPhoto.gpsphoto import GPSInfo, GPSPhoto
from datetime import datetime
from pathlib import Path

from get_metadata import check_metadata


logging.basicConfig(stream=sys.stdout, level=logging.INFO)

regex = re.compile(r'(20\d\d)([01]\d)([0123]\d)_([012]\d)([0-5]\d)(\d\d)')

def rename_file(path, sep=" ", rep="_", root_dir=False):
    logging.info(f"renameing all files and dir in {path}, repalcing `{sep}` to `{rep}`")
    for dir, dir_list, filenames in os.walk(path, topdown=False):
        for f in filenames:
            if sep in os.path.basename(f):
                new_file_name = os.path.basename(f).replace(sep, rep)
                full_path = os.path.join(dir, f)
                new_path = os.path.join(dir, new_file_name)
                os.rename(full_path, new_path)
                logging.info(f"file rename: {full_path} to {new_path}")
        for d in dir_list:
            if sep in d:
                new_dir = os.path.join(dir, d.replace(sep,rep))
                old_dir = os.path.join(dir,d)
                os.rename(old_dir, new_dir)
                logging.info(f"dir rename: {old_dir}, {new_dir}")
    if root_dir:
        level_up_path = os.path.dirname(dir)
        new_dir = os.path.join(level_up_path, os.path.basename(dir).replace(sep, rep))
        os.rename(dir, new_dir)
        logging.info(f"dir rename: {dir} to {new_dir}")


def update_time(file):
    '''
    This functions update the c_time and m_time of a file
    '''
    if Path(file).is_file() and Path(f'{file}.json').is_file():  # Check if .json metadata file to update the metadata
        with open(f'{file}.json') as f:
            metadata = json.load(f)
        m_time = int(metadata['creationTime']['timestamp'])
        c_time = int(metadata['modificationTime']['timestamp'])
        os.utime(f'{file}', (c_time, m_time))
        logging.info(f"Updated using json c_time:{c_time} and m_time :{m_time} for {file}")
        return True
    elif Path(file).is_file() and re.search(regex, Path(file).name):  # Check for fine name to update the metadata
        _find = re.findall(regex, Path(file).name)[0]
        y,m,d,h,mm,s = [int(_) for _ in _find]
        c_time = datetime(y,m,d,h,mm,s).timestamp()
        os.utime(f'{file}', (c_time, c_time))
        logging.info(f"Updated using filename c_time:{c_time} and m_time :{c_time} for {file}")
        return True

def organize_file(file, dst=None):
    '''
    This function checks the creation time of the file and pust the file in corrosponging year folder at the DST
    '''
    create_time =  datetime.fromtimestamp(os.stat(file).st_birthtime)
    dst = Path(dst) if dst else Path(file).parent

    dir_path = Path.joinpath(dst, str(create_time.year))
    if not Path(dir_path).is_dir():
        os.makedirs(dir_path)
        logging.info(f'mkdir: {dir_path}')
    move_file(file, dir_path)


def move_file(src, dst, metadata=True):
    '''
    return path of new file location
    '''
    if Path(src).is_file():
        if metadata:
            metadata_file = f'{src}.json'
            if Path(metadata_file).is_file():
                new_metadata_file = f'{dst}/{Path(src).name}.json'
                shutil.move(metadata_file, dst)
                logging.info(f'mv: src:{metadata_file}, dst:{new_metadata_file}')
        new_path = f'{dst}/{Path(src).name}'
        i = 0
        while os.path.exists(new_path):
            i+=1
            file_parts = os.path.splitext(os.path.basename(src))
            new_path = os.path.join(dst, file_parts[0] + "_" + str(i) + file_parts[1])
        shutil.move(src, new_path)
        logging.info(f'mv: src:{src}, dst:{new_path}')
        return new_path

def clean_up(file):
    if check_metadata(file):
        metadata_file = check_metadata(file)
        os.remove(metadata_file)
        logging.info(f'rm: {metadata_file}')
        return True
    else:
        logging.error(f'rm: no metadata file found')


def flatten(directory):
    '''
    The function below will flatten a multi-level directory and move all files to the root directory deleting all sub-folders in the process. 
    Any files with the same name will have a count appended to their filename. Eg. 1_1.jpg
    useage: flatten(os.path.dirname("/Users/amit/my-folder"))
    '''
    for dirpath, _, filenames in os.walk(directory, topdown=False):
        for filename in filenames:
            i = 0
            source = os.path.join(dirpath, filename)
            target = os.path.join(directory, filename)
            while os.path.exists(target):
                i += 1
                file_parts = os.path.splitext(os.path.basename(filename))
                target = os.path.join(
                    directory,
                    file_parts[0] + "_" + str(i) + file_parts[1],
                )
            shutil.move(source, target)
            logging.info(f"mv: src:{source}, dst:{target}")

        if dirpath != directory:
            os.rmdir(dirpath)
            logging.info(f"rmdir: {dirpath}")