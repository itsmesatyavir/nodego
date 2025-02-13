import requests
import time
import itertools
from colorama import Fore, Style, init

# Initialize colorama for colored output
init(autoreset=True)

# ───────────────────────────────────────────
#  🌲 forestarmy - NODEGO Unlimited Requests Script
#  Proudly made by itsmesatyavir
#  No selling | No Spam
# ───────────────────────────────────────────

banner = f"""{Fore.CYAN + Style.BRIGHT}
──────────────────────────────────────────
 🌲 FORESTARMY - NODEGO Unlimited Requests Script
 Proudly made by itsmesatyavir
 No selling | No Spam
──────────────────────────────────────────
{Style.RESET_ALL}"""
print(banner)

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
            if ping_response.status_code == 201:
                try:
                    print(f"{Fore.GREEN + Style.BRIGHT}[{request_count}] Ping Success: {ping_response.json()}{Style.RESET_ALL}")
                except ValueError:
                    print(f"{Fore.GREEN + Style.BRIGHT}[{request_count}] Ping Success (Non-JSON Response): {ping_response.text}{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED + Style.BRIGHT}[{request_count}] Ping Failed: {ping_response.status_code}, Response: {ping_response.text}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED + Style.BRIGHT}[{request_count}] Ping Error: {str(e)}{Style.RESET_ALL}")

        # Send GET request to client IP endpoint
        try:
            client_ip_response = requests.get(client_ip_url, headers=headers)
            if client_ip_response.status_code == 200:
                try:
                    print(f"{Fore.GREEN + Style.BRIGHT}[{request_count}] Client IP Success: {client_ip_response.json()}{Style.RESET_ALL}")
                except ValueError:
                    print(f"{Fore.GREEN + Style.BRIGHT}[{request_count}] Client IP Success (Non-JSON Response): {client_ip_response.text}{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED + Style.BRIGHT}[{request_count}] Client IP Failed: {client_ip_response.status_code}, Response: {client_ip_response.text}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED + Style.BRIGHT}[{request_count}] Client IP Error: {str(e)}{Style.RESET_ALL}")

        time.sleep(5)  # Delay to prevent excessive load
except KeyboardInterrupt:
    print("\nScript stopped by user.")
    
