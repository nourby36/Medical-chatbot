from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import speech_recognition as sr
from pydub import AudioSegment
import json
import io
import os

from generation_reponse_chatbot import generation_reponse
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}) 
UPLOAD_FOLDER = 'C:\\Users\\USER\\Desktop'
AudioSegment.converter = "C:\\PATH_programs\\ffmpeg.exe"
AudioSegment.ffprobe   = "C:\\PATH_programs\\ffprobe.exe"

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/convert_to_wav', methods=['POST'])
def convert_to_wav():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400

    audio_file = request.files['audio']
    if audio_file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    filename = audio_file.filename
    upload_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    try:
        audio_file.save(upload_path)
        sound = AudioSegment.from_file(upload_path)
        wav_path = os.path.splitext(upload_path)[0] + '.wav'
        sound.export(wav_path, format="wav")

        # Optionnel : Supprimer le fichier original pour ne conserver que le WAV
        os.remove(upload_path)

        return send_file(wav_path, as_attachment=True)
    except Exception as e:
        # Nettoyage: Assurez-vous de supprimer les fichiers partiellement traités en cas d'erreur
        if os.path.exists(upload_path):
            os.remove(upload_path)
        if os.path.exists(wav_path):
            os.remove(wav_path)
        return jsonify({'error': str(e)}), 500
@app.route('/')
def home():
    return 'Le serveur Flask fonctionne !'

@app.route('/chatbot', methods=['POST'])
def chatbot():
    user_input = request.json.get('user_input')
    # chatbot_response = generer_reponse(user_input)
    chatbot_response =  generation_reponse(user_input)
    print("ddd")
    print(chatbot_response)
    return jsonify({'response': chatbot_response})

@app.route('/recognize_speech', methods=['POST'])
def recognize_speech():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400

    audio_file = request.files['audio']
    if audio_file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    filename = audio_file.filename
    upload_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    print('upload_path')
    print(upload_path)

    try:
        audio_file.save(upload_path)
        # Convertit en WAV si nécessaire
        sound = AudioSegment.from_file(upload_path)
        wav_path = os.path.splitext(upload_path)[0] + '.wav'
        if upload_path != wav_path:
            sound.export(wav_path, format="wav")
            os.remove(upload_path)  # Supprime le fichier original

        recognizer = sr.Recognizer()
        with sr.AudioFile(wav_path) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data, language='zh-CN')  # Utilisez 'language' pour spécifier la langue

        # Supprimer le fichier WAV après la transcription
        os.remove(wav_path)

        return jsonify({'transcription': text})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
if __name__ == '__main__':
    app.run(debug=True)
