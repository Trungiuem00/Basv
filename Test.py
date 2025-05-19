import os
import requests
import time
import threading
from fastapi import FastAPI
import uvicorn

app = FastAPI()

# ==== CẤU HÌNH ====
CHANNEL_ID = "1372978987713826876"  # ← Thay bằng Channel ID thật
DELAY_BETWEEN_TOKENS = 5        # Giây nghỉ giữa mỗi token

# ==== ĐỌC TOKEN TỪ ENV ====
tokens_env = os.getenv("DISCORD_TOKENS", "")
tokens = [t.strip() for t in tokens_env.split(",") if t.strip()]
if not tokens:
    raise Exception("❌ Không tìm thấy token trong biến môi trường DISCORD_TOKENS!")

# ==== ĐỌC FILE ====
with open("noidung.txt", "r", encoding="utf-8") as f:
    raw = f.read().strip()
if not raw:
    raise Exception("❌ File noidung.txt rỗng!")

# ==== ĐỊNH DẠNG ====
formatted_message = "> # " + raw.replace("\n", "\n> # ")
url = f"https://discord.com/api/v9/channels/{CHANNEL_ID}/messages"

# ==== GỬI NỘI DUNG ====
def send_loop():
    while True:
        for i, token in enumerate(tokens):
            headers = {
                "Authorization": token,
                "Content-Type": "application/json",
                "User-Agent": "Mozilla/5.0"
            }
            data = {"content": formatted_message}
            res = requests.post(url, headers=headers, json=data)

            if res.status_code in [200, 201, 204]:
                print(f"[✓] Token {i + 1} gửi thành công.")
            else:
                print(f"[!] Token {i + 1} lỗi {res.status_code}: {res.text}")

            time.sleep(DELAY_BETWEEN_TOKENS)

# ==== API ====
@app.get("/")
def home():
    return {"status": "Bot is chạy. Dùng /start để bắt đầu gửi."}

@app.get("/start")
def start():
    threading.Thread(target=send_loop).start()
    return {"status": "Đã bắt đầu gửi nội dung liên tục."}

# ==== CHẠY SERVER (cho local test) ====
if __name__ == "__main__":
    uvicorn.run("Test:app", host="0.0.0.0", port=10000)
