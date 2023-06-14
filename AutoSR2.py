from transformers import pipeline
from pydub import AudioSegment
import os

cls = pipeline("automatic-speech-recognition", "facebook/wav2vec2-base-960h")

def save_to_text_file(result, file_path):
    text = str(result)
    with open(file_path, 'w') as file:
        file.write(text)
    print(f"Text saved to file: {file_path}")

def mp3_to_flac(mp3_file, flac_file):
    audio = AudioSegment.from_mp3(mp3_file)
    audio.export(flac_file, format='flac')

mp3_file = "20200918-105415_0767896855-all.mp3"
flac_file = "output.flac"
mp3_to_flac(mp3_file, flac_file)

in_file = "output.flac"
out_file = "sample.txt"


# def wav_to_flac(wav_file, flac_file):
#     audio = AudioSegment.from_wav(wav_file)
#     audio.export(flac_file, format='flac')

# wav_file = "Introduction_Medical_Society.wav"
# flac_file = "outputw.flac"
# mp3_to_flac(wav_file, flac_file)

# in_file = "outputw.flac"
# out_file = "sample.txt"

result = cls(in_file)

save_to_text_file(result, out_file)

print(result)