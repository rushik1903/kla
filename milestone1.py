file = open('Format_Source.txt','r')

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
    print(polygon[3].split())
    items = polygon[3].split()
    for i in range(1,len(items)):
        temp.append(int(items[i]))
    polys.append(temp)
# print(polys)


print(header)
print(polygons)
file.close()

f = open("mile1.txt", "w")
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
