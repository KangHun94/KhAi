import os
import configparser

#config file을 읽어주는 클래스
class a_KhConfigReader:

    def __init__(self,path):
        assert os.path.isfile(path) , 'A_KhConfigReader __init__ - config path error'
        self.ConfigRead(path)

    def ConfigRead(self,path):
        self.Config = configparser.ConfigParser()
        self.Config.read(path, encoding='utf-8')

    def Get_Config(self):
        return self.Config