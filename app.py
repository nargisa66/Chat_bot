from flask import Flask, request, jsonify, send_file, render_template
from flask_cors import CORS
import os
import pyttsx3
import speech_recognition as sr

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/text-to-speech", methods=["POST"])
def text_to_speech():
    data = request.get_json()
    text = data.get("text")

    if not text:
        return jsonify({"error": "Text is required"}), 400

    output_path = os.path.join(UPLOAD_FOLDER, "response.mp3")
    try:
        engine = pyttsx3.init()
        engine.save_to_file(text, output_path)
        engine.runAndWait()
        return jsonify({"audioFile": "/uploads/response.mp3"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/uploads/<filename>")
def fetch_audio(filename):
    return send_file(os.path.join(UPLOAD_FOLDER, filename), as_attachment=False)

if __name__ == "__main__":
    app.run(debug=True, port=5000)