from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/health")
def health():
    return jsonify({
        "service": "cosmetics-service",
        "status": "healthy"
    })


@app.route("/products")
def products():
    return jsonify([
        {
            "id": 1,
            "name": "Face Serum",
            "price": 799
        },
        {
            "id": 2,
            "name": "Moisturizer",
            "price": 599
        },
        {
            "id": 3,
            "name": "Sunscreen",
            "price": 699
        }
    ])


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)