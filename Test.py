import os
import requests
import time
import threading
from flask import Flask

# ==== CẤU HÌNH ====
CHANNEL_ID = "1364890863410352180"
DELAY_BETWEEN_TOKENS = 5

# ==== ĐỌC TOKEN ====
tokens_env = os.getenv("DISCORD_TOKENS", "")
tokens = [t.strip() for t in tokens_env.split(",") if t.strip()]
if not tokens:
    raise Exception("❌ Không tìm thấy token trong biến môi trường DISCORD_TOKENS!")

# ==== ĐỌC FILE ====
with open("noidung.txt", "r", encoding="utf-8") as f:
    raw = f.read().strip()
if not raw:
    raise Exception("❌ File noidung.txt rỗng!")

formatted_message = "> # " + raw.replace("\n", "\n> # ")
url = f"https://discord.com/api/v9/channels/{CHANNEL_ID}/messages"

# ==== GỬI LIÊN TỤC ====
def send_loop():
    while True:
        for i, token in enumerate(tokens):
            headers = {
                "Authorization": token,
                "Content-Type": "application/json",
                "User-Agent": "Mozilla/5.0"
            }
            data = {"content": formatted_message}
            try:
                res = requests.post(url, headers=headers, json=data)
                if res.status_code not in [200, 201, 204]:
                    print(f"[!] Token {i + 1} lỗi {res.status_code}: {res.text}")
            except Exception as e:
                print(f"[X] Token {i + 1} gặp lỗi: {e}")
            time.sleep(DELAY_BETWEEN_TOKENS)

# ==== FLASK CHO UPTIME ====
app = Flask(__name__)

@app.route("/")
def home():
    return "OK", 200

# ==== CHẠY ====
if __name__ == "__main__":
    threading.Thread(target=send_loop, daemon=True).start()
    app.run(host="0.0.0.0", port=10000)
