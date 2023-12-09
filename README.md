# Plakoto Project Update 🎲

## Table of Contents
- [Overview](#overview)
- [Progress Updates](#progress-updates)
  - [6/11/2023](#6112023)
  - [24/11/2023](#24112023)
  - [7/12/2023](#7122023)
  - [9/12/2023](#9122023)

## Overview
A little project about [Plakoto](https://en.wikipedia.org/wiki/Plakoto). To run the project, execute `python main` in the terminal.

## Progress Updates

### 6/11/2023
Currently working on the game logic part.

### 24/11/2023
Implemented a naive Plakoto player. However, it is extremely slow and doesn't seem to have an advantage over a random strategy computer player, which is weird.

### 7/12/2023 ❌
Now the Flat MC player functions correctly and has an average win rate of 52% against a random strategy player with a simulation time of 5. Turns out that I did not handle the simulation process correctly, resulting in the player getting extra dice and leading to incorrect results.

### 9/12/2023
I have to take back whatever I said last time, for it turned out to be only partly correct. Not only was there the issue of extra dice, but the possible moves function also caused errors by returning moves that could've been identical, making some moves that have an advantage in number gain a higher win rate than other moves, leading to wrong choices. 
I also realized that if I simply returned the move with the maximum win rate with the "max" function, it would also cause unsatisfying results as it returns only the first value meeting the expectations in order of the list. That would lead to a preference for moves of smaller positions and dice as ordered in the return value of the "possible moves" function in "helper.py."

In the meantime, I found that while simulating moves within the Flat MC, we don't have to actually go over every single game. We can simply track the minimum loses of games of moves so far. So for the next move, if it loses more than the minimum loses, it is guaranteed to be impossible to choose that move. Thus, we can simply exit the loop at this point, saving us some time. 😊

However, I have to admit that after fixing all the bugs above and utilizing the knowledge of exiting early, the win rate against a random strategy is not satisfying enough. Better than before, for sure, however inconsistent. Sometimes it loses, and sometimes wins at a 54% win rate. So in my opinion, it is still at the same level as the random strategy player but more inconsistent, with the luck to beat the opponent part of the time. I would love to say that the results can be a lot better if we increase the simulation time per move so that the win rate we get will be more accurate corresponding to the law of large numbers. But sadly, I tried 20 for the simulation time at most, not gaining the results I wanted, and it took too long, like 12-15 seconds per game. Further increasing would take too much time. 😭
