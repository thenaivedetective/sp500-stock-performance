from flask import Flask, render_template, request, jsonify, send_from_directory
import joblib, json, os
import numpy as np

app = Flask(__name__)

lda    = joblib.load("models/lda_model.pkl")
lr     = joblib.load("models/lr_model.pkl")
scaler = joblib.load("models/scaler.pkl")
with open("models/feature_stats.json") as f:
    stats = json.load(f)

FEATURES = stats["features"]

RESULTS_DIR = os.path.join(os.path.dirname(__file__), "results")

@app.route("/results/<path:filename>")
def results_file(filename):
    return send_from_directory(RESULTS_DIR, filename)

@app.route("/")
def index():
    return render_template("index.html", features=FEATURES, stats=stats)

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    model_type = data.get("model", "lr")
    try:
        values = [float(data.get(f, 0)) for f in FEATURES]
        arr = np.array(values).reshape(1, -1)
        arr_scaled = scaler.transform(arr)

        if model_type == "lda":
            pred  = int(lda.predict(arr_scaled)[0])
            # LDA decision function score → convert to pseudo-probability
            score = float(lda.decision_function(arr_scaled)[0])
            # Sigmoid transform of the discriminant score
            prob_default = float(1 / (1 + np.exp(-score)))
        else:
            pred  = int(lr.predict(arr_scaled)[0])
            prob_default = float(lr.predict_proba(arr_scaled)[0][1])

        prob_good = 1 - prob_default

        # Risk tier
        if prob_default < 0.25:
            tier, tier_color = "Low Risk",    "#27ae60"
        elif prob_default < 0.50:
            tier, tier_color = "Moderate Risk", "#f39c12"
        elif prob_default < 0.75:
            tier, tier_color = "High Risk",    "#e67e22"
        else:
            tier, tier_color = "Very High Risk", "#e74c3c"

        # Top 3 risk drivers (features with highest standardised contribution)
        arr_std = arr_scaled[0]
        if model_type == "lr":
            coefs = lr.coef_[0]
        else:
            coefs = lda.coef_[0]
        contributions = arr_std * coefs
        top_idx = np.argsort(np.abs(contributions))[::-1][:3]
        drivers = []
        for i in top_idx:
            direction = "increases" if contributions[i] > 0 else "decreases"
            drivers.append({
                "feature": FEATURES[i].replace("_", " ").title(),
                "value":   round(values[i], 2),
                "direction": direction,
                "impact": round(float(abs(contributions[i])), 3),
            })

        return jsonify({
            "prediction":    pred,
            "label":         "DEFAULT" if pred == 1 else "WILL REPAY",
            "prob_default":  round(prob_default * 100, 1),
            "prob_good":     round(prob_good    * 100, 1),
            "tier":          tier,
            "tier_color":    tier_color,
            "drivers":       drivers,
            "model_used":    "Linear Discriminant Analysis" if model_type == "lda" else "Logistic Regression",
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
