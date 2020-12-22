import re
import json
import copy
#import numpy as np
from collections import deque
import math

data = open("data.txt", "r")
lines = data.readlines()

player = 0 
main_deck = [deque()]

for line in lines:
    if line == "\n":
        continue

    line = line.strip()

    if "Player" in line:
        if len(main_deck[player]) > 0:
            player += 1
            main_deck.append(deque())

        if player == 2:
            break
        continue

    main_deck[player].append(int(line))

def round(deck):
    first = deck[0].popleft()
    second = deck[1].popleft()

    winner = 0

    if first <= len(deck[0]) and second <= len(deck[1]):
        # recursive game time
        print("new game", first, len(deck[0]), "second", second, len(deck[1]))
        new0 = deck[0].copy()
        while len(new0) > first:
            new0.pop()
        new1 = deck[1].copy()
        while len(new1) > second:
            new1.pop()

        winner = game([new0, new1])

    else:
        if (first > second):
            winner = 0
        else:
            winner = 1

    if winner == 0:
        deck[0].append(first)
        deck[0].append(second)
    else:
        deck[1].append(second)
        deck[1].append(first)

def score(deck):
    p = deck[0]
    if len(p) == 0:
        p = deck[1]

    score = 0

    while len(p) > 0:
        m = len(p)
        score += p.popleft() * m
        #print(score)

    print("score", score)

game_count = 1

# returns winning player index
def game(deck):
    count = 1
    global game_count
    game_index = game_count
    #print("starting game", game_index, deck[0], deck[1])
    game_count += 1

    seen = [set(),set()]

    seen[0].add(str(deck[0]))
    seen[1].add(str(deck[1]))

    while len(deck[0]) > 0 and len(deck[1]) > 0:
        round(deck)
        count += 1

        if count > 9999:
            print("failed to complete")
            break

        # remember what we've seen
        if str(deck[0]) in seen[0] or str(deck[1]) in seen[1]:
            # player one (index 0) wins if the deck has been played before
            # print("early out")
            return 0

        seen[0].add(str(deck[0]))
        seen[1].add(str(deck[1]))

        #print(game_index, count, deck[0], deck[1])

    winner = 0
    if len(deck[0]) == 0:
        # player two (index 1) wins
        winner = 1
    print(game_index, "winner", winner)
    return winner

game(main_deck)
score(main_deck)

