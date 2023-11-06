from random import choice
from Game import Game
from Player import Player
from startegies import strategy1

player1 = Player(strategy1)
player2 = Player(strategy1)
test_dice = lambda : 6
game = Game(player1, player2, test_dice, test_dice)

game.print_board()