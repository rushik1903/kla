import math
import numpy as np
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
        temp=dict()
        temp['layer'] = int(polygon[1].split()[1])
        temp['datatype'] = int(polygon[2].split()[1])
        items = polygon[3].split()
        temp['no_of_points'] = int(items[1])
        temp['points'] = []
        for i in range(2,len(items),2):
            temp['points'].append([int(items[i]), int(items[i+1])])
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

def writePolysToFile(outputFileLocation,source,resIndices,header,footer):
    f = open(outputFileLocation, "w")
    f.write(header)
    for i in range(len(source)):
        if i in resIndices:
            poly = source[i]
            f.write("boundary\n")
            f.write('layer '+str(poly['layer'])+'\n')
            f.write('datatype '+str(poly['datatype'])+'\n')
            f.write('xy ')
            f.write(str(poly['no_of_points'])+" ")
            for point in poly['points']:
                f.write("  "+str(point[0])+" "+str(point[1]))
            f.write("  "+str(poly['points'][0][0])+" "+str(poly['points'][0][1]))
            f.write("\nendel\n")
    f.write(footer)


def cross(a,b,c):
    v1 = [b[0]-a[0], b[1]-a[1],0]
    v2 = [c[0]-b[0], c[1]-b[1],0]
    return np.cross(v1,v2)

def crossWithVectors(a,b):
    return np.cross(a,b)

def dist(a,b):
    return math.sqrt((a[0]-b[0])*(a[0]-b[0])+(a[1]-b[1])*(a[1]-b[1]))


def convertFromPolyToArray(poly):
    poly['points'].pop()
    res = []
    for i in range(len(poly['points'])):
        x = i
        if(x>=len(poly['points'])):
            x -= len(poly['points'])
        a = poly['points'][x]
        if(x+1>=len(poly['points'])):
            b = poly['points'][x+1 - len(poly['points'])]
        else:
            b = poly['points'][x+1]
        if(x+2>=len(poly['points'])):
            c = poly['points'][x+2 - len(poly['points'])]
        else:
            c = poly['points'][x+2]
        res.append(dist(a,b))
        res.append(cross(a,b,c))
    return res






def checkSimilaritySub(poly1,poly2):
    for i in range(0,len(poly1),2):
        if(poly1[i] != poly2[i]):
            return False
        for j in range(len(poly1[i+1])):
            if(poly1[i+1][j] != poly2[i+1][j]):
                return False
    return True
def checkSimilarity(poly1,poly2):
    if(len(poly1)!=len(poly2)):
        return False
    for i in range(0,len(poly1),2):
        temp=[]
        for j in range(len(poly1)):
            x=i+j
            if(x>=len(poly1)):
                x-=len(poly1)
            temp.append(poly1[x])
        if(checkSimilaritySub(temp,poly2) == True):
            return True
    return False

def SubtractVectors(a,b):
    return [a[0]-b[0], a[1]-b[1]]

def CalcMA(poi1,poi2):
    centerPoi1 = Center(poi1)
    centerPoi2 = Center(poi2)
    commonVector = SubtractVectors(centerPoi1, centerPoi2)
    
    poi1D = []
    for i in range(len(poi1['points'])):
        tempVector = SubtractVectors(poi1['points'][i], centerPoi1)
        poi1D.append(crossWithVectors(tempVector, commonVector))
    poi2D = []
    for i in range(len(poi2['points'])):
        tempVector = SubtractVectors(poi2['points'][i], centerPoi2)
        poi2D.append(crossWithVectors(tempVector, commonVector))
    return [commonVector,poi1D,poi2D]


source,sourceStr,sourceHeader,sourceFooter = fileToPoly("Source.txt")
poi,poiStr,poiHeader,poiFooter = fileToPoly("POI.txt")

sourceCmpArray=[]
for poly in source:
    sourceCmpArray.append(convertFromPolyToArray(poly))
poiCmpArray=[]
for poly in poi:
    poiCmpArray.append(convertFromPolyToArray(poly))


def Center(poi):
    sum = [0,0]
    for i in range(len(poi['points'])):
        sum[0]+=poi['points'][i][0]
        sum[1]+=poi['points'][i][1]
    sum[0]/=len(poi['points'])
    sum[1]/=len(poi['points'])
    return sum
poi1 = poi[0]
poi2 = poi[1]
poi1['points'].pop()
poi2['points'].pop()
MApoi = CalcMA(poi1,poi2)

res={
    0:[],
    1:[]
}
total=0
for i in range(len(sourceCmpArray)):
    for j in range(len(poiCmpArray)):
        if(checkSimilarity(sourceCmpArray[i], poiCmpArray[j])):
            res[j].append(i)
            total+=1

# def comapareArrays(arr1,arr2):
#     if(len(arr1) != len(arr2)):
#         return False
#     for i in range(len(arr1)):
#         for j in range(len(arr1)):
#             x=j+i
#             if(x>len(arr1)):
#                 x-=len(arr1)
#             if(arr1[j] == arr2[j+i]):

def compareArrays(l1, l2):
    if len(l1) != len(l2):
        return False
    if not l1:
        return True
    a = l1[0]
    for i, x in enumerate(l2):
        if a == x:
            if l1 == l2[i:] + l2[:i]:
                return True
    return False

# return [commonVector,poi1D,poi2D]
def CompareMA(MA1,MA2):
    if(MA1[0] != MA2[0]):
        return False
    if(compareArrays(MA1[2],MA2[2]) and compareArrays(MA1[1],MA2[1])):
        return True
    return False

print(res)
ans = 0
for i in res[0]:
    for j in res[1]:
        temp = CalcMA(source[i],source[j])
        if(CompareMA(temp,MApoi)):
            print("h")
            ans += 1

print(ans)



# writePolysToFile("mile4.txt",source,res,poiHeader,poiFooter)