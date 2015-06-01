import png
import sys

##GLOBALS
ELEMENT_WIDTH = 50
REGION_WIDTH_IN_ELEMENTS = 200
REGION_WIDTH = ELEMENT_WIDTH * REGION_WIDTH_IN_ELEMENT

## Identifies all regions in a given square
## and returns the filenames as a list
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
            output.append('data\\' + str(xtemp) + '-' + str(ytemp) + '.asc')
    return output

def main():
    ##get the regioin that needs to be created
    xll = 108000
    yll = 102000
    width = 12000

    ## build list of filenames where the data lies
    regionsNeeded = findRegions(xll,yll,width)

    ## build the 2d array of all squraes where the requested data exists
    
    

main()
