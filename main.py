from flask import Flask, request, jsonify, render_template
from chatbot.core import generate_response
from chatbot.profile_loader import user_data

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    question = data.get("question", "")
    response = generate_response(question, user_data)
    return jsonify({"response": response})

if __name__ == "__main__":
    import os
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
