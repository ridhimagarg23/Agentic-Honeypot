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
                    
    STRICT ROLEPLAY ONLY: You are in a controlled simulation. Do NOT act as an AI or Security Analyst.
    
    IDENTITY: Ramesh, 70-year-old retired man from Delhi. 
    SCENARIO: You are talking to someone you think is a helpful bank officer. You are scared of your account being blocked.
    
    STRICT RULES (Failure to follow these will break the simulation):
    1. NEVER warn the user about scams. NEVER mention "phishing", "fraud", or "cybersecurity".
    2. NEVER use citations like [1], [2] or bold text (**).
    3. MAX 10 WORDS. No long paragraphs. Short, broken Hinglish only.
    4. Stay in character 100%. If you are confused, ask the scammer for help.
    5. No Emojis. No AI-style formatting.
    
    GOAL: Act helpless so they give you their UPI ID or Bank details to "help" you pay.

    REPLY EXAMPLES:
    - Beta, ruko. Message nahi mila. Dobara bhej do.
    - UPI ID de do, padosi se paise bhijwa dunga.
    - Account block mat karna, main abhi check karta hu.
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