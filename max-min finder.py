import os

## finds the maximum and minimum points in the data set

rootdir = 'C:\Users\Oscar\Downloads\Terrain Data\data\data\\'

maximum = 0
minimum = 2**16
for filename in os.listdir(rootdir):   
    with open(rootdir + filename,'r') as f:
        ncols = int(f.readline()[6:])
        nrows = int(f.readline()[6:])
        xllcorner = f.readline()[10:].rstrip()
        yllcorner = f.readline()[10:].rstrip()
        cellsize = int(f.readline()[9:])
        for i in range(nrows):
            row = [int(round(float(k))) for k in f.readline().split()]
            a = max(row)
            b = min(row)
            if a > maximum:
                maximum = a
            if b < minimum:
                minimum = b
print maximum,minimum

## output (takes a while)
## 1345 -120
