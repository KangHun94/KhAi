import open3d.ml.torch as ml3d
import open3d.ml as _ml3d

class C_KhSS:

    def __init__(self) -> None:
        pass

    def SettingSS(self,ModelName,ModelConfigPath):
        self.ModelName = ModelName
        self.ModelConfigPath = ModelConfigPath + self.ModelName + '.yml'
        self.ModelConfig = _ml3d.utils.Config.load_from_file(self.ModelConfigPath)

        if(self.ModelName == 'RandLANet'):
            self.RandLANetModel = ml3d.models.RandLANet(**self.ModelConfig.model)
            self.SSPipeline = ml3d.pipelines.SemanticSegmentation(self.RandLANetModel,None,device="gpu",**self.ModelConfig.pipeline)
            self.CheckPointFilePath = ModelConfigPath + self.ModelConfig['model']['ckpt_path']
            self.SSPipeline.load_ckpt(ckpt_path=self.CheckPointFilePath)

    def Run(self,Data):
        SSResult = self.SSPipeline.run_inference(Data)
        self.ResultData = [{'name': 'kh','points': Data["point"], 'color':Data["feat"],'label':SSResult["predict_labels"]}]

    def Get_ResultData(self):
        return self.ResultData