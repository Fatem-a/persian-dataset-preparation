
import json
import re
import random
import csv
import os

from hazm import sent_tokenize


# ==================================================
# 1. File paths
# ==================================================

telegram_json_path = r"data/telegram/result.json"

text_files = [
    r"data/github/news1.txt",
    r"data/github/news2.txt"
]

merged_text_path = "marineData.txt"
sentences_path = "marineData_sentences.txt"
clean_sentences_path = "marineData_clean.txt"
wrong_sentences_path = "wrongMarineData.txt"
output_csv_path = "finalMarineData.csv"


# ==================================================
# 2. Read Telegram JSON and extract messages
# ==================================================

with open(telegram_json_path, "r", encoding="utf-8") as file:
    data = json.load(file)


def clean_text(text):

    # If text is a list, convert it to a string
    if isinstance(text, list):
        text = ''.join([
            t if isinstance(t, str) else t.get('text', '')
            for t in text
        ])

    # Normalize Arabic characters
    text = text.replace("ي", "ی")
    text = text.replace("ك", "ک")

    # Remove unwanted characters
    cleaned = re.sub(
        r"[^\u0600-\u06FF\s،؛.؟!]",
        "",
        text
    )

    return cleaned.strip()


clean_texts = []

for msg in data.get("messages", []):

    if msg.get("type") == "message" and "text" in msg:

        cleaned = clean_text(msg["text"])

        if cleaned:
            clean_texts.append(cleaned)


# ==================================================
# 3. Read and merge other text datasets
# ==================================================

for filename in text_files:

    if os.path.exists(filename):

        with open(filename, "r", encoding="utf-8") as file:

            for line in file:

                clean_line = clean_text(line)

                if clean_line:
                    clean_texts.append(clean_line)


# Merge all collected texts
final_text = ' '.join(clean_texts)


with open(merged_text_path, "w", encoding="utf-8") as file:
    file.write(final_text)


print("Text sources merged successfully.")


# ==================================================
# 4. Sentence tokenization
# ==================================================

with open(merged_text_path, "r", encoding="utf-8") as file:
    text = file.read()


sentences = sent_tokenize(text)


with open(sentences_path, "w", encoding="utf-8") as file:

    for sentence in sentences:
        file.write(sentence.strip() + '\n')


print(f"{len(sentences)} sentences extracted.")


# ==================================================
# 5. Remove empty lines
# ==================================================

def remove_empty_lines(input_file, output_file):

    with open(input_file, "r", encoding="utf-8") as file:
        lines = file.readlines()

    cleaned_lines = [
        line for line in lines
        if line.strip()
    ]

    with open(output_file, "w", encoding="utf-8") as file:

        for line in cleaned_lines:
            file.write(line)


remove_empty_lines(
    sentences_path,
    clean_sentences_path
)


# ==================================================
# 6. Generate incorrect sentences
# ==================================================

def corrupt_word(word):

    if len(word) <= 3:
        return word

    methods = ['remove', 'swap', 'replace']
    method = random.choice(methods)

    if method == 'remove':

        idx = random.randint(0, len(word) - 1)

        return word[:idx] + word[idx+1:]

    elif method == 'swap' and len(word) >= 2:

        idx = random.randint(0, len(word) - 2)

        return (
            word[:idx]
            + word[idx+1]
            + word[idx]
            + word[idx+2:]
        )

    elif method == 'replace':

        idx = random.randint(0, len(word) - 1)

        char = random.choice(
            'ابتثجچحخدذرزژسشصضطظعغفقکگلمنوهی'
        )

        return word[:idx] + char + word[idx+1:]

    return word


def create_wrong_sentences(
    input_file,
    output_file,
    error_prob=0.2
):

    with open(input_file, "r", encoding="utf-8") as file:
        sentences = file.readlines()

    corrupted_sentences = []

    for sentence in sentences:

        sentence = sentence.strip()

        if not sentence:
            continue

        words = sentence.split()

        # Select words for corruption based on probability
        corrupted_indices = [
            idx for idx in range(len(words))
            if random.random() < error_prob
        ]

        # If no word was selected, choose one randomly
        if not corrupted_indices and words:
            corrupted_indices = [
                random.randint(0, len(words) - 1)
            ]

        for idx in corrupted_indices:
            words[idx] = corrupt_word(words[idx])

        corrupted_sentence = ' '.join(words)

        corrupted_sentences.append(corrupted_sentence)


    with open(output_file, "w", encoding="utf-8") as file:

        for sentence in corrupted_sentences:
            file.write(sentence + '\n')


create_wrong_sentences(
    clean_sentences_path,
    wrong_sentences_path,
    error_prob=0.2
)


# ==================================================
# 7. Create CSV dataset
# ==================================================

with open(clean_sentences_path, "r", encoding="utf-8") as correct_file:
    correct_sentences = correct_file.readlines()


with open(wrong_sentences_path, "r", encoding="utf-8") as wrong_file:
    wrong_sentences = wrong_file.readlines()


assert len(correct_sentences) == len(wrong_sentences), (
    "The number of correct and incorrect sentences is not equal."
)


with open(
    output_csv_path,
    "w",
    encoding="utf-8-sig",
    newline=""
) as csvfile:

    writer = csv.writer(csvfile)

    writer.writerow([
        'wrong_sentence',
        'correct_sentence'
    ])

    for wrong, correct in zip(
        wrong_sentences,
        correct_sentences
    ):

        writer.writerow([
            wrong.strip(),
            correct.strip()
        ])


print("CSV dataset created successfully.")
print("Total sentence pairs:", len(correct_sentences))
print("Output file:", output_csv_path)
