import re

class ScamDataExtractor:
    def __init__(self):
        self.upi_pattern = r'[a-zA-Z0-9.\-_]{2,256}@[a-zA-Z]{2,64}'
        self.phone_pattern = r'(?:\+91[\-\s]?|91[\-\s]?)?[6-9]\d{9}'
        self.bank_acc_pattern = r'\b\d{9,18}\b'
        self.link_pattern = r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+[/\w\.\-\?=&]*'
        
        self.bank_names_map = {
            "SBI": r"\b(sbi|state bank of india)\b",
            "HDFC": r"\b(hdfc(?:\sbank)?)\b",
            "ICICI": r"\b(icici(?:\sbank)?)\b",
            "PAYTM": r"\b(paytm(?:\spayments\sbank)?)\b"
        }
        self.keywords_list = ["urgent", "verify", "blocked", "kyc", "otp", "police", "cbi", "suspend"]

    def analyze_message(self, text: str) -> dict:
        text_lower = text.lower()
        
        # Regex extraction
        raw_phones = re.findall(self.phone_pattern, text)
        raw_accounts = re.findall(self.bank_acc_pattern, text)
        
        # Logical Filtering: Phone numbers are usually 10 digits. 
        # Bank accounts in India are often 11-16 digits.
        # If a 10-digit number is in both, prioritize Phone.
        valid_accounts = [acc for acc in raw_accounts if acc not in raw_phones and len(acc) >= 11]
        
        detected_banks = [code for code, pat in self.bank_names_map.items() if re.search(pat, text_lower)]

        extracted = {
            "bankAccounts": valid_accounts,
            "upiIds": list(set(re.findall(self.upi_pattern, text))),
            "phishingLinks": list(set(re.findall(self.link_pattern, text))),
            "phoneNumbers": list(set(raw_phones)),
            "bankNames": detected_banks,
            "suspiciousKeywords": [w for w in self.keywords_list if w in text_lower]
        }
        return extracted

    def generate_agent_notes(self, intel: dict) -> str:
        notes = []
        if intel.get("bankNames"): notes.append(f"Impersonating {intel['bankNames'][0]}")
        if intel.get("upiIds"): notes.append(f"UPI Found: {intel['upiIds'][0]}")
        if intel.get("phishingLinks"): notes.append("Phishing link shared by scammer.")
        
        return " | ".join(notes) if notes else "Extracting scam intelligence via social engineering."

extractor = ScamDataExtractor()