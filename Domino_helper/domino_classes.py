# I feel like I'm getting to understand more of OOP doing a tiny project like this and trying to
# follow the rule of 'let the object do the work'. It's really amazing.
#You konw what I feel like I should add a Card class, but it feels a bit to late
# =_= I'll definitely make a better work on the next project
class Player():
    starting_cards = 7

    def __init__(self, index, card_set):
        self.card_num = Player.starting_cards
        self.order = index
        self.game_card = card_set
        

    def play(self, ends):
        pass

    def take_cards(self):
        pass

    def update(self):
        pass

# You are the one who will get help from this simulator
class You(Player):
    #I'm pretty sure that I have violated some abstraction barriers here, but I'm not quite sure
    #how to avoid problems like this right now
    #of all cards except yours
    num_dic = {i: 7 for i in range(0, 7)}
    card_dic = {i:[max(i, j), min(i, j)] for i in range(0,7) for j in range(0,7)}
    others_info = [num_dic, card_dic]
    #of your cards
    point_freq_dic = {i:0 for i in range(0, 7)}
    card_freq_dic = {i:[] for i in range(0, 7)}
    your_info = [point_freq_dic, card_freq_dic]
          

    def __init__(self, index, card_set):
        super().__init__(index, card_set)
        self.cards = []
        self.take_cards()


    def take_cards(self):
        print("enter your cards one by one(example: 1,2)")
        for i in range(self.card_num):
            new_card = ask_for_card()
            self.dics_update(self.your_info, new_card, True)
            self.cards.append(new_card)
            self.game_card.remove(new_card)

    # We can imagine as if it is a real player who inspects whatever is happening on the table and
    # he receives all the information
    def update(self, thrown_card):
        self.dics_update(self.others_info, thrown_card, False)
        
    
    #This is the root of all your strategies.
    def dics_update(self, dics, card, if_add_True):
        if if_add_True:
            #Adds element to the point-frequency dic
            dics[0][card[0]] += 1
            dics[0][card[1]] += 1
            
            #Adds element to the card-frequency dic
            dics[1][card[0]].append(card)
            dics[1][card[1]].append(card)
        else:
            #Removes element from point-frequency dic
            dics[0][card[0]] -= 1
            dics[0][card[1]] -= 1
            
            #Removes element from card-frequency dic
            dics[1][card[0]].remove(card)
            dics[1][card[1]].remove(card)

            
    def play(self, ends):
        suggested_card = self.strategy_primitive(ends)
        print("I'm sure that " + str(suggested_card) + " would be a good idea")
        print('So what is your choice?')
        played_card = ask_for_card()
        while not played_card in self.cards or played_card == 'skip':
            print('Not a legal input')
            played_card = ask_for_card()
        
        if played_card != 'skip':    
            self.dics_update(self.your_info, played_card, False)
            self.cards.remove(played_card)
            self.card_num -= 1
        return played_card

    def strategy_primitive(self, ends):
        if ends == []:
            return [6,6]
        for card in self.cards:
            if card[0] == card[1] and card[0] in ends:
                return card
        
        flag1 = False
        flag2 = False
        for card in self.cards:
            if ends[0] in card:
                flag1 = True
            if ends[1] in card:
                flag2 = True
        if flag1 and flag2:
            point_num1 = self.your_info[0][ends[0]]
            point_num2 = self.your_info[0][ends[1]]
            most_point_card = self.your_info[1][ends[0]][0] if point_num1 > point_num2 \
                else self.your_info[1][ends[1]][0]
            return most_point_card
        elif flag1:
            return self.your_info[1][ends[0]][0]
        elif flag2:
            return self.your_info[1][ends[1]][0]
        else:
            return 'skip'
# Others are the other players


class Others(Player):

    def __init__(self, index, card_set):
        super().__init__(index, card_set)

    
    def play(self, ends):
        print("Tell me what did player" + str(self.order + 1)+" played or /'skip/' if he skipped")
        played_card = ask_for_card()
        if played_card != 'skip':    
            while not played_card in self.game_card:
                print('Not a legal input')
                played_card = ask_for_card()
            self.card_num -= 1
        return played_card


def ask_for_card():
    played_card = input()
    if played_card == 'skip':
        return played_card
    played_card = played_card.split()
    played_card = [int(card) for card in played_card]
    if played_card[0] < played_card[1]:
        played_card[0], played_card[1] = played_card[1], played_card[0]
    return played_card