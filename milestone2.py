
def fileToPoly(inputFileLocation):
    file = open(inputFileLocation,'r')

    header = ""
    data = file.readline()
    while(data != "boundary\n"):
        header+=data
        data = file.readline()

    #stores polygons in string format
    polygons = []
    temp = []
    while(data != "endstr\n"):
        if(data=="boundary\n"):
            temp.append(data)
        elif(data=="endel\n"):
            temp.append(data)
            polygons.append(temp)
            temp=[]
        else:
            temp.append(data)
        data = file.readline()
    footer = ""
    while(data != ""):
        footer+=data
        data = file.readline()
    #this variable stores all my polygons in int format
    polys = []
    for polygon in polygons:
        temp = []
        temp.append(int(polygon[1].split()[1]))
        temp.append(int(polygon[2].split()[1]))
        items = polygon[3].split()
        for i in range(1,len(items)):
            temp.append(int(items[i]))
        polys.append(temp)
    file.close()
    # writing in file
    f = open("mile2.txt", "w")
    f.write(header)
    i=0
    for polygon in polygons:
        i+=1
        if(i==3):
            break
        for item in polygon:
            f.write(item)
    f.write(footer)
    f.close()
    return polys,polygons,header,footer


source,sourceStr,sourceHeader,sourceFooter = fileToPoly("Source.txt")
poi,poiStr,poiHeader,poiFooter = fileToPoly("POI.txt")

def writePolysToFile(outputFileLocation,polys,header,footer):
    f = open(outputFileLocation, "w")
    f.write(header)
    for poly in polys:
        f.write("boundary\n")
        f.write('layer '+str(poly[0])+'\n')
        f.write('datatype '+str(poly[1])+'\n')
        f.write('xy ')
        f.write(str(poly[2])+" ")
        for i in range(3,len(poly)):
            if(i%2==1):
                f.write(str(poly[i])+" ")
            else:
                f.write(str(poly[i])+"  ")
        f.write("\nendel\n")
    f.write(footer)

res=[]
for sourcePoly in source:
    for poiPoly in poi:
        if(sourcePoly == poiPoly):
            print(sourcePoly)
            res.append(sourcePoly)

writePolysToFile("mile2.txt",res,poiHeader,poiFooter)