import sentencepiece as spm
import os

# 📦 Загрузка модели
sp = spm.SentencePieceProcessor()
sp.load(os.path.join("models", "kyrgyz_bpe_4000.model"))

# 📝 Пример текста
text = "Салам, дүйнө!"

# 🔹 Токенизация — в строки
tokens_str = sp.encode(text, out_type=str)
print("Токены (строки):", tokens_str)

# 🔸 Токенизация — в числовые ID
tokens_id = sp.encode(text, out_type=int)
print("Токены (ID):", tokens_id)

# 🔄 Обратное преобразование
reconstructed_text = sp.decode(tokens_str)
print("Восстановленный текст:", reconstructed_text)
