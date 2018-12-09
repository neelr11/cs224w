import sys
import json
import snap
import os

with open('chords_dict_jazz.txt', 'r') as file:
     dict = (json.load(file))
     chords_dict_jazz = {v: k for k, v in dict.iteritems()}

with open('chords_dict_rock.txt', 'r') as file:
     dict = (json.load(file))
     chords_dict_rock = {v: k for k, v in dict.iteritems()}

# Returns array of directed graphs (for motif analysis need directed)
def load_song_graphs(graph):
    if graph == "rock":
        path = '../data/song_graphs/rock_graphs/'
        dict = chords_dict_rock
    else:
        path = '../data/song_graphs/jazz_graphs/'
        dict = chords_dict_jazz

    graphs = []
    for filename in os.listdir(path):
        if filename == ".DS_Store":
            continue
        graphs.append(snap.LoadEdgeList(snap.PNGraph, path+filename, 0, 1))
    return graphs, dict

    # G_Multi = snap.LoadEdgeList(snap.PNEANet, filename, 0, 1)
    # G_Directed = snap.LoadEdgeList(snap.PNGraph, filename, 0, 1)
    # G_Undirected = snap.LoadEdgeList(snap.PUNGraph, filename, 0, 1)
    # return G_Multi, G_Directed, G_Undirected, dict
