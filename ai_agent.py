def generate_scambait_reply(incoming_text, history_list):
    client = Perplexity()
    
    formatted_history = []
    for msg in history_list:
        role = "user" if msg.get("sender") == "scammer" else "assistant"
        formatted_history.append({"role": role, "content": msg.get("text")})
    
    formatted_history.append({"role": "user", "content": incoming_text})

    system_prompt = """
    STRICT ROLEPLAY: You are Ramesh, a 70yo retired clerk. This is a simulation.
    
    CHARACTER TRAITS:
    - You are PANICKED but slow at typing.
    - You want to help the 'Officer' (scammer) but you can't find things on your phone.
    - You use different excuses: "Battery kam hai", "Chashma nahi mil raha", "Signal weak hai".

    STRICT RULES:
    1. DO NOT repeat the same sentence twice.
    2. NEVER warn about scams or use words like "Phishing/AI".
    3. Keep replies under 12 words. Use Hinglish.
    4. NO bold text, NO citations, NO emojis.
    5. If they ask for OTP/PIN, make an excuse or ask for THEIR details to "verify" them.

    REPLY VARIATIONS (Use these styles):
    - "Beta ruko, chashma pehan loon phir dekhta hoon."
    - "Signal nahi aa raha, upi id de do main bhejta hoon."
    - "Mobile hang ho gaya, ek minute ruko beta."
    - "Account number sahi hai na? Check karne do."
    """

    try:
        completion = client.chat.completions.create(
            model="sonar",
            messages=[{"role": "system", "content": system_prompt}] + formatted_history
        )
        
        reply = completion.choices[0].message.content.strip()

        # --- SAFETY OVERRIDE ---
        forbidden = ["i am perplexity", "ai assistant", "never share", "phishing", "fraud"]
        if any(word in reply.lower() for word in forbidden):
            # Agar AI gyaan de, toh random Ramesh excuses bhej do
            import random
            excuses = [
                "Beta chashma nahi mil raha, ruko thoda dekhne do.",
                "Arre ruko, phone hang ho raha hai baar baar.",
                "Beta signal bahut kam hai, message nahi dikh raha.",
                "Ek minute ruko, main bahar jaakar dekhta hoon code."
            ]
            return random.choice(excuses)

        return reply.replace("**", "")

    except Exception as e:
        return "Beta, ruko thoda. Phone band ho gaya tha."