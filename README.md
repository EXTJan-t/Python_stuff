# Plakoto 🎲
A little project about [Plakoto](https://en.wikipedia.oarg/wiki/Plakoto)
run "python main" on the terminal to run it
y
6/11/2023
currently working on the game logic part

24/11/2023

implemented a naive plakoto player however extremely slow and doesn't seems to have an advantage over random strategy computer player which is weird

7/12/2023
now the flat mc player functions correctly and has in average of 52% of win rate against random strategy player with a simulation time of 5.Turns out that I did not handle correctly the simulation process and thus the player got extra dices leading to uncorrect results. 

9/12/2023
I have to take back whatever I said last time, for it turned out to be only partly correct. Not only was there the issue of extra dices, but the possible moves function also caused errors by returning moves that could've been identical, making some moves that have advantage in number gain a higher win rate than other moves, leading to wrong choices. 
I also realized that if I simply returned the move with maximum win rate with the "max" function, it would also cause unsatisfying results as it returns only the first value meeting the expectations in order of the list. That would lead to a preference for moves of samller positions and dices as ordered in the return value of "possible moves" function in "helper.py"
In the meantime, I found that while simulating moves within the Flat MC, we don't have to actually go over every single game. We can simply track the minimum loses of games of moves so far. So for the next move, if it loses more than the minimum loses, it is guaranteed to be impossible the chosen move, so we can simply exit the loop at this point, thus saving us some time.😊
However, I have to admit that after fixing all the bugs above and utilizing the knowledge of exiting early, the win rate against random strategy are not satisfying enough. Better than before, for sure, however inconsistent, sometimes it loses, and sometimes wins at a 54% win rate. So in my opinion now it is still the same level of random strategy player, but more inconsistence, with the luck to beat the opponent part of the time. I would love to say that the results can be a lot better if we increase the simulation time per move so that the win rate we get will be more accurate corresponding the law of the large numbers. But sadly, I tried 20 for the simulation time at most not gaining the results I wanted and it took long, like 12-15 seconds per game, and further increasing would take too much time.😭