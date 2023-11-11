import os
from time import sleep
import helpers
class Game():
    clear_board = True
    stop_inbetween = False
    table_rotate = False
    round = 0
    #shown_board = [[-15, 0]] + [[0, 0] for i in range(22)] + [[15, 0]]#in player 1's perspective
    players = []

    #0 implies that of player 1 are on top, 1 for player 2 and -1 stands for no pieces there
    point_state  = [1] + [-1] * 22 + [0]
    p1_pieces = [0 for i in range(23)] + [15]
    p2_pieces = [15] + [0 for i in range(23)]
    p_pieces = [p1_pieces, p2_pieces]
    #pieces left for each player to win
    p_cnt = [15, 15]

    @property
    def p1_state(self):
        return [self.point_state] + self.p_pieces + [self.p_cnt]
    @property
    def p2_state(self):
        return [[1 - x if x != -1 else -1 for x in self.point_state][::-1]] + \
            [self.p_pieces[1][::-1], self.p_pieces[0][::-1]] + [self.p_cnt[::-1]]

    def __init__(self, player1, player2, dice1, dice2):
        self.players = [player1, player2]
        self.turn = 1
        self.dice1 = dice1
        self.dice2 = dice2 
        self.dice_roll = [1, 2]
   
    
    def play_a_round(self):
        """
        Obj ->

        two players get to play a round
        """
        #player 1 takes his turn
        self.turn = 1
        self.roll()
        while self.dice_roll and self.p_cnt[0] != 0 and self.winner() == -1:
            print("DEBUG:")
            print(helpers.possible_moves(self.dice_roll, self.p1_state))
            print(self.point_state)
            if not helpers.possible_moves(self.dice_roll, self.p1_state):
                print("DEBUG:", self.dice_roll)
                print(self.p1_state)
                print("No possible moves, passed")
                #for i in range(1000):
                if self.stop_inbetween:
                        input("press a key to continue")
                break
            self.move(self.players[0].play(self.dice_roll, self.p1_state))

        #player 2 takes his turn
        self.turn = 2
        self.update_table()
        self.roll()
        while self.dice_roll and self.p_cnt[1] != 0 and self.winner() == -1:
            print("DEBUG:")
            print(helpers.possible_moves(self.dice_roll, self.p2_state))
            print(self.point_state)
            if not helpers.possible_moves(self.dice_roll, self.p2_state):
                print("DEBUG:",self.dice_roll)
                print(self.p2_state)
                print("No possible moves, passed")
                #for i in range(1000):
                if self.stop_inbetween:
                        input("press a key to continue")
                break
            self.move(self.players[1].play(self.dice_roll, self.p2_state))
    
    def game(self):
        """
        Obj ->

        starts the game
        """
        #print("DEBUG:", self.p1_state)
        print("game starts")
        #two players roll to decide their order
        d1, d2 = self.dice1(), self.dice2()
        while d1 == d2:
            d1, d2 = self.dice1(), self.dice2()
        if d1  < d2:
            self.players.reverse()
        
        self.update_table()
        print(self.players[0].name,"has rolled", max(d1, d2),", so he will be player1")
        print(self.players[1].name,"has rolled", min(d1, d2),", so he will be player2")
        self.players[0].name = "player 1: " + self.players[0].name
        self.players[1].name = "player 2: " + self.players[1].name
        #just to simply let players see the line above
        
        sleep(1.5)
        while self.winner() == -1:
            self.play_a_round()
            self.round += 1
        self.update_table()
        print(self.winner())
        print("game ended, winner is", self.players[self.winner()].name)



    
    def winner(self):
        """
        int x int -> bool

        returns the "winner" state of the game
        -1 for not yet, 0 for player 1 wins the game, 1 for player 2 wins the game
        """
        if self.p_cnt[0] == 0:
            print(self.players[0].name,"achieved winning condition 1")
            print("DEBUG:")
            print(self.p1_state)
            return 0
        if self.p_cnt[1] == 0:
            print(self.players[1].name,"achieved winning condition 1")
            print("DEBUG:")
            print(self.p2_state)
            return 1
        if self.p2_pieces[0] == 1 and self.point_state[0] == 0:
            print(self.players[0].name,"achieved winning condition 2")
            print("DEBUG:")
            print(self.p1_state)
            return 0
        if self.p1_pieces[23] == 1 and self.point_state[23] == 1:
            print(self.players[1].name,"achieved winning condition 2")
            print("DEBUG:")
            print(self.p2_state)
            return 1
        return -1
    
    def move(self,act_seq):
        """
        int x list<list<int, list<int>>> x int

        we move the pieces following the sequences of actions provided by the players
        an act seq is as follows: [(starting_point1, roll1),(starting_point2, roll2)]
        """
        
        index = self.turn - 1
        dir = -1 if self.turn == 1 else 1
        for act in act_seq:
            start, roll = act
            if roll not in self.dice_roll:
                print("ILLEGAL MOVE, You haven't rolled", roll)
                break
            start -= 1
            if self.turn == 2:
                start = 23 - start
            end = start + dir * roll
            print("DEBUG:",self.players[index].name, "has chose to move",start + 1, end + 1)
            if not (0 <= start <= 23 and self.point_state[start] == index):
                print("ILLEGAL MOVE", start + 1, end + 1)
                print("There's no piece on point",start + 1)
                return
            
            if 0 <= end <= 23:
                #if can place on end:
                if self.point_state[end] == index or self.point_state[end] == -1:
                    self.p_pieces[index][end] += 1
                    self.p_pieces[index][start] -= 1
                    self.dice_roll.remove(roll)
                    self.point_state[end] = index

                    if self.p_pieces[index][start] == 0:
                            self.point_state[start] = -1
                    
                    if self.stop_inbetween:
                        input("press a key to continue")
                    #shown board changes
                    self.update_table()

                elif self.p_pieces[1 - index][end] == 1: # we pin the opponent
                    self.p_pieces[index][end] += 1
                    self.p_pieces[index][start] -= 1
                    self.point_state[end] = index
                    self.dice_roll.remove(roll)
                    if self.p_pieces[index][start] == 0:
                            self.point_state[start] = -1

                    if self.stop_inbetween:
                        input("press a key to continue")
                    #shown board changes
                    self.update_table()

                else:
                    print("ILLEGAL MOVE", start + 1, end + 1)
                    print("You can't place pieces at",end + 1)
                    print("DEBUG")
                    print(self.point_state)
                    print(self.p_pieces[index])
            else:
                #if pieces can go home
                home = -1 if index == 1 else 24
                if self.check_can_bear_off(self.turn):
                    if end == home or self.players[1 - index][home] < 1:
                        self.p_cnt[index] -= 1
                        self.dice_roll.remove(roll)
                        self.p_pieces[index][start] -= 1
                        if self.p_pieces[index][start] == 0:
                            self.point_state[start] = -1

                        if self.stop_inbetween:
                            input("press a key to continue")
                        #shown board changes
                        self.update_table()

                    else:
                        if self.p_pieces[index][home - dir * roll] != 0:
                            print("ILLEGAL MOVE", start + 1, end + 1)
                            print("You should first move pieces that can exactly go home")
                else:
                    print("ILLEGAL MOVE", start + 1, end + 1)
                    print("index limit exceeded")
        
        return
        
    def roll(self):
        """
        rolls the two dices and modifies the dice rolls
        duplicates if two rolls are identical
        """
        a, b = self.dice1(), self.dice2()
        result = [a, b]
        if a == b:
            result *= 2
        
        print(self.players[self.turn - 1].name, "has rolled",result)

        self.dice_roll = result
    
    def check_can_bear_off(self, p):
        """
        Obj -> bool

        returns if a player can bear off
        """
        return sum(self.p_pieces[p - 1][12: 24]) == 0
    

    def update_table(self):
        """
        updates the table shown to  players(in the perspective of player1)
        """
        self.shown_board = []
        for i in range(24):
            a, b, s = self.p1_pieces[i], -self.p2_pieces[i], self.point_state[i]
            #print("DEBUG:",a, b)
            if b == 0:
                self.shown_board.append([a, b])
            else:
                self.shown_board.append([b, a])
        #print("DEBUG:",self.shown_board)
        if self.turn == 1 or not self.table_rotate:
            self.table = [
                ["", " 13", " 14", " 15", " 16" , " 17", " 18", " 19", " 20", " 21", " 22", " 23"," 24",""],
                [""] + [format_str(self.shown_board[i][0]) for i in range(12, 24)] + [""],
                [""] + [format_str(self.shown_board[i][1]) for i in range(12, 24)] + ["|",format_str(15 - self.p_cnt[1])],
                [""] + [format_str(self.shown_board[i][1]) for i in range(0, 12)][::-1] + ["|",format_str(15 - self.p_cnt[0])],
                [""] + [format_str(self.shown_board[i][0]) for i in range(0, 12)][::-1] + [""],
                ["", " 12", " 11", " 10", "  9" , "  8", "  7", "  6", "  5", "  4", "  3", "  2","  1",""]
            ]
        else:
            self.table = [
                ["", " 13", " 14", " 15", " 16" , " 17", " 18", " 19", " 20", " 21", " 22", " 23"," 24",""],
                [""] + [format_str(-self.shown_board[i][0]) for i in range(12, 24)] + [""],
                [""] + [format_str(-self.shown_board[i][1]) for i in range(12, 24)] + ["|",format_str(15 - self.p_cnt[1])],
                [""] + [format_str(-self.shown_board[i][1]) for i in range(0, 12)][::-1] + ["|",format_str(15 - self.p_cnt[0])],
                [""] + [format_str(-self.shown_board[i][0]) for i in range(0, 12)][::-1] + [""],
                ["", " 12", " 11", " 10", "  9" , "  8", "  7", "  6", "  5", "  4", "  3", "  2","  1",""]
            ]
            self.table.reverse()
        self.print_board()

    def print_board(self):
        """
        Obj ->

        prints out the current distribution of pieces according to the state
        """
        if self.clear_board:
            #We clear the screen first
            if os.name == 'posix':  #for unix
                os.system('clear')
            if os.name == 'nt':  #for windows
                os.system('cls')
        print("Round", self.round)
        print("now it's "+ self.players[self.turn - 1].name,"'s turn")
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
