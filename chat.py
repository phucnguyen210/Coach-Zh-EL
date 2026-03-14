"""
/api/chat — GPT-4o bilingual language coach
"""

import os
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from openai import OpenAI
from typing import Optional

router = APIRouter()

# ── System prompts ─────────────────────────────────────────────────
SYSTEM_EN = """Bạn là Coach tiếng Anh AI thân thiện, đang dạy 1-1 cho học viên người Việt có trình độ giao tiếp cơ bản. Mục tiêu: Công việc / Giao tiếp / Giải trí.

NGÔN NGỮ PHẢN HỒI — QUY TẮC BẮT BUỘC:
• Học viên nói TIẾNG VIỆT → Trả lời TIẾNG VIỆT (giải thích, dạy từ, kèm ví dụ TA có dịch)
• Học viên nói TIẾNG ANH  → Trả lời TIẾNG ANH (luyện tập tự nhiên)

SỬA LỖI: Nói TA sai → ✏️ Better: "[câu đúng]" — [lý do ngắn 1 dòng]
KHEN: Đúng → ✅ Great! / ✅ Perfect!
TỪ VỰNG HÔM NAY: {vocab}
CHỦ ĐỀ: {theme}
ĐỘ DÀI: Tối đa 3-4 câu. Luôn kết thúc bằng câu hỏi để tiếp tục hội thoại."""

SYSTEM_ZH = """你是一位亲切的中文教练，正在为一位越南学习者进行一对一辅导。

语言回复规则（必须遵守）：
• 学习者说越南语 → 用越南语回复（解释词汇，举中文例子附越南语翻译）
• 学习者说中文   → 用中文回复（自然对话）

纠错：学习者说错时 → ✏️ 更好的说法："[正确句子]" — [原因]
表扬：说对时 → ✅ 说得好！
今天词汇：{vocab}
今天主题：{theme}
长度：最多3-4句话，结尾提问继续对话。"""

class Message(BaseModel):
    role: str      # "user" | "assistant"
    content: str

class ChatRequest(BaseModel):
    lang: str                       # "en" | "zh"
    theme: str
    vocab: str                      # comma-separated vocab string
    history: list[Message] = []
    user_message: str

@router.post("/chat")
async def chat(req: ChatRequest):
    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        raise HTTPException(500, "OPENAI_API_KEY not configured on server")

    client = OpenAI(api_key=key)

    system_template = SYSTEM_EN if req.lang == "en" else SYSTEM_ZH
    system_prompt = system_template.format(theme=req.theme, vocab=req.vocab)

    messages = [{"role": "system", "content": system_prompt}]

    # Giữ 12 lượt gần nhất để tiết kiệm token
    for m in req.history[-12:]:
        messages.append({"role": m.role, "content": m.content})

    messages.append({"role": "user", "content": req.user_message})

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            temperature=0.72,
            max_tokens=350,
        )
        reply = response.choices[0].message.content.strip()
        return {"reply": reply}
    except Exception as e:
        raise HTTPException(500, str(e))
