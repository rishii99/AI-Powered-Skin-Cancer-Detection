# Model Training Guide

## Setup

This project is designed to be trained on GPU in Google Colab or Kaggle for faster model convergence.

1. **Open Google Colab:**
   - Go to `https://colab.research.google.com`
   - Enable GPU via `Runtime > Change runtime type > GPU > T4`

2. **Create a Python environment locally (optional):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install training dependencies:**
   ```bash
   pip install tensorflow keras numpy pandas matplotlib scikit-learn opencv-python-headless
   ```

## Training EfficientNetB3

Create a notebook in `notebooks/train_model.ipynb`:

```python
import tensorflow as tf
from tensorflow import keras
from keras.applications import EfficientNetB3
import numpy as np

# Load HAM10000 dataset (download from https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/DBW86T)

# Preprocess and split
# model = EfficientNetB3(weights='imagenet', include_top=False)
# Add custom top layers for 7-class classification
# Compile with categorical crossentropy loss
# Train with class weights to handle imbalance
# Export to ONNX: python -m tf2onnx.convert --saved-model model_dir --output_file skin_cancer.onnx
```

## ONNX Export

After training in Keras/TensorFlow:

```bash
pip install tf2onnx
python -m tf2onnx.convert --saved-model ./model_path --output_file model/skin_cancer.onnx
```

Place the resulting `skin_cancer.onnx` file in `model/` directory.

## Grad-CAM Implementation

In `backend/app/services/analysis.py`, replace the placeholder with:

```python
from keras.models import Model
import tensorflow as tf

def build_gradcam_heatmap(model, image_array, class_index):
    # Create a model mapping to predictions and class activation map
    # Compute gradients of class output w.r.t. features
    # Generate heatmap and normalize
    pass
```

## HAM10000 Dataset Classes

- 0: melanocytic_nevus (nv)
- 1: melanoma (mel)
- 2: benign_keratosis (bkl)
- 3: basal_cell_carcinoma (bcc)
- 4: actinic_keratosis (akiec)
- 5: vascular_lesion (vasc)
- 6: dermatofibroma (df)

## Dataset Imbalance Handling

Use `class_weight` in Keras:

```python
class_weights = {0: 1.0, 1: 2.5, 2: 1.2, 3: 2.0, 4: 1.5, 5: 1.0, 6: 0.8}
model.fit(x_train, y_train, class_weight=class_weights)
```
