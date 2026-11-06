import math
from flask import Flask, request, jsonify

app = Flask(__name__)


@app.get("/health")
def health():
    return jsonify(status="ok", service="training-api")


@app.post("/double")
def double_value():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify(error="Expected JSON object"), 400

    value = data.get("value")

    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return jsonify(error="value must be numeric"), 400

    if not math.isfinite(value):
        return jsonify(error="value must be finite"), 400

    if abs(value) > 1000000:
        return jsonify(error="value outside allowed range"), 400

    return jsonify(result=value * 2)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001, debug=False)

