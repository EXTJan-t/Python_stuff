class Player():
    #tag implies the order of play of the player, 1 for player 1 and 2 for player 2
    tag = 1
    def __init__(self, strategy):
        self.stategy = strategy

    def play(self, dice_roll, state):
        """
        list<int> x list<list<int>> -> tuple
        
        the player plays following his strategy,
        and returns a move starting from point a and taking step steps
        """
        return self.stategy(self, dice_roll, state)

