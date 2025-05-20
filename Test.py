import os
import requests
import time
import threading
from flask import Flask

# ==== CẤU HÌNH ====
CHANNEL_ID = os.getenv("CHANNEL_ID", "")
DELAY_BETWEEN_TOKENS = 3  # giây

# ==== LẤY TOKEN ====
tokens_env = os.getenv("DISCORD_TOKENS", "")
tokens = [t.strip() for t in tokens_env.split(",") if t.strip()]
if not tokens:
    raise Exception("❌ Không tìm thấy token trong biến môi trường DISCORD_TOKENS!")
if not CHANNEL_ID:
    raise Exception("❌ Không có CHANNEL_ID trong biến môi trường!")

# ==== ĐỌC NỘI DUNG TỪ FILE ====
if not os.path.exists("noidung.txt"):
    raise Exception("❌ Thiếu file noidung.txt!")

with open("noidung.txt", "r", encoding="utf-8") as f:
    raw = f.read().strip()

if not raw:
    raise Exception("❌ File noidung.txt rỗng!")

formatted_message = "> # " + raw.replace("\n", "\n> # ")
url = f"https://discord.com/api/v9/channels/{CHANNEL_ID}/messages"

# ==== GỬI TIN NHẮN CHO MỖI TOKEN ====
def send_loop_token(token, index):
    while True:
        headers = {
            "Authorization": token,
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0"
        }
        data = {"content": formatted_message}
        try:
            res = requests.post(url, headers=headers, json=data)
            if res.status_code not in [200, 201, 204]:
                print(f"[!] Token {index + 1} lỗi {res.status_code}: {res.text}")
        except Exception as e:
            print(f"[X] Token {index + 1} gặp lỗi: {e}")
        time.sleep(DELAY_BETWEEN_TOKENS)

# ==== FLASK SERVER CHO UPTIME ====
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot đang chạy", 200

if __name__ == "__main__":
    for i, token in enumerate(tokens):
        threading.Thread(target=send_loop_token, args=(token, i), daemon=True).start()
    app.run(host="0.0.0.0", port=8080)
