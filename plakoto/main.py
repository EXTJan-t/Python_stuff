from random import choice
from Game import Game
from Player import Player
from startegies import strategy1

player1 = Player(strategy1)
player2 = Player(strategy1)
test_dice1 = lambda : 6
standard_dice = lambda : choice([range(1, 7)])
game = Game(player1, player2, test_dice1, test_dice1)

game.print_board()