def possible_moves(dice_roll:list, state:list):
    """
    list<int> x list<list<int>> -> list<tuple<int, int>>

    generates all possible moves of the current state
    """
    point_state, self_pieces, others_pieces = state[0], state[1], state[2]
    start_pos = [x for x in range(24) if point_state[x] == 0]
    #print("DEBUG:", start_pos)
    moves = []
    for pos in start_pos:
          for roll in dice_roll:
                if can_move(state, pos, roll):
                     moves.append((pos + 1, roll))
    #print("DEBUG:",moves)
    return moves


def check_can_bear_off(self_pieces:list):
    """
    list<int> -> bool

    returns if a player can bear off
    """
    return sum(self_pieces[12: 24]) == 0

def can_move(state:list,start:int, roll:int):
    end = start - roll
    point_state, self_pieces, others_pieces = state[0], state[1], state[2]
    if 0 <= end <= 23:
        if point_state[end] == 0 or point_state[end] == -1 or others_pieces[end] + self_pieces[end] == 1:
            return True
    elif end < 0:
        if check_can_bear_off(self_pieces):
            if end == -1 or self_pieces[roll - 1] == 0:
                 return True
            
                
    return False

