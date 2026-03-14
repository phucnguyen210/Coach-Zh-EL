"""
Language Coach AI — FastAPI Backend
Deploy lên Render.com (miễn phí)
Key OpenAI & Azure được giấu trong Environment Variables — 100% an toàn
"""

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import tts, chat, transcribe, pronunciation

app = FastAPI(title="Language Coach AI", version="2.0")

# CORS — cho phép GitHub Pages gọi API
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(tts.router,           prefix="/api")
app.include_router(chat.router,          prefix="/api")
app.include_router(transcribe.router,    prefix="/api")
app.include_router(pronunciation.router, prefix="/api")

@app.get("/")
def root():
    return {"status": "ok", "app": "Language Coach AI v2"}

@app.get("/health")
def health():
    return {"status": "healthy"}
