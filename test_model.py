import base64
from fastai.vision.all import *
from PIL import Image
from io import BytesIO
import sys

# Load the model
learn = load_learner('export.pkl')

def predict_from_file(image_path):
    img = Image.open(image_path).convert("RGB")
    pred, idx, probs = learn.predict(img)
    print(f"Prediction: {pred}")
    print(f"Probabilities: { {str(learn.dls.vocab[i]): float(prob) for i, prob in enumerate(probs)} }")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python test_model.py <image_path>")
        sys.exit(1)
    image_path = sys.argv[1]
    predict_from_file(image_path) 