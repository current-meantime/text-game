from start import Display, PlayerName
from settings import Settings
from rankings import RankingManager
from end import Finish
from player import Player
from combat import Combat
from words import WordProvider
from rankings import WordStatsManager
from time import time
from typing import Optional

class GameSession:
    def __init__(self, settings: Settings, display: Display, finish: Finish):
        self.settings = settings
        self.config = settings.load_settings()
        self.display = display
        self.finish = finish
        self.player_name: Optional[str] = None
        self.player: Optional[Player] = None
        self.ranking: Optional[RankingManager] = None
        self.start_time: float = 0
        
        # komponenety związane z walką
        self.word_provider = WordProvider()
        self.word_stats = WordStatsManager()
        self.combat = Combat(self.word_provider, self.word_stats)
        
    def setup_game(self, first_round: bool) -> None:
        """Initialize game session."""
        self.display.display_banner()
        self._handle_intro(first_round)
        self._setup_player()
        self._initialize_ranking()
        self.start_time = time() # zaczynamy liczyć czas rozgrywki
        
    def _handle_intro(self, first_round: bool) -> None:
        """Display introduction based on settings."""
        skip_intro = self.config["skip_intro"]
        skip_on_replay = self.config["skip_intro_on_replay"]
        
        if not skip_intro and (first_round or not skip_on_replay):
            self.display.display_introduction()
            
    def _setup_player(self) -> None:
        """Create player instance."""
        self.player_name = PlayerName(self.settings).get_player_name()
        self.player = Player(self.player_name)
        
    def _initialize_ranking(self) -> None:
        """Initialize and update ranking."""
        self.ranking = RankingManager(self.player_name)
        data = self.ranking.load()
        data["games_started"] += 1
        self.ranking.save(data)
        
    def run_combat(self) -> bool:
        """Run combat sequence. Returns True if player survives."""
        for level in range(1, 6): # przykładowo deklarujemy że będzie 5 leveli, do zmiany
            if not self._handle_level(level):
                return False
        return True
        
    def _handle_level(self, level: int) -> bool:
        """Handle single level. Returns True if player survives."""
        next_level = False
        # gracz przejdzie na wyższy level jedynie przy odpowiedniej ilości xp (i jeśli nie jest martwy)
        while not next_level and self.player.is_alive():
            if not self._process_combat_round(level):
                return False
            # przykładowo level up co 100 xp, do zmiany
            next_level = self.player.xp >= level * 100
            
        if self.player.is_alive():
            input("\nPress Enter to continue to the next level...")
        return True
            
    def _process_combat_round(self, level: int) -> bool:
        """Process single combat round. Returns True if player survives."""
        print(f"Your health: {self.player.hp}")
        print(f"Your experience: {self.player.xp}")
        
        word, passed_time = self.combat.fight(level, self.ranking, self.player_name)
        
        if passed_time == 0:
            damage = 20 * level
            self.player.take_damage(damage)
            if not self.player.is_alive():
                print(f"\nYou have been killed by the beast using the word '{word}' on level {level}.")
                return False
        else:
            self._handle_success(level)
        return True
            
    def _handle_success(self, level: int) -> None:
        """Handle successful combat round."""
        gained_xp = 20 * level
        heal_amount = 10 * level
        # TODO: dodać dodatkowe xp za krótki czas walki
        self.player.gain_experience(gained_xp)
        self.player.heal(heal_amount)
        if self.player.xp >= level * 100:
            print("\nYou are going to the next level!")
            
    def finish_game(self) -> bool:
        """Finish game and return whether to play again."""
        if self.player.is_alive():
            print("\n...many adventures happening, bla bla bla...\n")
            
        finish_time = time() - self.start_time
        self.ranking.update_best_gameplay_time(finish_time)
        data = self.ranking.load()
        data["games_finished"] += 1
        self.ranking.save(data)
        
        return self.finish.finish_game(data)

def main():
    settings = Settings()
    display = Display()
    finish = Finish()
    first_round = True
    wanna_play = True
    
    while wanna_play:
        game = GameSession(settings, display, finish)
        game.setup_game(first_round)
        game.run_combat()
        wanna_play = game.finish_game()
        first_round = False

if __name__ == "__main__":
    main()
