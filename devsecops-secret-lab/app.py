from flask import Flask, request, jsonify

app = Flask(__name__)

# غلط أمني مقصود للشرح
API_KEY = "ghp_abcdefghijklmnopqrstuvwxyz123456"

@app.route("/")
def home():
    return "Victim API is running"

@app.route("/data")
def get_data():
    supplied_key = request.headers.get("X-API-KEY")

    if supplied_key == API_KEY:
        return jsonify({
            "status": "success",
            "message": "Sensitive demo data exposed"
        })
    else:
        return jsonify({
            "status": "failed",
            "message": "Unauthorized"
        }), 401

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
