import os
import random
import string
from flask import Flask, request

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'upload/tts/'


@app.route('/tts', methods=['GET'])
def tts():
    from google.cloud import texttospeech

    text = request.args.get('text')
    language = request.args.get('language', 'en')
    voice = request.args.get('voice', 'en-US-Wavenet-D')
    speed = request.args.get('speed', '1.0')
    file_extension = 'wav'

    # Generate a random file name
    random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    file_name = f'{random_string}.{file_extension}'
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)

    """Synthesizes speech from the input string of text."""

    gcloud_project = request.args.get('id')
    gcloud_key = request.args.get('passw')

    client = texttospeech.TextToSpeechClient(client_options={"api_key": gcloud_key,
                                                             "quota_project_id": gcloud_project})

    input_text = texttospeech.SynthesisInput(text=text)

    # Note: the voice can also be specified by name.
    # Names of voices can be retrieved with client.list_voices().
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-Standard-C",
        ssml_gender=texttospeech.SsmlVoiceGender.FEMALE,
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MULAW
    )

    response = client.synthesize_speech(
        request={"input": input_text, "voice": voice, "audio_config": audio_config}
    )

    if response.audio_content:
        # Save the generated WAV file
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        with open(file_path, 'wb') as f:
            f.write(response.audio_content)

        # Format the response
        response = f'<HTML><HEAD/><BODY>Response = OK<br><HR>result = 1<br>file = http://tts.topsoffice.ca/upload/tts/{file_path}</BODY></HTML>'
    else:
        response = f'<HTML><HEAD/><BODY>Response = ERROR<br><HR>result = 0<br>file = ERROR</BODY></HTML>'

    return response, 200


if __name__ == '__main__':
    # run app in debug mode on port 5000
    app.run(host='0.0.0.0', debug=True, port=8081)
