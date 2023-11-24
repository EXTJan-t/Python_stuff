import os
from time import sleep
import helpers
import heapq
class Game():
    clear_board = False
    stop_inbetween = False
    table_rotate = False
    show_interface = False
    show_DEBUG = False
    def __init__(self, player1, player2, dice1, dice2):
        self.players = [player1, player2]
        self.round = 0
        #implies whose turn it is
        self.turn = 1
        self.dice1 = dice1
        self.dice2 = dice2 
        self.dice_roll = [1, 2]
        #0 implies that of player 1 are on top, 1 for player 2 and -1 stands for no pieces there
        self.point_state  = [1] + [-1] * 22 + [0]
        self.p1_pieces = [0 for i in range(23)] + [15]
        self.p2_pieces = [15] + [0 for i in range(23)]
        self.p_pieces = [self.p1_pieces, self.p2_pieces]
        #pieces left for each player to win
        self.p_cnt = [15, 15]

        
    @property
    def p1_state(self):
        return [self.point_state] + self.p_pieces + [self.p_cnt]
    @property
    def p2_state(self):
        return [[1 - x if x != -1 else -1 for x in self.point_state][::-1]] + \
            [self.p_pieces[1][::-1], self.p_pieces[0][::-1]] + [self.p_cnt[::-1]]
    
    def play_a_round(self):
        """
        Obj ->

        two players get to play a round
        """
        #player 1 takes his turn
        self.turn = 1
        self.roll()
        while self.dice_roll and self.p_cnt[0] != 0 and self.winner() == -1:
            if self.show_DEBUG and False:
                print("DEBUG:")
                print(helpers.possible_moves(self.dice_roll, self.p1_state))
                print(self.point_state)
            if not helpers.possible_moves(self.dice_roll, self.p1_state):
                if self.show_DEBUG:
                    print("DEBUG:", self.dice_roll)
                    print(self.p1_state)

                if self.show_interface:
                    print("No possible moves, passed")
                #self.print_board()
                #for i in range(2):#DEBUG
                if self.stop_inbetween:
                    input("press a key to continue")
                break
            self.move(self.players[0].play(self.dice_roll, self.p1_state))

        #player 2 takes his turn
        self.turn = 2
        self.update_table()
        self.roll()
        while self.dice_roll and self.p_cnt[1] != 0 and self.winner() == -1:
            if self.show_DEBUG and False:
                print("DEBUG:")
                print(helpers.possible_moves(self.dice_roll, self.p2_state))
                print(self.point_state)
            if not helpers.possible_moves(self.dice_roll, self.p2_state):
                if self.show_DEBUG:
                    print("DEBUG:",self.dice_roll)
                    print(self.p2_state)
                if self.show_interface:
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
        self.decide_game_order()
        #just to simply let players see the line above
        if self.stop_inbetween:
            sleep(1.5)
        while self.winner() == -1:
            self.play_a_round()
            self.round += 1
        self.update_table()
        if self.show_interface:
            print(self.winner())
            print("game ended, winner is", self.players[self.winner()].name)



    
    def winner(self):
        """
         -> int

        returns the "winner" state of the game
        -1 for not yet, 0 for player 1 wins the game, 1 for player 2 wins the game
        """
        if self.p_cnt[0] == 0:
            if self.show_interface:
                print(self.players[0].name,"achieved winning condition 1")
            if self.show_DEBUG:
                print("DEBUG:")
                print(self.p1_state)
            return 0
        if self.p_cnt[1] == 0:
            if self.show_interface:
                print(self.players[1].name,"achieved winning condition 1")
            if self.show_DEBUG:
                print("DEBUG:")
                print(self.p2_state)
            return 1
        if self.p2_pieces[0] == 1 and self.point_state[0] == 0:
            if self.show_interface:
                print(self.players[0].name,"achieved winning condition 2")
            if self.show_DEBUG:
                print("DEBUG:")
                print(self.p1_state)
            return 0
        if self.p1_pieces[23] == 1 and self.point_state[23] == 1:
            if self.show_interface:
                print(self.players[1].name,"achieved winning condition 2")
            if self.show_DEBUG:
                print("DEBUG:")
                print(self.p2_state)
            return 1
        return -1
    
    def move(self,act_seq):
        """
        tuple<tuple<int, int>>

        we move the pieces following the sequences of actions provided by the players
        an act seq is as follows: [(starting_point1, roll1),(starting_point2, roll2)]
        """
        
        index = self.turn - 1
        dir = -1 if self.turn == 1 else 1
        for act in act_seq:
            if self.can_go_home(self.turn) and len(self.dice_roll) > 1:
                if not self.check_first_go_home_action(act):
                    print( "Illegal move,",act,"you're wasting too much")
                    return
            start, roll = act
            if roll not in self.dice_roll:
                if self.show_interface:
                    print("ILLEGAL MOVE, You haven't rolled", roll)
                break
            start -= 1
            if self.turn == 2:
                start = 23 - start
            end = start + dir * roll
            if self.show_interface:
                print(self.players[index].name, "has chose to move",start + 1, end + 1)
            if not (0 <= start <= 23 and self.point_state[start] == index):
                if self.show_interface:
                    print("ILLEGAL MOVE", start + 1, end + 1)
                    print("There's no piece on point",start + 1)
                    return
            
            if 0 <= end <= 23:
                #if can place on end:
                if self.point_state[end] == index or self.point_state[end] == -1:
                    self.update_board(index, start, end, roll)

                elif self.p_pieces[1 - index][end] == 1 and self.p1_pieces[end] + self.p2_pieces[end] == 1: # we pin the opponent
                    self.update_board(index, start, end, roll)

                else:
                    if self.show_interface:
                        print("ILLEGAL MOVE", start + 1, end + 1)
                        print("You can't place pieces at",end + 1)
                    if self.show_DEBUG:
                        print("DEBUG")
                        print(self.point_state)
                        print(self.p_pieces[index])
            else:
                #if pieces can go home
                if self.can_go_home(self.turn):
                    temp = self.min_difference_home_move(roll)
                    if start == temp:
                        self.update_board(index, start, end, roll)
                        self.p_cnt[index] -= 1

                    else:
                        print("ILLEGAL MOVE", start + 1, end + 1)
                        print("You should first move pieces that can exactly go home")
                        
                else:
                    if self.show_interface:
                        print("ILLEGAL MOVE", start + 1, end + 1)
                        print("index limit exceeded")
        
        return
    


    def min_difference_home_move(self, roll):
        """
        int -> int

        returns a starting point for which the current roll will waste less
        """
        if self.turn == 1:
            for i in range(roll - 1, -1, -1):
                if self.p1_pieces[i] != 0:
                    return i

        elif self.turn == 2:
            for i in range(24 - roll, 25):
                if self.p2_pieces[i] != 0:
                    return i
    
    def check_first_go_home_action(self, act):
        """
        int -> int

        we check the moves except from the last one whether they're going to prevent player from taking more efficient
        steps of the dice_rolls
        """
        start, step = act
        if self.turn == 1:
            cur_pieces = []
            for i in range(5, -1, -1):
                cur_pieces +=  self.p1_pieces[i] * [i + 1] if self.point_state[i] == 0 else []
            
        elif self.turn == 2:
            cur_pieces = []
            for i in range(18, 24):
                cur_pieces +=  self.p2_pieces[i] * [24 - i] if self.point_state[i] == 1 else []
        if len(cur_pieces) <= 1:
                return True
        else:
            min_waste = sum(self.dice_roll) - sum(cur_pieces[0:min(len(cur_pieces) - 1, len(self.dice_roll))])
            t = [-x for x in cur_pieces[::1]]
            dr = sorted(self.dice_roll)
            min_waste = 0
            for d in dr:
                if not t:
                    min_waste += d
                    continue
                p = -heapq.heappop(t)
                rest  = p - d
                if rest > 0:
                    heapq.heappush(t, -rest)
                min_waste += max(0, -rest)
            if min_waste == 0:
                return True
            else:
                if self.show_DEBUG:
                    print("DEBUG:")
                    print(start, self.dice_roll, act)
                    print(cur_pieces)
                    print(sum(self.dice_roll) - step \
                    - sum(cur_pieces[0:min(len(cur_pieces), len(self.dice_roll))]), min_waste)
                    self.print_board()
                cur_pieces.remove(start)
                t = [-x for x in cur_pieces[::1]]
                dr = sorted(self.dice_roll)
                dr.remove(step)
                waste = step - start if start < step else 0
                if start > step:
                    heapq.heappush(t, step - start)
                for d in dr:
                    if not t:
                        min_waste += d
                        continue
                    p = -heapq.heappop(t)
                    rest  = p - d
                    if rest > 0:
                        heapq.heappush(t, -rest)
                    waste += max(0, -rest)
                comp = waste <= min_waste
                if not comp and (self.show_DEBUG or True):
                    print("DEBUG:")
                    print(start, self.dice_roll, act)
                    print(cur_pieces)
                    print(waste, min_waste,comp)
                    print(self.point_state)
                    self.print_board()
                return comp
    def update_board(self, index, start, end, roll):
        """
        int, int, int, int

        we update the current informations on the board that the game should record
        """
        if 0 <= end <= 23:
            self.p_pieces[index][end] += 1
            self.point_state[end] = index
        self.p_pieces[index][start] -= 1
        self.dice_roll.remove(roll)
        if self.p_pieces[index][start] == 0:
            if self.p_pieces[1 - index][start] == 0:
                self.point_state[start] = -1
            else:
                self.point_state[start] = 1 - index

        if self.stop_inbetween:
            input("press any key to continue")
        if self.show_interface:
            self.update_table()



    def roll(self):
        """
        rolls the two dices and modifies the dice rolls
        duplicates if two rolls are identical
        """
        a, b = self.dice1(), self.dice2()
        result = [a, b]
        if a == b:
            result *= 2
        
        if self.show_interface:
            print(self.players[self.turn - 1].name, "has rolled",result)

        self.dice_roll = result
    
    def can_go_home(self, p):
        """
        Obj -> bool

        returns if a player's pieces are all at home
        """
        if p == 1:
            return sum(self.p1_pieces[6:24]) == 0
        if p == 2:
            return sum(self.p2_pieces[0:18]) == 0
    

    def decide_game_order(self, pre_decided = False):
        """
        We decide the order of the player
        """
        if not pre_decided:
            if self.show_DEBUG:
                #print("DEBUG:", self.p1_state)
                pass
            if self.show_interface:
                print("game starts")
            #two players roll to decide their order
            d1, d2 = self.dice1(), self.dice2()
            while d1 == d2:
                d1, d2 = self.dice1(), self.dice2()
            if d1  < d2:
                self.players.reverse()
            if self.show_interface:
                self.update_table()
                print(self.players[0].name,"has rolled", max(d1, d2),", so he will be player1")
                print(self.players[1].name,"has rolled", min(d1, d2),", so he will be player2")
            self.players[0].name = "player 1: " + self.players[0].name
            self.players[1].name = "player 2: " + self.players[1].name
            self.players[0].turn = 1
            self.players[0].turn = 2


    def update_table(self):
        """
        updates the table shown to  players(in the perspective of player1)
        """
        self.shown_board = []
        for i in range(24):
            a, b, s = self.p1_pieces[i], -self.p2_pieces[i], self.point_state[i]
            #print("DEBUG:",a, b)
            if b == 0 or s == 1 and a != 0:
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
        if self.show_interface:
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
    
class Clean_Game(Game):
    show_interface = False
    show_DEBUG = False
    stop_inbetween = False
    track_progress = False
    def __init__(self, player1, player2, dice1, dice2):
        super().__init__(player1, player2, dice1, dice2)
    
    def move(self, act_seq):
        possible_moves = helpers.possible_moves(self.dice_roll, \
                                                self.p1_state if self.turn == 1 else self.p2_state) 
        index = self.turn - 1
        for act in act_seq:
            start, roll = act
            start -= 1
            end = start - roll
            if end < 0:
                self.p_cnt[index] -= 1
            if (start + 1, roll) in possible_moves:
                if self.turn == 1:
                    self.update_board(index, start, end, roll)
                else:
                    self.update_board(index, 23 - start, 23 - end, roll)
            else:
                continue
        if self.show_DEBUG:
            self.print_board()
            print(self.p1_state)
            print(self.point_state)
            print(self.dice_roll)
            print(possible_moves,(start, roll))
            input(act)

    def play_a_round(self):
        super().play_a_round()
        if self.track_progress:
            self.print_board()
            print(self.p1_state)
            print(self.dice_roll)
    def decide_game_order(self, pre_decided=False):
        pass
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
