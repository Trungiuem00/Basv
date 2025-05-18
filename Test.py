import os
import requests
import time

# ===== CẤU HÌNH =====
CHANNEL_ID = "1364890863410352180"  # ← Thay bằng Channel ID thật
DELAY_BETWEEN_TOKENS = 5        # Nghỉ giữa mỗi token
LOOP_FOREVER = True             # Đặt True để lặp mãi

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

# Định dạng toàn bộ nội dung
formatted_message = "> # " + raw.replace("\n", "\n> # ")

# ===== GỬI LIÊN TỤC =====
url = f"https://discord.com/api/v9/channels/{CHANNEL_ID}/messages"

while True:
    for i, token in enumerate(tokens):
        print(f"\n[>] Gửi bằng token {i + 1}/{len(tokens)}")

        headers = {
            "Authorization": token,
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0"
        }

        data = {"content": formatted_message}
        response = requests.post(url, headers=headers, json=data)

        if response.status_code in [200, 201, 204]:
            print(f"[✓] Gửi thành công toàn bộ nội dung.")
        else:
            print(f"[!] Lỗi {response.status_code}: {response.text}")

        print(f"[-] Nghỉ {DELAY_BETWEEN_TOKENS}s trước khi chuyển token...\n")
        time.sleep(DELAY_BETWEEN_TOKENS)

    if not LOOP_FOREVER:
        break
