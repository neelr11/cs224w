import load_genre_graphs as ld
import analysis
import snap
import numpy as np
import random
import networkx as nx
from collections import defaultdict
import node2vec as nv

ITERATIONS = 100
OUT_THRESHOLD = 0.7
MAX_SONG_LENGTH = 100


def random_walk_generation(G_Multi, i, id_to_chord, genre):
    chord_progression = []
    length = 0
    #instantiate song graph
    #G_Directed_i = snap.TNGraph.New() #song graph i
    node = G_Multi.BegNI()
    #G_Directed_i.AddNode(node.GetId())

    #while not at last node in the song
    while node.GetOutDeg() > 0 and length < MAX_SONG_LENGTH:
        nodeID = node.GetId()
        chord_progression.append(id_to_chord[nodeID])
        neighbors = [node.GetNbrNId(x) for x in xrange(node.GetOutDeg())]
        dstID = random.choice(neighbors)
    #    if not G_Directed_i.IsNode(dstID): #if edge dst isn't a node in G_Directed_i, add it
    #        G_Directed_i.AddNode(dstID)
    #    G_Directed_i.AddEdge(nodeID, dstID)
        node = G_Multi.GetNI(dstID)
        length += 1

    #add last chord to list
    chord_progression.append(id_to_chord[nodeID])

    #file_name = "generated_songs/random_generated_" + genre + "_song_" + str(i+1) + ".txt"
    #snap.SaveEdgeList(G_Directed_i, file_name)

    return chord_progression


def smart_walk_generation(G_Undirected, G_Multi, id_to_chord, genre, i = ""):
    clusters = analysis.get_communities(G_Undirected, id_to_chord, print=False) #List of sers of node IDs
    id_to_outdegree = {node.GetId() : node.GetOutDeg() for node in G_Multi.Nodes()}
    visited = set()
    chord_progression = []

    #instantiate song graph
    #G_Directed_i = snap.TNGraph.New() #song graph i

    #Get node in largest cluster
    #1. Get index of largest element of clusters
    cluster_index = np.argmax([len(x) for x in clusters])
    # Choose randomly from this set
    possible_next = clusters[cluster_index]
    nodeID = random.choice(clusters[cluster_index])

    #G_Directed_i.AddNode(nodeID)
    node = G_Multi.GetNI(nodeID)

    #while not at last node in the song
    while len(chord_progression) < MAX_SONG_LENGTH:
        visited.add(nodeID)
        chord_progression.append(id_to_chord[nodeID])
        neighbors = set([node.GetNbrNId(x) for x in xrange(node.GetOutDeg())])
        rand = random.random()
        probs = []

        #With probability X stay within cluster
        if rand < OUT_THRESHOLD:
            possible_next = set([x for x in clusters[cluster_index]]).intersection(set(neighbors))
        else:
            possible_next = (set([x for x in clusters[cluster_index]]).intersection(set(neighbors))).union(visited)
        if len(possible_next) == 0:
            possible_next = possible_next.union(visited)

        for x in possible_next:
            probs.extend([x] * id_to_outdegree[x])
        if len(probs) == 0:
            break
        dstID = random.choice(probs)

        #Update current cluster index
        if dstID not in clusters[cluster_index]:
            cluster_index = [i for i, x in enumerate(clusters) if dstID in x][0]

        #if edge dst isn't a node in G_Directed_i, add it
        #if not G_Directed_i.IsNode(dstID):
        #    G_Directed_i.AddNode(dstID)

    #    G_Directed_i.AddEdge(nodeID, dstID)
        node = G_Multi.GetNI(dstID)
        #Update node to current node
        nodeID = dstID


    #add last chord to list
    chord_progression.append(id_to_chord[nodeID])

    #if i is not "":
#        file_name = "generated_songs/smart_generated_" + genre + "_song_" + str(i+1) + ".txt"
#    else:
#        file_name =  "generated_songs/smart_generated_" + genre + "_song.txt"

    #Save generated graph
    #snap.SaveEdgeList(G_Directed_i, file_name)

    return chord_progression


def node2vec(G_Multi, G_nx, id_to_chord, genre, i):

    #if args.weighted:
    #	G = nx.read_edgelist(args.input, nodetype=int, data=(('weight',float),), create_using=nx.MultiGraph())
    #else:

    #if not args.directed:
    #	G = G.to_undirected()
    is_directed = True
    id_to_outdegree = {node.GetId() : node.GetOutDeg() for node in G_Multi.Nodes()}
    weighted_list = []
    for id in id_to_outdegree:
        weighted_list.extend([id] * id_to_outdegree[id])
    startID = random.choice(weighted_list)

    p, q = 5, 100 #want to have high prob of going back, and low p of going forward
    G = nv.Graph(G_nx, is_directed, p, q)
    G.preprocess_transition_probs()
    walk = G.node2vec_walk(MAX_SONG_LENGTH, startID)

    chord_progression = []
    for nodeID in walk:
        chord_progression.append(id_to_chord[nodeID])
    return chord_progression


def main(type):
    for genre in ["rock", "jazz"]:
        #Instantiate datasets
        G_Multi, G_Directed, G_Undirected, G_nx, id_to_chord = ld.load_genre_graphs(genre)
        generated_songs = [] #list of song graphs

        if (type == "random"):
            for i in range(ITERATIONS):
                chord_progression = random_walk_generation(G_Multi, i, id_to_chord, genre)
                while len(chord_progression) < MAX_SONG_LENGTH * 0.8:
                    chord_progression = random_walk_generation(G_Multi, i, id_to_chord, genre)
                generated_songs.append(chord_progression)
        elif (type == "smart"):
            for i in range(ITERATIONS):
                chord_progression = smart_walk_generation(G_Undirected, G_Multi, id_to_chord, genre, i)
                while len(chord_progression) < MAX_SONG_LENGTH * 0.8:
                    chord_progression = smart_walk_generation(G_Undirected, G_Multi, id_to_chord, genre, i)
                generated_songs.append(chord_progression)
        elif (type == "node2vec"):
            for i in range(ITERATIONS):
                chord_progression = node2vec(G_Multi, G_nx, id_to_chord, genre, i)
                while len(chord_progression) < MAX_SONG_LENGTH * 0.8:
                    chord_progression = node2vec(G_Multi, G_nx, id_to_chord, genre, i)
                generated_songs.append(chord_progression)

        fname = type + "_generated_" + genre + "_songs.txt"
        #Save generated song
        f = open(fname, "w")
        index = 1
        for song in generated_songs:
            f.write(str(index) + ". ")
            for chord in song:
                f.write(str(chord) + " ")
            f.write("\n")
            index += 1

if __name__ == "__main__":
    for type in ["random", "smart", "node2vec"]:
        main(type)
