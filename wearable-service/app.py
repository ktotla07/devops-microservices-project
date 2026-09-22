from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/health")
def health():
    return jsonify({
        "service": "wearable-service",
        "status": "healthy"
    })


@app.route("/products")
def products():
    return jsonify([
        {
            "id": 1,
            "name": "Smart Watch",
            "price": 4999
        },
        {
            "id": 2,
            "name": "Fitness Tracker",
            "price": 2999
        }
    ])


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)