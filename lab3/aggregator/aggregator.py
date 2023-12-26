import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

messages = []


@app.route("/aggregate", methods=["POST"])
def aggregate():
    global messages
    data = request.json
    messages.append(data["number"])

    if len(messages) == 10:
        requests.post("http://processor/process", json={"numbers": messages})
        messages = []

    return jsonify({"status": "received"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
