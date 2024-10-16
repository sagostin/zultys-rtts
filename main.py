import os
import random
import string
import sqlite3
import time
from flask import Flask, request
import logging

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'static/tts/'

logging.basicConfig(
    level=logging.INFO,  # Set the desired log level (e.g., INFO, DEBUG, ERROR)
    filename='logs.txt',  # Specify the file name for log output
    filemode='a',  # Use 'a' to append logs to the file, 'w' to overwrite it
    format='%(asctime)s - %(levelname)s - %(message)s'  # Define the log message format
)

def get_client_ip():
    if request.headers.get('X-Forwarded-For'):
        # X-Forwarded-For may contain multiple IPs, the first one is the client's IP
        client_ip = request.headers.get('X-Forwarded-For').split(',')[0].strip()
    else:
        client_ip = request.remote_addr
    return client_ip

def init_db():
    """Initialize the SQLite database and create the cache table if it doesn't exist."""
    conn = sqlite3.connect('tts_cache.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS cache (
            text TEXT PRIMARY KEY,
            file_name TEXT,
            timestamp REAL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/tts', methods=['GET'])
def tts():
    from google.cloud import texttospeech

    text = request.args.get('text')
    language = request.args.get('language', 'en-US')
    voice_name = request.args.get('voice', 'en-US-Wavenet-D')
    speed = request.args.get('speed', '1.0')
    file_extension = 'wav'
    force = request.args.get('force', '0')  # Use '1' to force re-generation

    # Input validation
    if not text:
        return 'Error: "text" parameter is required.', 400

    # Initialize database connection
    conn = sqlite3.connect('tts_cache.db')
    c = conn.cursor()

    # Check if the text already exists in the cache
    c.execute('SELECT file_name, timestamp FROM cache WHERE text = ?', (text,))
    result = c.fetchone()

    client_ip = get_client_ip()

    if result and force != '1':
        # File already exists, return the existing file
        file_name = result[0]
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
        logging.info(
            f"Using cached file {file_name} for text: {text}",
            extra={'clientip': client_ip}
        )
        # Assign the 'response' variable
        response = f'<HTML><HEAD/><BODY>Response = OK (Cached)<br><HR>result = 1<br>file = http://tts.topsoffice.ca/{file_path}<br><HR></BODY></HTML>'
    else:
        # Generate a random file name
        random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        file_name = f'{random_string}.{file_extension}'
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)

        # Synthesizes speech from the input string of text.
        gcloud_project = request.args.get('id')
        gcloud_key = request.args.get('passw')

        client = texttospeech.TextToSpeechClient(client_options={
            "api_key": gcloud_key,
            "quota_project_id": gcloud_project
        })

        input_text = texttospeech.SynthesisInput(text=text)

        # Define the voice parameters
        voice = texttospeech.VoiceSelectionParams(
            language_code=language,
            name=voice_name,
            # ssml_gender can be set if needed
        )

        # Define the audio configuration
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MULAW,
            sample_rate_hertz=8000,
            speaking_rate=float(speed)
        )

        response_tts = client.synthesize_speech(
            request={"input": input_text, "voice": voice, "audio_config": audio_config}
        )

        logging.info(
            f"Generated new file {file_name} for text: {text}",
            extra={'clientip': client_ip}
        )

        if response_tts.audio_content:
            # Save the generated audio file
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            with open(file_path, 'wb') as f:
                f.write(response_tts.audio_content)

            # Update the database with the new entry
            timestamp = time.time()
            c.execute('REPLACE INTO cache (text, file_name, timestamp) VALUES (?, ?, ?)',
                      (text, file_name, timestamp))
            conn.commit()

            # Assign the 'response' variable
            response = f'<HTML><HEAD/><BODY>Response = OK<br><HR>result = 1<br>file = http://tts.topsoffice.ca/{file_path}<br><HR></BODY></HTML>'
            logging.info(f"File saved as {file_path}, for text: {text}")
        else:
            response = f'<HTML><HEAD/><BODY>Response = ERROR<br><HR>result = 0<br>file = ERROR<br><HR></BODY></HTML>'
            logging.error(f"File FAILED to generate as {file_path}, for text: {text}")

    conn.close()
    return response, 200
    from google.cloud import texttospeech

    text = request.args.get('text')
    language = request.args.get('language', 'en-US')
    voice_name = request.args.get('voice', 'en-US-Wavenet-D')
    speed = request.args.get('speed', '1.0')
    file_extension = 'wav'
    force = request.args.get('force', '0')  # Use '1' to force re-generation

    # Input validation
    if not text:
        return 'Error: "text" parameter is required.', 400

    # Initialize database connection
    conn = sqlite3.connect('tts_cache.db')
    c = conn.cursor()

    # Check if the text already exists in the cache
    c.execute('SELECT file_name, timestamp FROM cache WHERE text = ?', (text,))
    result = c.fetchone()

    if result and force != '1':
        # File already exists, return the existing file
        file_name = result[0]
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
        logging.info(f"Using cached file {file_name} for text: {text}")
    else:
        # Generate a random file name
        random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        file_name = f'{random_string}.{file_extension}'
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)

        # Synthesizes speech from the input string of text.
        gcloud_project = request.args.get('id')
        gcloud_key = request.args.get('passw')

        client = texttospeech.TextToSpeechClient(client_options={
            "api_key": gcloud_key,
            "quota_project_id": gcloud_project
        })

        input_text = texttospeech.SynthesisInput(text=text)

        # Define the voice parameters
        voice = texttospeech.VoiceSelectionParams(
            language_code=language,
            name=voice_name,
            # ssml_gender can be set if needed
        )

        # Define the audio configuration
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MULAW,
            sample_rate_hertz=8000,
            speaking_rate=float(speed)
        )

        response = client.synthesize_speech(
            request={"input": input_text, "voice": voice, "audio_config": audio_config}
        )

        if response.audio_content:
            # Save the generated audio file
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            with open(file_path, 'wb') as f:
                f.write(response.audio_content)

            # Update the database with the new entry
            timestamp = time.time()
            c.execute('REPLACE INTO cache (text, file_name, timestamp) VALUES (?, ?, ?)',
                      (text, file_name, timestamp))
            conn.commit()

            # Format the response
            response = f'<HTML><HEAD/><BODY>Response = OK<br><HR>result = 1<br>file = http://tts.topsoffice.ca/{file_path}<br><HR></BODY></HTML>'
            logging.info(f"File saved as {file_path}, for text: {text}")
        else:
            response = f'<HTML><HEAD/><BODY>Response = ERROR<br><HR>result = 0<br>file = ERROR<br><HR></BODY></HTML>'
            logging.error(f"File FAILED to generate as {file_path}, for text: {text}")

    conn.close()
    return response, 200

@app.route('/purge', methods=['GET'])
def purge():
    """Purge cache entries older than a specified age."""
    # Purge cache entries older than a certain age (in seconds)
    max_age_seconds = int(request.args.get('max_age', 30 * 24 * 60 * 60))  # Default to 30 days
    current_time = time.time()
    cutoff_time = current_time - max_age_seconds

    # Initialize database connection
    conn = sqlite3.connect('tts_cache.db')
    c = conn.cursor()

    # Get entries older than cutoff_time
    c.execute('SELECT text, file_name FROM cache WHERE timestamp < ?', (cutoff_time,))
    old_entries = c.fetchall()

    # Delete old files and entries
    for text_entry, file_name in old_entries:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
        if os.path.exists(file_path):
            os.remove(file_path)
            logging.info(f"Deleted old file: {file_path}")
        else:
            logging.warning(f"File not found for deletion: {file_path}")
        # Delete from database
        c.execute('DELETE FROM cache WHERE text = ?', (text_entry,))

    conn.commit()
    conn.close()

    return f'Purged {len(old_entries)} old recordings.', 200

if __name__ == '__main__':
    init_db()
    # Run app in debug mode on port 8081
    app.run(host='0.0.0.0', debug=False, port=8081)