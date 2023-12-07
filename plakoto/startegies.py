import Player
import Game
import helpers
import random
from copy import deepcopy
standard_dice = lambda : random.choice(range(1, 7))

def strategy_input(dice_roll, state):
    """
    list<int> x list<list<int>> -> tuple

    decides the action to take according to dice_rolls and state
    """
    t = list(map(int, input("You have " + str(dice_roll) + ". What are you gonna do?(format:start1 step1 start2 step2)\n").split()))
    while len(t) % 2 != 0:
        print("Invalid input")
        t = list(map(int, input("You have " + str(dice_roll) + ". What are you gonna do?(format:start1 step1 start2 step2)\n").split()))
    act_seq = [(t[i], t[i + 1])for i in range(0, len(t), 2)]
    return act_seq


def strategy_random(dice_roll, state):
    possible_moves = helpers.possible_moves(dice_roll, state)
    if not possible_moves:
        print("DEBUG:",dice_roll)
        print(state)
    return random.choice(possible_moves),

def monte_carlo_tree_search(dice_roll, state):
    #input("HElloooooooooooooooooooooooooooooooooo")
    point_state, self_pieces, others_pieces, cnt = state[0], state[1], state[2], state[3]
    simulation_times = 5
    possible_moves = helpers.possible_moves(dice_roll, state)
    #input(str(len(possible_moves)))
    if not possible_moves:
        print("DEBUG:",dice_roll)
        print(state)
        return []
    win_rate = {}
    if self_pieces == [0] * 24 or others_pieces == [0] * 24:
        return []
    for move in possible_moves:
        win_rate[move] = 0
        
        #print(move)
        #REMINDER:[::]was very useful 😭
        #print(i)
        sub_game = Game.Clean_Game(Player.Naive_computer_player("1"), Player.Naive_computer_player("2"),standard_dice, standard_dice)
        #sub_game.decide_game_order = lambda :0
        sub_game.point_state = point_state[::1]
        sub_game.dice_roll = dice_roll[::1]
        sub_game.p_cnt = cnt[::1]
        sub_game.p1_pieces, sub_game.p2_pieces = self_pieces[::1], others_pieces[::1]
        sub_game.p_pieces = [sub_game.p1_pieces, sub_game.p2_pieces]
        #print("org", self_pieces, others_pieces)
        #print("aft", sub_game.p1_pieces, sub_game.p2_pieces)
        sub_game.move([move])
        #print(dice_roll, sub_game.dice_roll, move)

        for i in range(simulation_times):
            t = deepcopy(sub_game)
            t.game()
            if t.winner() == 0:
                win_rate[move] += 1
    return [max(possible_moves, key= lambda x:win_rate[x])]
        