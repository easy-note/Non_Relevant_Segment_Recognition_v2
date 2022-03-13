import argparse

def parse_opts():
    """
        Base arguments parser
    """
    parser = argparse.ArgumentParser()

    # --------------- Model basic info --------------------
    parser.add_argument('--model',
            default='mobilenetv3_large_100',
            type=str,
            help='Select model to train/test')
    
    parser.add_argument('--pretrained',
            action='store_true', # false
            help='If true, load pretrained backbone')

    parser.add_argument('--loss_fn',
            default='ce',
            type=str,
            # choices=['ce', 'focal'],
            help='Select loss_fn to train/test')
    
    parser.add_argument('--batch_size',
            default=2,
            type=int,
            help='Training/Testing batch size')
    
    parser.add_argument('--n_classes',
            default=8,
            type=int,
            help='If monitor value is not updated until this value, stop training')
    
    parser.add_argument('--target_metric',
            default='val_loss',
            type=str,
            help='What device to use for training or validation model')

    parser.add_argument('--max_epoch',
            default=1,
            type=int,
            help='Maximum training epoch')

    parser.add_argument('--num_gpus',
            default=1,
            type=int,
            help='How many GPUs to use for training')

    parser.add_argument('--device',
            default='cuda',
            type=str,
            choices=['cpu', 'cuda'],
            help='What device to use for training or validation model')

    parser.add_argument('--cuda_list',
            default='0',
            type=str,
            help='Name list of gpus that are used to train')

    parser.add_argument('--save_path', type=str, 
                        default='./logs', help='')

    parser.add_argument('--resume',
            action='store_true',
            help='If true, keep training from the checkpoint')

    parser.add_argument('--restore_path', 
            type=str, 
            default=None, 
            help='Resume or test to train the model loaded from the path')

    # --------------- Optimizer and Scheduler info ----------------------
    parser.add_argument('--init_lr',
            default=1e-3,
            type=float,
            help='Initial learning rate')

    parser.add_argument('--weight_decay',
            default=1e-5,
            type=float,
            help='Weight decay value')

    parser.add_argument('--optimizer',
            default='adam',
            type=str,
            choices=['sgd', 'adam', 'lamb'],
            help=('What optimizer to use for training'
                '[Types : sgd, adam]'))

    parser.add_argument('--lr_scheduler',
            default='step_lr',
            type=str,
            choices=['step_lr', 'mul_lr', 'mul_step_lr', 'reduced_lr', 'cosine_lr'],
            help='Learning scheduler selection \n[Types : step_lr, mul_lr]')

    parser.add_argument('--lr_scheduler_step', 
            type=int, 
            default=5, 
            help='Use for Step LR Scheduler')

    parser.add_argument('--lr_scheduler_factor',
            default=0.9,
            type=float,
            help='Multiplicative factor for decreasing learning rate')

    parser.add_argument('--lr_milestones',
            default=[9, 14],
            type=list,
            help='Multi-step milestones for decreasing learning rate')
    

    # -------------- Dataset --------------------
    parser.add_argument('--dataset', 
            default='mnist', 
            type=str, 
            choices=['mnist', 'jigsaws', 'misaw', 'petraw'], 
            help='choose a multimodal dataset')

    parser.add_argument('--data_base_path',
            default='/dataset3/multimodal',
            type=str,
            help='Data location')

    parser.add_argument('--data_type',
            default=['vd'],
            type=list,
            help='kinematic(ki), video(vd), other modality')

    parser.add_argument('--fold',
            default=1,
            help='valset 1, 2, 3, 4, 5, free=for setting train_videos, val_vidoes')

    parser.add_argument('--num_workers',
            default=6,
            type=int,
            help='How many CPUs to use for data loading')
    
    parser.add_argument('--augmentations',
            default={
                    't_resize': [256],
                    't_random_crop': [224, True],
                    't_to_tensor': [],
                    't_normalize': [0.5,0.5],
                    },
            type=dict,
            help='How many CPUs to use for data loading')
           
    parser.add_argument('--val_augmentations',
            default={
                    't_resize': [256],
                    't_center_crop': [224],
                    't_to_tensor': [],
                    't_normalize': [0.5,0.5],
                    },
            type=dict,
            help='How many CPUs to use for data loading')    
    
    # -------------- etc --------------------
    parser.add_argument('--random_seed', type=int, default=3829, help='dataset random seed')

    parser.add_argument('--save_top_n', type=int, default=3, help='save best top N models')
        
    return parser
