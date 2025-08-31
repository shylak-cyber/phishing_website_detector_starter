
from flask import Flask, request, jsonify, render_template
import joblib
import numpy as np
from feature_extractor import extract

app = Flask(__name__)

MODEL_PATH = "model.pkl"
CLF = None

def load_model():
    global CLF
    try:
        CLF = joblib.load(MODEL_PATH)
    except Exception as e:
        CLF = None

load_model()

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/api/predict", methods=["POST"])
def predict():
    global CLF
    data = request.get_json(force=True)
    url = data.get("url","").strip()
    X, feats, order = extract(url)
    if CLF is None:
        # Fallback simple heuristic if model not loaded
        score = 0.5
        # simple rules
        score += 0.2 if feats["has_ip_host"] else 0
        score += 0.15 if feats["suspicious_tld"] else 0
        score += 0.1 if feats["shortener"] else 0
        score += 0.15 if feats["num_at"]>0 else 0
        score += 0.1 if feats["digit_ratio"]>0.3 else 0
        score = min(score, 0.99)
        label = int(score>0.5)
        proba = [1-score, score]
    else:
        X = X.reshape(1, -1)
        proba = getattr(CLF, "predict_proba", None)
        if proba:
            proba = CLF.predict_proba(X)[0].tolist()
            label = int(np.argmax(proba))
        else:
            label = int(CLF.predict(X)[0])
            proba = [1-label, label]
    return jsonify({
        "url": url,
        "label": int(label),
        "phishing_probability": float(proba[1]),
        "features": feats
    })

if __name__ == "__main__":
 app.run(host="0.0.0.0", port=5000, debug=True)
