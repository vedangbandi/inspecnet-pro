import torch
import torch.nn as nn
from torchvision import models

class ModelFactory:
    @staticmethod
    def get_model(model_name, num_classes, pretrained=True, freeze_layers=False):
        """
        Factory method to create models.
        Supported: MobileNetV2, ResNet50, EfficientNet
        """
        model = None
        weights = None
        
        if pretrained:
            if model_name == "MobileNetV2":
                weights = models.MobileNet_V2_Weights.DEFAULT
            elif model_name == "ResNet50":
                weights = models.ResNet50_Weights.DEFAULT
            elif model_name.startswith("EfficientNet"):
                if model_name == "EfficientNetB0":
                    weights = models.EfficientNet_B0_Weights.DEFAULT
                elif model_name == "EfficientNetB4":
                    weights = models.EfficientNet_B4_Weights.DEFAULT

        if model_name == "MobileNetV2":
            model = models.mobilenet_v2(weights=weights)
            # Freeze features if requested
            if freeze_layers:
                for param in model.features.parameters():
                    param.requires_grad = False
            # Replace classifier
            model.classifier[1] = nn.Linear(model.last_channel, num_classes)
            
        elif model_name == "ResNet50":
            model = models.resnet50(weights=weights)
            if freeze_layers:
                for param in model.parameters():
                    param.requires_grad = False
            
            num_ftrs = model.fc.in_features
            model.fc = nn.Linear(num_ftrs, num_classes)
            
        elif model_name == "EfficientNetB0":
            model = models.efficientnet_b0(weights=weights)
            if freeze_layers:
                for param in model.features.parameters():
                    param.requires_grad = False
            
            num_ftrs = model.classifier[1].in_features
            model.classifier[1] = nn.Linear(num_ftrs, num_classes)
            
        elif model_name == "EfficientNetB4":
            model = models.efficientnet_b4(weights=weights)
            if freeze_layers:
                for param in model.features.parameters():
                    param.requires_grad = False
                    
            num_ftrs = model.classifier[1].in_features
            model.classifier[1] = nn.Linear(num_ftrs, num_classes)
            
        else:
            raise ValueError(f"Model {model_name} not supported.")
            
        return model
