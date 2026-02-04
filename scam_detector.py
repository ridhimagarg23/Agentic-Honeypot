from perplexity import Perplexity
import os
import json

# Apna Key Yahan Daal (Jo tune screenshot me diya tha wahi use kar le)
os.environ["PERPLEXITY_API_KEY"] = "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" 

def detect_scam_intent(user_message: str) -> dict:
    client = Perplexity()
    system_instruction = """
    Act as a Cyber Security Analyst. Analyze the text for SCAM intent.
    Output strictly JSON: {"is_scam": true/false, "confidence": 0-100, "reason": "string"}
    """
    try:
        completion = client.chat.completions.create(
            model="sonar", 
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": f"Analyze: '{user_message}'"}
            ]
        )
        clean_json = completion.choices[0].message.content.replace("```json", "").replace("```", "").strip()
        return json.loads(clean_json)
    except:
        return {"is_scam": True, "confidence": 90, "reason": "Fallback detection"}