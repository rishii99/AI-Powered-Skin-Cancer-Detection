import base64
import io
import os
from typing import Optional

import numpy as np
from PIL import Image
from app.core.config import settings

try:
    import tensorflow as tf
except ImportError:
    tf = None


def load_gradcam_model():
    if not settings.enable_gradcam or tf is None:
        return None
    if not os.path.isdir(settings.keras_model_path):
        return None
    try:
        return tf.keras.models.load_model(settings.keras_model_path)
    except Exception:
        return None

gradcam_model = load_gradcam_model()


def get_last_conv_layer(model):
    for layer in reversed(model.layers):
        if hasattr(layer, 'kernel_size') and len(getattr(layer, 'kernel_size', [])) == 2:
            return layer
    return None


def get_gradcam_heatmap(model, image_array: np.ndarray, class_index: int) -> np.ndarray:
    if tf is None or model is None:
        raise RuntimeError('TensorFlow is not available for Grad-CAM.')

    last_conv_layer = get_last_conv_layer(model)
    if last_conv_layer is None:
        raise RuntimeError('Unable to locate a convolutional layer for Grad-CAM.')

    grad_model = tf.keras.models.Model(
        [model.inputs],
        [last_conv_layer.output, model.output]
    )
    image_tensor = tf.convert_to_tensor(image_array)
    with tf.GradientTape() as tape:
        conv_outputs, predictions = grad_model(image_tensor)
        loss = predictions[:, class_index]
    grads = tape.gradient(loss, conv_outputs)
    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))
    conv_outputs = conv_outputs[0].numpy()
    pooled_grads = pooled_grads.numpy()
    for i in range(pooled_grads.shape[-1]):
        conv_outputs[:, :, i] *= pooled_grads[i]
    heatmap = np.mean(conv_outputs, axis=-1)
    heatmap = np.maximum(heatmap, 0)
    heatmap = heatmap / (np.max(heatmap) + 1e-8)
    return heatmap


def overlay_heatmap(image: Image.Image, heatmap: np.ndarray) -> str:
    heatmap_img = Image.fromarray(np.uint8(255 * heatmap)).resize(image.size, Image.BILINEAR)
    heatmap_rgba = Image.new('RGBA', image.size)
    heatmap_array = np.array(heatmap_img)
    overlay = np.zeros((image.size[1], image.size[0], 4), dtype=np.uint8)
    overlay[..., 0] = heatmap_array
    overlay[..., 3] = np.uint8(heatmap_array * 0.65)
    overlay_img = Image.fromarray(overlay, mode='RGBA')
    combined = Image.alpha_composite(image.convert('RGBA'), overlay_img)
    buffered = io.BytesIO()
    combined.save(buffered, format='PNG')
    return base64.b64encode(buffered.getvalue()).decode('utf-8')


def build_gradcam(image_bytes: bytes, class_index: int, label: str) -> dict:
    if gradcam_model is None:
        return {
            'heatmap': None,
            'explanation': 'Grad-CAM model is not loaded. Train a Keras saved model at model/skin_cancer_saved_model.'
        }
    image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
    image = image.resize((300, 300))
    array = np.array(image).astype(np.float32) / 255.0
    input_array = np.expand_dims(array, axis=0)
    try:
        heatmap = get_gradcam_heatmap(gradcam_model, input_array, class_index)
        overlay_base64 = overlay_heatmap(image, heatmap)
        return {
            'heatmap': overlay_base64,
            'explanation': f'Grad-CAM highlights the regions used by the model to predict {label}.'
        }
    except Exception as exc:
        return {
            'heatmap': None,
            'explanation': f'Grad-CAM could not be generated: {str(exc)}'
        }
