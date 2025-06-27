import torch
import torchaudio
from transformers import WhisperProcessor, WhisperForConditionalGeneration
from wav_convert import convert_m4a_to_wav
import re

# 중복 문장 제거
def remove_duplicate_sentences(text):
    sentences = re.split(r'(?<=[.?!])\s+', text)
    seen = set()
    unique_sentences = []
    for sentence in sentences:
        normalized = sentence.strip()
        if normalized and normalized not in seen:
            seen.add(normalized)
            unique_sentences.append(normalized)
    return ' '.join(unique_sentences)
def stt(record_path):
    print("토치",torch.cuda.is_available())
    # Hugging Face에서 다운로드한 모델을 로컬에서 불러오기
    processor = WhisperProcessor.from_pretrained("openai/whisper-small")
    model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-small")



    # GPU 사용 가능하면 모델을 GPU로 이동
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model.to(device)

    # 음성 파일을 불러와 변환
    file_path = convert_m4a_to_wav(record_path)
    waveform, sample_rate = torchaudio.load(file_path)

    # 16kHz로 변환 (Whisper 모델 요구사항)
    resampler = torchaudio.transforms.Resample(orig_freq=sample_rate, new_freq=16000)
    waveform = resampler(waveform)

    forced_decoder_ids = processor.get_decoder_prompt_ids(language="korean", task="transcribe")
    # 모델 입력 변환


    chunk_size = 30 * 16000  # ✅ 30초 단위로 나누기 (16kHz 샘플링 기준)
    transcriptions = []

    for i in range(0, waveform.shape[1], chunk_size):
        chunk = waveform[:, i:i+chunk_size]  # ✅ 음성 데이터 일부만 선택

        inputs = processor(
            chunk.squeeze(0),
            sampling_rate=16000,
            return_tensors="pt",
            padding=True
        )

        input_features = inputs.input_features.to(device)

        with torch.no_grad():
            predicted_ids = model.generate(
                input_features,
                forced_decoder_ids=forced_decoder_ids,
                max_length=448,  # ✅ 길이 조정
                return_timestamps="vtt",
                output_scores=True,  # 추가
                return_dict=True  # 추가
            )

        transcriptions.append(processor.batch_decode(predicted_ids, skip_special_tokens=True)[0])
        print("여기에요ㅕ",predicted_ids)

    result = " ".join(transcriptions)
    result = remove_duplicate_sentences(result)

    return result