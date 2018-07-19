import numpy as np
import networkx as nx
import operator
import params

seed_set = np.loadtxt(params.folder + "graph/seed_set.txt")
rr_sets_graph = nx.read_gpickle(params.folder + "graph/rr_sets_graph")

value_graph = nx.DiGraph()
for seed in seed_set:
    for edge in rr_sets_graph.edges(seed):
        value_graph.add_edge(edge[0], edge[1])

seed_set = set(seed_set)
for node in value_graph.nodes():
    if node not in seed_set:
        in_deg = value_graph.in_degree(node)
        value_graph.add_edges_from(value_graph.in_edges(node), w=(1 / in_deg))


seed_dict = {}
for seed in seed_set:
    seed_dict[seed] = value_graph.degree(seed, weight="w")

sorted_seed = sorted(seed_dict.items(), key=operator.itemgetter(1), reverse=True)
sorted_seed = np.array(sorted_seed)

np.savetxt(params.folder + "seeds.txt", sorted_seed[:, 0])
np.savetxt(params.folder + "values.txt", sorted_seed[:, 1])
