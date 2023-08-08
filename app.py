from flask import Flask, request, jsonify
from flask_limiter import Limiter
from apiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi
import openai
import os
import logging

logging.basicConfig(
    filename='app.log',  # Nombre del archivo de registro
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

app = Flask(__name__)

# Configura Flask-Limiter 
get_api_key = lambda : request.headers.get('X-API-Key')
api_key_limiter = Limiter(get_api_key,app=app,
                  default_limits=["100 per day", "10 per hour"])

@app.errorhandler(429)
def ratelimit_error(e):
    return jsonify(error='Rate limit exceeded', message=str(e.description)), 429

# Ruta protegida con registro de auditoría
@app.route('/resource', methods=['GET'])
@api_key_limiter.limit("5 per minute")
def protected_resource():
    api_key = request.headers.get('X-API-Key')
    logger = logging.getLogger('app')  # Crear un nuevo logger aquí
    logger.info(f"Solicitud recibida para la ruta /api/resource con clave API: {api_key}")

    if api_key == 'tu_clave_secreta':
        return jsonify(message='Acceso concedido a la API protegida')
    else:
        return jsonify(error='Acceso no autorizado'), 401


@app.route('/youtube_transcript', methods=['GET'])
@api_key_limiter.limit("5 per minute")
def youtube_transcript():
    API_KEY = os.environ["API_KEY_YOUTUBE_DATA"]
    SECRET_KEY_API = os.environ["SECRET_KEY_API"]
    openai.api_key = os.environ["TOKEN_OPENAI_CHATGPT"]
    # Set your OpenAI API key

    youtube = build('youtube', 'v3', developerKey=API_KEY)
    api_key = request.headers.get('X-API-Key')
    logger = logging.getLogger('app')  # Crear un nuevo logger aquí
    logger.info(f"Solicitud recibida para la ruta /apis/youtube_transcript con clave API_KEY: {api_key}")
    
    if api_key == SECRET_KEY_API:
        VIDEO_ID = request.args.get('video_id')
        try:
            responses = YouTubeTranscriptApi.get_transcript(VIDEO_ID, languages=['es','en'])
            logger.info('\n'+"Video: "+"https://www.youtube.com/watch?v="+str(VIDEO_ID)+'\n'+'\n'+"Captions:")
            text = ""
            for response in responses:
                text = text + " " + response['text']
            
            # Summarize the text
            mt = len(text)/2
            summary = openai.summarize(text, max_tokens=mt)  
            response = {'result': text,'summary':summary}
        except Exception as e:
            response = {'result': "error"}
            logger.info(e)
        
        return jsonify(response)
    else:
        return jsonify(error='Acceso no autorizado'), 401


if __name__ == '__main__':
    app.run(port=5001)
