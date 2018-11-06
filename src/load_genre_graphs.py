import sys

with open('chords_dict_jazz.txt', 'r') as file:
     dict = (json.load(file))
     chords_dict_rock = {v: k for k, v in dict.iteritems()}

with open('chords_dict_rock.txt', 'r') as file:
     dict = (json.load(file))
     chords_dict_jazz = {v: k for k, v in dict.iteritems()}

load_graphs(graph):
    if graph == "rock":
        filename = '../data/genre_graphs/rock_graph/rock_graph.txt'
        dict = chords_dict_rock
    else:
        filename = '../data/genre_graphs/jazz_graph/jazz_graph.txt'
        dict = chords_dict_jazz

    G_Multi = snap.LoadEdgeList(snap.PNEANet, "jazz_graph.txt", 0, 1)
    G_Directed = snap.LoadEdgeList(snap.PNGraph, "jazz_graph.txt", 0, 1)
    G_Undirected = snap.LoadEdgeList(snap.PUNGraph, "jazz_graph.txt", 0, 1)
    return G_Multi, G_Directed, G_Undirected, dict


G_Multi, G_Directed, G_Undirected, dict = load_graphs("rock")
