import png
import sys

##GLOBALS
ELEMENT_WIDTH = 50
REGION_WIDTH_IN_ELEMENTS = 200
REGION_WIDTH = ELEMENT_WIDTH * REGION_WIDTH_IN_ELEMENTS

## Identifies all regions in a given square
## Returns list of coordinates of lower left corner of all regions
def findRegions(x,y,w):
    xll = x/REGION_WIDTH * REGION_WIDTH
    yll = y/REGION_WIDTH * REGION_WIDTH
    xregions = []
    yregions = []
    ##populate x
    i = xll
    while i <= x+w:
        xregions.append(str(i))
        i += REGION_WIDTH
    ##populate y
    i = yll
    while i <= y+w:
        yregions.append(str(i))
        i += REGION_WIDTH
    output = []
    for xtemp in xregions:
        for ytemp in yregions:
            output.append((str(xtemp),str(ytemp)))
    return output

def makeFilename(x,y):
    return 'data\\' + str(x) + '-' + str(y) + '.asc'

## build 2d array for a region
def makeArrayForRegion(regionCoord):
    output = []
    filename = makeFilename(regionCoord[0],regionCoord[1])

    with open(filename,'r') as f:
        ncols = int(f.readline()[6:])
        nrows = int(f.readline()[6:])
        xllcorner = int(f.readline()[10:])
        yllcorner = int(f.readline()[10:])
        cellsize = int(f.readline()[9:])
        
        for i in range(nrows):
            newRow = [int(float(k)) for k in f.readline().split()]
            output.append(newRow)
            newRow = []

    return output

def appendMatrixLR(left,right):
    if len(left) != len(right):
        print "Matrix Dimension error"
        return False
    output = []
    for i in range(len(left)):
        newRow = left[i] + right[i]
        output.append(newRow)
    return output

def appendMatrixTB(top,bottom):
    ## basic check, not fully safe
    if len(top[0]) != len(bottom[0]):
        print "Matrix dimension error"
        return False
    output = top + bottom
    return output

def combineToColumns(regions,coords):
    output = []
    currentX = '-1'
    for i in range(len(regions)):
        ## if equal to last one then append
        if coords[i][0] == str(currentX):
            output[len(output)-1] = appendMatrixTB(regions[i],output[len(output)-1])
        else:
            output.append(regions[i])
            currentX = coords[i][0]
    return output

def combineToSquare(regions):
    output = regions[0]
    for i in range(1,len(regions)):
        output = appendMatrixLR(output,regions[i])
    return output

## input list of coordinates
## outputs 2d array of the combination of regions
def createDataArray(regionsNeeded):
    ## first construct a 2d array for each region and place in new list
    ## this list can be referenced using the regionsNeeded list
    regions = []
    for i in regionsNeeded:
        regions.append(makeArrayForRegion(i))

    ## combine regions into columns
    regions = combineToColumns(regions,regionsNeeded)

    ## combine columns into square
    regions = combineToSquare(regions)
    
    return regions

def main():
    ##get the region that needs to be created
    xll = 400000
    yll = 200000
    width = 30000

    ## build list of coordinates where the data lies
    regionsNeeded = findRegions(xll,yll,width)
  
    ## build the 2d array of all squraes where the requested data exists
    dataArray = createDataArray(regionsNeeded)
    

main()
