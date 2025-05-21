# Gender Classification API

This API service uses a fine-tuned FastAI model to classify gender from images.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Place your trained model file (model.pkl) in the root directory

3. Create a .env file with:
```
MODEL_PATH=model.pkl
```

## Running Locally

```bash
uvicorn app:app --reload
```

The API will be available at http://localhost:8000

## API Endpoints

### POST /predict
Predicts gender from a base64 encoded image.

Request body:
```json
{
    "image_base64": "base64_encoded_image_string"
}
```

Response:
```json
{
    "gender": "predicted_gender",
    "confidence": 0.95
}
```

### GET /health
Health check endpoint.

## Docker Deployment

1. Build the Docker image:
```bash
docker build -t gender-classification-api .
```

2. Run the container:
```bash
docker run -p 8000:8000 gender-classification-api
```

## AWS Deployment

1. Build and push the Docker image to Amazon ECR
2. Deploy using AWS ECS or AWS App Runner
3. Configure environment variables in AWS