import time
import os
import torch
import torch.nn as nn
import torch.optim as optim
from src.utils import logger
import numpy as np

class TrainingCallback:
    def on_epoch_start(self, epoch): pass
    def on_epoch_end(self, epoch, logs): pass
    def on_batch_end(self, batch, logs): pass

class Trainer:
    def __init__(self, model, device=None, criterion=None, optimizer=None):
        self.model = model
        
        # Robust Device Check
        if device:
            self.device = device
        else:
            if torch.cuda.is_available():
                self.device = torch.device("cuda")
                logger.info("CUDA detected. Training will run on GPU.")
            else:
                logger.warning("CUDA NOT detected. Training will run on CPU (SLOW).")
                self.device = torch.device("cpu")
                
        self.model.to(self.device)
        self.criterion = criterion if criterion else nn.CrossEntropyLoss()
        self.optimizer = optimizer
        self.scheduler = None 
        self.stop_training = False # abort flag
        self.use_early_stop = False # toggled from UI
        self.early_stop_patience = 10 # default patience (increased for better convergence)
        self._best_val_loss = 0.0  # Stores best validation accuracy (not loss)
        self._no_improve_cnt = 0

    def check_gpu(self):
        return torch.cuda.is_available()

    def set_optimizer(self, optimizer_name, lr, weight_decay=1e-5):
        if optimizer_name == "Adam":
            self.optimizer = optim.Adam(self.model.parameters(), lr=lr, weight_decay=weight_decay)
        elif optimizer_name == "RMSprop":
            self.optimizer = optim.RMSprop(self.model.parameters(), lr=lr, weight_decay=weight_decay)
        elif optimizer_name == "SGD":
            self.optimizer = optim.SGD(self.model.parameters(), lr=lr, momentum=0.9, weight_decay=weight_decay)
        else:
            raise ValueError(f"Optimizer {optimizer_name} not supported")
        
        # Scheduler for stability
        self.scheduler = optim.lr_scheduler.ReduceLROnPlateau(self.optimizer, mode='max', factor=0.5, patience=2)

    def train_model(self, train_loader, val_loader, epochs, callback=None, log_callback=None):
        def log(msg):
            if log_callback: log_callback(msg)
            else: logger.info(msg)

        best_acc = 0.0
        history = {
            'train_loss': [], 'train_acc': [],
            'val_loss': [], 'val_acc': [],
            'lr': [], 'epoch_times': []
        }
        
        self.model.to(self.device)
        log(f"Training started on device: {self.device}")
        
        for epoch in range(epochs):
            if self.stop_training:
                log("Training stopped by user.")
                break
            
            start_t = time.time()
            if callback: callback.on_epoch_start(epoch)
            
            # --- TRAIN ---
            self.model.train()
            r_loss, correct, total = 0.0, 0, 0
            
            for i, (images, labels) in enumerate(train_loader):
                if self.stop_training: break
                
                # Move to device non-blocking
                images = images.to(self.device, non_blocking=True)
                labels = labels.to(self.device, non_blocking=True)
                
                self.optimizer.zero_grad()
                outputs = self.model(images)
                loss = self.criterion(outputs, labels)
                loss.backward()
                
                # Clip Gradients
                torch.nn.utils.clip_grad_norm_(self.model.parameters(), max_norm=1.0)
                
                self.optimizer.step()
                
                r_loss += loss.item() * images.size(0)
                _, pred = outputs.max(1)
                total += labels.size(0)
                correct += pred.eq(labels).sum().item()
                
                if callback and i % 5 == 0:
                     callback.on_batch_end(i, {'batch_loss': loss.item(), 'epoch': epoch})
            
            if total == 0: total = 1 # Prevent DivZero
            epoch_loss = r_loss / total
            epoch_acc = correct / total
            
            # --- VAL ---
            val_loss, val_acc = self.validate(val_loader)
            
            # Step Scheduler
            if self.scheduler:
                self.scheduler.step(val_acc)
            
            # Early Stopping Check (monitors validation ACCURACY for improvement)
            if self.use_early_stop:
                if val_acc > self._best_val_loss:  # Using _best_val_loss variable to store best accuracy
                    self._best_val_loss = val_acc
                    self._no_improve_cnt = 0
                    log(f"✓ New best validation accuracy: {val_acc:.2%}")
                else:
                    self._no_improve_cnt += 1
                    log(f"Early-Stop: {self._no_improve_cnt}/{self.early_stop_patience} epochs without improvement.")
                    if self._no_improve_cnt >= self.early_stop_patience:
                        log("⚠️ Early-Stopping triggered – ending training.")
                        break
            
            duration = time.time() - start_t
            
            # Update History
            history['train_loss'].append(epoch_loss)
            history['train_acc'].append(epoch_acc)
            history['val_loss'].append(val_loss)
            history['val_acc'].append(val_acc)
            current_lr = self.optimizer.param_groups[0]['lr']
            history['lr'].append(current_lr)
            history['epoch_times'].append(duration)
            
            # Logs for UI
            logs = {
                'train_loss': epoch_loss, 'train_acc': epoch_acc, 
                'val_loss': val_loss, 'val_acc': val_acc,
                'lr': current_lr,
                'time': duration
            }
            
            if val_acc > best_acc:
                best_acc = val_acc
                # Save best
                os.makedirs('checkpoints', exist_ok=True)
                torch.save({
                    'epoch': epoch,
                    'model_state_dict': self.model.state_dict(),
                    'optimizer_state_dict': self.optimizer.state_dict(),
                    'val_acc': val_acc
                }, 'checkpoints/best_model.pt')
                log(f"Saved new best model with acc: {best_acc:.4f}")
            
            if callback: callback.on_epoch_end(epoch, logs)
            
            log(f"Epoch {epoch+1}/{epochs} - Train Loss: {epoch_loss:.4f} Acc: {epoch_acc:.4f} - Val Loss: {val_loss:.4f} Acc: {val_acc:.4f}")

        return self.model, history

    def validate(self, loader):
        self.model.eval()
        running_loss = 0.0
        correct = 0
        total = 0
        
        with torch.no_grad():
            for images, labels in loader:
                images = images.to(self.device, non_blocking=True)
                labels = labels.to(self.device, non_blocking=True)
                
                outputs = self.model(images)
                loss = self.criterion(outputs, labels)
                
                running_loss += loss.item() * images.size(0)
                _, predicted = outputs.max(1)
                total += labels.size(0)
                correct += predicted.eq(labels).sum().item()
                
        return (running_loss / total, correct / total) if total > 0 else (0.0, 0.0)
