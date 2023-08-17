import os
from a_KhConfigReader import a_KhConfigReader
from b_KhCloudPointReader import b_KhCloudPointReader

def main():
    #Config File 읽어오기
    TopFolderPath = os.getcwd()
    ConfigFilePath = TopFolderPath + "/config/khconfig.txt"
    ConfigReader = a_KhConfigReader(ConfigFilePath)
    config = ConfigReader.Get_Config()

    #Left CloudPoint Txt File -> Bin File로 변환
    TxtToBinChanger = b_KhCloudPointReader(config['path']['Interim'])



if __name__ == '__main__':
    main()