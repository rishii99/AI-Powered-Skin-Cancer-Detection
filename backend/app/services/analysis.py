def build_gradcam_placeholder() -> dict:
    # Placeholder data for frontend Grad-CAM visualization.
    # Replace this method with real Grad-CAM heatmap generation from a Keras model.
    return {
        'heatmap': None,
        'explanation': 'Grad-CAM will highlight the most important region of the image used by the model.'
    }
