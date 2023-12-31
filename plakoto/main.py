import time, os
from random import choice
from Game import Game,Clean_Game
from Player import Human_player,Naive_computer_player,Flat_MC_Player


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
print("what kind of game1 would you like?")
print("1.human player against human player")
print("2.Human player against computer")
print("3.Random computer against Random computer")
print("4.Flat Monte Carlo tree search computer against random computer")
match = int(input())
while match not in (1,2,3,4):
    match = int(input("Invalid choice"))

if match == 1:
    player1 = Human_player(1)
    player2 = Human_player(2)
    game1 = Game(player1, player2, standard_dice, standard_dice)
    game1.show_interface = True
    game1.stop_inbetween = True
    game1.game()

elif match == 2:
    player1 = Human_player(1)
    player2 = Naive_computer_player("Random")
    game1 = Game(player1, player2, standard_dice, standard_dice)
    game1.show_interface = True
    game1.stop_inbetween = True
    game1.game()

elif match == 3:
    test_times = 1000
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
elif match == 4:
    test_times = 200
    winners = [0, 0]
    start_time = time.time()
    for i in range(test_times):
        end_time = time.time()
        elapsed_time = end_time - start_time
        if (i + 1) % 1 == 0:
            os.system('cls')
            print("elpased_time", elapsed_time)
            print("currently on game",i + 1)

        computer1 = Flat_MC_Player("flat_mc")
        computer2 = Naive_computer_player("random")
        game1 = Clean_Game(computer1, computer2, standard_dice, standard_dice)
        game1.game()

        winners[game1.winner()] += 1
        
    end_time = time.time()
    elapsed_time = end_time - start_time
    print("test time:", elapsed_time)
    print(game1.players[0].name, "won", winners[0],"times", "winrate:", winners[0]/test_times)
    print(game1.players[1].name, "won", winners[1],"times", "winrate:",winners[1]/test_times)
