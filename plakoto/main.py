import time, os
from random import choice
from Game import Game
from Player import Human_player,Naive_computer_player


#player1 = Human_player(1)
#player2 = Human_player(2)
computer1 = Naive_computer_player("random1")
computer2 = Naive_computer_player("random2")
test_dice1 = lambda : 1
test_dice2 = lambda : 2
standard_dice = lambda : choice(range(1, 7))
#game1 = Game(computer1, computer2, standard_dice, standard_dice)
#game1.game()
#test_game = Game(player1, player2, test_dice1, test_dice2)
#test_game.game()
test_times = 10000
winners = [0, 0]
start_time = time.time()
for i in range(test_times):
    end_time = time.time()
    elapsed_time = end_time - start_time
    if (i + 1) % 100 == 0:
        os.system('cls')
        print("elpased_time", elapsed_time)
        print("currently on game",i + 1)

    computer1 = Naive_computer_player("random1")
    computer2 = Naive_computer_player("random2")
    game1 = Game(computer1, computer2, standard_dice, standard_dice)
    game1.game()

    winners[game1.winner()] += 1
    
end_time = time.time()
elapsed_time = end_time - start_time
print("test time:", elapsed_time)
print(game1.players[0].name, "won", winners[0],"times", "winrate:", winners[0]/test_times)
print(game1.players[1].name, "won", winners[1],"times", "winrate:",winners[1]/test_times)
