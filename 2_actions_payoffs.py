import numpy as np
import game
import params

k = params.k
max_node_value = params.max_node_value
n_consider_nodes = params.n_consider_nodes
seed_size = params.seed_size

actions = game.create_actions(k, max_node_value, n_consider_nodes, seed_size)
np.save(params.folder+"actions", actions)

seed_set, values = game.get_seeds(seed_size, params.folder)
payoff_player1, payoff_player2 = game.calculate_payoffs_zero_sum(actions, values)

np.save(params.folder + "payoff_table_player1", payoff_player1)
np.save(params.folder + "payoff_table_player2", payoff_player2)
