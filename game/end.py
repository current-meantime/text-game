import json

class Finish:
    def __init__(self):
        pass
    def finish_game(self, stats):
        print("\nTHE END\n")
        self.display_stats(stats)

        answer = input("Play again? (y/n) ").strip().lower()
        no = ["n", "no", "2", "0"] # zero bc in binary 0 is off, so 0 == no
        yes = ["y", "yes", "1"]
        if answer in no:
            return False
        if answer in yes:
            return True
        else:
            print("Can't type? You need to practise then. I'll take that as a yes.")
            return True

    def display_stats(self, stats):
        print("You've had so many adventures and you finished the game.\nThese are you current stats:")
        print(json.dumps(stats, indent=4, ensure_ascii=False))
