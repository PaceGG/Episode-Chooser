from random import randint, choices

n = 3
d = 1000000
lst = [0]*n

games = ["first", "second", "third"]
weight = [2,1,0]

chosen_game = choices(games, weights=weight, k=1)[0]


for i in range(d):
    chosen_game = choices(games, weights=weight, k=1)[0]
    if chosen_game == "first":
        lst[0] += 1
    if chosen_game == "second":
        lst[1] += 1
    if chosen_game == "third":
        lst[2] += 1
    if i%100 == 0:
        for i in lst:
            print(str(i/sum(lst)*100)[:4] + "%", end=" ")
        print()


    # c = randint(0,n-1)
    # lst[c] += 1