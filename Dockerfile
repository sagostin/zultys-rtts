# Use a slim Python base image
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# App lives here (equivalent to /opt/zultys-rtts in the service file)
WORKDIR /app

# Install system deps (none strictly required right now, just keep it minimal)
RUN apt-get update && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Copy repo contents into the container
# (Assumes Dockerfile is in the root of the zultys-rtts repo)
COPY . .

# Create the TTS output directory used by the app
# main.py uses: app.config['UPLOAD_FOLDER'] = 'static/tts/'
RUN mkdir -p static/tts

# Install Python dependencies
# main.py imports: flask, google.cloud.texttospeech, sqlite3 (stdlib), logging (stdlib)
RUN pip install --no-cache-dir \
    flask \
    google-cloud-texttospeech

# Flask app listens on port 8081 in main.py
EXPOSE 8081

# Match the systemd ExecStart:
# ExecStart=/usr/bin/python3 /opt/zultys-rtts/main.py
CMD ["python", "main.py"]