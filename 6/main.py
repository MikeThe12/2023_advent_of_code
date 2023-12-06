# Part 1
times = [59, 79, 65, 75]
distances = [597, 1234, 1032, 1328]

game_prod = 1
for i, t in enumerate(times):
    game_tot = 0
    for charge in range(times[i]):
        distance = (t - charge) * charge
        if distance > distances[i]:
            game_tot += 1
    game_prod *= game_tot

print(game_prod)

# Part 2
time = 59796575
distance = 597123410321328

game_tot=0
for charge in range(time):
    if ((time - charge) * charge) > distance:
        game_tot += 1

print(game_tot)