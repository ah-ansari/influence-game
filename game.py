import numpy as np
import networkx as nx
import tools
import pickle
import operator


def get_seeds(seed_size, folder):
    seed_set = np.loadtxt(folder + "seeds.txt")
    values = np.loadtxt(folder + "values.txt")

    seed_set = seed_set[:seed_size]
    values = values[:seed_size]

    return seed_set, values


# values needed by create_actions
max_node_value_global = None
n_consider_nodes_global = None
actions_list = None


# Create actions in the way that, only the first n_consider_nodes are considered and each of them will be allocated
# a value less or equal to the max_node_value.
# The value that remains will be allocated to other nodes (indexed after n_consider_nodes), 1 per node
# So x1+x2+x3+...+x_seedS-size = k,
#  xi<=max_node_value where i<n_consider_nodes
#  xi=1 or xi=0 where i>n_consider_nodes
def create_actions(k, max_node_value, n_consider_nodes, seed_size):
    global actions_list
    global max_node_value_global, n_consider_nodes_global

    max_node_value_global = max_node_value
    n_consider_nodes_global = n_consider_nodes

    # preparing actions with constrained values, only first nodes have value
    actions_list = []
    constrained_value_actions([0] * seed_size, 0, k)

    # adding value to the second nodes
    actions_list = np.array(actions_list)
    for i in range(actions_list.shape[0]):
        remained_value = k - np.sum(actions_list[i, :])
        if remained_value > seed_size - n_consider_nodes_global:
            remained_value = seed_size - n_consider_nodes_global
        for j in range(n_consider_nodes_global, n_consider_nodes_global + remained_value):
            actions_list[i, j] = 1

    return actions_list


def constrained_value_actions(numbers, index, remained_budget):
    global actions_list
    global max_node_value_global, n_consider_nodes_global

    if remained_budget < 0:
        return

    if index == n_consider_nodes_global:
        actions_list.append(numbers)
        return

    for value in range(max_node_value_global):
        numbers_c = numbers.copy()
        numbers_c[index] = value
        constrained_value_actions(numbers_c, index + 1, remained_budget - value)


# Calculate the payoff matrix according to the given actions and the values for each node
def calculate_payoffs(actions, values):
    actions_num = actions.shape[0]
    seed_size = actions.shape[1]

    player1 = np.zeros((actions_num, actions_num))
    player2 = np.zeros((actions_num, actions_num))

    for i in range(actions_num):
        for j in range(actions_num):
            for k in range(seed_size):
                if (actions[i, k] > actions[j, k]) and (actions[i, k] != 0):
                    player1[i, j] += values[k]
                elif (actions[j, k] > actions[i, k]) and (actions[j, k] != 0):
                    player2[i, j] += values[k]
                elif (actions[j, k] == actions[i, k]) and (actions[j, k] != 0):
                    player1[i, j] += values[k] / 2
                    player2[i, j] += values[k] / 2

    return player1, player2


# Calculate the payoffs in zero sum manner
def calculate_payoffs_zero_sum(actions, values):
    player1, player2 = calculate_payoffs(actions, values)

    player1_zs = player1 - player2
    player2_zs = player2 - player1

    return player1_zs, player2_zs


# get the actions and run in the network and returns the diffusion result
def run_result(g: nx.Graph, action1, action2, seed_set):
    seed_set1 = []
    seed_set2 = []

    for i in range(len(seed_set)):
        if (action1[i] > action2[i]) and (action1[i] != 0):
            seed_set1.append(seed_set[i])
        elif (action2[i] > action1[i]) and (action2[i] != 0):
            seed_set2.append(seed_set[i])
        elif (action1[i] == action2[i]) and (action1[i] != 0):
            r = np.random.uniform(0, 1)
            if r < 0.5:
                seed_set1.append(seed_set[i])
            else:
                seed_set2.append(seed_set[i])

    for node in seed_set1:
        tools.activate(g, node, 1)
    for node in seed_set2:
        tools.activate(g, node, 2)

    tools.diffuse(g, seed_set1, seed_set2)
    activated1_number = len(g.graph["1"])
    activated2_number = len(g.graph["2"])
    return activated1_number, activated2_number
