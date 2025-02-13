import requests
import time
import itertools

# ───────────────────────────────────────────
#  🌲 FORESTARMY - NodeGO Multi-Account Script
#  Proudly made by itsmesatyavir
#  No selling | No Spam
# ───────────────────────────────────────────

# Endpoints
ping_url = "https://nodego.ai/api/user/nodes/ping"
client_ip_url = "https://api.bigdatacloud.net/data/client-ip"

# Default Authorization token
default_token = "eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxMzAxNjcwMjYzODA0Mzk1NTIwIiwiaWF0IjoxNzM5MzQwMTM5LCJleHAiOjE3NDA1NDk3Mzl9.S_1r665mmdG1h-ph9tdZz7pzESUiMxI5tDlLFxjjskjRXUMPbYb58mo7M8UXAK2u7ggZUu0v2ZA5H0pPlUN4Xw"

# Load tokens from forest.txt
def load_tokens(filename="forest.txt"):
    try:
        with open(filename, "r") as f:
            tokens = [line.strip() for line in f if line.strip()]
        return tokens if tokens else [default_token]  # Use default if file is empty
    except FileNotFoundError:
        return [default_token]  # Use default if file doesn't exist

tokens = load_tokens()
token_cycle = itertools.cycle(tokens)  # Rotate tokens

# Headers for client IP request
headers = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-US,en;q=0.9",
    "Origin": "chrome-extension://jbmdcnidiaknboflpljihfnbonjgegah",
    "Sec-Ch-Ua": '"Chromium";v="130", "Mises";v="130", "Not?A_Brand";v="99"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": '"Android"',
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "cross-site",
    "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
}

# Payload for ping request
ping_payload = {"type": "extension"}

# Infinite request loop
request_count = 0

try:
    while True:
        request_count += 1
        current_token = next(token_cycle)  # Get the next token

        # Headers for ping request
        ping_headers = headers.copy()
        ping_headers["Authorization"] = f"Bearer {current_token}"
        ping_headers["Content-Type"] = "application/json"

        # Send POST request to ping endpoint
        try:
            ping_response = requests.post(ping_url, headers=ping_headers, json=ping_payload)
            print(f"[{request_count}] Ping Status: {ping_response.status_code}, Response: {ping_response.json()}")
        except Exception as e:
            print(f"[{request_count}] Ping Error: {str(e)}")

        # Send GET request to client IP endpoint
        try:
            client_ip_response = requests.get(client_ip_url, headers=headers)
            print(f"[{request_count}] Client IP Status: {client_ip_response.status_code}, Response: {client_ip_response.json()}")
        except Exception as e:
            print(f"[{request_count}] Client IP Error: {str(e)}")

        time.sleep(1)  # Delay to prevent excessive load
except KeyboardInterrupt:
    print("\nScript stopped by user.")
