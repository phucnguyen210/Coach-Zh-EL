"""
/api/tts — Text to Speech
Nhận text + lang, trả về audio/mpeg (base64)
"""

import os, base64
from fastapi import APIRouter, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel
from openai import OpenAI

router = APIRouter()

VOICES = {"en": "nova", "zh": "shimmer"}

class TTSRequest(BaseModel):
    text: str
    lang: str = "en"
    hd: bool = False          # True = tts-1-hd (chất lượng cao hơn, chậm hơn)

@router.post("/tts")
async def text_to_speech(req: TTSRequest):
    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        raise HTTPException(500, "OPENAI_API_KEY not configured on server")

    client = OpenAI(api_key=key)
    model  = "tts-1-hd" if req.hd else "tts-1"
    voice  = VOICES.get(req.lang, "nova")

    # Làm sạch ký tự markdown trước khi đọc
    clean = req.text
    for ch in ["✏️", "✅", "**", "*", "# "]:
        clean = clean.replace(ch, "")

    try:
        response = client.audio.speech.create(model=model, voice=voice, input=clean)
        audio_bytes = response.read()
        b64 = base64.b64encode(audio_bytes).decode()
        return {"audio_b64": b64, "format": "mp3"}
    except Exception as e:
        raise HTTPException(500, str(e))
