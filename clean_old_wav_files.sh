#!/bin/bash

# Change directory to the desired location
cd /opt/zultys-rtts/static/tts

# Remove all files with .wav extension that are older than 1 day
find . -type f -name "*.wav" -mtime +1 -delete