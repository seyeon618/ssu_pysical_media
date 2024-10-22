from flask import Flask, request
from google.cloud import speech_v1p1beta1 as speech
import os

app = Flask(__name__)

# # Google Cloud 인증 키 파일 경로 설정
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "civil-dolphin-438711-b9-ddded773dbcc.json"


def transcribe_audio(audio_content):
    client = speech.SpeechClient()
    audio = speech.RecognitionAudio(content=audio_content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="ko-KR"
    )

    response = client.recognize(config=config, audio=audio)
    for result in response.results:
        return result.alternatives[0].transcript


@app.route('/upload', methods=['POST'])
def upload_audio():
    audio_file = request.files['file'].read()
    print('upload success')
    transcript = transcribe_audio(audio_file)
    return transcript


if __name__ == '__main__':
    app.run(debug=True)

# 실행 명령어
# curl -X POST -F file=@static/sample/turnOff.wav http://127.0.0.1:5000/upload