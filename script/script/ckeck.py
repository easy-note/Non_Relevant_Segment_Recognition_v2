import os
import natsort

base_path = "/workspace/disk1/robot/vihub/img"
patient_list = natsort.natsorted(os.listdir(base_path))
print(patient_list)


vihub = {
    'train': {
        # 1: ['R_1',],
        1: ['01_ViHUB_B1_R_1',
'01_ViHUB_B1_R_4',
'01_ViHUB_B1_R_6',
'01_ViHUB_B1_R_9',
'01_ViHUB_B1_R_10',
'01_ViHUB_B1_R_11',
'01_ViHUB_B1_R_12',
'01_ViHUB_B1_R_13',
'01_ViHUB_B1_R_14',
'01_ViHUB_B1_R_15',
'01_ViHUB_B1_R_16',
'01_ViHUB_B1_R_38',
'01_ViHUB_B1_R_39',
'01_ViHUB_B1_R_40',
'01_ViHUB_B1_R_42',
'01_ViHUB_B1_R_43',
'01_ViHUB_B1_R_44',
'01_ViHUB_B1_R_45',
'01_ViHUB_B1_R_48',
'01_ViHUB_B1_R_49',
'01_ViHUB_B1_R_50',
'01_ViHUB_B1_R_51',
'01_ViHUB_B1_R_52',
'01_ViHUB_B1_R_55',
'01_ViHUB_B1_R_57',
'01_ViHUB_B1_R_62',
'01_ViHUB_B1_R_69',
'01_ViHUB_B1_R_70',
'01_ViHUB_B1_R_71',
'01_ViHUB_B1_R_72',
'01_ViHUB_B1_R_74',
'01_ViHUB_B6_R_120',
'01_ViHUB_B6_R_121',
'01_ViHUB_B6_R_122',
'01_ViHUB_B6_R_123',
'01_ViHUB_B6_R_125',
'01_ViHUB_B6_R_126',
'01_ViHUB_B6_R_127',
'01_ViHUB_B6_R_130',
'01_ViHUB_B6_R_131',
'01_ViHUB_B6_R_132',
'01_ViHUB_B6_R_134',
'01_ViHUB_B6_R_136',
'01_ViHUB_B6_R_137',
'01_ViHUB_B6_R_141',
'01_ViHUB_B6_R_143',
'01_ViHUB_B6_R_145',
'01_ViHUB_B6_R_146',
'01_ViHUB_B6_R_147',
'01_ViHUB_B6_R_148',
'01_ViHUB_B6_R_149',
'01_ViHUB_B6_R_150',
'01_ViHUB_B6_R_151'],
        # -1: ['R_1'], # sample validation
    },
    'val': {
        # 1: ['R_2', ],
        1: ["01_ViHUB_B1_R_3",
"01_ViHUB_B1_R_5",
"01_ViHUB_B1_R_7",
"01_ViHUB_B1_R_8",
"01_ViHUB_B1_R_37",
"01_ViHUB_B1_R_41",
"01_ViHUB_B1_R_46",
"01_ViHUB_B1_R_47",
"01_ViHUB_B1_R_53",
"01_ViHUB_B1_R_54",
"01_ViHUB_B1_R_61",
"01_ViHUB_B1_R_63",
"01_ViHUB_B1_R_64",
"01_ViHUB_B1_R_67",
"01_ViHUB_B6_R_124",
"01_ViHUB_B6_R_128",
"01_ViHUB_B6_R_129",
"01_ViHUB_B6_R_138",
"01_ViHUB_B6_R_140",
"01_ViHUB_B6_R_142"],

        # -1: ['R_2',], # sample validation
    },
}
