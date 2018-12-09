import networkx as nx
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import os
import node2vec as nv

f_name = os.getcwd() + '/graph/karate.edgelist'
print f_name
G = nx.read_edgelist(f_name)
print sorted(G.degree(G.nodes), key=lambda x:x[1], reverse=True)
#f = plt.figure()
#nx.draw_networkx(G)
#f.savefig("graph.png")

#Node 33 seems to play an integral role connecting different communities in the graph.


#2.4
#is_directed = False
#p, q = 2, 1000 #want to have high prob of going back, and low p of going forward
#G = nv.Graph(G, is_directed, p, q)
#walk_length, start_node = 10, 33
#G.preprocess_transition_probs()
#walk = G.node2vec_walk(walk_length, start_node)
#print walk
