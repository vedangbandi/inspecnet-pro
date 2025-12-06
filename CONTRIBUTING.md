# Contributing to InspecNet Pro

First off, thank you for considering contributing to InspecNet Pro! It's people like you that make this tool better for everyone.

## Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the existing issues to avoid duplicates. When you create a bug report, include as many details as possible:

- **Use a clear and descriptive title**
- **Describe the exact steps to reproduce the problem**
- **Provide specific examples** (dataset structure, settings used, etc.)
- **Describe the behavior you observed** and what you expected
- **Include screenshots** if relevant
- **Include your environment details**:
  - OS version
  - Python version
  - PyTorch version
  - GPU model (if applicable)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion:

- **Use a clear and descriptive title**
- **Provide a detailed description** of the suggested enhancement
- **Explain why this enhancement would be useful**
- **List some examples** of how it would be used

### Pull Requests

1. **Fork the repository** and create your branch from `main`
2. **Make your changes**:
   - Follow the existing code style
   - Add comments for complex logic
   - Update documentation if needed
3. **Test your changes**:
   - Ensure the application runs without errors
   - Test with different datasets
   - Verify GPU and CPU modes work
4. **Commit your changes**:
   - Use clear commit messages
   - Reference issues if applicable
5. **Push to your fork** and submit a pull request

## Development Setup

```bash
# Clone your fork
git clone https://github.com/yourusername/inspecnet-pro.git
cd inspecnet-pro

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

## Code Style Guidelines

### Python Code
- Follow PEP 8 style guide
- Use meaningful variable names
- Add docstrings to functions and classes
- Keep functions focused and small
- Use type hints where appropriate

Example:
```python
def train_model(self, train_loader: DataLoader, val_loader: DataLoader, 
                epochs: int, callback: TrainingCallback = None) -> Tuple[nn.Module, dict]:
    """
    Train the model with given data loaders.
    
    Args:
        train_loader: DataLoader for training data
        val_loader: DataLoader for validation data
        epochs: Number of training epochs
        callback: Optional callback for progress updates
        
    Returns:
        Tuple of (trained model, training history)
    """
    # Implementation
```

### UI Code
- Use consistent styling from `ui_styles.py`
- Follow Qt best practices
- Use signals/slots for thread safety
- Add tooltips to all interactive elements

### Commit Messages
- Use present tense ("Add feature" not "Added feature")
- Use imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit first line to 72 characters
- Reference issues and pull requests

Examples:
```
Add early stopping patience control
Fix accuracy monitoring in early stopping (#42)
Update documentation for ONNX export
```

## Project Structure

```
inspecnet-pro/
├── main.py              # Application entry point
├── src/
│   ├── dataset.py      # Dataset handling
│   ├── model.py        # Model architectures
│   ├── trainer.py      # Training logic
│   ├── exporter.py     # ONNX export
│   ├── ui_styles.py    # UI styling
│   └── ui_components.py # Custom widgets
└── docs/               # Documentation
```

## Testing

Before submitting a pull request:

1. **Test basic functionality**:
   - Load a dataset
   - Train for a few epochs
   - Export to ONNX
   - Run inference

2. **Test edge cases**:
   - Empty dataset
   - Single class dataset
   - Very small/large batch sizes
   - GPU and CPU modes

3. **Test UI**:
   - All buttons work
   - Tooltips display correctly
   - Progress updates smoothly
   - No UI freezing

## Documentation

- Update README.md if you change functionality
- Add docstrings to new functions/classes
- Update CHANGELOG.md with your changes
- Add examples if introducing new features

## Questions?

Feel free to open an issue with the "question" label if you need help or clarification.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to InspecNet Pro! 🎉
