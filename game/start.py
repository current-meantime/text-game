from time import sleep
from colorama import init, Fore, Style

class Display:
    def __init__(self):
        init() # to init jest z colorama

    def display_banner(self):
        """Show off how cool the game is. :3"""
        print(Fore.MAGENTA + "\n" + r"""
     __      __                .___  __      __            .__       .___    _____       .___                    __                         
    /  \    /  \___________  __| _/ /  \    /  \___________|  |    __| _/   /  _  \    __| _/__  __ ____   _____/  |_ __ _________   ____  
    \   \/\/   /  _ \_  __ \/ __ |  \   \/\/   /  _ \_  __ \  |   / __ |   /  /_\  \  / __ |\  \/ // __ \ /    \   __\  |  \_  __ \_/ __ \ 
     \        (  <_> )  | \/ /_/ |   \        (  <_> )  | \/  |__/ /_/ |  /    |    \/ /_/ | \   /\  ___/|   |  \  | |  |  /|  | \/\  ___/ 
      \__/\  / \____/|__|  \____ |    \__/\  / \____/|__|  |____/\____ |  \____|__  /\____ |  \_/  \___  >___|  /__| |____/ |__|    \___  >
           \/                   \/         \/                         \/          \/      \/           \/     \/                        \/ 
        """ + Style.RESET_ALL)
        return "Word World Adventure"

    def display_introduction(self):
        """Narratively explain the main goal of the game to the player."""
        message = [
            "You know who you are - you are the greatest knight of the Word-World kingdom!",
            "Your king has just told you that great danger comes upon it - the evil Word-Eater wants to destroy it.",
            "His armies are coming. There's no time to waste.",
            "In order to protect your people, you must defeat his beasts and the Word-Eater himself.",
            "You will have to prove your word-fighting mastery."
        ]

        for sentence in message:
            sleep(1.5)
            print(sentence.center(134) + "\n")
            sleep(3)


class PlayerName:
    def __init__(self, settings):
        self.settings = settings
        self.config = self.settings.load_settings()
        self.registered_players = self.config.get("registered_players", [])

    def get_player_name(self):
        """Get the player's name, either by selecting from existing players or entering a new one."""
        print("What shall we call you?")

        if not self.registered_players:
            return self.prompt_new_player_name("I am: ")

        self.display_registered_players()

        while True:
            answer = input("I am: ").strip()
            existing = self.find_existing_player(answer)

            if existing:
                print(f"Welcome back!")
                return self.finalize_player(existing)
            elif answer.lower() == "someone else" or answer == str(len(self.registered_players) + 1):
                return self.prompt_new_player_name()
            else:
                print("Enter a valid existing name or a number representing the name.\n")

    def display_registered_players(self):
        padding = " " * 5
        for idx, name in enumerate(self.registered_players, start=1):
            print(f"{padding}{idx}. {name}")
        print(f"{padding}{len(self.registered_players) + 1}. someone else\n")
        sleep(1.3)

    def prompt_new_player_name(self, msg="What name shall we use? "):
        """Prompt the user for a new player name while validating the input."""
        while True:
            new_name = input(msg).strip()
            if new_name.isdigit():
                print(f"'{new_name}'? A great knight like you should have some letters in their name.")
            elif not new_name:
                print("Please enter a name.")
            else:
                existing = self.find_existing_player(new_name)
                if existing:
                    result = self.handle_existing_name(existing)
                    if result:
                        return result
                    else:
                        continue  # <- wraca do pytania o imię
                else:
                    return self.finalize_player(new_name)

    def handle_existing_name(self, name):
        """Handle the case when the player enters a name that already exists."""
        not_intentional = input(f"A knight of the name '{name}' already exists.\nIf it is you, press Enter. If not, press anything else. ")
        if not not_intentional:
            print("I hope it really is you - the time is nigh!")
            return self.finalize_player(name)
        return False

    def finalize_player(self, name):
        """Save player name to the settings and let them finally move on to gameplay."""
        if name not in self.registered_players:
            self.registered_players.append(name)
            # add the new player to the list of registered players in settings
            self.config["registered_players"] = self.registered_players
            self.settings.save_settings(self.config)
        print(f"\nThe fate of the Word-World kingdom is in your hands, {name}.")
        input("\nPress Enter to begin your journey.\n")
        return name

    def find_existing_player(self, answer):
        """Finds out if the player is already registered."""
        if answer.isdigit():
            index = int(answer)
            if 1 <= index <= len(self.registered_players):
                return self.registered_players[index - 1]
        else:
            for name in self.registered_players:
                if name.lower() == answer.lower():
                    return name
        return None
