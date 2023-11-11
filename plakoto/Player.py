import startegies
class Player():
    def __init__(self, strategy):
        self.stategy = strategy
        self.name = ""


    def play(self, dice_roll, state):
        """
        list<int> x list<list<int>> -> tuple
        
        the player plays following his strategy,
        and returns a move starting from point a and taking step steps
        """
        return self.stategy(dice_roll, state)


class Human_player(Player):
    strategy = startegies.strategy_input
    def __init__(self, temp):
        super().__init__(Human_player.strategy)
        if temp == 1:
            t = "first"
        elif temp == 2:
            t = "second"
        self.name = input("What would the " + t +" player like to be called?\n")

class Naive_computer_player():
    strategy = startegies.strategy_random
    def __init__(self, temp):
        super().__init__(Naive_computer_player.strategy)
        self.name = temp