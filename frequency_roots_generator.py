import json
import string
import xml.etree.ElementTree as ET
from collections import Counter


languages = ['English', 'German', 'Polish', 'Spanish', 'Turkish', 'Ukrainian']


def generate_substrings(s):
    substrings = []
    n = len(s)
    for i in range(n):
        for j in range(i + 1, n + 1):
            substrings.append(s[i:j])
    return substrings


def replace_punctuation_with_spaces(text):
    translator = str.maketrans('', '', string.punctuation)
    cleaned_text = text.translate(translator).replace('\n', ' ')
    return cleaned_text


def create_bible_txt(language):
    root = ET.fromstring(open(f'Bibles/XML/{language}.xml', encoding="utf-8").read())
    with open(f'Bibles/TXT/{language}.txt', 'w', encoding='utf-8') as out:
        for n in root.iter('seg'):
            out.write(n.text.strip() + '\n')


def process_bible_text_to_roots(language):
    # Read the contents of the Bible file
    with open(f'Bibles/TXT/{language}.txt', 'r', encoding='utf-8') as file:
        bible = file.read()
        # Replace punctuation with spaces and split into words
        words = replace_punctuation_with_spaces(bible).split(" ")

        res = []
        for word in words:
            res.extend(generate_substrings(word))

        long_list = [char for char in res]
        word_set = set(long_list)

        # Write the substrings to a JSON file
        output_file_path = f'Bibles/Roots/{language}.json'
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            json.dump(list(word_set), output_file, indent=4, ensure_ascii=False)

        print(f'JSON data written to {output_file_path}')

        return res


def calculate_word_frequencies_and_save(language, res):
    word_list = res
    word_counts = Counter(word_list)
    word_counts_dict = dict(sorted(word_counts.items(), key=lambda item: item[1], reverse=True))

    # Write word frequencies to a JSON file
    file_name = f'Bibles/Frequency/{language}_frequency.json'
    with open(file_name, "w", encoding='utf-8') as json_file:
        json.dump(word_counts_dict, json_file, indent=4, ensure_ascii=False)


for language in languages:
    create_bible_txt(language)
    res = process_bible_text_to_roots(language)
    calculate_word_frequencies_and_save(language, res)
