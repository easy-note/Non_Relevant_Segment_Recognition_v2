import os
import json
import natsort
from core.util.parser import DBParser
from core.util.database import DBHelper
from config.meta_db_config import subset_condition

class Anno2Json():
    def __init__(self, args,results,video_assets):
        self.args = args
        self.results = results
        self.video_assets = video_assets
        self.dp = DBParser(self.args, state='test')
        self.db_helper = DBHelper(args)

    def make_json(self,version):
        asset_df = self.db_helper.select(subset_condition["test"])
        for data in asset_df.values:
            patient = data[2]
            patient_path = self.args.data_base_path + '/toyset/{}/{}/{}'.format(*data[:3])
            for video_name in natsort.natsorted(os.listdir(patient_path)):


                new_data_video_value=(self.results.get(patient).get(video_name))
                new_data_totalframe=len(new_data_video_value[0])
                new_data_label=new_data_video_value[1]
                new_data_anno=[]
                idx_list_nrs=[]
                for k in range(len(new_data_label)):
                    if new_data_label[k]==1:
                        idx_list_nrs.append(k)
                idx_list_nrs_copy = idx_list_nrs.copy()

                if version == "autolabel":
                    for k in range(len(idx_list_nrs)-2):
                        if idx_list_nrs[k]+1==idx_list_nrs[k+1]:
                            if idx_list_nrs[k+1]+1 < idx_list_nrs[k+2]:
                                pass
                            else:
                                idx_list_nrs_copy.remove(idx_list_nrs[k+1])
                    for k in range(0,len(idx_list_nrs_copy)-1,2):
                        new_data_start_end = {"start": idx_list_nrs_copy[k],"end": idx_list_nrs_copy[k+1], "code":1}
                        new_data_anno.append(new_data_start_end)

                    new_json = {
                    "totalFrame": new_data_totalframe,
                    "frameRate": 30,
                    "width": 1920,
                    "height": 1080,
                    "_id": "61afe4e12bd5d3001b3578dc",
                    "annotations": new_data_anno,
                    "annotationType": "NRS",
                    "createdAt":"",  
                    "updatedAt": "", 
                    "annotator": "30",
                    "name": video_name,
                    "label": {"1": "NonRelevantSurgery"}
                    }

                elif version == "ssim":
                    pass

                anno_base_path = patient_path + f'/{video_name}/anno/v1'
                if os.path.exists(anno_base_path):
                    pass
                else:
                    os.mkdir(anno_base_path)
                
                if "R_" in anno_base_path:
                    json_name = anno_base_path + "/"+ video_name + "_TBE_30.json"
                    print("json_name", json_name)                     
                    with open(json_name, 'w') as f:
                        json.dump(new_json, f)
                elif "L_" in anno_base_path:
                    json_name = anno_base_path + "/"+ video_name + "_NRS_30.json"
                    print("json_name", json_name)
                    with open(json_name, 'w') as f:
                        json.dump(new_json, f)