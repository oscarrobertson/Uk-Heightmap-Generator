import os

rootdir = 'C:\Users\Oscar\Downloads\Terrain Data\data\data'

for files in os.walk(rootdir):
    for file in files:
        print file
