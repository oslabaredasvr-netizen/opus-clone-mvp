from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.api.videos import router as videos_router
from app.api.art import router as art_router
import os

app = FastAPI(title="Video Automation API", version="1.0.0")

# Ensure public dir exists for statically serving videos locally
os.makedirs("public/clips", exist_ok=True)
app.mount("/clips", StaticFiles(directory="public/clips"), name="clips")

# Allow requests from Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(videos_router, prefix="/api/v1/videos", tags=["Videos"])
app.include_router(art_router, prefix="/api/v1/art", tags=["Art"])

@app.get("/")
def root():
    return {"message": "Video Automation API is running"}
