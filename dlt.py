arr = [1,2,3,4,5,6,7,8]

def rot(arr):
    for i in range(0,len(arr),2):
        temp=[]
        for j in range(len(arr)):
            x=i+j
            if(x>=len(arr)):
                x-=len(arr)
            print(x,end='')
            temp.append(arr[x])
        print()
        print(temp)

rot(arr)