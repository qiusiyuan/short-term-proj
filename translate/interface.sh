#!/bin/bash
python3 audio_collect.py
node speech_text.js
python3 audio_read.py