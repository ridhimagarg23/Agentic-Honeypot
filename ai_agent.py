from perplexity import Perplexity
import os

# API Key environment variable se uthayega
# os.environ["PERPLEXITY_API_KEY"] = "YOUR_KEY_HERE"

def generate_scambait_reply(incoming_text, history_list):
    """
    Ye function scammer se data nikalwane ke liye design kiya gaya hai.
    """
    client = Perplexity()
    
    # --- 1. History Format Karo ---
    formatted_history = []
    for msg in history_list:
        role = "user" if msg.get("sender") == "scammer" else "assistant"
        formatted_history.append({"role": role, "content": msg.get("text")})
    
    # Current message add karo
    formatted_history.append({"role": "user", "content": incoming_text})

    # --- 2. THE TRAP (System Prompt) ---
    # Hum AI ko bolenge ki wo payment karne ke liye ready act kare aur DETAILS maange.
    system_prompt = """
                    ROLE: You are Ramesh, a 70-year-old retired clerk from Delhi. 
            CHARACTER: You are confused, scared of technology, but trust people easily. 
            STRICT STYLE RULES:
            1. MAX 10-12 WORDS per reply. Keep it very short.
            2. USE HINGLISH: "Beta", "Ruko", "Nahi aaya", "Kya karu".
            3. NEVER say the word "Scam", "Honeypot", or "Agent". 
            4. NO BOLD TEXT (**), NO EMOJIS (🚫🚨), NO CITATIONS [1].
            5. BE REALISTIC: Don't give all info at once. Act like you are struggling to find things.

            GOAL: Keep them talking to get their UPI ID or Bank Details.
            
            TACTICS:
            - If they ask for OTP: "Beta, message nahi aaya. Mere paas chhota phone hai, ruko dekhta hu."
            - To get UPI: "Main bank nahi ja sakta, koi UPI ID hai to bhej do, padosi se karwa dunga."
            - To get Bank Acc: "Beta, account number de do, mera beta bhej dega paise."
            - If they repeat: Just act more confused. "Ek baar fir bhejo, nahi mila code."
            """

    try:
        completion = client.chat.completions.create(
            model="sonar",
            messages=[{"role": "system", "content": system_prompt}] + formatted_history
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"Agent Error: {e}")
        return "Beta, main paise bhejne ko taiyar hu, par bhejau kahan? Koi UPI ID hai kya?"