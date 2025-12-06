import torch
import numpy as np
from sklearn.metrics import confusion_matrix, classification_report

class Analyzer:
    def __init__(self, model, device=None):
        self.model = model
        self.device = device if device else torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)
        self.model.eval()

    def get_predictions(self, loader):
        all_preds = []
        all_labels = []
        probs = []
        
        with torch.no_grad():
            for images, labels in loader:
                images = images.to(self.device)
                outputs = self.model(images)
                probabilities = torch.nn.functional.softmax(outputs, dim=1)
                _, preds = torch.max(outputs, 1)
                
                all_preds.extend(preds.cpu().numpy())
                all_labels.extend(labels.numpy())
                probs.extend(probabilities.cpu().numpy())
                
        return np.array(all_labels), np.array(all_preds), np.array(probs)

    def generate_report(self, loader, class_names):
        y_true, y_pred, y_probs = self.get_predictions(loader)
        
        if len(y_true) == 0:
            return np.zeros((len(class_names), len(class_names))), {}, np.array([]), np.array([])
            
        cm = confusion_matrix(y_true, y_pred, labels=range(len(class_names)))
        
        # Avoid crash if some classes are never predicted
        report = classification_report(
            y_true, 
            y_pred, 
            target_names=class_names, 
            output_dict=True, 
            labels=range(len(class_names)),
            zero_division=0
        )
        
        return cm, report, y_true, y_pred

    @staticmethod
    def get_training_suggestions(history):
        """
        Analyze training history to generate suggestions.
        """
        suggestions = []
        
        if len(history['train_loss']) < 2:
            return ["🟢 Models needs more epochs to analyze trends."]

        current_epoch = len(history['train_loss'])
        train_loss = history['train_loss'][-1]
        val_loss = history['val_loss'][-1]
        train_acc = history['train_acc'][-1]
        val_acc = history['val_acc'][-1]
        
        # Overfitting check
        if train_loss < val_loss * 0.8 and current_epoch > 5:
            suggestions.append("🔴 Overfitting detected: Validation loss significantly higher than Training loss. Try increasing Dropout or Weight Decay.")
            
        # Convergence check
        if train_acc > 0.95 and val_acc > 0.90:
            suggestions.append("🟢 Excellent convergence! Model is performing well.")
            
        # Underfitting check
        if train_acc < 0.6 and current_epoch > 10:
             suggestions.append("🟡 Underfitting: Model is confusing classes. Try a more complex architecture (e.g., EfficientNetHybrid) or lower Learning Rate.")
             
        # LR check
        if len(history['val_loss']) > 3:
            recent_losses = history['val_loss'][-3:]
            if recent_losses[0] < recent_losses[1] < recent_losses[2]:
                suggestions.append("🟡 Divergence detected: Loss is increasing. REDUCE Learning Rate immediately.")

        return suggestions

    def get_misclassified_images(self, loader, class_names, top_k=5):
        self.model.eval()
        misclassified = []
        
        with torch.no_grad():
            for images, labels in loader:
                images_dev = images.to(self.device)
                outputs = self.model(images_dev)
                probs = torch.nn.functional.softmax(outputs, dim=1)
                conf, preds = torch.max(probs, 1)
                
                for i in range(len(labels)):
                    true_label = labels[i].item()
                    pred_label = preds[i].item()
                    
                    if true_label != pred_label:
                        misclassified.append({
                            'image': images[i], # CPU tensor
                            'true_class': class_names[true_label],
                            'pred_class': class_names[pred_label],
                            'confidence': conf[i].item()
                        })
        
        # Sort by confidence (high confidence errors are worst)
        misclassified.sort(key=lambda x: x['confidence'], reverse=True)
        return misclassified[:top_k]
    
    def get_per_class_accuracy(self, cm, class_names):
        accuracies = {}
        for i, cls in enumerate(class_names):
            tp = cm[i, i]
            total = cm[i, :].sum()
            acc = tp / total if total > 0 else 0
            accuracies[cls] = acc
        return accuracies
