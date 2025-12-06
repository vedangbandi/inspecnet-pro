import os
import shutil
import random
from pathlib import Path
from PIL import Image
import torch
from torch.utils.data import Dataset, DataLoader, random_split
from torchvision import transforms, datasets
from src.utils import logger, validate_image_file

class CustomDataset(Dataset):
    def __init__(self, file_paths, labels, class_to_idx, transform=None):
        self.file_paths = file_paths
        self.labels = labels
        self.transform = transform
        self.class_to_idx = class_to_idx
        self.classes = list(class_to_idx.keys())

    def __len__(self):
        return len(self.file_paths)

    def __getitem__(self, idx):
        img_path = self.file_paths[idx]
        label = self.labels[idx]
        
        try:
            image = Image.open(img_path).convert('RGB')
            if self.transform:
                image = self.transform(image)
            return image, label
        except Exception as e:
            logger.error(f"Error loading image {img_path}: {e}")
            # Return a black image in case of error to avoid crashing the loader
            # In a production system we might want to skip this index
            image = Image.new('RGB', (224, 224), color='black')
            if self.transform:
                image = self.transform(image)
            return image, label

class DatasetHandler:
    def __init__(self, config):
        self.config = config
        self.data_dir = None
        self.classes = []
        self.class_to_idx = {}
        # Lists for flat structure
        self.file_paths = []
        self.labels = []
        # Dictionaries for split structure
        self.split_data = {'train': [], 'val': [], 'test': []}
        self.has_splits = False
        
    def load_local_dataset(self, data_path):
        data_path = Path(data_path)
        if not data_path.exists():
            raise FileNotFoundError(f"Directory {data_path} does not exist.")
            
        self.data_dir = data_path
        
        # Check for split structure (train/val or train/test)
        subdirs = [d.name.lower() for d in data_path.iterdir() if d.is_dir()]
        self.has_splits = any(x in subdirs for x in ['train', 'validation', 'val', 'test'])
        
        valid_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif', '.webp'}
        
        if self.has_splits:
            # Load from splits
            logger.info("Detected split structure.")
            # Determine classes from 'train' folder usually
            train_dir =  data_path / 'train' if (data_path / 'train').exists() else None
            if not train_dir:
                 # Fallback to finding any split folder
                 for s in ['train', 'val', 'validation', 'test']:
                     if (data_path / s).exists():
                         train_dir = data_path / s
                         break
            
            if not train_dir:
                raise ValueError("Could not find classes in split folders.")

            self.classes = sorted([d.name for d in train_dir.iterdir() if d.is_dir()])
            self.class_to_idx = {cls_name: i for i, cls_name in enumerate(self.classes)}
            
            for split_name in ['train', 'val', 'validation', 'test']:
                split_dir = data_path / split_name
                if not split_dir.exists():
                    continue
                
                # Normalize 'validation' to 'val'
                internal_split = 'val' if split_name in ['val', 'validation'] else split_name
                
                for cls_name in self.classes:
                    cls_dir = split_dir / cls_name
                    if not cls_dir.exists(): continue
                    
                    for img_file in cls_dir.iterdir():
                        if img_file.suffix.lower() in valid_extensions:
                            self.split_data[internal_split].append(
                                (str(img_file), self.class_to_idx[cls_name])
                            )
            
            # Populate flat lists just for stats/compatibility
            for split in self.split_data:
                for f, l in self.split_data[split]:
                    self.file_paths.append(f)
                    self.labels.append(l)

        else:
            # Flat structure
            self.classes = sorted([d.name for d in data_path.iterdir() if d.is_dir()])
            self.class_to_idx = {cls_name: i for i, cls_name in enumerate(self.classes)}
            
            self.file_paths = []
            self.labels = []
            
            for cls_name in self.classes:
                cls_dir = data_path / cls_name
                for img_file in cls_dir.iterdir():
                    if img_file.suffix.lower() in valid_extensions:
                        self.file_paths.append(str(img_file))
                        self.labels.append(self.class_to_idx[cls_name])
                    
        logger.info(f"Loaded {len(self.file_paths)} total images from {len(self.classes)} classes.")
        return self.get_stats()

    def get_stats(self):
        class_counts = {cls: 0 for cls in self.classes}
        for label in self.labels:
            class_name = self.classes[label]
            class_counts[class_name] += 1
        return class_counts

    def get_data_loaders(self, batch_size=32, train_split=0.7, val_split=0.15, test_split=0.15, transform_params=None):
        img_size = 224
        
        train_transform = transforms.Compose([
            transforms.Resize((img_size, img_size)),
            transforms.RandomHorizontalFlip(),
            transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2, hue=0.1),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])
        
        val_test_transform = transforms.Compose([
            transforms.Resize((img_size, img_size)),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])

        train_dataset = None
        val_dataset = None
        test_dataset = None

        if self.has_splits:
            # Use pre-defined splits
            train_items = self.split_data['train']
            val_items = self.split_data['val']
            test_items = self.split_data['test']
            
            # If train is empty, we can't do anything with splits
            if not train_items:
                 logger.warning("Split structure detected but 'train' is empty. Falling back to random split if possible.")
                 if not self.file_paths:
                     raise ValueError("No images found in dataset.")
                 # Fall through to random split logic
                 self.has_splits = False
            else:
                # If val is empty but test exists, use test as val
                if not val_items and test_items:
                    val_items = test_items
                
                # If val and test are empty, we need to split train
                if not val_items and not test_items:
                    logger.warning("Train split found but no val/test. Splitting train...")
                     # Logic to split train_items into train/val
                    total_train = len(train_items)
                    val_size = int(total_train * 0.2)
                    
                    random.shuffle(train_items)
                    val_items = train_items[:val_size]
                    train_items = train_items[val_size:]

                # Dataset creation
                train_dataset = CustomDataset([x[0] for x in train_items], [x[1] for x in train_items], self.class_to_idx, transform=train_transform)
                val_dataset = CustomDataset([x[0] for x in val_items], [x[1] for x in val_items], self.class_to_idx, transform=val_test_transform)
                test_dataset = CustomDataset([x[0] for x in test_items], [x[1] for x in test_items], self.class_to_idx, transform=val_test_transform) if test_items else val_dataset

        if not self.has_splits:
            # Random Split
            total_size = len(self.file_paths)
            if total_size == 0: raise ValueError("No images loaded.")
            
            indices = list(range(total_size))
            random.shuffle(indices)
            
            train_size = int(total_size * train_split)
            val_size = int(total_size * val_split)
            
            train_indices = indices[:train_size]
            val_indices = indices[train_size:train_size + val_size]
            test_indices = indices[train_size + val_size:]
            
            train_dataset = CustomDataset([self.file_paths[i] for i in train_indices], [self.labels[i] for i in train_indices], self.class_to_idx, transform=train_transform)
            val_dataset = CustomDataset([self.file_paths[i] for i in val_indices], [self.labels[i] for i in val_indices], self.class_to_idx, transform=val_test_transform)
            test_dataset = CustomDataset([self.file_paths[i] for i in test_indices], [self.labels[i] for i in test_indices], self.class_to_idx, transform=val_test_transform)
        
        # GPU Optimization: pin_memory=True if CUDA is available
        pin = torch.cuda.is_available()
        
        train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True, num_workers=0, pin_memory=pin)
        val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False, num_workers=0, pin_memory=pin)
        test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False, num_workers=0, pin_memory=pin)
        
        return train_loader, val_loader, test_loader

    def set_manual_splits(self, train_path, val_path, test_path):
        """
        Manually configure splits from distinct directories.
        """
        self.split_data = {'train': [], 'val': [], 'test': []}
        self.classes = set()
        self.has_splits = True
        
        paths = {'train': train_path, 'val': val_path, 'test': test_path}
        valid_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif', '.webp'}
        
        for split, path in paths.items():
            if not path or not os.path.exists(path):
                continue
                
            path_obj = Path(path)
            # Assume classes are subfolders
            for cls_dir in path_obj.iterdir():
                if cls_dir.is_dir():
                    self.classes.add(cls_dir.name)
                    
                    for img_file in cls_dir.iterdir():
                        if img_file.suffix.lower() in valid_extensions:
                            self.split_data[split].append(
                                (str(img_file), cls_dir.name) # Store Name temporarily to resolve index later
                            )
                            
        self.classes = sorted(list(self.classes))
        self.class_to_idx = {cls: i for i, cls in enumerate(self.classes)}
        
        # Resolve class names to indices and populate flat lists
        self.file_paths = []
        self.labels = []
        
        # Re-map stored (path, name) to (path, idx)
        for split in self.split_data:
            new_list = []
            for path, cls_name in self.split_data[split]:
                idx = self.class_to_idx[cls_name]
                new_list.append((path, idx))
                
                self.file_paths.append(path)
                self.labels.append(idx)
            self.split_data[split] = new_list
            
        logger.info(f"Manual Splits Configured. Classes: {len(self.classes)}")
        return self.get_stats()

    def get_sample_images(self, n=16):
        """
        Returns a list of (image_path, class_name) tuples for visualization.
        """
        if not self.file_paths:
            return []
            
        # Sampling
        samples = []
        indices = random.sample(range(len(self.file_paths)), min(n, len(self.file_paths)))
        
        for idx in indices:
            path = self.file_paths[idx]
            label_idx = self.labels[idx]
            cls_name = self.classes[label_idx]
            samples.append((path, cls_name))
            
        return samples
