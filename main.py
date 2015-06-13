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

    try:
        with open(filename,'r') as f:
            ncols = int(f.readline()[6:])
            nrows = int(f.readline()[6:])
            xllcorner = int(f.readline()[10:])
            yllcorner = int(f.readline()[10:])
            cellsize = int(f.readline()[9:])
            
            for i in range(nrows):
                newRow = [int(round(float(k))) for k in f.readline().split()]
                output.append(newRow)
                newRow = []
    ## if the file does not exist then use the base file
    except:
        baseFilename = "data\\BASE.asc"
        with open(baseFilename,'r') as f:
            ncols = int(f.readline()[6:])
            nrows = int(f.readline()[6:])
            f.readline()
            f.readline()
            xllcorner = regionCoord[0]
            yllcorner = regionCoord[1]
            cellsize = int(f.readline()[9:])

            for i in range(nrows):
                newRow = [int(round(float(k))) for k in f.readline().split()]
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

def refineDataArray(dataArray, xll, yll, width):
    ## the ll coord of the whole input square
    squareXll = xll/REGION_WIDTH * REGION_WIDTH
    squareYll = yll/REGION_WIDTH * REGION_WIDTH
    ## the ll coord of the desired region in terms of number of elements
    xStart = (xll-squareXll)/ELEMENT_WIDTH
    yStart = (yll-squareYll)/ELEMENT_WIDTH
    ## length of side of desired region in terms of number of elements
    length = width/ELEMENT_WIDTH
    output = []
    i = yStart
    while i < yStart+length:
        newRow = dataArray[i][xStart:xStart+length]
        output.append(newRow)
        i+=1
        
    return output

## takes an array and a float index
## returns float vaule of linear estimation of index
def advancedIndex(array,index):
    left = int(index)
    right = left + 1
    fraction = index - left
    if right == len(array):
        return array[left]
    difference = array[right]-array[left]
    return array[left] + difference*fraction

## lengthens the given 1D array using value estimation
def lengthenArray(arrayIn, outputLength):
    step = (len(arrayIn)-1)/float(outputLength-1)
    output = []
    k = 0
    for i in range(outputLength):
        output.append(k)
        k += step
    for i in range(len(output)):
        output[i] = int(round(advancedIndex(arrayIn,output[i])))
    return output

## transposes 2D array
def transpose(array):
    output = []
    for i in range(len(array[0])):
        newRow = []
        for j in range(len(array)):
            newRow.append(array[j][i])
        output.append(newRow)
    return output

## makes an array bigger
def resizeArray(array, width):
    temp = transpose(array)
    temp2 = []
    output = []
    for col in temp:
        temp2.append(lengthenArray(col,width))
    temp2 = transpose(temp2)
    for row in temp2:
        output.append(lengthenArray(row,width))
    return output

## find max and min points of data set
def findMinMax(data):
    maximum = 0
    minimum = 2**16
    for row in data:
        a = max(row)
        b = min(row)
        if a > maximum:
            maximum = a
        if b < minimum:
            minimum = b
    return [minimum,maximum]

## funcion to apply full contrast to a store array
def applyFullContrast(data):
    minMax = findMinMax(data)
    return applyContrast(data,minMax[0],minMax[1])

## applies full contrast over dataset using max and min from the whole country
def applyOverallContrast(data):
    return applyContrast(data,-120,1345)

## this function applies contrast to the given dataset given the min and max values
## it will turn the minimum you give into zero and the maximum into (2**16)-1
## points inbetween will be scaled linearly
def applyContrast(data,minimum,maximum):
    factor = (2**16-1)/(maximum-minimum)
    output = []
    for row in data:
        newRow = [int(round((x-minimum)*factor)) for x in row]
        output.append(newRow)
    return output

def main():
    ## location data to input 
    xll = 0
    yll = 800000
    width = 10000
    desiredSize = 1000

    ## contrast setting:
    ## 0 - Maximum contrast
    ## 1 - Maximum contrast over country
    ## 2 - Manual contrast, make sure you set the manualMax and manualMin values
    contrastSetting = 0

    ## ignore unless you set contrast setting to 2
    manualMin = -200
    manualMax = 2000
    
    ## build list of coordinates where the data lies
    regionsNeeded = findRegions(xll,yll,width)
  
    ## build the 2d array of all squraes where the requested data exists
    dataArray = createDataArray(regionsNeeded)
    
    ## refine array to just data included in the request
    dataArray = refineDataArray(dataArray, xll, yll, width)

    ## resize the array to the output size
    dataArray = resizeArray(dataArray,desiredSize)

    ## apply contrast
    if contrastSetting == 0:
        dataArray = applyFullContrast(dataArray)
    elif contrastSetting == 1:
        dataArray = applyOverallContrast(dataArray)
    else:
        dataArray = applyContrast(dataArray,manualMin,manualMax)

    ## print the png
    f = open('output.png', 'wb') 
    w = png.Writer(desiredSize, desiredSize, greyscale=True, bitdepth=16)
    w.write(f, dataArray)
    f.close()    

    return dataArray

main()
