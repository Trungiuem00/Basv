import os
import requests
import time

CHANNEL_ID = "YOUR_CHANNEL_ID"  # Thay bằng ID kênh thật
DELAY_BETWEEN_MESSAGES = 3
DELAY_BETWEEN_TOKENS = 5

# Lấy token từ biến môi trường, tách bằng dấu phẩy
tokens_env = os.getenv("DISCORD_TOKENS", "")
tokens = [t.strip() for t in tokens_env.split(",") if t.strip()]

with open('noidung.txt', 'r', encoding='utf-8') as f:
    contents = [line.strip() for line in f if line.strip()]

if not tokens:
    raise Exception("Không tìm thấy token trong biến môi trường DISCORD_TOKENS!")
if not contents:
    raise Exception("noidung.txt rỗng!")

url = f"https://discord.com/api/v9/channels/{CHANNEL_ID}/messages"

while True:
    for idx, token in enumerate(tokens):
        print(f"\n[>] Gửi bằng token {idx + 1}/{len(tokens)}")

        headers = {
            "Authorization": token,
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0"
        }

        for line in contents:
            message = f"> # {line}"
            data = {"content": message}

            response = requests.post(url, headers=headers, json=data)
            if response.status_code in [200, 201, 204]:
                print(f"[+] Gửi thành công: {message}")
            else:
                print(f"[!] Lỗi {response.status_code}: {response.text}")

            time.sleep(DELAY_BETWEEN_MESSAGES)

        print(f"[-] Token {idx + 1} đã gửi xong, nghỉ {DELAY_BETWEEN_TOKENS}s\n")
        time.sleep(DELAY_BETWEEN_TOKENS)
 
