import sentencepiece as spm

# Загрузка пользовательских символов
with open("user_defined_symbols.txt", "r", encoding="utf-8") as f:
    symbols = [line.strip() for line in f if line.strip()]

# Параметры модели
lang = "kyrgyz"
model_type = "unigram" # "bpe", "unigram", "bpe", "char", "word"
vocab_size = 51200 # Размер словаря (количество токенов)
model_prefix = f"models/{lang}_{model_type}_{vocab_size}"

print(f"Количество пользовательских символов: {len(symbols)}")
print(f"Пользовательские символы: {symbols}")
print(f"Итоговый префикс: {model_prefix}")

# Тренировка
spm.SentencePieceTrainer.train(
    input="kyrgyz_clean_sentences.txt",
    model_prefix=model_prefix,
    vocab_size=vocab_size,
    model_type=model_type,
    character_coverage=1.0,
    pad_id=0,
    unk_id=1,
    bos_id=2,
    eos_id=3,
    user_defined_symbols=symbols
)
