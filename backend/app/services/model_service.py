import io
import numpy as np
from PIL import Image
import onnxruntime as ort
from app.core.config import settings
from app.services.analysis import build_gradcam_placeholder

labels = [
    'melanocytic_nevus',
    'melanoma',
    'benign_keratosis',
    'basal_cell_carcinoma',
    'actinic_keratosis',
    'vascular_lesion',
    'dermatofibroma'
]

try:
    session = ort.InferenceSession(settings.model_path, providers=['CPUExecutionProvider'])
except Exception:
    session = None


def preprocess_image(image_bytes: bytes) -> np.ndarray:
    image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
    image = image.resize((300, 300))
    array = np.array(image).astype(np.float32) / 255.0
    array = np.transpose(array, (2, 0, 1))
    return np.expand_dims(array, axis=0)


def predict(image_bytes: bytes) -> dict:
    if session is None:
        raise RuntimeError('ONNX model session is not available. Ensure the model exists at the configured path.')
    input_tensor = preprocess_image(image_bytes)
    result = session.run(None, {'input': input_tensor})
    scores = np.squeeze(result[0]).astype(float)
    top_idx = np.argsort(scores)[::-1]
    top_predictions = [
        {
            'label': labels[int(idx)],
            'confidence': round(float(scores[int(idx)]) * 100, 2)
        }
        for idx in top_idx[:3]
    ]
    return {
        'predictions': top_predictions,
        'primary': top_predictions[0],
        'confidence': top_predictions[0]['confidence'],
        'risk_level': 'high' if top_predictions[0]['confidence'] >= 60 and top_predictions[0]['label'] in ['melanoma', 'basal_cell_carcinoma', 'actinic_keratosis'] else 'low',
        'uncertain': top_predictions[0]['confidence'] < 60,
        'gradcam': build_gradcam_placeholder()
    }
