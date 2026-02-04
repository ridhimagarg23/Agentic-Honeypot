from flask import Flask, request, jsonify
import threading
import requests
import os
from datetime import datetime

# Import modules (Ensure these files are in the same directory)
try:
    from scam_detector import detect_scam_intent
    from ai_agent import generate_scambait_reply
    from scam_data_extractor import extractor
except ImportError as e:
    print(f"Import Error: Make sure your module files are present. {e}")

app = Flask(__name__)

# --- CONFIG ---
# Pro-tip: Use environment variables for production!
REQUIRED_API_KEY = os.getenv("HONEYPOT_API_KEY", "RIDHIMAGARG2301")
GUVI_CALLBACK_URL = "https://hackathon.guvi.in/api/updateHoneyPotFinalResult"

# Global Session Storage (In-memory)
session_storage = {}

def send_guvi_callback(session_id, session_data):
    """
    STRICT JSON PAYLOAD SENDER
    Runs in background on standard VPS/PaaS.
    """
    try:
        payload = {
            "sessionId": session_id,
            "scamDetected": session_data["scamDetected"],
            "totalMessagesExchanged": session_data["msg_count"],
            "extractedIntelligence": {
                "bankAccounts": session_data["intel"].get("bankAccounts", []),
                "upiIds": session_data["intel"].get("upiIds", []),
                "phishingLinks": session_data["intel"].get("phishingLinks", []),
                "phoneNumbers": session_data["intel"].get("phoneNumbers", []),
                "suspiciousKeywords": session_data["intel"].get("suspiciousKeywords", [])
            },
            "agentNotes": extractor.generate_agent_notes(session_data["intel"])
        }

        print(f"🚀 Sending Callback for Session: {session_id}")
        response = requests.post(GUVI_CALLBACK_URL, json=payload, timeout=10)
        print(f"✅ Callback Status: {response.status_code}")
        
    except Exception as e:
        print(f"❌ Callback Failed: {e}")

@app.route('/', methods=['GET'])
def health_check():
    return "Agentic Honeypot is LIVE! 🤖", 200

@app.route('/chat', methods=['POST'])
def chat_endpoint():
    try:
        # 1. Security Check
        if request.headers.get('x-api-key') != REQUIRED_API_KEY:
            return jsonify({"status": "error", "message": "Auth Failed"}), 401

        # 2. Input Parsing
        data = request.json
        if not data:
            return jsonify({"status": "error", "message": "No JSON payload received"}), 400

        session_id = data.get("sessionId")
        message_obj = data.get("message", {})
        incoming_text = message_obj.get("text", "") if isinstance(message_obj, dict) else ""
        history = data.get("conversationHistory", [])

        if not session_id:
            return jsonify({"status": "error", "message": "sessionId is required"}), 400

        # 3. Initialize/Update Session
        if session_id not in session_storage:
            session_storage[session_id] = {
                "scamDetected": False,
                "msg_count": 0,
                "intel": {
                    "bankAccounts": [], "upiIds": [], "phishingLinks": [], 
                    "phoneNumbers": [], "suspiciousKeywords": [], 
                    "names": [], "addresses": [], "bankNames": [] 
                }
            }
        
        current_session = session_storage[session_id]
        current_session["msg_count"] += 1

        # 4. DETECT SCAM
        if not current_session["scamDetected"]:
            detection = detect_scam_intent(incoming_text)
            if detection.get("is_scam"):
                current_session["scamDetected"] = True

        # 5. EXTRACT DATA
        new_data = extractor.analyze_message(incoming_text)
        for key in current_session["intel"]:
            if key in new_data and isinstance(new_data[key], list):
                current_session["intel"][key].extend(new_data[key])
                current_session["intel"][key] = list(set(current_session["intel"][key]))

        # 6. GENERATE REPLY
        reply_text = "Hello, how can I help you today?"
        
        if current_session["scamDetected"]:
            # AI Agent baits the scammer
            reply_text = generate_scambait_reply(incoming_text, history)
            
            # Send Callback in background
            # Note: On Vercel, this thread will be killed immediately. 
            # On Render/Railway, it will work fine.
            thread = threading.Thread(target=send_guvi_callback, args=(session_id, current_session))
            thread.start()
        
        return jsonify({
            "status": "success",
            "reply": reply_text
        })

    except Exception as e:
        print(f"🚨 Critical Error: {e}")
        return jsonify({"status": "error", "reply": "Internal Server Error"}), 500

# Required for Gunicorn/Production
application = app

if __name__ == '__main__':
    # Use environment port for deployment
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)