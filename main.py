import requests
import time
import os

from urllib.parse import urlparse


class NodeGoPinger:
    def __init__(self, token, proxy_url=None):
        self.api_base_url = "https://nodego.ai/api"
        self.bearer_token = token
        self.session = requests.Session()

        if proxy_url:
            self.set_proxy(proxy_url)

    def set_proxy(self, proxy_url):
        parsed_url = urlparse(proxy_url)

        if proxy_url.startswith("socks"):
            self.session.proxies = {"http": proxy_url, "https": proxy_url}
        elif proxy_url.startswith("http"):
            self.session.proxies = {"http": proxy_url, "https": proxy_url}
        else:
            http_url = f"http://{proxy_url}"
            self.session.proxies = {"http": http_url, "https": http_url}

    def make_request(self, method, endpoint, data=None):
        url = f"{self.api_base_url}{endpoint}"
        headers = {
            "Authorization": f"Bearer {self.bearerToken}",
            "Content-Type": "application/json",
            "Accept": "*/*",
        }

        try:
            response = self.session.request(
                method, url, json=data, headers=headers, timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return None

    def get_user_info(self):
        response = self.make_request("GET", "/user/me")
        if response:
            metadata = response.get("metadata", {})
            return {
                "username": metadata.get("username"),
                "email": metadata.get("email"),
                "totalPoint": metadata.get("rewardPoint"),
                "nodes": [
                    {
                        "id": node.get("id"),
                        "totalPoint": node.get("totalPoint"),
                        "todayPoint": node.get("todayPoint"),
                        "isActive": node.get("isActive"),
                    }
                    for node in metadata.get("nodes", [])
                ],
            }
        return None

    def ping(self):
        response = self.make_request("POST", "/user/nodes/ping", {"type": "extension"})
        if response:
            return {
                "statusCode": response.get("statusCode"),
                "message": response.get("message"),
                "metadataId": response.get("metadata", {}).get("id"),
            }
        return None


class MultiAccountPinger:
    def __init__(self):
        self.accounts = self.load_accounts()
        self.is_running = True

    def load_accounts(self):
        try:
            with open("forest.txt", "r", encoding="utf-8") as f:
                account_data = [line.strip() for line in f if line.strip()]

            proxy_data = []
            if os.path.exists("proxies.txt"):
                with open("proxies.txt", "r", encoding="utf-8") as f:
                    proxy_data = [line.strip() for line in f if line.strip()]

            return [
                {"token": account_data[i], "proxy": proxy_data[i] if i < len(proxy_data) else None}
                for i in range(len(account_data))
            ]

        except Exception as e:
            print(f"Error reading accounts: {e}")
            exit(1)

    def process_single_account(self, account):
        pinger = NodeGoPinger(account["token"], account["proxy"])
        
        user_info = pinger.get_user_info()
        if not user_info:
            print("Failed to retrieve user info")
            return

        ping_response = pinger.ping()
        if ping_response:
            print("=" * 50)
            print(f"🌲 [FORESTARMY] Username: {user_info['username']}")
            print(f"📧 Email: {user_info['email']}")
            for index, node in enumerate(user_info["nodes"], start=1):
                print(f"\n🌳 Node {index}:")
                print(f"  🔹 ID: {node['id']}")
                print(f"  🔸 Total Points: {node['totalPoint']}")
                print(f"  🔹 Today's Points: {node['todayPoint']}")
                print(f"  🔸 Status: {'✅ Active' if node['isActive'] else '❌ Inactive'}")
            print(f"\n🏆 Total Points: {user_info['totalPoint']}")
            print(f"📡 Status Code: {ping_response['statusCode']}")
            print(f"💬 Ping Message: {ping_response['message']}")
            print(f"🆔 Metadata ID: {ping_response['metadataId']}")
            print("=" * 50)

    def run_pinger(self):
        print("\n🌲 [FORESTARMY] Proudly made by itsmesatyavir 🌲")
        print("🚀 No selling, No spam 🚀")

        while self.is_running:
            print(f"\n⏰ Ping Reset at {time.strftime('%Y-%m-%d %H:%M:%S')}")

            for account in self.accounts:
                if not self.is_running:
                    break
                self.process_single_account(account)

            if self.is_running:
                time.sleep(15)


# Run the multi-account pinger
if __name__ == "__main__":
    pinger = MultiAccountPinger()
    pinger.run_pinger()
