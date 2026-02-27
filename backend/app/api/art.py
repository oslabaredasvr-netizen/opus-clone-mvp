from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import urllib.parse
from google import genai
from google.genai import types
from app.core.config import settings
import json

router = APIRouter()

class ArtRequest(BaseModel):
    theme: str

@router.post("/generate")
@router.post("/generate/")
async def generate_art(request: ArtRequest):
    if not settings.gemini_api_key:
        raise HTTPException(status_code=500, detail="Chave GEMINI_API_KEY não configurada no .env.")

    try:
        client = genai.Client(api_key=settings.gemini_api_key)
        
        prompt = f"""
        Você é um Designer Especialista em Thumbnails Virais (Capas de Vídeo) para YouTube e TikTok.
        O usuário solicitou o seguinte tema/nicho: "{request.theme}"
        
        Sua tarefa é criar um conceito visual de altíssima conversão para uma miniatura (thumbnail).
        Retorne ESTRITAMENTE um JSON válido com os seguintes campos:
        - "titulo_chamativo": Um texto curto, impactante e curioso (máximo 5 palavras) para colocar na imagem.
        - "image_prompt": Um prompt detalhado em inglês para um gerador de imagens por IA (Midjourney/DALL-E style). Deve descrever uma cena hiper-realista, iluminação dramática, cores vibrantes, e o elemento principal em destaque. Não inclua texto no prompt da imagem.
        
        Exemplo de saída:
        {{
            "titulo_chamativo": "O Fim do Dinheiro!",
            "image_prompt": "Hyper-realistic close-up of a broken golden coin shattering on a dark neon background, cinematic lighting, 8k resolution, highly detailed"
        }}
        """
        
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        
        # Limpar o markdown do JSON de retorno
        content = response.text
        if content.startswith("```json"):
            content = content.replace("```json", "").replace("```", "").strip()
        elif content.startswith("```"):
            content = content.replace("```", "").strip()
            
        data = json.loads(content)
        
        # Gera a imagem gratuitamente sem chave extra usando Pollinations (Texto -> Imagem)
        safe_img_prompt = urllib.parse.quote(data['image_prompt'])
        image_url = f"https://image.pollinations.ai/prompt/{safe_img_prompt}?width=1080&height=1920&nologo=true"
        
        return {
            "status": "success",
            "theme": request.theme,
            "title": data['titulo_chamativo'],
            "image_url": image_url,
            "image_prompt": data['image_prompt']
        }
        
    except Exception as e:
        print(f"Erro ao gerar arte: {e}")
        raise HTTPException(status_code=500, detail=str(e))
