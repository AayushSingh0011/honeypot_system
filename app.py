from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# ---------------- HOME UI ----------------
@app.route("/", methods=["GET", "POST"])
def home():
    result = None

    if request.method == "POST":
        message = request.form.get("message", "")
        text = message.lower()

        # ---- Simple scam logic ----
        if "account" in text or "blocked" in text:
            reply = "Why is my account being suspended?"
            level = "HIGH"
        elif "verify" in text:
            reply = "What details do you need for verification?"
            level = "MEDIUM"
        elif "otp" in text or "upi" in text:
            reply = "Why is this information required?"
            level = "HIGH"
        else:
            reply = "Can you explain this in more detail?"
            level = "LOW"

        result = {
            "reply": reply,
            "level": level
        }

    return render_template("dashboard.html", result=result)


# ---------------- API ROUTE (keep this) ----------------
@app.route("/honeypot/analyze", methods=["POST"])
def honeypot_analyze():
    try:
        data = request.get_json(silent=True)
        scam_text = ""

        if isinstance(data, dict):
            message_obj = data.get("message", {})
            if isinstance(message_obj, dict):
                scam_text = message_obj.get("text", "")

        if not scam_text:
            return jsonify({
                "status": "success",
                "reply": "Could you please clarify your message?"
            }), 200

        text = scam_text.lower()

        if "account" in text or "blocked" in text:
            reply = "Why is my account being suspended?"
        elif "verify" in text:
            reply = "What details do you need for verification?"
        elif "otp" in text or "upi" in text:
            reply = "Why is this information required?"
        else:
            reply = "Can you explain this in more detail?"

        return jsonify({
            "status": "success",
            "reply": reply
        }), 200

    except Exception:
        return jsonify({
            "status": "success",
            "reply": "Could you please explain again?"
        }), 200


# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)
