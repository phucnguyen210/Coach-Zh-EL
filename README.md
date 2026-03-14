<<<<<<< HEAD
# 🎙️ Language Coach AI — Deploy Guide

**Frontend**: GitHub Pages (miễn phí, tự động deploy)  
**Backend**: Render.com (miễn phí, giấu API key an toàn)

---

## 📁 Cấu trúc repo

```
langcoach-web/
├── frontend/
│   └── index.html          ← Chạy trên GitHub Pages
├── backend/
│   ├── main.py             ← FastAPI app
│   ├── requirements.txt
│   └── routers/
│       ├── tts.py
│       ├── chat.py
│       ├── transcribe.py
│       └── pronunciation.py
├── .github/
│   └── workflows/
│       └── deploy.yml      ← Tự động deploy GitHub Pages
├── render.yaml             ← Cấu hình Render.com
└── README.md
```

---

## 🚀 Bước 1 — Push lên GitHub

```bash
# 1. Tạo repo mới trên github.com (đặt tên: langcoach-web)
# 2. Clone về hoặc init trong thư mục này:

git init
git add .
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/langcoach-web.git
git push -u origin main
```

---

## 🖥️ Bước 2 — Deploy Backend lên Render (miễn phí)

### 2a. Tạo tài khoản Render
Vào [render.com](https://render.com) → Sign up with GitHub

### 2b. Tạo Web Service mới
1. Dashboard → **New** → **Web Service**
2. Chọn repo `langcoach-web`
3. Cấu hình:
   - **Root Directory**: `backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Plan**: Free

### 2c. Thêm Environment Variables (Đây là chỗ giấu key an toàn!)
Trong Render dashboard → **Environment**:

| Key | Value |
|-----|-------|
| `OPENAI_API_KEY` | `sk-...` (key của bạn) |
| `AZURE_SPEECH_KEY` | key Azure (tùy chọn) |
| `AZURE_SPEECH_REGION` | `eastasia` |
| `ALLOWED_ORIGINS` | `https://YOUR_USERNAME.github.io` |

### 2d. Copy URL backend
Sau khi deploy xong, Render sẽ cho URL dạng:
```
https://langcoach-api-xxxx.onrender.com
```

---

## 🌐 Bước 3 — Cập nhật URL backend vào frontend

Mở file `frontend/index.html`, tìm dòng:
```javascript
const API_BASE = "https://YOUR-APP-NAME.onrender.com";
```

Thay bằng URL Render thật của bạn:
```javascript
const API_BASE = "https://langcoach-api-xxxx.onrender.com";
```

Commit và push lại:
```bash
git add frontend/index.html
git commit -m "update API_BASE url"
git push
```

---

## 📄 Bước 4 — Bật GitHub Pages

1. Vào repo GitHub → **Settings** → **Pages**
2. Source: **GitHub Actions**
3. Lần push tiếp theo sẽ tự động deploy!

URL GitHub Pages của bạn sẽ là:
```
https://YOUR_USERNAME.github.io/langcoach-web/
```

---

## ✅ Kết quả cuối cùng

```
Người dùng
    │
    ▼
GitHub Pages (index.html)
    │  Gọi API qua HTTPS
    ▼
Render.com (FastAPI backend)
    │  Dùng key từ Environment Variables
    ▼
OpenAI API + Azure Speech API
```

**API Key an toàn tuyệt đối** — chỉ lưu trong Render Environment Variables, không có trong code.

---

## ⚠️ Lưu ý quan trọng

**Render Free Plan**:
- Server tắt sau 15 phút không có request
- Lần đầu gọi sau khi tắt sẽ chờ ~30 giây để khởi động lại
- Giải pháp: dùng [UptimeRobot](https://uptimerobot.com) ping mỗi 10 phút để giữ server luôn chạy (miễn phí)

**CORS**:
- Nhớ đặt `ALLOWED_ORIGINS` đúng URL GitHub Pages của bạn
- Format: `https://username.github.io` (không có `/` ở cuối)
=======
# Coach-Zh-EL
>>>>>>> c0b9af929738b23da6dcb9e7869b0d10e073657d
