import os
import sys
import json
import subprocess
from datetime import datetime
import imageio_ffmpeg
from groq import Groq
from app.core.config import settings

# Initialize Groq only if the key is provided
client = Groq(api_key=settings.groq_api_key) if settings.groq_api_key else None
ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()


def extract_audio(video_path: str, audio_path: str):
    command = [ffmpeg_exe, "-i", video_path, "-q:a", "0", "-map", "a", audio_path, "-y"]
    subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def transcribe_audio(audio_path: str) -> str:
    if not client:
        return "[00:00:00] Transcrição Mockada porque não há Chave API do Groq configurada."
        
    with open(audio_path, "rb") as file:
        transcription = client.audio.transcriptions.create(
            file=(audio_path, file.read()),
            model="whisper-large-v3",
            response_format="verbose_json",
        )
        
    formatted_text = ""
    for segment in transcription.segments:
        start = int(segment['start']) if isinstance(segment, dict) else int(segment.start)
        m, s = divmod(start, 60)
        h, m = divmod(m, 60)
        time_str = f"{h:02d}:{m:02d}:{s:02d}"
        text = segment['text'] if isinstance(segment, dict) else segment.text
        formatted_text += f"[{time_str}] {text}\n"
        
    return formatted_text

def get_viral_cuts(transcription_text: str) -> list:
    if not client:
        # Se não tiver chave, devolve um corte falso usando o novo formato de modelo
        return [{
            "id_clipe": 1,
            "titulo_sugerido": "Corte Demonstrativo (SEM IA)",
            "virality_score": 90,
            "explicacao_do_score": "Mock local sem Chave da Groq no .env",
            "start_time": "00:00:00",
            "end_time": "00:00:10"
        }]
        
    prompt = f"""
    Você é um Produtor de Conteúdo Viral Sênior e Estrategista de Retenção, especialista nos algoritmos do TikTok, Instagram Reels e YouTube Shorts. Sua missão é ler a transcrição de um vídeo longo (com marcações de tempo) e garimpar os "momentos de ouro" para criar clipes curtos.

    Regras de Seleção (O que faz um clipe ser viral):
    - O Gancho (Hook): O trecho deve começar com uma afirmação forte, uma pergunta intrigante ou uma quebra de expectativa nos primeiros 3 segundos.
    - Compreensão Isolada: O clipe deve fazer sentido por si só. O espectador não precisa ter assistido ao vídeo original para entender o contexto.
    - Duração: Cada clipe deve ter estritamente entre 30 e 60 segundos.
    - Ponto Alto (Payoff): O trecho deve entregar um valor claro (educacional, entretenimento ou polêmica) antes de terminar.
    - Corte Preciso: Não inicie ou termine o clipe no meio de uma palavra ou frase incompleta.

    Instruções de Saída:
    Analise a transcrição fornecida e retorne os 3 melhores clipes potenciais.
    Você DEVE responder ÚNICA e EXCLUSIVAMENTE em formato JSON válido, sem nenhuma introdução, conclusão ou formatação markdown (sem ```json).

    Formato de Saída Obrigatório:
    [
      {{
        "id_clipe": 1,
        "titulo_sugerido": "Como a IA vai dominar o Trading Esportivo",
        "virality_score": 95,
        "explicacao_do_score": "O trecho revela uma estratégia não óbvia sobre agentes autônomos, gerando alta curiosidade e retenção inicial.",
        "start_time": "00:12:34",
        "end_time": "00:13:20"
      }}
    ]

    Transcrição a ser analisada:
    {transcription_text}
    """
    
    response = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama3-8b-8192",
        temperature=0.3
    )
    
    try:
        content = response.choices[0].message.content
        content = content.replace('```json', '').replace('```', '').strip()
        return json.loads(content)
    except Exception as e:
        print(f"Erro no JSON do Groq: {e}")
        return []

def calcular_duracao(start_time, end_time):
    """Calcula a duração do clipe subtraindo o tempo final do inicial."""
    # Trata caso onde start_time seria já em float
    if isinstance(start_time, float) or isinstance(start_time, int):
        return str(float(end_time) - float(start_time))
        
    try:
        # Tenta formato com hora "00:00:10"
        formato = "%H:%M:%S"
        inicio = datetime.strptime(start_time, formato)
        fim = datetime.strptime(end_time, formato)
        duracao = fim - inicio
        return str(duracao)
    except Exception:
        # Fallback de segurança para outros formatos
        return str(end_time)

def cut_and_subtitle_video(video_path: str, start, end, output_path: str):
    duracao = calcular_duracao(start, end)
    
    command = [
        ffmpeg_exe, 
        "-y",
        "-ss", str(start), 
        "-i", video_path, 
        "-t", duracao, 
        "-c:v", "libx264", 
        "-preset", "fast",
        "-c:a", "aac", 
        output_path
    ]
    subprocess.run(command, check=True)

def orchestrate_viral_clip_pipeline(video_url: str, job_id: str):
    base_dir = "public/clips"
    os.makedirs(base_dir, exist_ok=True)
    video_path = os.path.join(base_dir, f"{job_id}.mp4")
    
    # Download with yt-dlp instead of urllib
    # It supports YouTube and many other sites
    print(f"Baixando video de {video_url} via yt-dlp...")
    dl_command = [sys.executable, "-m", "yt_dlp", "--ffmpeg-location", ffmpeg_exe, "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4", "-o", video_path, video_url]
    subprocess.run(dl_command, check=True)
    
    # Se o arquivo baixado for .webm por conta do format, forçamos renomear ou yt-dlp ja baixa
    actual_video_path = video_path
    if not os.path.exists(video_path):
        # yt-dlp might append .mkv or other extension
        for file in os.listdir(base_dir):
            if file.startswith(job_id):
                actual_video_path = os.path.join(base_dir, file)
                break
    
    audio_path = actual_video_path.replace(".mp4", ".mp3").replace(".mkv", ".mp3").replace(".webm", ".mp3")
    
    print("1. Extraindo Audio...")
    extract_audio(actual_video_path, audio_path)
    
    print("2. Gerando Transcrição...")
    text = transcribe_audio(audio_path)
    
    print("3. Analisando cortes virais...")
    cuts = get_viral_cuts(text)
    
    generated_files = []
    print("4. Executando recortes FFmpeg...")
    for index, cut in enumerate(cuts):
        output_file = f"clip_{index}_{job_id}.mp4"
        output_path = os.path.join(base_dir, output_file)
        
        # A API pode retornar end_time maior que o video se houver alucinação.
        try:
            cut_and_subtitle_video(actual_video_path, cut['start_time'], cut['end_time'], output_path)
            # Fetch default value to title using the new property names
            title = cut.get('titulo_sugerido', f'Clipe {index}')
            generated_files.append({"path": f"/clips/{output_file}", "title": title, "start": cut['start_time'], "end": cut['end_time']})
        except Exception as e:
            print(f"Aviso: Erro ao cortar trecho {cut}: {e}")
            
    # Limpar originais para economizar espaço
    if os.path.exists(actual_video_path): os.remove(actual_video_path)
    if os.path.exists(audio_path): os.remove(audio_path)
        
    return generated_files
