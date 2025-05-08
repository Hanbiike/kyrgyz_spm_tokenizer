import sentencepiece as spm
import os
import pandas as pd

# Путь к тестовому корпусу
test_file = "kyrgyz_clean_sentences.txt"
models_dir = "models"

# Загружаем первые 1000 предложений
with open(test_file, "r", encoding="utf-8") as f:
    sentences = [line.strip() for line in f if line.strip()]
sentences = sentences[:10000]

# Найдём все .model файлы в папке models
models = sorted([f for f in os.listdir(models_dir) if f.endswith(".model")])

results = []

for model_file in models:
    model_path = os.path.join(models_dir, model_file)
    sp = spm.SentencePieceProcessor()
    sp.load(model_path)

    total_tokens = 0
    total_unk = 0
    total_chars = 0
    total_words = 0

    for sentence in sentences:
        ids = sp.encode(sentence)
        pieces = sp.encode(sentence, out_type=str)
        total_tokens += len(ids)
        total_words += 1
        total_unk += ids.count(sp.unk_id())
        total_chars += sum(len(p) for p in pieces)

    avg_tokens = total_tokens / total_words
    avg_token_len = total_chars / total_tokens
    unk_rate = total_unk / total_tokens

    results.append({
        "model": model_file,
        "avg_tokens": round(avg_tokens, 2),
        "avg_token_len": round(avg_token_len, 2),
        "unk_rate_%": round(unk_rate * 100, 2)
    })

df = pd.DataFrame(results)
df = df.sort_values("avg_tokens")

print(df)

import matplotlib.pyplot as plt

# 🎨 График 1: Среднее количество токенов
plt.figure(figsize=(12, 6))
plt.bar(df["model"], df["avg_tokens"])
plt.title("📏 Average Number of Tokens per Sentence")
plt.ylabel("Average Token Count")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()

