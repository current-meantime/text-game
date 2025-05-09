import json
import os
import matplotlib.pyplot as plt

# run from terminal: python -m game.testing.testing

BASE_DIR = os.path.dirname(__file__)  # czyli: text_game/game/testing

WORD_STATS_FILE = os.path.abspath(
    os.path.join(BASE_DIR, "..", "..", "rankings", "word_stats.json")
)

TEST_WORD_STATS_FILE = os.path.join(BASE_DIR, "test_word_stats.json")
file_to_use = TEST_WORD_STATS_FILE # można zmienić na 'TEST_WORD_STATS_FILE' albo WORD_STATS_FILE

def load_word_stats():
    with open(file_to_use, "r", encoding="utf-8") as f:
        return json.load(f)

def show_most_difficult_word_per_length(length):
    data = load_word_stats()
    filtered = {
        word: stats for word, stats in data.items()
        if len(word) == length and stats["encounters"] > 0
    }

    if not filtered:
        print(f"No data for words of length {length}")
        return

    most_difficult = max(filtered.items(), key=lambda x: x[1]["average_time"])
    word, stats = most_difficult
    print(f"Most difficult word of length {length}: '{word}' with avg time {stats['average_time']:.2f}s")

def show_generally_difficult_words(limit=10):
    stats = load_word_stats()
    sorted_words = sorted(
        stats.items(),
        key=lambda x: (-x[1].get("incorrectly_typed_count", 0), x[1].get("average_time", float('inf')))
    )
    print(f"\nTop {limit} najtrudniejszych słów:")
    for word, data in sorted_words[:limit]:
        print(f"{word}: błędy={data['incorrectly_typed_count']}, avg={data['average_time']:.2f}s")


def top_n_words_by_avg_time(n=5, reverse=True):
    data = load_word_stats()
    filtered = [
        (word, stats["average_time"], stats["encounters"])
        for word, stats in data.items()
        if stats["encounters"] > 0  
    ]

    sorted_words = sorted(filtered, key=lambda x: x[1], reverse=reverse)[:n]

    print(f"\nTop {n} {'hardest' if reverse else 'easiest'} words by average time:")
    for word, avg_time, count in sorted_words:
        print(f"  - {word}: {avg_time:.2f}s (based on {count} entries)")

def words_with_fewest_encounters(n=5):
    data = load_word_stats()
    sorted_words = sorted(data.items(), key=lambda x: x[1]["encounters"])[:n]

    print(f"\nTop {n} least tested words:")
    for word, stats in sorted_words:
        print(f"  - {word}: {stats['encounters']} encounters")

def show_all_stats_for_word(word):
    data = load_word_stats()
    stats = data.get(word)
    if not stats:
        print(f"No data for word: {word}")
    else:
        print(f"\nStats for '{word}':")
        print(json.dumps(stats, indent=4, ensure_ascii=False))

def filter_words_by_success_rate(min_rate=0.5):
    with open(file_to_use, "r", encoding="utf-8") as f:
        data = json.load(f)

    for word, stats in data.items():
        if stats["encounters"] == 0:
            continue
        success_rate = (stats["encounters"] - stats["incorrectly_typed_count"]) / stats["encounters"]  # Changed formula
        if success_rate < min_rate:
            print(f"{word}: skuteczność {success_rate:.2%}, avg time: {stats['average_time']:.2f}s")


def plot_avg_time_by_word_length(): #TODO: można dodać coś w stylu ignore outliers
    with open(file_to_use, "r", encoding="utf-8") as f:
        data = json.load(f)

    length_buckets = {}

    for word, stats in data.items():
        if stats["encounters"] == 0:
            continue
        length = len(word)
        avg_time = stats["average_time"]

        if length not in length_buckets:
            length_buckets[length] = []
        length_buckets[length].append(avg_time)

    lengths = sorted(length_buckets.keys())
    avg_times = [sum(times) / len(times) for length, times in sorted(length_buckets.items())]

    plt.figure(figsize=(10, 5))
    plt.bar(lengths, avg_times, color='darkred')
    plt.xlabel("Długość słowa")
    plt.ylabel("Średni czas wpisania (s)")
    plt.title("Średni czas wpisywania słów wg długości")
    plt.grid(axis="y")
    plt.tight_layout()
    plt.show()

def repair_word_stats(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    for word, stats in data.items():
        stats.setdefault("incorrectly_typed_count", 0)
        stats.setdefault("average_time", 0)
        stats.setdefault("passed_time_encounters", 0)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# Użycie:
# repair_word_stats(WORD_STATS_FILE)


# Przykładowe wywołania:
if __name__ == "__main__":
    repair_word_stats(file_to_use)
    show_most_difficult_word_per_length(4)
    show_generally_difficult_words()
    top_n_words_by_avg_time(5)
    top_n_words_by_avg_time(5, reverse=False)
    words_with_fewest_encounters()
    filter_words_by_success_rate()
    show_all_stats_for_word("atak")
    plot_avg_time_by_word_length()
