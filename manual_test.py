import requests
import json

# Tera Ngrok URL
url = "https://postureteric-transriverina-alessandro.ngrok-free.dev/chat"

# Tera Payload (Jo tum bhejna chahte the)
payload = {
    "sessionId": "test-session-manual-1",
    "message": {
        "sender": "scammer",
        "text": "Ok Ramesh, verified. Now send 10rs penalty to my UPI: chor@paytm immediately to unblock."
    },
    "conversationHistory": [
        {"sender": "scammer", "text": "Your account blocked."},
        {"sender": "user", "text": "Sir please don block. My account is 30981234567."}
    ],
    "metadata": {
        "channel": "SMS",
        "language": "English",
        "locale": "IN"
    }
}

headers = {
    "Content-Type": "application/json",
    "x-api-key": "RIDHIMAGARG2301"
}

try:
    print(f"Sending message to {url}...")
    response = requests.post(url, json=payload, headers=headers)
    print("\n--- RESPONSE FROM YOUR SERVER ---")
    print(f"Status Code: {response.status_code}")
    print("Response JSON:", response.json())
except Exception as e:
    print(f"Error: {e}")