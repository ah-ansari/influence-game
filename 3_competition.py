import numpy as np
import game
import params


def select_action_mixed(strategy):
    p = np.random.random()
    for i in range(len(strategy)):
        if (sum(nash1[0:i]) <= p) and (p < sum(nash1[0:i + 1])):
            return i


def action_nash(strategy):
    action_i = select_action_mixed(strategy)
    action = actions_list[action_i]
    return action


def action_random(k, seed_size):
    action = np.zeros(seed_size)
    for i in range(seed_size):
        action[i] = np.random.randint(k - sum(action) + 1)
    return action


def action_c_per_each(k, seed_size, c):
    action = np.zeros(seed_size)
    n_nodes = int(k/c)
    for i in range(n_nodes):
        action[i] = c
    return action


actions_list = np.load(params.folder+"actions.npy")
nash = np.load(params.folder+"nash.npy")

n_actions = actions_list.shape[0]
nash1 = nash[:n_actions]
nash2 = nash[n_actions:]

seed_set, values = game.get_seeds(params.seed_size, params.folder)
g = params.load_graph()

diffusion_rounds = 10000
r = np.zeros(diffusion_rounds)

for i in range(diffusion_rounds):
    action1 = action_nash(nash1)
    # action1 = action_random(params.k, params.seed_size)
    # action1 = action_c_per_each(params.k, params.seed_size, 1)

    # action2 = action_nash(nash2)
    # action2 = action_random(params.k, params.seed_size)
    action2 = action_c_per_each(params.k, params.seed_size, 1)

    rr1, rr2 = game.run_result(g.copy(), action1, action2, seed_set.copy())
    r[i] = rr1 - rr2


file = open(params.folder + "competition_result.txt", "a")
file.write("-------------------------------------------------\n")
file.write(" diffusion rounds:  " + str(diffusion_rounds) + "\n")
file.write(" action1:  " + "nash" + "\n")
file.write(" action2:  " + "2-each" + "\n")

file.write(" * mean:  " + str(np.average(r)) + "   std:  " + str(np.std(r)) + "   var:  " + str(np.var(r)) + "\n")

win_rate = sum(r > 0) / diffusion_rounds
file.write(" * win rate:  " + str(win_rate) + "\n")
file.close()
