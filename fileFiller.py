import os

##makes a flat sea tile

rootdir = 'C:\Users\Oscar\Downloads\Terrain Data\data\data\\'

row = "-4 "*200
f = open("BASE.asc","w")
f.write("ncols 200\n")
f.write("nrows 200\n")
f.write("xllcorner 0\n")
f.write("yllcorner 0\n")
f.write("cellsize 50\n")

row = "-4 "*199 + "-4\n"

for i in range(200):
    f.write(row)

f.close()
