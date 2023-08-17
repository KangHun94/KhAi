import os
import glob
import open3d as o3d
import numpy as np

class b_KhCloudPointReader:

    def __init__(self,InterimPath):
        LeftPointFolderPath = InterimPath + 'LeftPoint'
        assert os.path.isdir(LeftPointFolderPath) , 'B_KhTxtToBinChanger __init__ - config path error'
        
        self.ChoiceLoadCustomData(LeftPointFolderPath)
        

    def ChoiceLoadCustomData(self,path):
        GlobDatas = glob.glob(path + "/*")
        i = 0
        for GlobData in GlobDatas:
            FileName = os.path.basename(GlobData)
            print('Index' + str(i) + ' - ' + str(FileName))
            i += 1
        print("Input To Select DateFolder Index")
        self.ChoiceDateIndex = int(input()) #날짜 선택
        ChoiceDateFolder = GlobDatas[self.ChoiceDateIndex]

        GlobDatas = glob.glob(ChoiceDateFolder + "/*")
        i = 0
        for GlobData in GlobDatas:
            FileName = os.path.basename(GlobData)
            print('Index' + str(i) + ' - ' + str(FileName))
            i += 1
        print("Input To Select DataFolder Index")
        self.ChoiceDataFolderIndex = int(input()) #폴더 선택(파일 이름)
        ChoiceDataFolder = GlobDatas[self.ChoiceDataFolderIndex]

        GlobDatas = glob.glob(ChoiceDataFolder + "/*")
        i = 0
        for GlobData in GlobDatas:
            FileName = os.path.basename(GlobData)
            print('Index' + str(i) + ' - ' + str(FileName))
            i += 1
        print("Input To Select NumberFolder Index")
        self.ChoiceNumberFolderIndex = int(input()) #폴더 선택(파일 이름)
        self.ChoiceNumberFolder = GlobDatas[self.ChoiceNumberFolderIndex]
        GlobDatas = glob.glob(self.ChoiceNumberFolder + "/*.*")

        if(len(GlobDatas) > 1): #bin File 있음
            BinFilePath = os.path.splitext(GlobDatas[0])[0] +".bin"
        else: #bin file 없음
            print("Bin File 제작 중")
            TxtData = o3d.io.read_point_cloud(GlobDatas[0], format = 'xyzrgb')
            TxtData.remove_non_finite_points()
            TxtDataPoints = np.array(TxtData.points, dtype=np.float32)
            TxtDataColors = np.array(TxtData.colors, dtype=np.float32)
            Datas = np.zeros([len(TxtDataPoints), 6], dtype=np.float32)
            for i in range(len(TxtDataPoints)):
                Datas[i][:3] = TxtDataPoints[i].astype(np.float32)
                Datas[i][3:] = TxtDataColors[i].astype(np.float32)

            BinFilePath = os.path.splitext(GlobDatas[0])[0] +".bin"
            with open(BinFilePath, 'wb') as f:
                f.write(Datas.tobytes())

        self.ChoiceFilePath = BinFilePath
        self.ChoiceFileName = str(os.path.splitext(os.path.basename(self.ChoiceFilePath))[0])