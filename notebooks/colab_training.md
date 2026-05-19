# Google Colab Training Guide

Use this guide to train the model on a GPU-enabled Google Colab session.

1. Open https://colab.research.google.com
2. Set Runtime > Change runtime type > GPU > T4
3. Upload the HAM10000 dataset or mount Google Drive
4. Install required packages:
   ```bash
   !pip install tensorflow keras numpy pandas matplotlib scikit-learn
   ```
5. Use EfficientNetB3 transfer learning with class weights and data augmentation.
6. Save the trained model as a Keras SavedModel:
   ```python
   model.save('/content/skin_cancer_saved_model')
   ```
7. Export to ONNX:
   ```bash
   !pip install tf2onnx
   python -m tf2onnx.convert --saved-model /content/skin_cancer_saved_model --output /content/skin_cancer.onnx
   ```
8. Download the ONNX model to the local `model/` folder in this project.

## Notes
- Use class weights to handle HAM10000 imbalance.
- Track Melanoma recall carefully during validation.
- Save evaluation metrics and confusion matrix to update `README.md`.
