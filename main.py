from flask import Flask, request, jsonify, send_file
from TTS.api import TTS

app = Flask(__name__)


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

    # Init TTS with the target model name
    tts = TTS(model_name=model_name, progress_bar=progress_bar, gpu=gpu)

    response = ''

    if speaker:
        # Text to speech with a numpy output
        file_path = f'static/{file_name}'
        wav = tts.tts(text=text, speaker=speaker, language=language)
        # Text to speech to a file
        tts.tts_to_file(text=text, speaker=speaker, language=language, file_path=file_path)

        # Format the response
        response = f'<HTML><HEAD/><BODY>Response = OK<br><HR>result = 1<br>file = http://tts.zultys-support.com/{file_path}</BODY></HTML>'
    else:
        response = f'<HTML><HEAD/><BODY>Response = ERROR<br><HR>result = 0<br>file = ERROR</BODY></HTML>'

    return response, 200


if __name__ == '__main__':
    # run app in debug mode on port 5000
    app.run(debug=True, port=5000)
