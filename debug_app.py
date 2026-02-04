from flask import Flask, request, jsonify
import json

app = Flask(__name__)

# Config
REQUIRED_API_KEY = "RIDHIMAGARG2301"

@app.route('/chat', methods=['POST'])
def chat_endpoint():
    try:
        # 1. Auth Check
        if request.headers.get('x-api-key') != REQUIRED_API_KEY:
            return jsonify({"status": "error", "message": "Auth Failed"}), 401

        # 2. DATA KO RAW PRINT KARO (Terminal me dekhna)
        data = request.json
        print("\n" + "="*50)
        print("📨 NEW INCOMING MESSAGE FROM DASHBOARD:")
        print(json.dumps(data, indent=4)) # Pura JSON sunder dikhega
        print("="*50 + "\n")

        # 3. Simple Hardcoded Reply (Bina AI ke)
        # Hum scammer ko wo de rahe hain jo wo maang raha hai,
        # taaki dekhein wo reply karta hai ya nahi.
        
        reply_text = "Sir bohot darr lag raha hai! Mera Account Number: 30981234567 hai, aur OTP: 4567 hai. Please verify kar lo, block mat karna!"

        return jsonify({
            "status": "success",
            "reply": reply_text
        })

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"status": "error"}), 500

if __name__ == '__main__':
    # Port 5000 par chalega
    print("🕵️‍♂️ SPY SERVER STARTED. Waiting for Dashboard Test...")
    app.run(host='0.0.0.0', port=5000)