import torch
import torch_directml
import soundfile as sf  # <-- Importamos a biblioteca para ler o áudio
from transformers import pipeline

# 1. Ativa o suporte para a placa AMD
device_amd = torch_directml.device()
print(f"Utilizando o dispositivo: {device_amd}")

# 2. Define o modelo do Hugging Face
model_id = "Dpngtm/wav2vec2-emotion-recognition"

# 3. Inicializa o pipeline passando o dispositivo AMD
classifier = pipeline("audio-classification", model=model_id, device=device_amd)

# 4. Lê o áudio manualmente para contornar a necessidade do FFmpeg
audio_path = "audio.wav"
print("Carregando o arquivo de áudio...")

# Lê o áudio convertendo para o formato exato que a IA exige (float32)
audio_array, sample_rate = sf.read(audio_path, dtype='float32')

print("Analisando os sentimentos na voz via GPU AMD...")
# Entregamos para a IA um dicionário com o áudio já aberto
predictions = classifier({"array": audio_array, "sampling_rate": sample_rate})

# 5. Exibe os resultados
print("\n--- Resultados ---")
for pred in predictions:
    porcentagem = pred['score'] * 100
    print(f"Emoção: {pred['label'].capitalize()} -> {porcentagem:.2f}%")