import sys, re, os
from pathlib import Path
file_list = sys.stdin

def rchop(s, suffix='\n'):
    if suffix and s.endswith(suffix):
        return s[:-len(suffix)]
    return s

# Regex
schar = re.compile(r'[@]')
video_format = re.compile(r'(\d+p)')
website_reg = re.compile(r'(?:[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[a-z0-9])?\.)+[a-z0-9][a-z0-9-]{0,61}[a-z0-9]')

# Some regex to check

#Veer-Isha Nu Seemant (2022) www.9xMovie.casa 1080p HDRip Full Gujarati Movie ESubs [2GB]
regex_1 = re.compile(r'(?P<movie_name>.*)\s\((?P<movie_year>\d+)\)\s(?P<website>(?:[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[a-z0-9])?\.)+[a-z0-9][a-z0-9-]{0,61}[a-z0-9])\s(?P<format>\d*[pi]).*(?P<size>\[.*\])')

for file in file_list:
	file = Path(rchop(file))
	dir, file_name, extension = file.parent, file.stem, file.suffix
	new_file_name = re.sub(regex_1,r'\g<movie_name> \g<movie_year>', file_name)
	new_file_name = re.sub(video_format, '', file_name)
	new_file_name = re.sub(website_reg, '', file_name)
	new_file_path = f"{dir}/{new_file_name}{extension}"
	os.rename(file, new_file_path)