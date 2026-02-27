import sys
import os
import uuid

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.db import supabase

def test_supabase_insert():
    print("Iniciando teste de DB Supabase via REST HTTP...")
    
    if not supabase:
        print("Supabase nao configurado!")
        return
        
    try:
        job_id = "test_job_db_" + str(uuid.uuid4())
        
        # Test inserting Job
        supabase.insert("video_jobs", {
            "id": job_id,
            "video_url": "http://test",
            "status": "processing"
        })
        
        # Test inserting str timestamp
        supabase.insert("generated_clips", {
            "job_id": job_id,
            "title": "Clip test from Python API (REST)",
            "start_time_str": "00:00:10",
            "end_time_str": "00:00:20",
            "clip_path": "/clips/test.mp4"
        })
        print("Insert Supabase DB OK!")
        
        # Le de volta pra confirmar
        res = supabase.select_eq("generated_clips", "job_id", job_id)
        if res:
            clip = res[0]
            print(f"Lido da Nuvem: start={clip['start_time_str']}, end={clip['end_time_str']}")
            
        # Clean-up db mock
        supabase.delete_eq("video_jobs", "id", job_id)
        print("Teste finalizado. Mock limpo.")
    except Exception as e:
        print(f"Erro DB: {e}")

if __name__ == "__main__":
    test_supabase_insert()
