"""
/api/transcribe — Whisper STT
Nhận audio file (webm/wav), trả về text
"""

import os, tempfile
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from openai import OpenAI

router = APIRouter()

@router.post("/transcribe")
async def transcribe_audio(
    audio: UploadFile = File(...),
    lang: str = Form("auto"),   # "auto" = Whisper tự nhận diện
):
    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        raise HTTPException(500, "OPENAI_API_KEY not configured on server")

    client = OpenAI(api_key=key)
    audio_bytes = await audio.read()

    # Detect extension từ content_type
    ct = audio.content_type or ""
    ext = ".webm"
    if "wav" in ct:   ext = ".wav"
    elif "mp4" in ct: ext = ".mp4"
    elif "ogg" in ct: ext = ".ogg"

    with tempfile.NamedTemporaryFile(suffix=ext, delete=False) as f:
        f.write(audio_bytes)
        tmp = f.name

    try:
        kwargs = {"model": "whisper-1", "file": open(tmp, "rb")}
        if lang != "auto":
            kwargs["language"] = lang   # "en" hoặc "zh"
        result = client.audio.transcriptions.create(**kwargs)
        return {"text": result.text.strip(), "lang_detected": lang}
    except Exception as e:
        raise HTTPException(500, str(e))
    finally:
        os.unlink(tmp)
