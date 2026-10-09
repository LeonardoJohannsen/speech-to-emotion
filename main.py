import os
import torch
import torch_directml
import soundfile as sf
import numpy as np
from transformers import pipeline

device_amd = torch_directml.device()
print(f"Utilizando AMD para Emoção: {device_amd}")

# ==========================================
# 1. CARREGANDO OS 3 MODELOS
# ==========================================
print("Carregando modelos (Isso leva alguns segundos)...")

# 1.1 Modelo de Emoção da Voz (Roda na GPU AMD)
classifier_audio = pipeline("audio-classification", model="Dpngtm/wav2vec2-emotion-recognition", device=device_amd)

# 1.2 Modelo de Transcrição Whisper (Sozinho na CPU, agora na versão mais inteligente)
transcriber = pipeline("automatic-speech-recognition", model="openai/whisper-medium")

# 1.3 Modelo de Análise Psicológica do Texto (Roda na CPU para evitar erro do DirectML)
classificador_texto = pipeline("zero-shot-classification", model="MoritzLaurer/mDeBERTa-v3-base-mnli-xnli")

# ==========================================
# 2. CONFIGURAÇÕES DA ANÁLISE
# ==========================================
# Categorias que a IA vai procurar no texto (você pode editar como quiser)
categorias_psicologicas = [
    "Feedback Positivo e Bom Humor",
    "Exaustão Física ou Sobrecarga",
    "Atrito Interpessoal ou Briga",
    "Desmotivação, frustração ou falta de perspectiva", # <-- Resolve os áudios 'desmotivado'
    "Intenção de pedir demissão ou sair do emprego",     # <-- Resolve os áudios 'largando'
    "Denúncia de infração, assédio ou perigo físico"     # <-- Ajuda a IA a entender a 'situacao'
]

# Configure a pasta com seus áudios de teste (Lembrete: áudios do RAVDESS sempre darão "Rotina normal")
pasta_dataset = "C:/Users/leona/OneDrive/Documentos/faculdade/AudioToText/pasta_teste"
arquivos = [f for f in os.listdir(pasta_dataset) if f.endswith(".wav")]

print(f"\nIniciando análise profunda de {len(arquivos)} arquivos...\n")
print("="*60)

# ==========================================
# 3. LOOP DE TESTE
# ==========================================
for arquivo in arquivos:
    caminho_completo = os.path.join(pasta_dataset, arquivo)
    
    # --- LENDO O ÁUDIO ---
    audio_array, sample_rate = sf.read(caminho_completo, dtype='float32')
    if len(audio_array.shape) > 1:
        audio_array = np.mean(audio_array, axis=1)

    # --- IA 1: EMOÇÃO DA VOZ ---
    predictions_audio = classifier_audio({"array": audio_array, "sampling_rate": sample_rate})
    emocao_voz = predictions_audio[0]['label'].upper() 
    
    # --- IA 2: TRANSCRIÇÃO (WHISPER) ---
    texto_extraido = transcriber({"raw": audio_array, "sampling_rate": sample_rate}, generate_kwargs={"task": "transcribe", "language": "pt"})['text'].strip()

    # --- IA 3: ANÁLISE ZERO-SHOT DO TEXTO ---
    # Só analisa se o Whisper conseguiu entender alguma palavra
    if texto_extraido:
        analise_texto = classificador_texto(
            texto_extraido, 
            categorias_psicologicas, 
            hypothesis_template="O relato deste funcionário sobre o trabalho indica um cenário de {}.", # <-- ISSO MUDA TUDO
            multi_label=False
        )
        # Pega a categoria com maior pontuação
        categoria_texto = analise_texto['labels'][0]
        confianca_texto = analise_texto['scores'][0] * 100
    else:
        categoria_texto = "Inconclusivo (Áudio mudo)"
        confianca_texto = 0.0

    palavras_criticas = ["choque", "vazando", "assédio", "machista", "roubo", "dinheiro do caixa", "denunciar"]

    # Depois que o Whisper gerar o 'texto_extraido':
    texto_min = texto_extraido.lower()
    alerta_seguranca = False

    for palavra in palavras_criticas:
        if palavra in texto_min:
            alerta_seguranca = True
            break

    if alerta_seguranca:
        print("🚨 ALERTA RH: POSSÍVEL CRIME OU RISCO DE VIDA DETECTADO!")
    # --- IMPRIMINDO O CRUZAMENTO DE DADOS ---
    print(f"Arquivo: {arquivo}")
    print(f"Fala: \"{texto_extraido}\"")
    print(f"🎤 Tom de Voz : {emocao_voz}")
    print(f"🧠 Tema Falado: {categoria_texto.upper()} ({confianca_texto:.1f}%)")
    print("-" * 60)