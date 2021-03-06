from torch.utils.data import DataLoader
from core.util.sampler import OverSampler
from core.dataset.robot_dataset import RobotDataset
from core.dataset.lapa_dataset import LapaDataset
from core.dataset.infer_dataset import InferDataset
from core.dataset.sub_dataset import SubDataset


__all__ = [
    'load_data', 'RobotDataset', 'LapaDataset',
    'InferDataset', 'SubDataset',
]


def load_data(args):
    if args.dataset == 'robot':
        trainset = RobotDataset(args, state='train', sample_type=args.sample_type)
        valset = RobotDataset(args, state='val', sample_type=args.sample_type)
        
    elif args.dataset == 'lapa':
        trainset = LapaDataset(args, state='train', sample_type=args.sample_type)
        valset = LapaDataset(args, state='val', sample_type=args.sample_type)
    
    if args.sampler == 'oversampler':
        train_loader = DataLoader(trainset,
                                batch_size=args.batch_size,
                                num_workers=args.num_workers,
                                sampler=OverSampler(trainset.label_list, args.batch_size//2, args.batch_size),
                                pin_memory=True,
                                )
    else:
        train_loader = DataLoader(trainset,
                              batch_size=args.batch_size,
                              num_workers=args.num_workers,
                              shuffle=True,
                              pin_memory=True,
                              )
    
    val_loader = DataLoader(valset,
                              batch_size=args.batch_size,
                              num_workers=args.num_workers,
                              shuffle=False,
                              pin_memory=True,
                              )
    
    return train_loader, val_loader