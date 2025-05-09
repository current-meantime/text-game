import json
import os
from time import time
from game.words import level_words

# run from terminal: python -m game.testing.trainer

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_STATS_FILE = os.path.join(BASE_DIR, "test_word_stats.json")
CUSTOM_WORDS_FILE = os.path.join(BASE_DIR, "custom_words.json")

def load_custom_words(path=CUSTOM_WORDS_FILE):
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            # Load JSON array instead of reading lines
            return json.load(f)
    except json.JSONDecodeError:
        return []

def save_test_stats(stats):
    with open(TEST_STATS_FILE, "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=4, ensure_ascii=False)

def load_test_stats():
    if not os.path.exists(TEST_STATS_FILE):
        return {}
    try:
        with open(TEST_STATS_FILE, "r", encoding="utf-8") as f:
            content = f.read()
            return json.loads(content) if content else {}
    except json.JSONDecodeError:
        return {}

def update_word_stats(stats, word, time_taken, error=False):
    entry = stats.setdefault(word, {
        "encounters": 0,
        "incorrectly_typed_count": 0,
        "best_time": time_taken,
        "average_time": time_taken,
        "times": []
    })

    entry["encounters"] += 1
    if error:
        entry["incorrectly_typed_count"] += 1
    entry["times"].append(time_taken)
    entry["best_time"] = min(entry["best_time"], time_taken)
    entry["average_time"] = sum(entry["times"]) / len(entry["times"])

def trainer(words_source):
    stats = load_test_stats()
    for word in words_source:
        print(f"\nPrzepisz słowo: {word}")
        start = time()
        attempt = input(">>> ").strip().lower()
        duration = time() - start
        if attempt == word.lower(): # case insensitive
            print(f"Poprawnie! Czas: {duration:.2f}s")
            update_word_stats(stats, word, duration)
        else:
            update_word_stats(stats, word, duration, True)
            print("Błąd. Noted.")

    save_test_stats(stats)


if __name__ == "__main__":
    mode = input("Wybierz tryb (1=LVL1-3, 2=custom): ").strip()
    if mode == "1":
        words = sum(level_words, [])
    elif mode == "2":
        words = load_custom_words()
    else:
        print("Nieprawidłowy wybór.")
        exit()

    trainer(words)
