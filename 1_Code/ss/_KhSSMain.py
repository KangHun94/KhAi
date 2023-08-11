import os
from A_KhConfigReader import A_KhConfigReader
from B_KhCloudPointReader import B_KhCloudPointReader
from C_KhSS import C_KhSS
from D_KhSave import D_KhSave
import time

def main():
    #Config File 읽어오기
    TopFolderPath = os.getcwd()
    ConfigFilePath = TopFolderPath + "/config/khconfig.txt"
    ConfigReader = A_KhConfigReader(ConfigFilePath)
    config = ConfigReader.Get_Config()

    #Cloud File 읽고 Text File로 변환하여 저장, 이미 있는 친구는 Text File에서 읽어옴
    BaseDataInterimFolderPath = config["path"]["Interim"] + "BaseData_Txt/"
    CloudPointReader = B_KhCloudPointReader(config["path"]["BaseData"],BaseDataInterimFolderPath)

    SS = C_KhSS()
    SS.SettingSS(config['model']['Name'] ,config["path"]["SS"])
    SS.Run(CloudPointReader.Get_Data())

    Save = D_KhSave()
    Save.ResultDataSave(SS.Get_ResultData(),config['save']['SSLabel'],config['path']['Result'], config['path']['Interim'],
                      CloudPointReader.Get_ChoiceFileName() ,config['LabelToName'] ,CloudPointReader.Get_LasFileInfo())
    
    while(not Save.Get_CheckThreadEnd()):
        print("")
        print("서브 쓰레드 종료 대기중")
        print("")
        time.sleep(1)

if __name__ == '__main__':
    main()