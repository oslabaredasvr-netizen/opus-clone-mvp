import sys
import os

# Adapt path to allow importing app
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.video import orchestrate_viral_clip_pipeline

if __name__ == "__main__":
    test_url = "https://www.youtube.com/watch?v=jNQXAC9IVRw"
    job_id = "test_job_abc"
    print(f"Iniciando teste de pipeline para URL: {test_url}")
    try:
        resultados = orchestrate_viral_clip_pipeline(test_url, job_id)
        print("Teste concluído com sucesso!")
        print(resultados)
    except Exception as e:
        print(f"Erro durante o teste: {e}")
