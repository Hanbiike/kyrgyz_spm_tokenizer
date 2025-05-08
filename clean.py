import os
import re

# ✅ Настройки
input_folder = "text/"                      # Папка с входными файлами
output_file = "kyrgyz_clean_sentences.txt"
to_lower = True                         # ← переключатель: True = приводить к нижнему регистру

# 📝 Список файлов
file_list = [
    "kir_community_2017-sentences.txt",
    "kir_newscrawl_2011_300K-sentences.txt",
    "kir_newscrawl_2016_1M-sentences.txt",
    "kir_wikipedia_2010_10K-sentences.txt",
    "kir_wikipedia_2016_300K-sentences.txt",
    "kir_wikipedia_2021_300K-sentences.txt"
]

# 🔍 Регулярки
only_cyrillic = re.compile(r'^[\u0400-\u04FF0-9\s.,:;!?«»“”"\'\-–—()№…]+$', re.UNICODE)
must_contain_cyrillic = re.compile(r'[А-Яа-яЁё]')

# 📊 Статистика
counters = {
    "total": 0,
    "valid": 0,
    "starts_with_bang": 0,
    "contains_chinese_html": 0,
    "contains_latin": 0,
    "no_cyrillic": 0,
    "invalid_chars": 0
}

all_sentences = set()

for file_name in file_list:
    path = os.path.join(input_folder, file_name)
    if not os.path.isfile(path):
        continue

    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            counters["total"] += 1
            parts = line.strip().split("\t")
            if len(parts) != 2:
                continue
            sentence = parts[1].strip()

            # 🔽 Приведение к нижнему регистру, если включено
            if to_lower:
                sentence = sentence.lower()

            # 🧹 Фильтрация
            if sentence.startswith("!"):
                counters["starts_with_bang"] += 1
                continue
            if re.search(r'[\u4E00-\u9FFF<>]', sentence):  # китайские или html
                counters["contains_chinese_html"] += 1
                continue
            if re.search(r'[A-Za-z]', sentence):  # латиница
                counters["contains_latin"] += 1
                continue
            if not must_contain_cyrillic.search(sentence):
                counters["no_cyrillic"] += 1
                continue
            if not only_cyrillic.match(sentence):
                counters["invalid_chars"] += 1
                continue

            all_sentences.add(sentence)
            counters["valid"] += 1

# 💾 Сохраняем очищенные предложения
with open(output_file, 'w', encoding='utf-8') as out:
    for sent in sorted(all_sentences):
        out.write(sent + '\n')

# 📈 Итоговая статистика
print("📊 Статистика очистки:")
print(f"• Всего строк обработано:     {counters['total']}")
print(f"• Оставлено валидных строк:   {counters['valid']}")
print(f"• Удалено (начинается с !):   {counters['starts_with_bang']}")
print(f"• Удалено (китайский/HTML):   {counters['contains_chinese_html']}")
print(f"• Удалено (латиница):         {counters['contains_latin']}")
print(f"• Удалено (нет кириллицы):    {counters['no_cyrillic']}")
print(f"• Удалено (плохие символы):   {counters['invalid_chars']}")
print(f"✅ Итоговый файл:              {output_file}")
print(f"🔠 Приведение к нижнему регистру: {'ВКЛЮЧЕНО' if to_lower else 'ВЫКЛЮЧЕНО'}")
