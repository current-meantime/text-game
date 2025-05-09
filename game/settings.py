import json # przy obsłudze json dawać wszędzie ensure_ascii=False, żeby nie było np. ""obra\u017cenia"" zamiast "obrażenia"

SETTINGS_FILE = "settings.json"

DEFAULT_SETTINGS_TEMPLATE = {
    "mode": "offline",
    "skip_intro": False,
    "skip_intro_on_replay": True,
    "save_records": True,
    "difficulty": "normal",
    "registered_players": [
        "dev1",
        "dev2"
    ]
}

class Settings:
    def __init__(self):
        self.SETTINGS_FILE = SETTINGS_FILE
        self.TEMPLATE = DEFAULT_SETTINGS_TEMPLATE.copy()

    def create_settings_file(self):
        """Create a settings file with default values."""
        try:
            with open(self.SETTINGS_FILE, "w") as file:
                json.dump(self.TEMPLATE, file, indent=4, ensure_ascii=False)
            print("Settings file created successfully!")
        except Exception as e:
            print(f"Error creating settings file: {e}")
        return self.TEMPLATE

    def load_settings(self):
        """Load data from JSON file."""
        try:
            with open(self.SETTINGS_FILE, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            # if file does not exist, create a new one with default settings
            print("Settings file not found. Creating a new one with the following content:")
            print(self.TEMPLATE)
            self.create_settings_file()
            return self.TEMPLATE
        except json.JSONDecodeError:
            # if file is corrupted, create a new one with default settings
            print("Settings file is corrupted. Creating a new one with the following content:")
            print(self.TEMPLATE)
            self.create_settings_file()
            return self.TEMPLATE

    def save_settings(self, config):
        """Save configuration to JSON file."""
        try:
            with open(self.SETTINGS_FILE, "w") as file:
                json.dump(config, file, indent=4, ensure_ascii=False)
            print("Settings saved successfully!")
        except FileNotFoundError:
            print("Settings file not found. Creating a new one.")
            self.create_settings_file()
        except Exception as e:
            print(f"Error saving settings: {e}")