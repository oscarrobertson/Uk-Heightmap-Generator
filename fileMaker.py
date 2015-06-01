import os

##renames the orignal ascii files into a more useful format

rootdir = 'C:\Users\Oscar\Downloads\Terrain Data\data\data\\'

for filename in os.listdir(rootdir):
    xllcorner = ""
    yllcorner = ""
    with open(rootdir + filename,'r') as f:
        ncols = int(f.readline()[6:])
        nrows = int(f.readline()[6:])
        xllcorner = f.readline()[10:].rstrip()
        yllcorner = f.readline()[10:].rstrip()
        cellsize = int(f.readline()[9:])
    os.rename(rootdir + filename, rootdir + xllcorner + '-' + yllcorner + '.asc')
    if ncols != 200 or nrows != 200 or cellsize != 50:
        print filename
