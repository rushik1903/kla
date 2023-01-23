file = open('Format_Source.txt','r')

header = ""
data = file.readline()
while(data != "boundary\n"):
    header+=data
    data = file.readline()

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

print(header)
for i in range(2):
    for item in polygons[i]:
        print(item,end='')
# print(polygons)
file.close()