from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import base64
from io import BytesIO
from PIL import Image
import torch
from fastai.vision.all import *
import os
from dotenv import load_dotenv
import tempfile

# Load environment variables
load_dotenv()

app = FastAPI(title="Gender Classification API")
learn = load_learner('export.pkl')

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ImagePayload(BaseModel):
    image_base64: str

@app.post("/predict")
async def predict_gender(payload: ImagePayload):
    try:
        # Decode base64 to bytes
        image_data = base64.b64decode(payload.image_base64)
        # Open image
        img = Image.open(BytesIO(image_data)).convert("RGB")
        # Save to a temporary file
        with tempfile.NamedTemporaryFile(suffix=".jpg") as temp:
            img.save(temp, format="JPEG")
            temp.flush()
            # Predict using file path
            pred, idx, probs = learn.predict(temp.name)
        return {
            "prediction": pred,
            "probabilities": {str(learn.dls.vocab[i]): float(prob) for i, prob in enumerate(probs)}
        }
    except Exception as e:
        import traceback
        print("Error during prediction:", traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 