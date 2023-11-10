import os
class Game():
    shown_board = [[-15, 0]] + [[0, 0] for i in range(22)] + [[15, 0]]#in player 1's perspective
    players = []

    #0 implies that of player 1 are on top, 1 for player 2 and -1 stands for no pieces there
    point_state  = [1] + [-1] * 22 + [0]
    p1_pieces = [15] + [0 for i in range(23)]
    p2_pieces = [0 for i in range(23)] + [15]
    p_pieces = [p1_pieces, p2_pieces]
    #pieces left for each player to win
    p_cnt = [15, 15]

    @property
    def p1_state(self):
        return [self.point_state] + self.p_pieces + self.p_cnt
    @property
    def p2_state(self):
        return [1 - x if x != -1 else -1 for x in self.point_state][::-1] + \
            [self.p_pieces[1][::-1], self.p_pieces[0][::-1]] + self.p_cnt[::-1]

    def __init__(self, player1, player2, dice1, dice2):
        self.players = [player1, player2]
        self.dice1 = dice1
        self.dice2 = dice2 
        self.update_table()
        self.print_board()

   
    
    def print_board(self):
        """
        Obj ->

        prints out the current distribution of pieces according to the state
        """
        #We clear the screen first
        if os.name == 'posix':  #for unix
            os.system('clear')
        if os.name == 'nt':  #for windows
            os.system('cls')
        print()
        print()
        print()
        table = self.table
        print(" | ".join(table[0]))
        print("-" * 80)
        print(" | ".join(table[1]))
        print(" | ".join(table[2]))
        print("-" * 80)
        print(" | ".join(table[3]))
        print(" | ".join(table[4]))
        print("-" * 80)
        print(" | ".join(table[5]))
        print()
        print()
        return
    
    def play_a_round(self):
        """
        Obj ->

        two players get to play a round
        """
        #player 1 takes his turn
        dice_roll = self.roll()
        while dice_roll and self.p_cnt[0] != 0:
            self.move(1, *self.players[0].play(dice_roll, self.p1_state), dice_roll)
            self.print_board()
        #player 2 takes his turn
        dice_roll = self.roll()
        while dice_roll and self.p_cnt[1] != 0:
            self.move(2, *self.players[1].play(dice_roll, self.p2_state), dice_roll)
            self.print_board()
        
    
    def game(self):
        """
        Obj ->

        starts the game
        """
        #two players roll to decide their order
        d1, d2 = self.dice1(), self.dice2()
        while d1 == d2:
            d1, d2 = self.dice1(), self.dice2()
        if d1  < d2:
            reversed(self.players)

        while not self.winner:
            self.play_a_round()
    



    #-1 for not yet, 0 for player 1 wins the game, 1 for player 2 wins the game
    def winner(self):
        """
        int x int -> bool

        checks if the game has ended
        """
        if self.p_cnt[0] == 0:
            return 0
        if self.p_cnt[1] == 0:
            return 1
        if self.p1_pieces[0] == 1 and self.point_state[0] == 0:
            return 0
        if self.p1_pieces[0] == 1 and self.point_state[0] == 0:
            return 1
        return -1
    
    def move(self, p, act_seq, dice_roll):
        """
        int x list<list<int, list<int>>> x int

        we move the pieces following the sequences of actions provided by the players
        an act seq is as follows: [(starting_point1, roll1),(starting_point2, roll2)]
        """
        index = p - 1
        dir = 1 if p == 1 else -1
        for act in act_seq:
            start, roll = act
            if roll not in dice_roll:
                print("ILLEGAL MOVE, You haven't rolled", roll)
                break
            start -= 1
            end = start + dir * roll
            if not (0 <= start <= 23 and self.point_state[0][start] == index):
                print("ILLEGAL MOVE", start + 1, end + 1)
                print("There's no piece on point",start + 1)
                return
            
            if 0 <= end <= 23:
                #if can place on end:
                if self.point_state[end] == index:
                    self.p_pieces[index][end] += 1
                    self.p_pieces[index][start] -= 1
                    dice_roll.remove(roll)
                    if self.p_pieces[index][start] == 0:
                            self.point_state[start] = -1

                    #shown board changes
                    self.update_table
                    
                elif self.p_pieces[1 - index] == 1: # we pin the opponent
                    self.p_pieces[index][end] += 1
                    self.p_pieces[index][start] -= 1
                    self.point_state[end] = index
                    dice_roll.remove(roll)
                    if self.p_pieces[index][start] == 0:
                            self.point_state[start] = -1

                    #shown board changes
                    self.update_table()
                    

                else:
                    print("ILLEGAL MOVE", start + 1, end + 1)
                    print("You can't place pieces at",end + 1)

            else:
                #if pieces can go home
                if self.check_can_bear_off(p):
                    if end == 24:
                        self.p_cnt[index] -= 1
                        dice_roll.remove(roll)
                        if self.p_pieces[index][start] == 0:
                            self.point_state[start] = -1

                        #shown board changes
                        self.update_table()
                        
                    else:
                        if self.p_pieces[index][23 - roll] != 0:
                            print("ILLEGAL MOVE", start + 1, end + 1)
                            print("You should first move pieces that can exactly go home")
                else:
                    print("ILLEGAL MOVE", start + 1, end + 1)
                    print("index limit exceeded")
        return
        
    def roll(self):
        """
        func x func -> list<int>

        rolls the two dices and returns a list with dice rolls
        duplicates if two rolls are identical
        """
        a, b = self.dice1(), self.dice2()
        result = [a, b]
        if a == b:
            result *= 2
        
        print("You have rolled " + result)

        return result
    
    def check_can_bear_off(self, p):
        """
        Obj -> bool

        returns if a player can bear off
        """
        return sum(self.p_pieces[p - 1][0: 12]) == 0
    

    def update_table(self):
        """
        updates the table shown to  players(in the perspective of player1)
        """
        self.shown_board = []
        for i in range(24):
            a, b, s = self.p1_pieces[i], -self.p2_pieces[i], self.point_state[i]
            if a * s == 0:#a or s == 0
                a, b = b, a
            self.shown_board.append([a, b])
        
        self.table = [
            ["", " 13", " 14", " 15", " 16" , " 17", " 18", " 19", " 20", " 21", " 22", " 23"," 24",""],
            [""] + [format_str(self.shown_board[i][0]) for i in range(12, 24)] + [""],
            [""] + [format_str(self.shown_board[i][1]) for i in range(12, 24)] + ["|",format_str(15 - self.p_cnt[0])],
            [""] + [format_str(self.shown_board[i][1]) for i in range(0, 12)][::-1] + ["|",format_str(15 - self.p_cnt[0])],
            [""] + [format_str(self.shown_board[i][0]) for i in range(0, 12)][::-1] + [""],
            ["", " 12", " 11", " 10", "  9" , "  8", "  7", "  6", "  5", "  4", "  3", "  2","  1",""]
        ]


def format_str(num):
    """
    int -> str

    outputs numbers in a format of "xx"
    """
    t = str(num)
    if len(t) == 3:
        return t
    elif len(t) == 2:
        return " " + t
    else:
        return "  " + t
