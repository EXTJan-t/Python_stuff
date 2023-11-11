from random import choice
from Game import Game
from Player import Human_player


player1 = Human_player(1)
player2 = Human_player(2)
test_dice1 = lambda : 1
test_dice2 = lambda : 2
standard_dice = lambda : choice(range(1, 7))
game1 = Game(player1, player2, standard_dice, standard_dice)
game1.game()
#test_game = Game(player1, player2, test_dice1, test_dice2)
#test_game.game()