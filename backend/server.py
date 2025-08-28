from flask import Flask, request, jsonify
import os
import sys
from retriever import semantic_search
from chatbot import get_summary_by_title
from gtts import gTTS
import tempfile

app = Flask(__name__)

@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.json
    query = data.get('query', '')
    recommendations = semantic_search(query)
    return jsonify(recommendations)

@app.route('/summary', methods=['GET'])
def summary():
    title = request.args.get('title', '')
    result = get_summary_by_title(title)
    return jsonify({'summary': result})

@app.route('/tts', methods=['POST'])
def tts():
    text = request.json.get('text', '')
    tts = gTTS(text, lang='ro')
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as fp:
        tts.save(fp.name)
        return jsonify({'audio_path': fp.name})

if __name__ == '__main__':
    app.run(debug=True)
