def strategy1(dice_roll, state):
    """
    list<int> x list<list<int>> -> tuple

    decides the action to take according to dice_rolls and state
    """
    a, b = map(int, input("You have " + str(dice_roll) + ". What are you gonna do?(format:start step)\n").split())
    return (a, b),