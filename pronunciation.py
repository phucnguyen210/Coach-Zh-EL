"""
/api/pronunciation — Azure Speech pronunciation assessment
Trả về điểm % phát âm cho từng từ và tổng thể
"""

import os, tempfile
from fastapi import APIRouter, UploadFile, File, Form, HTTPException

router = APIRouter()

@router.post("/pronunciation")
async def assess_pronunciation(
    audio: UploadFile = File(...),
    reference_text: str = Form(...),
    lang: str = Form("en"),         # "en" = en-US, "zh" = zh-CN
):
    azure_key    = os.environ.get("AZURE_SPEECH_KEY", "")
    azure_region = os.environ.get("AZURE_SPEECH_REGION", "eastasia")

    if not azure_key:
        # Trả về None thay vì lỗi — frontend xử lý "không có Azure"
        return {"available": False, "reason": "Azure Speech not configured"}

    try:
        import azure.cognitiveservices.speech as speechsdk
    except ImportError:
        return {"available": False, "reason": "azure-cognitiveservices-speech not installed"}

    LANG_MAP = {"en": "en-US", "zh": "zh-CN"}
    speech_lang = LANG_MAP.get(lang, "en-US")

    audio_bytes = await audio.read()
    ext = ".webm"
    ct = audio.content_type or ""
    if "wav" in ct: ext = ".wav"

    with tempfile.NamedTemporaryFile(suffix=ext, delete=False) as f:
        f.write(audio_bytes); tmp = f.name

    try:
        speech_config = speechsdk.SpeechConfig(subscription=azure_key, region=azure_region)
        speech_config.speech_recognition_language = speech_lang

        audio_config = speechsdk.audio.AudioConfig(filename=tmp)
        pron_config = speechsdk.PronunciationAssessmentConfig(
            reference_text=reference_text,
            grading_system=speechsdk.PronunciationAssessmentGradingSystem.HundredMark,
            granularity=speechsdk.PronunciationAssessmentGranularity.Word,
        )
        recognizer = speechsdk.SpeechRecognizer(
            speech_config=speech_config,
            audio_config=audio_config,
        )
        pron_config.apply_to(recognizer)
        result = recognizer.recognize_once_async().get()

        if result.reason == speechsdk.ResultReason.RecognizedSpeech:
            pron = speechsdk.PronunciationAssessmentResult(result)
            words = []
            if hasattr(pron, "words"):
                for w in pron.words:
                    words.append({"word": w.word, "score": round(w.accuracy_score)})
            return {
                "available": True,
                "overall": round(pron.pronunciation_score),
                "accuracy": round(pron.accuracy_score),
                "fluency": round(pron.fluency_score),
                "completeness": round(pron.completeness_score),
                "words": words,
            }
        else:
            return {"available": True, "overall": 0, "error": "Could not recognize speech"}

    except Exception as e:
        return {"available": False, "reason": str(e)}
    finally:
        os.unlink(tmp)
