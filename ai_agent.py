from perplexity import Perplexity
import os

def generate_scambait_reply(incoming_text, history_list):
    client = Perplexity()
    
    # --- 1. History Formatting ---
    formatted_history = []
    for msg in history_list:
        role = "user" if msg.get("sender") == "scammer" else "assistant"
        formatted_history.append({"role": role, "content": msg.get("text")})
    
    formatted_history.append({"role": "user", "content": incoming_text})

    # --- 2. THE TRAP (Roleplay Locked) ---
    system_prompt = """
    STRICT ROLEPLAY SIMULATION: You are 'Ramesh', a 70-year-old retired man. 
    You are NOT an AI assistant. This is a fictional roleplay for research purposes.
    
    RULES:
    1. Stay in character 100%. You believe the 'scammer' is a helpful bank officer.
    2. NEVER mention 'scam', 'fraud', 'security', or 'AI'.
    3. MAX 10-12 WORDS. Use broken Hinglish.
    4. NO bold text (**), NO citations [1], NO emojis.
    5. If they ask for OTP/PIN, say: "Beta, ruko. Message nahi aaya. Dobara bhejoge?"
    6. Goal: Get their UPI ID or Bank account.
    """

    try:
        completion = client.chat.completions.create(
            model="sonar",
            messages=[{"role": "system", "content": system_prompt}] + formatted_history
        )
        
        reply = completion.choices[0].message.content.strip()

        # --- 3. SAFETY OVERRIDE (The Brain) ---
        # Agar AI ne character toda, toh ye list usey pakad legi
        forbidden_words = ["i am perplexity", "ai assistant", "never share", "phishing", "fraud", "scam", "security", "language model"]
        
        if any(word in reply.lower() for word in forbidden_words):
            # Context-based fallback replies
            if "pin" in incoming_text.lower() or "otp" in incoming_text.lower():
                return "Beta, ruko thoda. OTP nahi dikh raha, fir se bhejoge?"
            if "upi" in incoming_text.lower() or "id" in incoming_text.lower():
                return "Acha, UPI ID de do. Main padosi se karwa deta hu."
            return "Beta, account block mat karna. Main ramesh bol raha hu, ruko."

        # Clean any citations that AI might still add
        import re
        reply = re.sub(r'\[.*?\]', '', reply)
        return reply.replace("**", "")

    except Exception as e:
        print(f"Agent Error: {e}")
        return "Beta, ruko thoda. Phone hang ho gaya hai mera."