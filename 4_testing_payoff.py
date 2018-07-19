import numpy as np
import game
import params


node_number = 9877
theta = 3710342

actions = np.load(params.folder + "actions.npy")
payoffs = np.load(params.folder + "payoff_table_player1.npy")

seed_set, values = game.get_seeds(params.seed_size, params.folder)
g = params.load_graph()

diffusion_rounds = 5000

r = np.zeros(diffusion_rounds)

action_pairs = np.array([[45, 24, 241, 203, 133], [174, 215, 52, 154, 120]])

file = open(params.folder + "payoff_testing_result.txt", "w")
file.write(" diffusion_rounds: " + str(diffusion_rounds) + "\n")

for action_index in range(action_pairs.shape[1]):
    action1 = action_pairs[0, action_index]
    action2 = action_pairs[1, action_index]

    file.write("-------------------------------------------------\n")
    file.write(" player1:  " + str(action1) + "   player2:  " + str(action2) + "\n")
    payoff1 = (payoffs[action1, action2] * node_number) / theta
    payoff2 = (payoffs[action2, action1] * node_number) / theta
    file.write(" payoffs:  "+str(payoff1)+"  "+str(payoff2) + "\n")

    for i in range(diffusion_rounds):
        rr1, rr2 = game.run_result(g.copy(), actions[action1], actions[action2], seed_set.copy())
        r[i] = rr1 - rr2

    file.write(" * mean:  "+str(np.average(r))+"   std:  "+str(np.std(r))+"   var:  "+str(np.var(r)) + "\n")

file.close()
