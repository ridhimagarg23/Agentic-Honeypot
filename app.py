from flask import Flask, request, jsonify
import threading
import requests
from datetime import datetime

# Import modules
from scam_detector import detect_scam_intent
from ai_agent import generate_scambait_reply
from scam_data_extractor import extractor

app = Flask(__name__)

# --- CONFIG ---
REQUIRED_API_KEY = "RIDHIMAGARG2301"
GUVI_CALLBACK_URL = "https://hackathon.guvi.in/api/updateHoneyPotFinalResult"

# Global Session Storage
session_storage = {}

def send_guvi_callback(session_id, session_data):
    """
    STRICT JSON PAYLOAD SENDER
    """
    try:
        # Prepare strictly formatted payload
        payload = {
            "sessionId": session_id,
            "scamDetected": session_data["scamDetected"],
            "totalMessagesExchanged": session_data["msg_count"],
            "extractedIntelligence": {
                "bankAccounts": session_data["intel"]["bankAccounts"],
                "upiIds": session_data["intel"]["upiIds"],
                "phishingLinks": session_data["intel"]["phishingLinks"],
                "phoneNumbers": session_data["intel"]["phoneNumbers"],
                "suspiciousKeywords": session_data["intel"]["suspiciousKeywords"]
            },
            "agentNotes": extractor.generate_agent_notes(session_data["intel"])
        }

        # Send to GUVI
        print(f"Sending Callback for {session_id}...")
        response = requests.post(GUVI_CALLBACK_URL, json=payload, timeout=5)
        print(f"Callback Status: {response.status_code} | Payload Sent: {payload['extractedIntelligence']}")
        
    except Exception as e:
        print(f"Callback Failed: {e}")

@app.route('/chat', methods=['POST'])
def chat_endpoint():
    try:
        # Security Check
        if request.headers.get('x-api-key') != REQUIRED_API_KEY:
            return jsonify({"status": "error", "message": "Auth Failed"}), 401

        # Input Parsing
        data = request.json
        session_id = data.get("sessionId")
        incoming_text = data.get("message", {}).get("text", "")
        history = data.get("conversationHistory", [])

        # Initialize Session
        if session_id not in session_storage:
            session_storage[session_id] = {
                        "scamDetected": False,
                        "msg_count": 0,
                        "intel": {
                            "bankAccounts": [], 
                            "upiIds": [], 
                            "phishingLinks": [], 
                            "phoneNumbers": [], 
                            "suspiciousKeywords": [], 
                            "names": [], 
                            "addresses": [],
                            "bankNames": [] 
                }
            }
        
        current_session = session_storage[session_id]
        current_session["msg_count"] += 1

        # 1. DETECT SCAM (If not already)
        if not current_session["scamDetected"]:
            detection = detect_scam_intent(incoming_text)
            if detection["is_scam"]:
                current_session["scamDetected"] = True

        # 2. EXTRACT DATA (Always run this on every message)
        new_data = extractor.analyze_message(incoming_text)
        
        # Accumulate Data (Purana + Naya)
        for key in current_session["intel"]:
            if key in new_data:
                current_session["intel"][key].extend(new_data[key])
                current_session["intel"][key] = list(set(current_session["intel"][key]))

        # 3. GENERATE REPLY & SEND CALLBACK
        reply_text = "Hello, who is this?"
        
        if current_session["scamDetected"]:
            # AI Agent will now try to BAIT the scammer for data
            reply_text = generate_scambait_reply(incoming_text, history)
            
            # Send Callback in background (Har reply ke baad update bhejo)
            thread = threading.Thread(target=send_guvi_callback, args=(session_id, current_session))
            thread.start()
        
        return jsonify({
            "status": "success",
            "reply": reply_text
        })

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"status": "error", "reply": "Server Error"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)