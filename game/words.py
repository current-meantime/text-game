from random import randrange
from string import ascii_lowercase
import requests
from settings import Settings

# ofc to wszystko jest do zmiany albo dostosowania
LVL1_WORDS = [
    "cios",
    "atak",
    "unik",
    "strzał",
    "pocisk",
    "skok"
]
LVL2_WORDS = [
    "kołczan",
    "pancerz",
    "obrażenia",
    "rycerze",
    "strzelcy",
    "łucznicy",
]

LVL3_WORDS = [
    "przestrzelony",
    "broczący krwią",
    "ciężkozbrojny rycerz",
    "zabójcza strzała",
    "znani uciekinierzy",
    "niezłomny obrońca"
]

level_words = [LVL1_WORDS, LVL2_WORDS, LVL3_WORDS]

class WordProvider:
    def __init__(self):
        self.settings = Settings()
        self.config = self.settings.load_settings()
        self.is_online = self.config.get("mode") == "online"

    def get_word_from_api(self, length):
        if not self.is_online:
            return None
        # randomowe słowo z API
        url = f"https://random-word-api.herokuapp.com/word?length={length}"
        try:
            response = requests.get(url, timeout=3)  # 3 second timeout
            if response.status_code == 200:
                words = response.json()
                if words and len(words) > 0:
                    return words[0]
        except (requests.RequestException, ValueError):
            print("Error fetching a word from API. Falling back to default words.")
        return None
    
    def nonsensical_word(self, length):
        nonsensical_word = ''.join([ascii_lowercase[randrange(0, len(ascii_lowercase))] for _ in range(length)])
        return nonsensical_word

    def provide_word(self, level):
        # obliczamy długość słowa na podstawie poziomu
        level_index = level - 1 # poziomy zaczynają się od 1, więc odejmujemy 1
        word_length = level * 2 if level_index >= len(level_words) else level + 3
        
        # bierzemy słowo z API jeśli mode jest online
        if self.is_online:
            api_word = self.get_word_from_api(word_length)
            if api_word:
                return api_word
        
        # jeśli mode to offline albo API zawiedzie, to bierzemy słowo z listy
        if level >= len(level_words):
            return self. nonsensical_word(word_length)
        else:
            lvl_words = level_words[level]
            return lvl_words[randrange(0, len(lvl_words))]