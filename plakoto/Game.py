import os
class Game():
    point_state = [[-15, 0]] + [[0, 0] for i in range(22)] + [[15, 0]]
    players = []
    p1_state = [15] + [0 for i in range(23)]
    p2_state = [15] + [0 for i in range(23)]
    p_state = [p1_state, p2_state]
    #pieces left for each player to win
    p_cnt = [15, 15]

    def __init__(self, player1, player2, dice1, dice2):
        self.players = [player1, player2]
        self.dice1 = dice1
        self.dice2 = dice2 
        self.update_table()

    
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
        while dice_roll:
            self.move(1, *self.players[0].play(dice_roll, self.state), dice_roll)
            self.print_board()
        #player 2 takes his turn
        dice_roll = self.roll()
        while dice_roll:
            self.move(2, *self.players[1].play(dice_roll, self.state), dice_roll)
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

        while not self.check_game_end:
            self.play_a_round()
    




    def check_game_end(self):
        """
        int x int -> bool

        checks if the game has ended
        """
        return 0 in self.p_cnt
    
    def move(self, p, act_seq, dice_roll):
        """
        int x list<list<int, list<int>>> x int

        we move the pieces following the sequences of actions provided by the players
        an act seq is as follows: [(starting_point1, roll1),(starting_point2, roll2)]
        """
        cur = self.p_state[p - 1]
        dir = 1 if p == 1 else -1
        for act in act_seq:
            start, roll = act
            start -= 1
            end = start + dir * roll
            if not (0 <= start <= 23 and cur[start] > 0):
                print("ILLEGAL MOVE")
                print("There's no piece on point " + str(start + 1))
                return
            
            if 0 <= end <= 23:
                if can place on end:
                    pass 
                else:
                    pass
            else:
                if can bear off:
                    pass
                else:
                    pass
        
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
    
    def check_can_bear_off(self):
        """
        Obj -> list<int>

        returns a list of players that can bear off
        """
        ans = []
        if sum(self.p_state[0][0: 12]) == 0:
            ans += [1]
        if sum(self.p2_state[1][0: 12]) == 0:
            ans += [2]
        
        return ans

    def update_table(self):
        self.table = [
            ["", " 13", " 14", " 15", " 16" , " 17", " 18", " 19", " 20", " 21", " 22", " 23"," 24",""],
            [""] + [self.format_str(self.point_state[i][0]) for i in range(12, 24)] + [""],
            [""] + [self.format_str(self.point_state[i][1]) for i in range(12, 24)] + ["|",self.format_str(15 - self.p_cnt[0])],
            [""] + [self.format_str(self.point_state[i][1]) for i in range(0, 12)][::-1] + ["|",self.format_str(15 - self.p_cnt[0])],
            [""] + [self.format_str(self.point_state[i][0]) for i in range(0, 12)][::-1] + [""],
            ["", " 12", " 11", " 10", "  9" , "  8", "  7", "  6", "  5", "  4", "  3", "  2","  1",""]
        ]


    def format_str(self, num):
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
