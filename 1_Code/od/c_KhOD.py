from mmdet3d.apis import inference_detector, init_model

class c_KhOD:
    def __init__(self) -> None:
        pass

    def SettingOD(self,ConfigFile,CheckPointFile):
        self.Model = init_model(ConfigFile, CheckPointFile, device='cuda:0')


    def Run(self,DataPath):
        print('Model Inference Ready')
        self.Result, self.Data = inference_detector(self.Model,DataPath)

        self.bboxes_3d = self.Result._pred_instances_3d['bboxes_3d']
        self.labels_3d = self.Result._pred_instances_3d['labels_3d']
        self.scores_3d = self.Result._pred_instances_3d['scores_3d']
