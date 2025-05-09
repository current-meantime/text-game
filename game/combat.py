from time import time
from typing import Tuple, Optional
from words import WordProvider
from rankings import WordStatsManager

class Combat:
    """Handles combat mechanics including word typing challenges."""
    
    def __init__(self, word_provider: WordProvider, word_stats: WordStatsManager):
        """Initialize Combat instance.
        
        Args:
            word_provider: Provider for combat words
            word_stats: Manager for word statistics
        """
        self.word_provider = word_provider
        self.word_stats = word_stats
        
    def _calculate_time_limit(self, level: int) -> float:
        """Calculate time limit based on level."""
        # TODO: test and optimize params
        return (level * 12) - (5.7 * level)
        
    def _display_combat_start(self, level: int, enemy: str, time_limit: float, word: str) -> None:
        """Display initial combat information."""
        print(f"\nYou're on game level {level}.")
        print(f"You've met a level {level} beast called '{enemy}'")
        print("In order to defeat him, you'll need to type in a given word.\n")
        print(f"The time you'll have is {time_limit:.1f}s.")
        input(f"\nPress Enter when you're ready.")
        print(f"\nGiven word:\t{word}")
        
    def _handle_defeat(self, word: str, ranking, player_name: str) -> Tuple[str, float]:
        """Handle player defeat scenario."""
        print("\nYou took too long, time passed.\n")
        ranking.add_player_defeat()
        self.word_stats.update_word(word, 0, player_name, True)  # 0 = defeat
        return word, 0
        
    def _handle_victory(self, word: str, passed_time: float, ranking, player_name: str) -> None:
        """Handle player victory scenario."""
        print(f"You managed to fight him in {passed_time:.2f}s!")
        ranking.add_enemy_defeat()
        ranking.update_word_time(word, passed_time)
        self.word_stats.update_word(word, passed_time, player_name)
        
    def fight(self, level: int, ranking, player_name: str, enemy: str = "Default") -> Tuple[str, float]:
        """
        Execute combat sequence.
        
        Args:
            level: Current game level
            ranking: Player ranking manager
            player_name: Name of the current player
            enemy: Name of the enemy (default: "Default")
            
        Returns:
            Tuple containing (word, time_taken)
            If time_taken is 0, player lost
        """
        word = self.word_provider.provide_word(level)
        time_limit = self._calculate_time_limit(level)
        self._display_combat_start(level, enemy, time_limit, word)
        
        start_time = time()
        
        while True:
            answer = input("Your word: \t").strip().lower()
            passed_time = time() - start_time
            
            if passed_time > time_limit:
                return self._handle_defeat(word, ranking, player_name)
                
            if answer == word:
                self._handle_victory(word, passed_time, ranking, player_name)
                return word, passed_time
