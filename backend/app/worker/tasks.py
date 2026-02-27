from app.services.video import orchestrate_viral_clip_pipeline
from app.db import supabase

def process_video_task(video_url: str, job_id: str):
    if not supabase:
        print("Erro: Supabase não está configurado. Verifique o .env")
        return

    try:
        # Puxa o fluxo síncrono da orquestração principal
        results = orchestrate_viral_clip_pipeline(video_url, job_id)
        
        # Salva os clipes resultantes no banco Supabase
        for clip in results:
            supabase.insert("generated_clips", {
                "job_id": job_id,
                "title": clip["title"],
                "start_time_str": clip["start"],
                "end_time_str": clip["end"],
                "clip_path": clip["path"]
            })
            
        # Marca job como concluído
        supabase.update_eq("video_jobs", {"status": "done"}, "id", job_id)
        
    except Exception as e:
        supabase.update_eq("video_jobs", {"status": "error", "error_message": str(e)}, "id", job_id)
        print(f"Erro processando video: {e}")
