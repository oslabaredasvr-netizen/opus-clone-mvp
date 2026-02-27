import requests
import time

API_URL = "http://localhost:8080/api/v1"

def test_art_generation():
    print("\n--- Teste 2: O Motor de Artes (Estilo Canva) ---")
    payload = {"theme": "3 dicas para vender mais"}
    print(f"Enviando tema: '{payload['theme']}' para {API_URL}/art/generate")
    
    try:
        response = requests.post(f"{API_URL}/art/generate/", json=payload)
        response.raise_for_status()
        data = response.json()
        print("\nSUCESSO! Arte Gerada:")
        print(f"-> Titulo Gerado pela IA: {data.get('title')}")
        print(f"-> Prompt Imagem IA: {data.get('image_prompt')}")
        print(f"URL: {data.get('image_url')}")
        return True
    except Exception as e:
        print(f"FALHA ao gerar arte: {e}")
        if hasattr(e, 'response') and e.response:
            print(e.response.text)
        return False


def test_video_generation():
    print("\n--- Teste 1: O Motor de Cortes (Estilo Opus) ---")
    # Um video curto publico pequeno para teste rapido (aprox 1 min)
    payload = {"video_url": "https://www.youtube.com/watch?v=M7FIvfx5J10"}
    print(f"Enviando URL: '{payload['video_url']}' para {API_URL}/videos/cut")
    
    try:
        response = requests.post(f"{API_URL}/videos/cut", json=payload)
        response.raise_for_status()
        job_id = response.json().get("job_id")
        print(f"Job criado com ID: {job_id}. Aguardando processamento...")
        
        # Poll status
        for _ in range(20): # Espera até 60 segundos
            time.sleep(3)
            status_res = requests.get(f"{API_URL}/videos/status/{job_id}")
            status_data = status_res.json()
            
            status = status_data.get("status")
            print(f"Status atual: {status}")
            
            if status == "done":
                clips = status_data.get("clips", [])
                print(f"\nSUCESSO! {len(clips)} Clipes Gerados:")
                for i, clip in enumerate(clips):
                    print(f"Clip {i+1}:")
                    print(f"   Titulo: {clip.get('title')}")
                    print(f"   Inicio: {clip.get('start_time')} | Fim: {clip.get('end_time')}")
                    print(f"   URL: {clip.get('url')}")
                return True
            elif status == "error":
                print(f"Erro no processamento: {status_data.get('error')}")
                return False
                
        print("Timeout aguardando processamento de vídeo.")
        return False
        
    except Exception as e:
        print(f"FALHA ao iniciar vídeo: {e}")
        return False

if __name__ == "__main__":
    art_ok = test_art_generation()
    video_ok = test_video_generation()
    
    if art_ok and video_ok:
        print("\n[OK] TODOS OS TESTES E2E FORAM APROVADOS!")
    else:
        print("\n[FALHA] ALGUNS TESTES FALHARAM.")
