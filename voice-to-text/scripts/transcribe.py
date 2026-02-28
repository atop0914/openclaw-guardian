#!/usr/bin/env python3
"""Voice to Text using faster-whisper"""

import sys
from faster_whisper import WhisperModel

def transcribe(audio_path):
    model = WhisperModel('tiny', device='cpu', compute_type='int8')
    segments, info = model.transcribe(audio_path)
    result = []
    for segment in segments:
        result.append(segment.text)
    return ''.join(result).strip()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: transcribe.py <audio_file>", file=sys.stderr)
        sys.exit(1)
    
    audio_path = sys.argv[1]
    text = transcribe(audio_path)
    print(text)
