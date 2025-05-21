import torch
import torchaudio
import base64
import os
from pydub import AudioSegment
from transformers import WhisperProcessor, WhisperForConditionalGeneration
import urllib3
import json
import base64
import urllib3
import requests

def code2wav(code):
    result= code
    return result

def convert_mp4_to_wav_pydub(input_mp4, output_wav):
    """pydub을 사용한 MP4 → WAV 변환"""
    audio = AudioSegment.from_file(input_mp4, format="mp4")
    audio = audio.set_frame_rate(16000).set_channels(1)  # Whisper 요구사항: 16kHz, 모노 채널
    audio.export(output_wav, format="wav")
    print(f"✅ 변환 완료: {output_wav}")

def convert_m4a_to_wav(input_m4a):
    """M4A 파일을 WAV로 변환 (16kHz, 모노)"""
    output_wav=input_m4a[:-4]+".wav"
    audio = AudioSegment.from_file(input_m4a, format="m4a")
    audio = audio.set_frame_rate(16000).set_channels(1)  # Whisper 요구사항: 16kHz, 모노 채널
    audio = audio[:30 * 1000]  # 30초 (밀리초 단위)
    audio.export(output_wav, format="wav")
    print(f"✅ 변환 완료: {output_wav}")
    return output_wav

def convert_m4a_to_base64(input_m4a):
    """M4A 파일을 WAV로 변환 후 Base64 인코딩"""

    output_wav=convert_m4a_to_wav(input_m4a)  # M4A를 WAV로 변환

    with open(output_wav, "rb") as wav_file:
        wav_bytes = wav_file.read()
        base64_audio = base64.b64encode(wav_bytes).decode("utf-8")  # Base64로 인코딩

    print(f"✅ Base64 인코딩 완료: (길이: {len(base64_audio)})")


    os.remove(output_wav)  # 임시 WAV 파일 삭제

    return base64_audio

def audio_score(m4a):
    openApiURL = "http://aiopen.etri.re.kr:8000/WiseASR/PronunciationKor" # 한국어
    accessKey = 'd5fa34f5-4abe-4f8d-9768-d39c0536f595'
    languageCode = 'korean'


    audio_data=convert_m4a_to_base64(m4a)
    requestJson = {   
        "argument": {
            "language_code": languageCode,
            "audio": audio_data
        }
    }
    http = urllib3.PoolManager()
    response = http.request(
        "POST",
        openApiURL,
        headers={"Content-Type": "application/json; charset=UTF-8","Authorization": accessKey},
        body=json.dumps(requestJson)
    )
    
    print("[responseCode] " + str(response.status))
    print("[responBody]")
    response_body_str = response.data.decode('utf-8')
    response_data = json.loads(response_body_str)

    recognized_text = response_data["return_object"]["recognized"]
    score = response_data["return_object"]["score"]
    return score
