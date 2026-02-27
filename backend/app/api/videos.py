from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
import uuid

from app.worker.tasks import process_video_task
from app.db import supabase

router = APIRouter()

class VideoRequest(BaseModel):
    video_url: str

@router.post("/cut")
async def generate_clip(request: VideoRequest, background_tasks: BackgroundTasks):
    if not supabase:
        raise HTTPException(status_code=500, detail="Supabase não conectado.")

    job_id = str(uuid.uuid4())
    
    supabase.insert("video_jobs", {
        "id": job_id,
        "video_url": request.video_url,
        "status": "processing"
    })
    
    # Envia o job pro background asyncio native
    background_tasks.add_task(process_video_task, request.video_url, job_id)
    return {"message": "Processamento iniciado", "job_id": job_id}

@router.get("/status/{job_id}")
async def get_status(job_id: str):
    if not supabase:
        raise HTTPException(status_code=500, detail="Supabase não conectado.")

    jobs = supabase.select_eq("video_jobs", "id", job_id)
    
    if not jobs:
        raise HTTPException(status_code=404, detail="Job não encontrado")
        
    job = jobs[0]
        
    clips = []
    if job.get("status") == "done":
        db_clips = supabase.select_eq("generated_clips", "job_id", job_id)
        clips = [
            {
                "title": c["title"], 
                "start_time": c["start_time_str"], 
                "end_time": c["end_time_str"], 
                "url": f"http://localhost:8080{c['clip_path']}"
            } for c in db_clips
        ]
        
    return {
        "job_id": job["id"],
        "status": job["status"],
        "error": job.get("error_message"),
        "clips": clips
    }

@router.get("/list")
async def list_latest():
    if not supabase:
        raise HTTPException(status_code=500, detail="Supabase não conectado.")

    jobs = supabase.select_all_desc("video_jobs", "id", 10)
    
    result = []
    for job in jobs:
        clips_res = supabase.select_eq("generated_clips", "job_id", job["id"])
        result.append({
            "id": job["id"],
            "url": job["video_url"],
            "status": job["status"],
            "clips_generated": len(clips_res)
        })
    return result
