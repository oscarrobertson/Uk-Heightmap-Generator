import png
import sys
import shutil

##FLAGS:
## -c   apply full contrast to region
## -cm  manual contrast settings
## -a   specifying starting coordinates

##applies contrast given parameters
def customContrast(sto,add,divide):
    newSto = []
    for row in sto:
        newRow = []
        for elem in row:
            #account for exceeding max and min
            factor = 2**16/divide
            newElem = int((elem+add)*factor)
            if newElem >= 2**16:
                newElem = 2**16-1
            elif newElem < 0:
                newElem = 0
            newRow.append(newElem)
        newSto.append(newRow)
    return newSto

## funcion to apply full contrast to a store array
def findScaleFactors(sto):
    maximum = 0
    minimum = 1000
    for row in sto:
        a = max(row)
        b = min(row)
        if a > maximum:
            maximum = a
        if b < minimum:
            minimum = b
    minFac = max(minimum,-minimum)
    factor = 2**16/(maximum+minFac)
    newSto = []
    for row in sto:
        newRow = [int((x-minimum)*factor) for x in row]
        newSto.append(newRow)
    return newSto

def baseCoord(regionName):
    try:
        with open(regionName + "00.asc", 'r') as f:
            f.readline()
            f.readline()
            ##finds the base point for the region
            BASEX = int(f.readline()[10:])
            BASEY = int(f.readline()[10:])
            return (BASEX,BASEY)
    except:
        print "No zero file for region: " + regionName
        print "Please specify starting co-ordinates as two more options and use the -a flag"
        sys.exit("Could not establish starting co-odinates")
        return False


## this function builds the map for a region
## region name is 2 capital letters
## fullContrast is boolean
def makeMap(regionName, fullContrast):
    total = []
    newRow = []
    baseFileName1_1 = regionName.lower() + "/" + regionName.upper()+"0" ##"SP0"
    baseFileName1_2 = regionName.lower() + "/" + regionName.upper() ##"SP"
    baseFileName2 = ".asc"
    store = []

    startingCoord = baseCoord(baseFileName1_2)
    BASEX = startingCoord[0]
    BASEY = startingCoord[1]
    
    for j in range(100):
        try:
            if j<10:
                base = baseFileName1_1
            else:
                base = baseFileName1_2
            with open(base + str(j) + baseFileName2, 'r') as f:
                ncols = int(f.readline()[6:])
                nrows = int(f.readline()[6:])
                xllcorner = int(f.readline()[10:])
                yllcorner = int(f.readline()[10:])
                cellsize = int(f.readline()[9:])
                x_val = (xllcorner-BASEX)/(cellsize)
                y_val = (yllcorner-BASEY)/(cellsize)

                ##builds a grid for one of the 100 sections of the region
                for i in range(nrows):
                    newRow = [int(float(k)) for k in f.readline().split()]
                    total.append(newRow)
                    newRow = []

                ## if the row has x position 0 then just add a row to the store    
                if x_val == 0:
                    for l in range(len(total)-1,-1,-1):
                        store.append(total[l])
                ##if not 0 it had to be appended it in the right place        
                else:
                    z = 0
                    ##values set for proper allingment
                    for l in range(y_val-9*nrows,y_val-10*nrows,-1):
                        store[l] += total[z]
                        z += 1
                
                ##for testing
##                f = open('#output' + str(j)+'.png', 'wb') 
##                w = png.Writer(200, 200, greyscale=True)
##                w.write(f, total)
##                f.close()
                
                total = []
        except:
            ##this means that the file does not exist yet
            ##make a flat empty one to process
            print "Err on: " + str(j)
    store.reverse()

    if (fullContrast == True):
        ##store = customContrast(store,320,-47)
        store = findScaleFactors(store)
    
    f = open('output' + '-' + str(BASEX) + '-' + str(BASEY) + '.png', 'wb') 
    w = png.Writer(2000, 2000, greyscale=True, bitdepth=16)
    w.write(f, store)
    f.close()
    store = []

def main():
    makeMap("sp",True)

main()
