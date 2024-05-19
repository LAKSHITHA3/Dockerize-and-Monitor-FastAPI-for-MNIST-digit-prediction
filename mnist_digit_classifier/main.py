# main.py

from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import JSONResponse
from keras.models import load_model as keras_load_model
from keras.src.engine.sequential import Sequential
from PIL import Image
import numpy as np
import io
import sys
import time
from prometheus_client import Counter, Gauge, generate_latest, REGISTRY

app = FastAPI()

# Prometheus metrics
REQUEST_COUNT = Counter("request_count", "Total number of requests", ["client_ip"])
REQUEST_LATENCY = Gauge("request_latency", "Latency of requests", ["client_ip", "input_length"])
REQUEST_TL_TIME = Gauge("request_tl_time", "Effective processing time per character", ["client_ip", "input_length"])

# Load the model from the given path
def load_model(path: str) -> Sequential:
    return keras_load_model(path)

# Predict the digit from the image data
def predict_digit(model: Sequential, data_point: list) -> str:
    data = np.array(data_point).reshape(1, 28, 28, 1)
    prediction = model.predict(data)
    digit = np.argmax(prediction)
    return str(digit)

# Format the image to a 28x28 grayscale array
def format_image(image_bytes: bytes) -> list:
    image = Image.open(io.BytesIO(image_bytes)).convert('L')
    image = image.resize((28, 28))
    image_array = np.array(image).astype('float32') / 255
    serialized_array = image_array.flatten().tolist()
    return serialized_array

# API endpoint to predict the digit
@app.post('/predict')
async def predict(request: Request, file: UploadFile = File(...)):
    start_time = time.time()
    client_ip = request.client.host

    image_bytes = await file.read()
    data_point = format_image(image_bytes)
    input_length = len(data_point)

    digit = predict_digit(model, data_point)

    end_time = time.time()
    total_time = end_time - start_time
    tl_time = (total_time * 1000) / input_length  # Convert to microseconds per character

    # Update Prometheus metrics
    REQUEST_COUNT.labels(client_ip=client_ip).inc()
    REQUEST_LATENCY.labels(client_ip=client_ip, input_length=input_length).set(total_time)
    REQUEST_TL_TIME.labels(client_ip=client_ip, input_length=input_length).set(tl_time)

    return JSONResponse(content={"digit": digit})

# Prometheus metrics endpoint
@app.get('/metrics')
async def metrics():
    return generate_latest(REGISTRY)

if __name__ == "__main__":
    model_path = sys.argv[1]  # Path to the model passed as command line argument
    model = load_model(model_path)
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)