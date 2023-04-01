from flask import Flask, render_template, request, jsonify, send_from_directory
import os
from werkzeug.utils import secure_filename
from langchain import LangChain, AgentExecutor
from transcribe import transcribe_audio
from chatgpt import generate_response
from text_to_speech import synthesize_speech

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "uploads"
app.config["ALLOWED_EXTENSIONS"] = {"wav", "mp3", "ogg"}

openai_api_key = os.environ["OPENAI_API_KEY"]
zapier_nla_api_key = os.environ["ZAPIER_NLA_API_KEY"]

lang_chain = LangChain(api_key=openai_api_key)

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route('/transcribe', methods=['POST'])
def transcribe_route():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
        transcription = transcribe_audio(os.path.join(app.config["UPLOAD_FOLDER"], filename))
        return jsonify({"transcription": transcription})
    return jsonify({"error": "Invalid file type"}), 400

@app.route('/ask', methods=['POST'])
def ask():
    conversation = request.json.get("conversation", [])
    response = generate_response(lang_chain, conversation)
    return jsonify({"response": response})

@app.route('/run_agent_action', methods=['POST'])
def run_agent_action():
    user_input = request.form.get("user_input", "")
    action_result = lang_chain.run_agent_action(user_input)
    return jsonify({"result": action_result})

@app.route("/synthesize", methods=["POST"])
def synthesize():
    text = request.json.get("text", "")
    audio_filename = synthesize_speech(text)
    return jsonify({"audio_filename": audio_filename})

@app.route("/audio/<filename>")
def audio(filename):
    return send_from_directory("audio", filename)

if __name__ == '__main__':
    app.run(debug=True)
