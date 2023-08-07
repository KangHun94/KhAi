import os
from A_KhConfigReader import A_KhConfigReader
from B_KhCloudPointReader import B_KhCloudPointReader
from C_KhSS import C_KhSS
from D_KhSave import D_KhSave

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
    SS.SettingSS(config["path"]["SS"])
    SS.Run(CloudPointReader.Get_Data())

    Save = D_KhSave()

if __name__ == '__main__':
    main()