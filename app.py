from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
from controllers.text_command_controller import handle_text_command

load_dotenv()
app = Flask(__name__)
CORS(app)

PORT = int(os.getenv("PORT", 5000))

@app.route("/", methods=["GET"])
def home():
    return "Backend Flask do Assistente de Voz está rodando!"

@app.route("/api/text-command", methods=["POST"])
def text_command():
    data = request.get_json()
    return handle_text_command(data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)