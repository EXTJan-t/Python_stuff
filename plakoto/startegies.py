import Player
import Game
import helpers
import random

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
    possible_moves = helpers.possible_moves(dice_roll, state)
    if not possible_moves:
        print("DEBUG:",dice_roll)
        print(state)
        return []
    rates = {}
    for move in possible_moves:
        win_cnt = 0
        sub_game = Game.Game(Player.Naive_computer_player("1"), Player.Naive_computer_player("1"))