from perplexity import Perplexity
import os
import random
import re

def generate_scambait_reply(incoming_text, history_list):
    from perplexity import Perplexity
    client = Perplexity()
    
    formatted_history = []
    for msg in history_list:
        role = "user" if msg.get("sender") == "scammer" else "assistant"
        formatted_history.append({"role": role, "content": msg.get("text")})
    
    formatted_history.append({"role": "user", "content": incoming_text})

    # System Prompt with "Randomness" and "Fake Data Generation" instructions
    system_prompt = """
    STRICT ROLEPLAY: You are Ramesh (70yo). This is a simulation.
    
    GOAL: Keep the scammer interested by giving FAKE details and making human excuses. 
    
    STRICT RULES:
    1. NEVER repeat your previous response. If you said "OTP nahi aaya" before, say something else now.
    2. BE CREATIVE: If they ask for Account/PIN, give a FAKE one but act scared.
    3. MAX 12 WORDS. Use Hinglish. No bold, no citations.
    4. ACT HELPLESS: "Chashma nahi mil raha", "Signal kam hai", "Beta ruko".

    DYNAMIC BEHAVIOR:
    - If scammer asks for Account No: Give a fake 11-digit number like 3098XXXXX.
    - If scammer asks for OTP/PIN: Give a fake 4 or 6 digit number or say "Galat bata raha hai phone".
    - If they keep pushing: Ask for THEIR UPI ID so you can "send 1 rupee to verify".
    """

    try:
        completion = client.chat.completions.create(
            model="sonar",
            messages=[{"role": "system", "content": system_prompt}] + formatted_history
        )
        
        reply = completion.choices[0].message.content.strip()

        # --- LOOP BREAKER (Hardcoded Randomness) ---
        # Agar AI phir bhi loop mein jaye (check history), toh hum forcibly change karenge
        last_responses = [msg.get("text") for msg in history_list if msg.get("sender") == "user"][-3:]
        
        if reply in last_responses or "ruko" in reply.lower() and len(last_responses) > 2:
            excuses = [
                f"Account mil gaya beta, ye lo: 3021{random.randint(100000, 999999)}",
                "Beta chashma pehan liya, ye lo OTP: " + str(random.randint(111111, 999999)),
                "Signal aa gaya! Par ye UPI PIN 4321 galat bata raha hai.",
                "Beta bank ka naam kya hai? Main bhool gaya.",
                "Ruko ruko, padosi ko bulaya hai help ke liye."
            ]
            return random.choice(excuses)

        # AI Safety filter (Same as before)
        forbidden = ["i am perplexity", "ai assistant", "never share", "phishing", "fraud"]
        if any(word in reply.lower() for word in forbidden):
            return "Beta ruko, phone hang ho gaya. Fir se batana kya chahiye?"

        return reply.replace("**", "")

    except Exception as e:
        return "Beta, light chali gayi hai yahan. Ruko thoda."