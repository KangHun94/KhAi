import os
import open3d as o3d
import laspy
import numpy as np
import glob
from tqdm import tqdm
from pathlib import Path
import configparser

class B_KhCloudPointReader:

    def __init__(self,BasePath,Interimpath):
        assert os.path.isdir(BasePath) , 'B_KhCloudPointReader __init__ - BasePath error'
        assert os.path.isdir(Interimpath) , 'B_KhCloudPointReader __init__ - Interimpath error'

        #데이터 선택
        self.ChoiceDataPath = self.ChoiceLoadCustomData(BasePath)

        print("Data Reading...")

        #변환 했던 파일이 아니라면 변환 시켜서 저장한다
        if(not self.CheckTextFile(Interimpath)):
            Extension = os.path.splitext(self.ChoiceDataPath)[1]
            if(Extension == '.las'):
                self.LoadLasData(self.ChoiceDataPath)
            elif(Extension == '.txt'):
                self.LoadTextData(self.ChoiceDataPath)
            self.DataSave()
        else:
            self.LoadTextData(self.ChoiceTextDataPath)

        #Load Bin 만든다면 함수 안에 self.LasInfo = None 써줘야함

    def ChoiceLoadCustomData(self,path):
        GlobDatas = glob.glob(path + "/*.*")
        i = 0
        for GlobData in GlobDatas:
            FileName = os.path.basename(GlobData)
            print('Index' + str(i) + ' - ' + str(os.path.splitext(FileName)))
            i += 1
        print("Input To Select Data Index")
        self.ChoiceDataIndex = int(input())
        self.ChoiceFileName = str(os.path.splitext(os.path.basename(GlobDatas[self.ChoiceDataIndex]))[0])
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

        self.Set_LasFileInfo(LasData.points.array,LasData.header.offsets,LasData.header.scales)

        LasDataArray = LasData.points.array
        Len = len(LasDataArray)
        for i in tqdm(range(Len), desc = 'Color Loading'):
            Colors[i][0] = LasDataArray[i][red]/256.0
            Colors[i][1] = LasDataArray[i][green]/256.0
            Colors[i][2] = LasDataArray[i][blue]/256.0

        self.Data = {'point':Points, 'feat': Colors, 'label': np.zeros((len(Points),), dtype=np.int32)}

    def LoadTextData(self,path):
        CustomData = o3d.io.read_point_cloud(path, format = 'xyzrgb')
        CustomData.remove_non_finite_points()
        Points = np.array(CustomData.points, dtype=np.float32)
        Feat = np.array(CustomData.colors, dtype=np.float32)
        self.Data = {'point':Points, 'feat': Feat, 'label': np.zeros((len(Points),), dtype=np.int32)}
        self.LasInfo = None

    def DataSave(self):
        SaveDataLength = len(self.Data['point'])
        if(SaveDataLength > 0):
            SaveFile = open(self.ChoiceTextDataPath , 'w')
            WriteData = ""
            for i in tqdm(range(SaveDataLength), desc = 'Text File Saving'):
                for Point in self.Data['point'][i]:
                    WriteData += format(float(Point),'.3f') + ' '
                for Feat in self.Data['feat'][i]:
                    WriteData += str(int(Feat)) + ' '
                WriteData += '\n'
                SaveFile.write(WriteData)
                WriteData = ""
            SaveFile.close()
        
        if(self.LasInfo != None):
            config = configparser.ConfigParser()
            # 설정파일 오브젝트 만들기
            config['LasInfo'] = {}
            config['LasInfo']['intensity'] = str(self.LasInfo['intensity'])
            config['LasInfo']['bit_fields'] = str(self.LasInfo['bit_fields'])
            config['LasInfo']['offsetx'] = str(self.LasInfo['offset'][0])
            config['LasInfo']['offsety'] = str(self.LasInfo['offset'][1])
            config['LasInfo']['offsetz'] = str(self.LasInfo['offset'][2])
            config['LasInfo']['scalesx'] = str(self.LasInfo['scales'][0])
            config['LasInfo']['scalesy'] = str(self.LasInfo['scales'][1])
            config['LasInfo']['scalesz'] = str(self.LasInfo['scales'][2])
            # 설정파일 저장
            with open(os.path.dirname(self.ChoiceTextDataPath) + "/" + Path(self.ChoiceDataPath).stem +"LasInfo.txt", 'w', encoding='utf-8') as configfile:
                config.write(configfile)


    def Get_Data(self):
        return self.Data
    
    def Set_LasFileInfo(self,LasDatapointsArray,OffSet,Scales):
        i = 0
        for name in LasDatapointsArray.dtype.names:
            if(name == 'intensity'):
                intensityNum = i
            elif(name == 'bit_fields'):
                bit_fieldsNum = i
            i += 1
        self.LasInfo = {'intensity':LasDatapointsArray[0][intensityNum],'bit_fields' : LasDatapointsArray[0][bit_fieldsNum],'offset':OffSet,'scales':Scales}

    def Get_LasFileInfo(self):
        if(self.LasInfo == None):
            LasInfoFilePath = os.path.dirname(self.ChoiceTextDataPath) + "/" + Path(self.ChoiceDataPath).stem +"LasInfo.txt"
            if(os.path.isfile(LasInfoFilePath)):
                LasInfoConfig = configparser.ConfigParser()
                LasInfoConfig.read(LasInfoFilePath, encoding='utf-8')
                OffSet = np.array[float(LasInfoConfig['LasInfo']['offsetx']),float(LasInfoConfig['LasInfo']['offsety']),float(LasInfoConfig['LasInfo']['offsetz'])]
                Scales = np.array[float(LasInfoConfig['LasInfo']['scalesx']),float(LasInfoConfig['LasInfo']['scalesy']),float(LasInfoConfig['LasInfo']['scalesz'])]
                self.LasInfo = {'intensity':int(LasInfoConfig['LasInfo']['intensity']),
                                'bit_fields' : int(LasInfoConfig['LasInfo']['bit_fields']),
                                'offset':OffSet,'scales':Scales}
                return self.LasInfo
            return None
        return self.LasInfo

    def Get_ChoiceFileName(self):
        return self.ChoiceFileName
