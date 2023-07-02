from domino_classes import *

class Game_play:
    player_num = 4
    players = []
    card_set = [[i,j] for i in range(0, 7) for j in range(0,i + 1)] #Generates the whole cards_set of domino
    ends = []
        
    def __init__(self, your_order):
        
        for i in range(self.player_num):
            if  i == your_order - 1:
                self.real_player = You(i, self.card_set) 
                self.players.append(self.real_player)
            else: 
                self.players.append(Others(i,self.card_set))
            
    
    #Judges if the game is over
    def game_end(self):
        #Case where someone has thrown all of his cards and he wins
        for player in self.players:
            if player.card_num == 0:
                return True
            
        #Case where we meet a dead end and we decide the winner otherwise
        if not self.ends:
            return False
        else:
            all_remaining_cards = self.card_set + self.real_player.cards
            for card in all_remaining_cards:
                if self.ends[0] in card or self.ends[1] in card:
                    return False
        return True
    
        
        
    #I realized that the two cards in the two ends of the domino cards are crucial, and we should
    #modified it whenever a player has thrown a card
    #Also we can transfer the message to the real_player so that he can decide his strategy
    def update(self, card_played, turn):
        turn_index = turn % self.player_num
        if  turn_index != self.real_player.order:
            self.card_set.remove(card_played)
                
        #As is known to all, [3,4][4,5] makes [3,5] in domino
        if not self.ends:
            self.ends = card_played
        else:
            self.card_merge(card_played)
    
    
    #Returns the winner of the game
    #But on another thought, as a domino helper this isn't really necessary
    def winner(self):
        pass
    
    
    def game(self):
        turn = 0
        while not self.game_end():
            played_card = self.players[turn % self.player_num].play(self.ends)
            if played_card != 'skip':
                self.update(played_card, turn)
            turn += 1
        print('game ends ^_^')
        
        
    def card_merge(self,card_played):
        if card_played[0] in self.ends:
                meeted_end = self.ends.index(card_played[0])
                self.ends[meeted_end] = card_played[1]
        elif card_played[1] in self.ends:
                meeted_end = self.ends.index(card_played[1])
                self.ends[meeted_end] = card_played[0]


your_index = int(input('What is your order in the game(1,2...)'))
new_dominoGame = Game_play(your_index)
new_dominoGame.game()

