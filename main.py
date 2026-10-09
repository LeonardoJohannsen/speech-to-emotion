import os
import torch
import torch_directml
import soundfile as sf
import numpy as np
from transformers import pipeline

device_amd = torch_directml.device()
print(f"Utilizando AMD para Emoção: {device_amd}")

# ==========================================
# 1. CARREGANDO OS MODELOS (Apenas uma vez)
# ==========================================
print("Carregando modelos (Isso leva alguns segundos)...")
classifier = pipeline("audio-classification", model="Dpngtm/wav2vec2-emotion-recognition", device=device_amd)
transcriber = pipeline("automatic-speech-recognition", model="openai/whisper-small") # CPU

# ==========================================
# 2. CONFIGURAÇÕES DO DATASET
# ==========================================
# ⚠️ IMPORTANTE: Coloque o caminho exato da pasta onde estão os áudios
pasta_dataset = "C:/Users/leona/OneDrive/Documentos/faculdade/AudioToText/archive/audio_speech_actors_01-24/Actor_24"

# Dicionário do RAVDESS: O 3º número do arquivo indica a emoção real
mapa_emocoes = {
    "01": "neutral", "02": "calm", "03": "happy", "04": "sad",
    "05": "angry", "06": "fearful", "07": "disgust", "08": "surprised"
}

# Lista todos os arquivos .wav da pasta (pegando só os 5 primeiros para um teste rápido)
# Se quiser testar todos, apague o [:5] no final da linha abaixo
arquivos = [f for f in os.listdir(pasta_dataset) if f.endswith(".wav")]

total_arquivos = len(arquivos)
acertos = 0

print(f"\nIniciando o teste com {total_arquivos} arquivos...\n")
print("="*60)

# ==========================================
# 3. LOOP DE TESTE
# ==========================================
for arquivo in arquivos:
    caminho_completo = os.path.join(pasta_dataset, arquivo)
    
    # --- DESCOBRINDO A EMOÇÃO REAL (GABARITO) ---
    # Divide o nome '03-01-04-01-01-01-01.wav' pelos traços
    partes_nome = arquivo.split("-")
    
    # Pega o 3º número (índice 2)
    codigo_emocao = partes_nome[2] 
    emocao_real = mapa_emocoes.get(codigo_emocao, "desconhecida")
    
    # --- LENDO O ÁUDIO ---
    audio_array, sample_rate = sf.read(caminho_completo, dtype='float32')
    if len(audio_array.shape) > 1:
        audio_array = np.mean(audio_array, axis=1)

    # --- IA DE EMOÇÃO ---
    predictions = classifier({"array": audio_array, "sampling_rate": sample_rate})
    emocao_ia = predictions[0]['label'].lower() # Pega a de maior porcentagem em minúsculo
    
    # --- IA DE TEXTO (WHISPER) ---
    # Coloquei "en" porque o RAVDESS é em inglês. Se testar áudios BR depois, mude para "pt"
    texto = transcriber({"raw": audio_array, "sampling_rate": sample_rate}, generate_kwargs={"task": "transcribe", "language": "en"})['text'].strip()

    # --- COMPARANDO RESULTADOS ---
    acertou = emocao_ia == emocao_real
    if acertou:
        acertos += 1
        status = "✅ ACERTOU"
    else:
        status = "❌ ERROU"

    # --- IMPRIMINDO NA TELA ---
    print(f"Arquivo: {arquivo}")
    print(f"Fala: \"{texto}\"")
    print(f"Emoção Real: {emocao_real.upper()} | Emoção da IA: {emocao_ia.upper()} -> {status}")
    print("-" * 60)

# ==========================================
# 4. RESULTADO FINAL
# ==========================================
if total_arquivos > 0:
    acuracia = (acertos / total_arquivos) * 100
    print(f"\n🎯 ACURÁCIA FINAL: {acuracia:.2f}% ({acertos} acertos de {total_arquivos} áudios)\n")
else:
    print("\nNenhum arquivo .wav foi encontrado na pasta informada!")