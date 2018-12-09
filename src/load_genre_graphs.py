import sys
import json
import snap
import networkx as nx

with open('chords_dict_jazz.txt', 'r') as file:
     dict = (json.load(file))
     chords_dict_jazz = {v: k for k, v in dict.iteritems()}


with open('chords_dict_rock.txt', 'r') as file:
     dict = (json.load(file))
     chords_dict_rock = {v: k for k, v in dict.iteritems()}

def load_genre_graphs(graph):
    if graph == "rock":
        filename = '../data/genre_graphs/rock_graph/rock_graph.edgelist'
        dict = chords_dict_rock
    else:
        filename = '../data/genre_graphs/jazz_graph/jazz_graph.edgelist'
        dict = chords_dict_jazz

    G_Multi = snap.LoadEdgeList(snap.PNEANet, filename, 0, 1)
    G_Directed = snap.LoadEdgeList(snap.PNGraph, filename, 0, 1)
    G_Undirected = snap.LoadEdgeList(snap.PUNGraph, filename, 0, 1)


    #hacky way to get by the mutligraph issue
    G_nx_multi = nx.read_edgelist(filename, nodetype=int, create_using=nx.MultiGraph())
    G_nx = nx.read_edgelist(filename, nodetype=int, create_using=nx.DiGraph())

    for edge in G_nx.edges():
        G_nx[edge[0]][edge[1]]['weight'] = G_nx_multi.number_of_edges(edge[0], edge[1])

    return G_Multi, G_Directed, G_Undirected, G_nx, dict
