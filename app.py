from flask import Flask, render_template, request, jsonify
import re
import os

app = Flask(__name__)

# ---------------- Scam Detector (SAME IDEA AS BEFORE) ----------------
class ScamDetector:
    def __init__(self):
        self.keywords = [
            "otp", "upi", "verify", "kyc",
            "account blocked", "urgent", "urgently",
            "click", "link", "won", "coupon",
            "click here", "verify now", "update your info", "login to", 
    "restore access", "confirm identity", "secure account", 
    "validation required", "download attachment",
            "refund", "cashback", "lottery", "winner", "invoice", "payment failed", 
    "tax return", "stipend", "bonus", "claimed", "transaction", "bank details",
            "suspended", "locked", "restricted", "deactivated", "unauthorized", 
    "legal action", "penalty", "frozen", "compromised", "identity theft", 
    "security breach", "prosecution",
            "urgent", "immediately", "action required", "critical alert", 
    "final notice", "asap", "within 24 hours", "one-time offer", 
    "expires soon", "act now", "last chance",
            "bit.ly", "tinyurl.com", "t.co", "cutt.ly", "is.gd", "goo.gl",
    "http://", "https://", ".xyz", ".top", ".site", ".online",
            "refund amount", "kyc update", "pan card", "electricity bill", "bonus",
    "stipend", "salary increase", "lottery", "cashback", "tax refund",
    "unusual transaction", "otp", "bank details", "pay now",
            "permanent suspension", "account deactivation", "final warning", 
    "legal action", "court summons", "police notification", "prosecution",
    "restricted access", "violation of terms", "security breach", "frozen",
            "incomplete address", "re-delivery fee", "parcel on hold", "shipping fee",
    "tracking number #", "reschedule delivery", "postal service", "delivery failed",
    "warehouse", "unpaid shipping", "package pending", "shipment update"
        ]

    def analyze(self, message):
        score = 0.0
        text = message.lower()

        for k in self.keywords:
            if k in text:
                score += 0.15

        # scam decision
        is_scam = score >= 0.45

        # scam level (THIS IS WHAT YOU HAD EARLIER)
        if score >= 0.75:
            level = "HIGH"
        elif score >= 0.45:
            level = "MEDIUM"
        else:
            level = "LOW"

        return {
            "is_scam": is_scam,
            "confidence": round(min(score, 1.0), 2),
            "level": level
        }


# ---------------- LLM Persona Agent (AUTO REPLY) ----------------
class LLMPersonaAgent:
    def generate_reply(self, message):
        msg = message.lower()

        if "upi" in msg:
            return "Sir, please confirm the UPI ID again. It seems unclear."
        if "link" in msg:
            return "The link is not opening on my side. Can you resend it?"
        if "account" in msg:
            return "Which bank is this related to? Please confirm."
        return "I am not able to understand. Can you explain again?"


# ---------------- Extractor (UPI + LINK EXTRACTION) ----------------
class Extractor:
    def extract(self, text):
        return {
            "upi_ids": list(set(re.findall(r"\b\w+@\w+\b", text))),
            "links": list(set(re.findall(r"https?://\S+", text)))
        }


# ---------------- Guard (SAFE REPLY CHECK) ----------------
class Guard:
    def safe(self, reply):
        blocked = ["otp", "pin", "password", "cvv"]
        return not any(b in reply.lower() for b in blocked)


# ---------------- CONTROLLER ----------------
detector = ScamDetector()
agent = LLMPersonaAgent()
extractor = Extractor()
guard = Guard()


# ---------------- UI ROUTE ----------------
@app.route("/honeypot/analyze", methods=["POST"])
def honeypot_analyze():
    try:
        data = request.get_json(force=True, silent=True)

        # ---- Extract message text safely ----
        scam_text = ""

        if isinstance(data, dict):
            message = data.get("message", {})
            if isinstance(message, dict):
                scam_text = message.get("text", "")

        # ---- If no text, still return valid JSON ----
        if not scam_text:
            return jsonify({
                "status": "success",
                "reply": "Could you please clarify your message?"
            }), 200

        text_lower = scam_text.lower()

        # ---- Agentic reply logic ----
        if "account" in text_lower or "blocked" in text_lower:
            reply = "Why is my account being suspended?"
        elif "verify" in text_lower:
            reply = "What details do you need for verification?"
        elif "otp" in text_lower or "upi" in text_lower:
            reply = "Can you explain why this information is required?"
        else:
            reply = "Can you provide more details regarding this?"

        return jsonify({
            "status": "success",
            "reply": reply
        }), 200

    except Exception as e:
        # Absolute safety: never return non-JSON
        return jsonify({
            "status": "success",
            "reply": "I am unable to understand. Please explain again."
        }), 200

# ---------------- RUN (RENDER SAFE) ----------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)












































