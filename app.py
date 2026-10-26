
from pathlib import Path

import joblib
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)

CORS(
    app,
    resources={
        r"/check": {
            "origins": "https://sathvikajeeviguntla-2427.github.io"
        },
        r"/chat": {
            "origins": "https://sathvikajeeviguntla-2427.github.io"
        }
    }
)

# --------------------------------------------------
# LOAD THE TRAINED ML CHATBOT MODEL
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "chatbot_model.pkl"

model = None

try:
    model = joblib.load(MODEL_PATH)
    app.logger.info("ML chatbot model loaded successfully.")
except FileNotFoundError:
    app.logger.warning(
        "chatbot_model.pkl not found. The chatbot will be unavailable "
        "until the model is added."
    )
except Exception:
    app.logger.exception("Failed to load chatbot_model.pkl.")


# --------------------------------------------------
# SAMPLE GOVERNMENT SCHEMES DATA
# --------------------------------------------------

schemes = [
    {
        "name": "PM Kisan",
        "desc": "₹6000/year for farmers",
        "category": "Farmer",
        "income": 200000,
        "ageMin": 18,
        "ageMax": 65,
        "occupation": "farmer"
    },
    {
        "name": "Ujjwala Yojana",
        "desc": "Free LPG for women",
        "category": "Women",
        "income": 100000,
        "ageMin": 18,
        "ageMax": 60,
        "occupation": "any"
    },
    {
        "name": "Ayushman Bharat",
        "desc": "₹5 lakh health insurance",
        "category": "General",
        "income": 150000,
        "ageMin": 0,
        "ageMax": 100,
        "occupation": "any"
    }
]


# --------------------------------------------------
# PREDEFINED RESPONSES FOR CHATBOT INTENTS
# These keys must match the model's training labels.
# --------------------------------------------------

responses = {
    "farmer_schemes": (
        "You can explore PM Kisan and other farmer schemes. "
        "Check the eligibility criteria and official portal."
    ),
    "health_schemes": (
        "Ayushman Bharat PM-JAY provides health coverage to "
        "eligible beneficiaries. Check the official portal for details."
    ),
    "documents": (
        "Common documents may include Aadhaar, income certificate, "
        "bank details, and category or land records where applicable. "
        "Requirements vary by scheme."
    ),
    "application_process": (
        "Open the scheme's official portal, review the eligibility "
        "requirements, prepare the required documents, and follow "
        "the official application process."
    ),
    "greeting": (
        "Namaste! I can help you explore government schemes, "
        "benefits, documents, and application procedures."
    ),
    "thanks": (
        "You're welcome! Ask me about another government scheme."
    ),
    "scheme_information": (
        "I can help you explore scheme information. Please mention "
        "the scheme name or use the scheme cards for official links."
    )
}


# --------------------------------------------------
# HELPER FUNCTION
# --------------------------------------------------

def normalise_text(value):
    """Trim whitespace and make comparisons case-insensitive."""
    return value.strip().casefold()


# --------------------------------------------------
# API 1: CHECK GOVERNMENT SCHEME ELIGIBILITY
# POST /check
# --------------------------------------------------

@app.route("/check", methods=["POST"])
def check():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "error": "A valid JSON object is required."
        }), 400

    required_fields = ["age", "income", "category", "occupation"]

    for field in required_fields:
        if field not in data or data[field] is None:
            return jsonify({
                "error": f"Missing required field: {field}."
            }), 400

    # Validate numeric fields.
    try:
        age_value = data["age"]
        income_value = data["income"]

        # Reject booleans, which Python otherwise treats as integers.
        if isinstance(age_value, bool) or isinstance(income_value, bool):
            raise ValueError

        age = int(age_value)
        income = float(income_value)

        # Reject fractional ages and non-finite values.
        if float(age_value) != age:
            raise ValueError

        if not (0 <= age <= 120):
            return jsonify({
                "error": "Age must be between 0 and 120."
            }), 400

        if income < 0 or income == float("inf") or income != income:
            return jsonify({
                "error": "Income must be a valid non-negative number."
            }), 400

        if income == float("-inf"):
            return jsonify({
                "error": "Income must be a valid non-negative number."
            }), 400

    except (TypeError, ValueError, OverflowError):
        return jsonify({
            "error": "Age must be a whole number and income must be a valid number."
        }), 400

    category = data["category"]
    occupation = data["occupation"]

    if not isinstance(category, str) or not category.strip():
        return jsonify({
            "error": "Category must be a non-empty string."
        }), 400

    if not isinstance(occupation, str) or not occupation.strip():
        return jsonify({
            "error": "Occupation must be a non-empty string."
        }), 400

    category = normalise_text(category)
    occupation = normalise_text(occupation)

    results = []

    for scheme in schemes:

        # Check age eligibility.
        if not (scheme["ageMin"] <= age <= scheme["ageMax"]):
            continue

        # Check income eligibility.
        if income > scheme["income"]:
            continue

        # Check category eligibility.
        scheme_category = normalise_text(scheme["category"])

        if (
            scheme_category != "general"
            and scheme_category != category
        ):
            continue

        # Check occupation eligibility.
        scheme_occupation = normalise_text(scheme["occupation"])

        if (
            scheme_occupation != "any"
            and scheme_occupation != occupation
        ):
            continue

        results.append(scheme)

    # Preserve your original response format: a JSON list.
    return jsonify(results), 200


# --------------------------------------------------
# API 2: ML-BASED CHATBOT
# POST /chat
# --------------------------------------------------

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "reply": "Please send a valid JSON request."
        }), 400

    message = data.get("message", "")

    if not isinstance(message, str) or not message.strip():
        return jsonify({
            "reply": "Please enter a question."
        }), 400

    message = message.strip()

    # Check whether the model loaded successfully.
    if model is None:
        return jsonify({
            "reply": (
                "The chatbot model is unavailable. Please make sure "
                "chatbot_model.pkl exists and can be loaded."
            )
        }), 503

    try:
        # Predict the user's intent.
        intent = str(model.predict([message])[0])

        # Predict confidence only if the model supports it.
        confidence = None

        if hasattr(model, "predict_proba"):
            probabilities = model.predict_proba([message])[0]
            confidence = float(max(probabilities))

        # Handle uncertain predictions.
        if confidence is not None and confidence < 0.40:
            reply = (
                "I'm not sure I understood. Try asking about farmer "
                "schemes, health coverage, documents, or how to apply."
            )
        else:
            reply = responses.get(
                intent,
                "Please rephrase your question about government schemes."
            )

        result = {
            "reply": reply,
            "intent": intent
        }

        if confidence is not None:
            result["confidence"] = round(confidence, 3)

        return jsonify(result), 200

    except Exception:
        app.logger.exception("Chatbot prediction failed.")

        return jsonify({
            "reply": "The chatbot encountered an error. Please try again."
        }), 500


# --------------------------------------------------
# HOME ROUTE: CHECK WHETHER THE API IS RUNNING
# --------------------------------------------------

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "SchemeWise API is running.",
        "chatbot_model_loaded": model is not None,
        "endpoints": ["/check", "/chat"]
    })


# --------------------------------------------------
# RUN FLASK
# --------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True)
