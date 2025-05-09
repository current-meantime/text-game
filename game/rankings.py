import json
import os

class BaseJsonManager:
    def __init__(self, filepath, default_data=None):
        self.filepath = filepath
        self.default_data = default_data or {}
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
        if not os.path.exists(self.filepath):
            self.save(self.default_data)

    def load(self):
        with open(self.filepath, "r", encoding="utf-8") as f:
            return json.load(f)

    def save(self, data):
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)


PLAYER_RANKING_TEMPLATE = {
    "games_started": 0,
    "games_finished": 0,
    "fastest_completion_time": None,
    "total_enemies_defeated": 0,
    "total_defeats_of_player": 0,
    "best_words_stats": {}
}

class RankingManager(BaseJsonManager):
    def __init__(self, player_name):
        filepath = os.path.join("rankings", f"{player_name}.json")
        super().__init__(filepath, PLAYER_RANKING_TEMPLATE)
        self.player_name = player_name

    def add_enemy_defeat(self):
        data = self.load()
        data["total_enemies_defeated"] += 1
        self.save(data)

    def add_player_defeat(self):
        data = self.load()
        data["total_defeats_of_player"] += 1
        self.save(data)

    def update_best_gameplay_time(self, time):
        data = self.load()
        best = data["fastest_completion_time"]
        if best is None or time < best:
            print(f"Congrats! New best finish time of {time}s.")
            data["fastest_completion_time"] = time
            self.save(data)

    def update_word_time(self, word, time_seconds):
        data = self.load()
        best = data["best_words_stats"].get(word)
        if best is None or time_seconds < best:
            print(f"Congrats! New best score for word '{word}'.")
            data["best_words_stats"][word] = time_seconds
            self.save(data)

class WordStatsManager(BaseJsonManager):
    def __init__(self):
        super().__init__(os.path.join("rankings", "word_stats.json"), {})

    def update_word(self, word, time_seconds, player_name, time_passed=False):
        data = self.load()
        word_data = data.get(word, {
            "encounters": 0,
            "given_time_ended": 0,
            "best_time": time_seconds,
            "average_time": time_seconds,
            "player_times": {}
        })

        times = word_data["player_times"].get(player_name, [])
        times.append(time_seconds)
        word_data["player_times"][player_name] = times

        word_data["encounters"] += 1
        word_data["best_time"] = min(word_data["best_time"], time_seconds)

        all_times = [t for pl_times in word_data["player_times"].values() for t in pl_times]
        word_data["average_time"] = sum(all_times) / len(all_times)

        if time_passed:
            word_data["given_time_ended"] += 1

        data[word] = word_data
        self.save(data)



'''import json # przy obsłudze json dawać wszędzie ensure_ascii=False, żeby nie było np. ""obra\u017cenia"" zamiast "obrażenia"
import os

PLAYER_RANKING_TEMPLATE = {
    "games_started": 0,
    "games_finished": 0,
    "fastest_completion_time": None,
    "total_enemies_defeated": 0,
    "total_defeats_of_player": 0,
    "best_words_stats": {}  # słowo: czas w sekundach
}

WORD_RANKING_TEMPLATE = {
    "word": {
        "encounters": 0,
        "best_time": 0,
        "avarage_time": 0,
        "player_times": {
            "player1": [
                1.34,
                2.21,
                1.15
            ],
            "player2": [
                4.23,
                2.99
            ]
        }
    }
}

RANKINGS_DIR = "rankings"


class RankingManager:
    def __init__(self, player_name):
        self.player_name = player_name
        self.file_path = os.path.join(RANKINGS_DIR, f"{player_name}.json")
        self._ensure_player_file_exists() # tworzenie pliku z rankingiem/statami dla każdego zarejestrowanego gracza

    def _ensure_player_file_exists(self):
        os.makedirs(RANKINGS_DIR, exist_ok=True)
        if not os.path.exists(self.file_path):
            self.save(PLAYER_RANKING_TEMPLATE)

    def load(self):
        with open(self.file_path, "r") as f:
            return json.load(f)

    def save(self, ranking_data):
        with open(self.file_path, "w") as f:
            json.dump(ranking_data, f, indent=4, ensure_ascii=False)

    def update_stat(self, key, value):
        data = self.load()
        data[key] = value
        self.save(data)

    def add_enemy_defeat(self):
        data = self.load()
        data["total_enemies_defeated"] += 1
        self.save(data)

    def add_player_defeat(self):
        data = self.load()
        data["total_defeats_of_player"] += 1
        self.save(data)

    def update_word_time(self, word, time_seconds):
        data = self.load()
        current_best = data["best_words_stats"].get(word)
        if current_best is None or time_seconds < current_best:
            data["best_words_stats"][word] = time_seconds
            print(f"updating {word}")
            self.save(data)

    def update_word_stats(self, word, time_seconds):

        import json
        import os

        class BaseJsonManager:
            def __init__(self, filepath, default_data=None):
                self.filepath = filepath
                self.default_data = default_data or {}
                self._ensure_file_exists()

            def _ensure_file_exists(self):
                os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
                if not os.path.exists(self.filepath):
                    self.save(self.default_data)

            def load(self):
                with open(self.filepath, "r", encoding="utf-8") as f:
                    return json.load(f)

            def save(self, data):
                with open(self.filepath, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=4, ensure_ascii=False)

'''
