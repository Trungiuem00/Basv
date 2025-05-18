import os
import requests
import time
import threading
from fastapi import FastAPI
import uvicorn

app = FastAPI()

# ===== CẤU HÌNH =====
CHANNEL_ID = "1364890863410352180"  # ← Thay bằng ID kênh thật
DELAY_BETWEEN_TOKENS = 5

# ===== ĐỌC TOKEN =====
tokens_env = os.getenv("DISCORD_TOKENS", "")
tokens = [t.strip() for t in tokens_env.split(",") if t.strip()]
if not tokens:
    raise Exception("❌ Không tìm thấy token trong biến môi trường DISCORD_TOKENS!")

# ===== ĐỌC NỘI DUNG =====
with open("noidung.txt", "r", encoding="utf-8") as f:
    raw = f.read().strip()
if not raw:
    raise Exception("❌ File noidung.txt rỗng!")

# Format nội dung
formatted_message = "> # " + raw.replace("\n", "\n> # ")
url = f"https://discord.com/api/v9/channels/{CHANNEL_ID}/messages"

def send_loop():
    while True:
        for idx, token in enumerate(tokens):
            headers = {
                "Authorization": token,
                "Content-Type": "application/json",
                "User-Agent": "Mozilla/5.0"
            }

            data = {"content": formatted_message}
            response = requests.post(url, headers=headers, json=data)

            if response.status_code in [200, 201, 204]:
                print(f"[✓] Token {idx + 1} gửi thành công")
            else:
                print(f"[!] Token {idx + 1} lỗi {response.status_code}: {response.text}")

            time.sleep(DELAY_BETWEEN_TOKENS)

@app.get("/")
def root():
    return {"status": "Running. Use /start to begin sending."}

@app.get("/start")
def start():
    threading.Thread(target=send_loop).start()
    return {"status": "Gửi nội dung đang chạy trong nền."}

# ===== Khởi động server khi chạy trực tiếp =====
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=10000)
