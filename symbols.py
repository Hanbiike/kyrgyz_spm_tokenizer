from collections import Counter
import re
from pathlib import Path

# Проверим, существует ли файл корпуса
corpus_path = "kyrgyz_clean_sentences.txt"
output_path = "user_defined_symbols.txt"

# Повторим анализ, если файл существует
if Path(corpus_path).exists():
    char_counter = Counter()
    with open(corpus_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            for char in line:
                if not char.isalnum() and not char.isspace():
                    char_counter[char] += 1

    # Оставим только символы, которые встретились хотя бы 10 раз (можно изменить порог)  if count >= 10
    filtered = [char for char, count in char_counter.items()]

    # Сохраняем в файл
    with open(output_path, "w", encoding="utf-8") as out:
        for symbol in filtered:
            out.write(symbol + "\n")

    result = (len(filtered), output_path)
else:
    result = ("Файл не найден", corpus_path)

print(result)

