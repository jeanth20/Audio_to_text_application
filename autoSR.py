import json
import requests

API_TOKEN = "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"

headers = {"Authorization": f"Bearer {API_TOKEN}"}
API_URL = "https://api-inference.huggingface.co/models/facebook/wav2vec2-base-960h"

def query(filename):
    with open(filename, "rb") as f:
        data = f.read()
    response = requests.request("POST", API_URL, headers=headers, data=data)
    return json.loads(response.content.decode("utf-8"))

data = query("sample1.flac")

from transformers import pipeline

with open("sample.flac", "rb") as f:
  data = f.read()

pipe = pipeline("automatic-speech-recognition", "facebook/wav2vec2-base-960h")
pipe("sample.flac")
# {'text': "GOING ALONG SLUSHY COUNTRY ROADS AND SPEAKING TO DAMP AUDIENCES IN DRAUGHTY SCHOOL ROOMS DAY AFTER DAY FOR A FORTNIGHT HE'LL HAVE TO PUT IN AN APPEARANCE AT SOME PLACE OF WORSHIP ON SUNDAY MORNING AND HE CAN COME TO US IMMEDIATELY AFTERWARDS"}
