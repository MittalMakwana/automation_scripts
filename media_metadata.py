import json

# make sure to hve media-info library added or mac it would be
# brew install media-info
from pymediainfo import MediaInfo

file_path = "File path"
mi = MediaInfo.parse(file_path, output="JSON")
metadata = json.loads(mi)
print(json.dumps(metadata, indent=4))