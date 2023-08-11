import os
import threading
from datetime import datetime
import laspy
import numpy as np
from tqdm import tqdm

class D_KhSave:

    def __init__(self) -> None:
        pass


    def ResultDataSave(self,ResultData,SaveLabels,ResultPath,InterimPath,LasDataFileName, LabelToName,LasFileInfo = None):
        SavePointAccordingToLableThreadArray = []
        ResultSaveFolder = ResultPath + str(datetime.now().date()) + '/' 
        if(not os.path.isdir(ResultSaveFolder)):
            os.mkdir(ResultSaveFolder)
        ResultSaveFolder += LasDataFileName+'/'
        if(not os.path.isdir(ResultSaveFolder)):
            os.mkdir(ResultSaveFolder)

        InterimSaveFolder = InterimPath + "LeftPoint/" + str(datetime.now().date()) +  '/'
        if(not os.path.isdir(InterimSaveFolder)):
            os.mkdir(InterimSaveFolder)
        InterimSaveFolder += LasDataFileName +  '/'
        if(not os.path.isdir(InterimSaveFolder)):
            os.mkdir(InterimSaveFolder)

        ResultSavePath = ResultSaveFolder + str(len(os.listdir(ResultSaveFolder))) +  '/'
        if(not os.path.isdir(ResultSavePath)):
            os.mkdir(ResultSavePath)

        InterimSavePath = InterimSaveFolder + str(len(os.listdir(InterimSaveFolder))) +  '/'
        if(not os.path.isdir(InterimSavePath)):
            os.mkdir(InterimSavePath)

        #분류
        IntSaveLabels, DataWithLabels = self.ClassifyDataWithLabels(ResultData,SaveLabels)

        self.ThreadEnd = []

        #쓰레드 준비
        for i in IntSaveLabels:
            if(i == (len(IntSaveLabels) - 1)):
                self.ThreadEnd.append(False)
                SavePointAccordingToLableThreadArray.append(
                threading.Thread(target=self.SavePointAccordingToLable_Txt,args=(DataWithLabels[len(DataWithLabels)-1],LasDataFileName,InterimSavePath)))
            else:
                self.ThreadEnd.append(False)
                SavePointAccordingToLableThreadArray.append(
                threading.Thread(target=self.SavePointAccordingToLable_Las,args=(DataWithLabels[i],ResultSavePath,i,LabelToName,LasFileInfo)))
        
        #쓰레드 시작
        for SavePointAccordingToLableThread in SavePointAccordingToLableThreadArray:
            SavePointAccordingToLableThread.daemon = True
            SavePointAccordingToLableThread.start()


    def ClassifyDataWithLabels(self,ResultData,SaveLabels):
        DataWithLabels = []
        IntSaveLabels = []
        for LabelNumber in SaveLabels:
            if(LabelNumber == ' ' or LabelNumber == ','):
                continue
            DataWithLabel = {'points':[] , 'color':[]}
            DataWithLabels.append(DataWithLabel)
            IntSaveLabels.append(int(LabelNumber))
        DataWithLabel = {'points':[] , 'color':[]}
        DataWithLabels.append(DataWithLabel)
        LeftLabelNumber = len(IntSaveLabels)
        IntSaveLabels.append(LeftLabelNumber)

        SaveDataLength = len(ResultData["points"])
        Points = ResultData["points"]
        Colors = ResultData["color"]
        Label = ResultData["label"]
        for i in tqdm(range(SaveDataLength), desc = 'ClassifyDataWithLabels'):
            for LabelNumber in IntSaveLabels:
                if(LabelNumber == LeftLabelNumber):
                    DataWithLabels[LabelNumber]['points'].append(Points[i])
                    DataWithLabels[LabelNumber]['color'].append(Colors[i])
                    break
                if(Label[i] == LabelNumber):
                    DataWithLabels[LabelNumber]['points'].append(Points[i])
                    DataWithLabels[LabelNumber]['color'].append(Colors[i])
                    break
        return IntSaveLabels, DataWithLabels
        

    #Las로 저장할 친구들
    def SavePointAccordingToLable_Las(self,SaveDataWithLabel,ResultSavePath ,LabelNum, LabelToName,LasFileInfo = None):
        ResultSavePath = ResultSavePath + LabelToName[str(LabelNum)] +".las"
        
        point_count = len(SaveDataWithLabel['points'])
        filler = np.empty((point_count,1), dtype = int)
        pointrecord = laspy.create(file_version="1.4", point_format=7)
        pointrecord.header.point_count = point_count
        pointrecord = laspy.create(point_format=7,file_version="1.4") 
        points = np.ascontiguousarray(SaveDataWithLabel['points'], dtype='float32')
        color = np.ascontiguousarray(SaveDataWithLabel['color'], dtype='uint8')*256

        if(LasFileInfo == None):
            intensity = 0    
            bit_fields = 0
            pointrecord.header.offsets = np.floor(np.min(points,axis=1))
            pointrecord.header.scales = np.array([0.001,0.001,0.001 ], dtype=np.float32)
        else:
            intensity = LasFileInfo['intensity']
            bit_fields = LasFileInfo['bit_fields']
            pointrecord.header.offsets = LasFileInfo['offset']
            pointrecord.header.scales = LasFileInfo['scales']


        pointrecord.x = points[:,0]
        pointrecord.y = points[:,1]
        pointrecord.z = points[:,2]
        filler.fill(intensity)
        pointrecord.intensity = filler[:,0]
        filler.fill(bit_fields)
        pointrecord.bit_fields = filler[:,0]
        pointrecord.red = color[:,0]
        pointrecord.green = color[:,1]
        pointrecord.blue = color[:,2]
        pointrecord.write(ResultSavePath)

        self.ThreadEnd[LabelNum] = True


    #나머지 txt로 저장할 친구들
    def SavePointAccordingToLable_Txt(self,SaveDataWithLabel, LasDataFileName,InterimSavePath):
        InterimSavePath = InterimSavePath + LasDataFileName + "LeftPoint.txt"

        SaveDataLength = len(SaveDataWithLabel['points'])
        if(SaveDataLength > 0):
            SaveFile = open(InterimSavePath , 'w')
            for i in tqdm(range(SaveDataLength), desc = 'All left point saving'):
                WriteData = ''
                for Point in SaveDataWithLabel["points"][i]:
                    WriteData += format(float(Point),'.3f') + ' '
                for Color in SaveDataWithLabel["color"][i]:
                    WriteData += str(int(Color)) + ' '
                WriteData += '\n'
                SaveFile.write(WriteData)
            SaveFile.close()
        
        self.ThreadEnd[len(self.ThreadEnd) - 1] = True

    
    def Get_CheckThreadEnd(self):
        for ThreadEnd in self.ThreadEnd:
            if(ThreadEnd == False):
                return False
            
        return True

