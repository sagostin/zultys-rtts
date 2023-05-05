import os
import random
import string
import requests
from flask import Flask, request

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'static/tts/'


@app.route('/tts', methods=['GET'])
def tts():
    from google.cloud import texttospeech

    text = request.args.get('text')
    language = request.args.get('language', 'en')
    voice = request.args.get('voice', 'en-US-Wavenet-D')
    speed = request.args.get('speed', '1.0')
    file_extension = 'wav'

    api_key = request.args.get('api_key', 'YOUR_API_KEY')

    # Generate a random file name
    random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    file_name = f'{random_string}.{file_extension}'
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)

    """Synthesizes speech from the input string of text."""

    client = texttospeech.TextToSpeechClient(credentials=api_key)

    input_text = texttospeech.SynthesisInput(text=text)

    # Note: the voice can also be specified by name.
    # Names of voices can be retrieved with client.list_voices().
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-Standard-C",
        ssml_gender=texttospeech.SsmlVoiceGender.FEMALE,
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        request={"input": input_text, "voice": voice, "audio_config": audio_config}
    )

    if response.status_code == 200:
        # Save the generated WAV file
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        with open(file_path, 'wb') as f:
            f.write(response.content)

        # Format the response
        response = f'<HTML><HEAD/><BODY>Response = OK<br><HR>result = 1<br>file = http://tts.zultys-support.com/{file_path}</BODY></HTML>'
    else:
        response = f'<HTML><HEAD/><BODY>Response = ERROR<br><HR>result = 0<br>file = ERROR</BODY></HTML>'

    return response, 200


if __name__ == '__main__':
    # run app in debug mode on port 5000
    app.run(host='0.0.0.0', debug=True, port=8081)
