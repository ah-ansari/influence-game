import tools

data_set = "CA-HepTh.txt"
is_directed = False
folder = data_set[:-4] + "/"

k = 20
max_node_value = 3
n_consider_nodes = 5
seed_size = 25


def load_graph():
    if is_directed:
        g = tools.load_graph_directed("datasets/" + data_set)
    else:
        g = tools.load_graph_undirected("datasets/" + data_set)

    return g


def print_params():
    file = open(folder + "params.txt", "w")
    file.write(" data set: " + data_set + "\n")
    file.write(" is_directed: " + str(is_directed) + "\n")
    file.write(" k: " + str(k) + "\n")
    file.write(" max_node_value: " + str(max_node_value) + "\n")
    file.write(" n_consider_nodes: " + str(n_consider_nodes) + "\n")
    file.write(" seed_size: " + str(seed_size) + "\n")
    file.close()

print_params()
