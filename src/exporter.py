
import torch
import torch.onnx
import os
from src.utils import logger

class ModelExporter:
    @staticmethod
    def export_to_onnx(model, input_shape=(1, 3, 224, 224), export_path="model_exports"):
        """
        Export a PyTorch model to ONNX format.
        """
        try:
            os.makedirs(export_path, exist_ok=True)
            model_name = model.__class__.__name__
            output_file = os.path.join(export_path, f"{model_name}.onnx")
            
            # Ensure model is in eval mode and on CPU for export usually (safer)
            model.eval()
            dummy_input = torch.randn(input_shape, device=next(model.parameters()).device)
            
            torch.onnx.export(
                model, 
                dummy_input, 
                output_file, 
                export_params=True,
                opset_version=11,
                do_constant_folding=True,
                input_names=['input'],
                output_names=['output'],
                dynamic_axes={'input': {0: 'batch_size'}, 'output': {0: 'batch_size'}}
            )
            
            logger.info(f"Model exported successfully to {output_file}")
            return output_file, True
        except Exception as e:
            logger.error(f"Failed to export model: {e}")
            return str(e), False
