from flask import Flask, request, jsonify
from flask_limiter import Limiter
import logging

logging.basicConfig(
    filename='app.log',  # Nombre del archivo de registro
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

app = Flask(__name__)

@app.errorhandler(429)
def ratelimit_error(e):
    return jsonify(error='Rate limit exceeded', message=str(e.description)), 429

# Ruta protegida con registro de auditoría
@app.route('/api/resource', methods=['GET'])
def protected_resource():
    api_key = request.headers.get('X-API-Key')
    logger = logging.getLogger('app')  # Crear un nuevo logger aquí
    logger.info(f"Solicitud recibida para la ruta /api/resource con clave API: {api_key}")

    # Configura Flask-Limiter con la función de clave
    limiter = Limiter(
        app,
        key_func=lambda: api_key,  # Usar la clave API obtenida de la solicitud
        default_limits=["100 per day", "10 per hour"]
    )

    if api_key == 'tu_clave_secreta':
        return jsonify(message='Acceso concedido a la API protegida')
    else:
        return jsonify(error='Acceso no autorizado'), 401


# Filtro de solicitud para autenticación
@limiter.request_filter
def is_not_authenticated():
    api_key = request.headers.get('X-API-Key')
    return api_key is None

if __name__ == '__main__':
    app.run()

"""
from apiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi
import os
 
API_KEY = os.environ["API_KEY_YOUTUBE_DATA"]
# Set your API key and video ID
print(API_KEY)
VIDEO_ID = "5EfFqAAWvqw"
channel_id = 'Your Channel_id'  # replace it with your channel id
youtube = build('youtube', 'v3', developerKey=API_KEY)

try:
    responses = YouTubeTranscriptApi.get_transcript(VIDEO_ID, languages=['es'])
    print('\n'+"Video: "+"https://www.youtube.com/watch?v="+str(VIDEO_ID)+'\n'+'\n'+"Captions:")
    for response in responses:
        text = response['text']
        print(text)
except Exception as e:
    print(e)
"""
