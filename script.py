import numpy as np

nash = np.load("saves/nash_zs_3_5.npy")
actions_list = np.load("saves/constrained_actions_3_5.npy")
n_actions = actions_list.shape[0]

print("number of actions: " + str(n_actions))

nash = nash[0]
nash1 = nash[:n_actions]
nash2 = nash[n_actions:]

print("player1:")
for i in range(n_actions):
    if nash1[i] != 0:
        print(i)
        print(nash1[i])
        print(actions_list[i])
        print("-------------------")

print("player2:")
for i in range(n_actions):
    if nash2[i] != 0:
        print(i)
        print(nash2[i])
        print(actions_list[i])
        print("-------------------")

if nash1.any() == nash2.any():
    print("totally the same")
