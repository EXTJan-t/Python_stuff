import helpers
import random
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