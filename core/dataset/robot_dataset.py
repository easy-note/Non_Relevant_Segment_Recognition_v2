import os
import sys
import random
import numpy as np
import torch
from glob import glob
from PIL import Image
import pandas as pd
import natsort
from torch.utils.data import Dataset

from core.dataset.fold_robot import *
from core.dataset.aug_info import *
from core.util.data.sampler import BoundarySampler



class RobotDataset(Dataset):
    def __init__(self, args, state='train', sample_type='boundary'):
        super().__init__()
        
        self.args = args
        self.state = state
        self.sample_type = sample_type
        self.fold = self.args.fold        
        self.img_list, self.label_list = None, None
        
        # set data path
        # self.anno_path = self.args.data_base_path + '/{}/{}/anno/{}/anno.csv'.format(self.args.dataset,
        #                                                                             self.args.datatype,
        #                                                                             self.args.data_version)
        self.anno_path = self.args.data_base_path + '/{}/{}/anno/{}'.format(self.args.dataset,
                                                                                    self.args.datatype,
                                                                                    self.args.data_version)
        
        if self.args.datatype == 'vihub':
            pass
        elif self.args.datatype == 'etc':
            pass
        elif self.args.datatype == 'mola':
            self.patients_name = mola[self.state][self.fold]
            
        self.load_data()
        
        # augmentation setup
        if self.args.experiment_type == 'ours':
            if self.args.model == 'mobile_vit':
                d_transforms = data_transforms_mvit
            else:    
                d_transforms = data_transforms
        elif self.args.experiment_type == 'theator':
            d_transforms = data_transforms_theator
        
        self.aug = d_transforms[self.state]
        
    def __len__(self):
        return len(self.img_list)

    # return img, label
    def __getitem__(self, index):
        img_path, label = self.img_list[index], self.label_list[index]

        img = Image.open(img_path)
        img = self.aug(img)

        return img_path, img, label
    

    def load_data(self):
        if self.args.appointment_assets_path != '':
            print('\n\n\t ==> APPOINTMENT ASSETS PATH: {}'.format(self.args.appointment_assets_path))

            appointment_assets_df = pd.read_csv(self.args.appointment_assets_path, low_memory=False) # read appointment csv

            # select patient frame 
            print('==> \tPATIENT ({})'.format(len(self.patients_name)))
            print('|'.join(self.patients_name))
            patients_name_for_parser = [patient + '_' for patient in self.patients_name]
            
            # select patient video
            assets_df = appointment_assets_df[appointment_assets_df['img_path'].str.contains('|'.join(patients_name_for_parser))]
            assets_df = assets_df.sort_values(by=['img_path'])

            print('\n==== FIANL STAGE ASSTES ====')
            print(assets_df)
            print('==== FIANL STAGE ASSTES ====\n')
            
        else: # assets type check
            print('ANNOTATION PATH : {}'.format(self.anno_path))
            patient_list = natsort.natsorted(os.listdir(self.anno_path))
            
            refine_df = pd.DataFrame(columns=['img_path', 'class_idx'])
            
            for patient in patient_list:
                print(patient)
                anno_df = pd.read_csv(self.anno_path + f'/{patient}', low_memory=False)[::self.args.target_fps] # read inbody csv
                refine_df = refine_df.append(anno_df)
                print(patient, '   end')
            
            # anno_df = pd.read_csv(self.anno_path, low_memory=False) # read inbody csv

            # # select patient frame 
            # print('==> \tPATIENT ({})'.format(len(self.patients_name)))
            # print('|'.join(self.patients_name))
            # patients_name_for_parser = [patient + '_' for patient in self.patients_name]
            
            # # fit to target fps
            # for _patient in patients_name_for_parser:
            #     print(_patient)
            #     # ids = anno_df.index[anno_df['img_path'].str.contains('|'.join(_patient))]
            #     ids = anno_df.index[anno_df['img_path'].str.contains(_patient)]
            #     df = anno_df.loc[ids][::self.args.target_fps]
            #     anno_df.drop(ids)
                
            #     # df = anno_df[anno_df['img_path'].str.contains('|'.join(_patient))][::self.args.target_fps]
            #     refine_df = refine_df.append(df)
            #     print(_patient, '   end')

            # hueristic_sampling
            if self.sample_type == 'boundary':
                print('\n\n\t ==> HUERISTIC SAMPLING ... IB_RATIO: {}, WS_RATIO: {}\n\n'.format(self.IB_ratio, self.WS_ratio))            
                bs = BoundarySampler(self.args.IB_ratio, self.args.WS_ratio)
                assets_df = bs.sample(refine_df)

            elif self.sample_type == 'random':
                print('\n\n\t ==> RANDOM SAMPLING ... IB_RATIO: {}\n\n'.format(self.args.IB_ratio))
                # random_sampling and setting IB:OOB data ratio
                # ratio로 구성 불가능 할 경우 전체 set 모두 사용
                nrs_ids = refine_df.index[refine_df['class_idx'] == 1].tolist()
                nrs_df = refine_df.loc[nrs_ids]
                rs_df = refine_df.drop(nrs_ids, inplace=True)
                
                
                max_ib_count, target_ib_count = len(rs_df), int(len(nrs_df)) * self.args.IB_ratio
                sampling_ib_count = max_ib_count if max_ib_count < target_ib_count else target_ib_count
                print('Random sampling from {} to {}'.format(max_ib_count, sampling_ib_count))
                
                rs_df = rs_df.sample(n=sampling_ib_count, replace=False) # 중복뽑기x, random seed 고정, OOB개수의 IB_ratio 개
                assets_df = pd.concat([rs_df, nrs_df])
                
            elif self.sample_type == 'all':
                assets_df = refine_df

        # last processing
        self.img_list = assets_df.img_path.tolist()
        self.label_list = assets_df.class_idx.tolist()

        self.assets_df = assets_df
    
    def number_of_rs_nrs(self):
        return self.label_list.count(0) ,self.label_list.count(1)

    # 해당 robot_dataset의 patinets별 assets 개수 (hem train할때 valset만들어서 hem_helper의 args.hem_per_patinets에서 사용됨.)     
    def number_of_patient_rs_nrs(self):
        patient_per_dic = {}

        val_assets_df = self.assets_df
        val_assets_df['patient'] = val_assets_df.img_path.str.split('/').str[4]
        patients_list = natsort.natsorted(list(set(val_assets_df['patient'])))
        
        total_rs_count, total_nrs_count = val_assets_df.groupby('class_idx').count()[val_assets_df.columns[1]].values
    
        for patient in patients_list:
            patient_df = val_assets_df[val_assets_df['patient']==patient]            
            patient_rs_count, patient_nrs_count = patient_df.groupby('class_idx').count()[patient_df.columns[1]].values

            patient_per_dic.update(
                {
                    patient : {
                    'rs': patient_rs_count,
                    'nrs': patient_nrs_count,
                    'rs_ratio': patient_rs_count/total_rs_count,
                    'nrs_ratio': patient_nrs_count/total_nrs_count
                    } 
                }
            )

        return patient_per_dic