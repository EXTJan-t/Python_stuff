def strategy1(dice_roll, state):
    """
    list<int> x list<list<int>> -> tuple

    decides the action to take according to dice_rolls and state
    """
    act = map(int, input("You have", dice_roll,"What are you gonna do?"))
    return tuple(act)