import os
import random
import string

from TTS.api import TTS
from flask import Flask, request

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'static/tts/'


@app.route('/tts', methods=['GET'])
def tts():
    model_name = request.args.get('model_name')
    text = request.args.get('text')
    language = request.args.get('language', None)
    speaker = request.args.get('speaker', None)
    speaker_wav = request.args.get('speaker_wav', None)
    file_name = request.args.get('file_name')
    emotion = request.args.get('emotion', None)
    speed = request.args.get('speed', None)
    gpu = request.args.get('gpu', False)
    progress_bar = request.args.get('progress_bar', False)

    # constants?
    language = 'en'
    model_name = TTS.list_models()[0]

    # Init TTS with the target model name
    tts = TTS(model_name=model_name, progress_bar=progress_bar, gpu=gpu)

    speaker = tts.speakers[0]

    response = ''

    # todo require auth, and save file to local directory
    # return already generated files if they exist?

    if speaker:

        # Generate a random file name
        file_extension = 'wav'
        random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        file_name = f'{random_string}.{file_extension}'
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)

        # Save the generated WAV file
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

        # Text to speech with a numpy output
        wav = tts.tts_to_file(text=text, speaker=speaker, language=language, file=file_path)

        # Format the response
        response = f'<HTML><HEAD/><BODY>Response = OK<br><HR>result = 1<br>file = http://tts.zultys-support.com/{file_path}</BODY></HTML>'
    else:
        response = f'<HTML><HEAD/><BODY>Response = ERROR<br><HR>result = 0<br>file = ERROR</BODY></HTML>'

    return response, 200


if __name__ == '__main__':
    # run app in debug mode on port 5000
    app.run(host='0.0.0.0', debug=True, port=5000)
