# backend/app/plantnet_api.py
import requests
import os

PLANTNET_API_KEY = os.getenv("PLANTNET_API_KEY")
PLANTNET_ENDPOINT = "https://my-api.plantnet.org/v2/identify/all"

def analyze_with_plantnet(image_bytes: bytes):
    if not PLANTNET_API_KEY:
        raise RuntimeError("PlantNet API key not set.")

    files = {
        "images": ("image.jpg", image_bytes, "image/jpeg")
    }

    params = {
        "api-key": PLANTNET_API_KEY,
        "include-related-images": "true",
        "include-organ": "flower,leaf,fruit,habit"
    }

    response = requests.post(
        PLANTNET_ENDPOINT,
        files=files,
        params=params
    )

    if response.status_code != 200:
        raise RuntimeError(f"PlantNet returned error: {response.status_code}, {response.text}")

    return response.json()