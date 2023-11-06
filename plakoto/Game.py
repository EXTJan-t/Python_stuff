class Game():
    point_state = [[0, 0] for i in range(24)]
    point_state[0] = [15, 0]
    point_state[23] = [15, 0]
    p1_state = [0 for i in range(24)]
    p2_state =  [0 for i in range(24)]
    p1_cnt = 15
    p2_cnt = 15

    def __init__(self, player1, player2, dice1, dice2):
        self.player1 = player1
        self.player2 = player2
        self.dice1 = dice1
        self.dice2 = dice2

    
    def print_board(self):
        """
        Obj ->

        prints out the current distribution of pieces according to the state
        """
        table = [
            ["", "13", "14", "15", "16" , "17", "18", "19", "20", "21", "22", "23","24",""],
            [""] + [self.format_str(self.point_state[i][0]) for i in range(12, 24)] + [""],
            [""] + [self.format_str(self.point_state[i][1]) for i in range(12, 24)] + [""],
            [""] + [self.format_str(self.point_state[i][1]) for i in range(0, 12)][::-1] + [""],
            [""] + [self.format_str(self.point_state[i][0]) for i in range(0, 12)][::-1] + [""],
            ["", "12", "11", "10", " 9" , " 8", " 7", " 6", " 5", " 4", " 3", " 2"," 1",""]
        ]
        print(" | ".join(table[0]))
        print("-" * 64)
        print(" | ".join(table[1]))
        print(" | ".join(table[2]))
        print("-" * 64)
        print(" | ".join(table[3]))
        print(" | ".join(table[4]))
        print("-" * 64)
        print(" | ".join(table[5]))
        return
    
    def play_a_round(self):
        """
        Obj ->

        two players get to play a round
        """
        #player 1 takes his turn
        dice_roll = self.roll()
        while dice_roll:
            self.move(1, *self.player1.play(dice_roll, self.state), dice_roll)
            self.print_board()
        #player 2 takes his turn
        dice_roll = self.roll()
        while dice_roll:
            self.move(2, *self.player2.play(dice_roll, self.state), dice_roll)
            self.print_board()
        
    
    def game(self):
        """
        Obj ->

        starts the game
        """
        d1 = self.dice1()
        d2 = self.dice2()
        if d1 < d2:
            self.player1, self.player2 = self.player2, self.player1
        self.player2.tag = 2
        while not self.check_game_end:
            self.play_a_round()
    




    def check_game_end(self):
        """
        int x int -> bool

        checks if the game has ended
        """
        return self.p1_cnt == 0 or self.p2_cnt == 0
    
    def move(self, p, a, step, dice_roll):
        """
        int x int x int

        player p moves a piece on point a, (step) steps
        """
        cur = self.p1_state
        if p == 2:
            cur = self.p2_state
        a = a - 1
        b = a + step
        assert 0 <= a <= 23 and cur[a] > 0, "There's no pieces at point " + str(a + 1)
        if  0  <= b <= 23 and self.table[b] == 0 or self.table[b] == p:
            cur[b] += 1 
            cur[a] -= 1
            dice_roll.pop()
        elif p in self.check_can_bear_off():
            if b == 23:
                cur[b] -= 1
                self.p1_cnt -= 1
                dice_roll.pop()
            elif b > 23:
                x
            return
    def roll(self):
        """
        func x func -> list<int>

        rolls the two dices and returns a list with dice rolls
        duplicates if two rolls are identical
        """
        a = self.dice1()
        b = self.dice2()
        result = [a, b]
        if a == b:
            result *= 2
        return result
    
    def check_can_bear_off(self):
        """
        Obj -> list<int>

        returns a list of players that can bear off
        """
        ans = []
        if sum(self.p1_state[0: 17]) == 0:
            ans += [1]
        else:
            ans += [-1]
        
        return ans

    def format_str(self, num):
        """
        int -> str

        outputs numbers in a format of "xx"
        """
        if num >= 10:
            return str(num)
        else:
            return " " + str(num)
