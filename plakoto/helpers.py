import heapq
def possible_moves(dice_roll:list, state:list):
    """
    list<int> x list<list<int>> -> list<tuple<int, int>>

    generates all possible moves of the current state
    """
    point_state, self_pieces, others_pieces = state[0], state[1], state[2]
    start_pos = [x for x in range(24) if point_state[x] == 0]
    #print("DEBUG:", start_pos)
    moves = []
    for pos in set(start_pos):
          for roll in set(dice_roll):
                if can_move(state, pos, roll):
                    if not check_can_bear_off(self_pieces) or len(dice_roll) <= 1 or check_first_go_home_action((pos, roll), self_pieces, point_state, dice_roll):
                        moves.append((pos + 1, roll))
    #print("DEBUG:",moves)
    return moves


def check_can_bear_off(self_pieces:list):
    """
    list<int> -> bool

    returns if a player can bear off
    """
    return sum(self_pieces[6: 24]) == 0

def can_move(state:list,start:int, roll:int):
    end = start - roll
    point_state, self_pieces, others_pieces = state[0], state[1], state[2]
    if 0 <= end <= 23:
        if point_state[end] == 0 or point_state[end] == -1 or others_pieces[end] + self_pieces[end] == 1:
            return True
    elif end < 0:
        if check_can_bear_off(self_pieces):
            if start == min_difference_home_move(self_pieces, roll):
                return True
    return False

def min_difference_home_move(self_pieces, roll):
        """
        list<int> x int -> int

        returns a starting point for which the current roll will waste less
        """
        for i in range(roll - 1, -1, -1):
            if self_pieces[i] != 0:
                return i

def check_first_go_home_action(act, self_pieces, point_state, dice_roll):
    """
    int -> int

    we check the moves except from the last one whether they're going to prevent player from taking more efficient
    steps of the dice_rolls
    """
    #print(self_pieces)
    start, step = act
    start += 1
    cur_pieces = []
    for i in range(5, -1, -1):
        cur_pieces +=  self_pieces[i] * [i + 1] if point_state[i] == 0 else []
    if len(cur_pieces) <= 1:
        return True
    else:
        min_waste = sum(dice_roll) - sum(cur_pieces[0:min(len(cur_pieces) - 1, len(dice_roll))])
        t = [-x for x in cur_pieces[::1]]
        dr = sorted(dice_roll)
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
            cur_pieces.remove(start)
            t = [-x for x in cur_pieces[::1]]
            dr = sorted(dice_roll)
            dr.remove(step)
            waste = max(step - start, 0)
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
            return comp