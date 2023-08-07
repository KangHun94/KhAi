import laspy
import numpy
from tqdm import tqdm

def main():
    LasData = laspy.read('/home/kh/Git/Repo/KhAi/0_BaseData/SDFloor.las')

    i = 0
    for name in LasData.points.array.dtype.names:
        if(name == 'red'):
            red = i
        elif(name == 'green'):
            green = i
        elif(name == 'blue'):
            blue = i
        i += 1

    LasDataArray = LasData.points.array
    Len = len(LasDataArray)
    a = []
    for i in tqdm(range(Len), desc = 'Color 추출중'):
        aa = []
        aa.append(LasDataArray[i][red])
        aa.append(LasDataArray[i][green])
        aa.append(LasDataArray[i][blue])
        a.append(aa)

    print(a[0])

if __name__ == '__main__':
    main()