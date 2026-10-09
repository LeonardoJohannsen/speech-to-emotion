import torch
import torch_directml
import soundfile as sf
import numpy as np
from transformers import pipeline

device_amd = torch_directml.device()
print(f"Utilizando o dispositivo AMD para Emoção: {device_amd}")

audio_path = "audio.wav"
print("\nCarregando o arquivo de áudio...")
audio_array, sample_rate = sf.read(audio_path, dtype='float32')

if len(audio_array.shape) > 1:
    audio_array = np.mean(audio_array, axis=1)

audio_input_emocao = {"array": audio_array, "sampling_rate": sample_rate}
audio_input_texto = {"raw": audio_array, "sampling_rate": sample_rate}

# ==========================================
# 3. ANÁLISE DE EMOÇÃO (Roda na GPU AMD)
# ==========================================
print("\n[1/2] Analisando emoções...")
emotion_model_id = "Dpngtm/wav2vec2-emotion-recognition"
classifier = pipeline("audio-classification", model=emotion_model_id, device=device_amd)
predictions = classifier(audio_input_emocao)

# ==========================================
# 4. TRANSCRIÇÃO DE TEXTO (Roda na CPU)
# ==========================================
print("\n[2/2] Extraindo texto (Whisper)...")
transcription_model_id = "openai/whisper-small" 

# Removido o 'device=device_amd' para usar a estabilidade da CPU na geração de texto
transcriber = pipeline("automatic-speech-recognition", model=transcription_model_id)

# Forçamos o idioma ("en" para inglês, "pt" para português) para evitar alucinações
texto_extraido = transcriber(audio_input_texto, generate_kwargs={"task": "transcribe", "language": "pt"})

# ==========================================
# 5. RESULTADOS FINAIS
# ==========================================
print("\n" + "="*40)
print("             RESULTADOS")
print("="*40)

print(f"\nTexto falado: \n\"{texto_extraido['text']}\"\n")

print("Emoções detectadas:")
for pred in predictions:
    porcentagem = pred['score'] * 100
    print(f" - {pred['label'].capitalize()}: {porcentagem:.2f}%")
print("="*40)