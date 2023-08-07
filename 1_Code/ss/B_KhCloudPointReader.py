import os
import open3d as o3d
import laspy
import numpy as np
import glob
from tqdm import tqdm
from pathlib import Path

class B_KhCloudPointReader:

    def __init__(self,BasePath,Interimpath):
        assert os.path.isdir(BasePath) , 'B_KhCloudPointReader __init__ - BasePath error'
        assert os.path.isdir(Interimpath) , 'B_KhCloudPointReader __init__ - Interimpath error'

        #데이터 선택
        self.ChoiceDataPath = self.ChoiceLoadCustomData(BasePath)

        #변환 했던 파일이 아니라면 변환 시켜서 저장한다
        if(not self.CheckTextFile(Interimpath)):
            Extension = os.path.splitext(self.ChoiceDataPath)[1]
            if(Extension == '.las'):
                self.LoadLasData(self.ChoiceDataPath)
            elif(Extension == '.txt'):
                self.LoadTextData(self.ChoiceDataPath)
            self.DataSave()
        else:
            self.LoadTextData(self.ChoiceDataPath)

    def ChoiceLoadCustomData(self,path):
        GlobDatas = glob.glob(path + "/*.*")
        i = 0
        for GlobData in GlobDatas:
            FileName = os.path.basename(GlobData)
            print('Index' + str(i) + ' - ' + str(os.path.splitext(FileName)))
            i += 1
        self.ChoiceDataIndex = int(input())
        return GlobDatas[self.ChoiceDataIndex]

    def CheckTextFile(self,Interimpath):
        FileName = Path(self.ChoiceDataPath).stem
        self.ChoiceTextDataPath = Interimpath + FileName + '.txt'
        return os.path.isfile(self.ChoiceTextDataPath)


    def LoadLasData(self,path):
        LasData = laspy.read(path)
        xyz = np.array(LasData.xyz)
        Points = np.array(xyz, dtype=np.float32)
        Colors = np.zeros((Points.shape[0],Points.shape[1]), dtype=np.float32)

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
        for i in tqdm(range(Len), desc = 'Color Loading'):
            Colors[i][0] = LasDataArray[i][red]/255.0
            Colors[i][1] = LasDataArray[i][green]/255.0
            Colors[i][2] = LasDataArray[i][blue]/255.0

        self.Data = {'point':Points, 'feat': Colors, 'label': np.zeros((len(Points),), dtype=np.int32)}

    def LoadTextData(self,path):
        CustomData = o3d.io.read_point_cloud(path, format = 'xyzrgb')
        CustomData.remove_non_finite_points()
        Points = np.array(CustomData.points, dtype=np.float32)
        Feat = np.array(CustomData.colors, dtype=np.float32)
        self.Data = {'point':Points, 'feat': Feat, 'label': np.zeros((len(Points),), dtype=np.int32)}

    def DataSave(self):
        SaveDataLength = len(self.Data['point'])
        if(SaveDataLength > 0):
            SaveFile = open(self.ChoiceTextDataPath , 'w')
            WriteData = ""
            for i in tqdm(range(SaveDataLength), desc = 'Text File Saving'):
                for Point in self.Data['point'][i]:
                    WriteData += format(float(Point),'.3f') + ' '
                for Feat in self.Data['feat'][i]:
                    WriteData += format(float(Feat),'.3f') + ' '
                WriteData += '\n'
                SaveFile.write(WriteData)
                WriteData = ""
            SaveFile.close()

    def Get_Data(self):
        return self.Data
