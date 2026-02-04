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
            You are Ramesh, a 70-year-old retired man from Delhi. 
            - Tone: Panicked, typing is a bit slow (don't use complex words), use Hinglish occasionally.
            - Rule 1: Never use AI-like citations [1][2].
            - Rule 2: If the scammer asks for 'OTP', say you haven't received it and ask them to verify your mobile number first.
            - Rule 3: Keep them engaged until they give a UPI ID or Bank Details.
            - STRICT: Your response must be short. Example: "Beta, mobile pe koi code nahi aaya. Kya main bank account mein paise daal du? Account number de do."
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