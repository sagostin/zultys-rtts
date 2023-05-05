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
    file_path = request.args.get('file_path')
    emotion = request.args.get('emotion', None)
    speed = request.args.get('speed', None)
    gpu = request.args.get('gpu', False)
    progress_bar = request.args.get('progress_bar', False)

    # Init TTS with the target model name
    tts = TTS(model_name=model_name, progress_bar=progress_bar, gpu=gpu)

    if speaker_wav:
        # Example voice cloning
        tts.tts_to_file(text=text, speaker_wav=speaker_wav, language=language, file_path=file_path)
    elif speaker:
        # Text to speech with a numpy output
        wav = tts.tts(text=text, speaker=speaker, language=language)
        # Text to speech to a file
        tts.tts_to_file(text=text, speaker=speaker, language=language, file_path=file_path)

    return send_file(file_path, as_attachment=True)
