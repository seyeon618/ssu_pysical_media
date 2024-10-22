import os
from google.cloud import speech_v1p1beta1 as speech
from openai import OpenAI

client = OpenAI(api_key="")

# Google Cloud 인증 키 파일 경로 설정
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "civil-dolphin-438711-b9-ddded773dbcc.json"

# OpenAI API Key 설정
  # OpenAI API 키 추가

def transcribe_audio_from_file(file_path):
    """로컬 오디오 파일을 텍스트로 변환하는 함수"""
    client = speech.SpeechClient()

    # 로컬 오디오 파일 읽기
    with open(file_path, "rb") as audio_file:
        audio_content = audio_file.read()

    audio = speech.RecognitionAudio(content=audio_content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=48000,  # 파일의 샘플링 레이트에 맞게 설정
        language_code="ko-KR"
    )

    response = client.recognize(config=config, audio=audio)
    for result in response.results:
        return result.alternatives[0].transcript

def analyze_text_with_gpt(transcribed_text):
    """ChatGPT에 텍스트를 분석하여 'turn on' 또는 'turn off'로 응답하는 함수"""
    prompt = f"다음 요청이 불을 꺼달라는 내용이면 'turn off', 불을 켜달라는 내용이면 'turn on'이라고 응답해줘: {transcribed_text}"

    response = client.chat.completions.create(model="gpt-3.5-turbo",  # 모델 선택
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ])

    return response.choices[0].message.content.strip()

if __name__ == "__main__":
    # 로컬 오디오 파일 경로
    audio_file_path = "./static/sample/turnOff.wav"  # 오디오 파일 경로 설정

    # 1. 오디오 파일을 텍스트로 변환 (Google Speech-to-Text API)
    transcribed_text = transcribe_audio_from_file(audio_file_path)
    print(f"Transcribed text: {transcribed_text}")

    # 2. 변환된 텍스트를 ChatGPT로 분석하여 'turn on' 또는 'turn off'로 응답 받기
    gpt_response = analyze_text_with_gpt(transcribed_text)
    print(f"ChatGPT response: {gpt_response}")
