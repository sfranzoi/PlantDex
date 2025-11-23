# backend/app/main.py
from fastapi import FastAPI, UploadFile, File
from app.models import PlantnetResponseModel, AnalysisResult
from app.plantnet_api import analyze_with_plantnet

app = FastAPI(
    title="PlantDex ML Backend",
    description="Hybrid backend for processing plant images using PlantNet API",
    version="0.1"
)

@app.get("/")
def root():
    return {"message": "PlantDex backend is running!"}

@app.post("/analyze", response_model=AnalysisResult)
async def analyze_endpoint(image: UploadFile = File(...)):
    # read raw bytes
    image_bytes = await image.read()

    # pass to PlantNet API wrapper
    plantnet_data = analyze_with_plantnet(image_bytes)

    # transform into UI-ready structure
    result = AnalysisResult.from_plantnet(plantnet_data)

    return result