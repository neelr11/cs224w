
import load_genre_graphs as ld
import analysis
import snap
import numpy as np
import random

ITERATIONS = 100
OUT_THRESHOLD = 0.7
MAX_SONG_LENGTH = 100


def random_walk_generation(G_Multi, i, id_to_chord, genre):
    chord_progression = []
    length = 0
    #instantiate song graph
    G_Directed_i = snap.TNGraph.New() #song graph i
    node = G_Multi.BegNI()
    G_Directed_i.AddNode(node.GetId())

    #while not at last node in the song
    while node.GetOutDeg() > 0 and length < MAX_SONG_LENGTH:
        nodeID = node.GetId()
        chord_progression.append(id_to_chord[nodeID])
        neighbors = [node.GetNbrNId(x) for x in xrange(node.GetOutDeg())]
        dstID = random.choice(neighbors)
        if not G_Directed_i.IsNode(dstID): #if edge dst isn't a node in G_Directed_i, add it
            G_Directed_i.AddNode(dstID)
        G_Directed_i.AddEdge(nodeID, dstID)
        node = G_Multi.GetNI(dstID)
        length += 1

    #add last chord to list
    chord_progression.append(id_to_chord[nodeID])

    file_name = "generated_songs/random_generated_" + genre + "_song_" + str(i+1) + ".txt"
    snap.SaveEdgeList(G_Directed_i, file_name)

    fname = "Random_generated_" + genre + "_songs.txt"
    return fname, chord_progression


def smart_walk_generation(G_Undirected, G_Multi, id_to_chord, genre, i = ""):
    clusters = analysis.get_communities(G_Undirected, id_to_chord) #List of sers of node IDs
    visited = set()
    chord_progression = []
    length = 0

    #instantiate song graph
    #G_Directed_i = snap.TNGraph.New() #song graph i

    #Get node in largest cluster
    #1. Get index of largest element of clusters
    cluster_index = np.argmax([len(x) for x in clusters])
    possible_next = clusters[cluster_index]
    # Choose randomly from this
    nodeID = random.choice(clusters[cluster_index])
    #G_Directed_i.AddNode(nodeID)
    node = G_Multi.GetNI(nodeID)
    #while not at last node in the song
    while length < MAX_SONG_LENGTH:
        visited.add(nodeID)
        chord_progression.append(id_to_chord[nodeID])
        rand = random.random()

        #With probability X stay within cluster
        if rand < OUT_THRESHOLD:
            dstID = random.choice(clusters[cluster_index])

        else:
            neighbors = set([node.GetNbrNId(x) for x in xrange(node.GetOutDeg())])
            possible_next = [x for x in clusters[cluster_index]]
            possible_next.extend(visited.union(neighbors))
            dstID = random.choice(possible_next)

            #Update current cluster index
            if dstID not in clusters[cluster_index]:
                cluster_index = [i for i, x in enumerate(clusters) if dstID in x][0]

            #if edge dst isn't a node in G_Directed_i, add it
            #if not G_Directed_i.IsNode(dstID):
            #    G_Directed_i.AddNode(dstID)

        #    G_Directed_i.AddEdge(nodeID, dstID)
            node = G_Multi.GetNI(dstID)
            length += 1

        #Update node to current node
        nodeID = dstID
        node = G_Multi.GetNI(nodeID)


    #add last chord to list
    chord_progression.append(id_to_chord[nodeID])

    if i is not "":
        file_name = "generated_songs/smart_generated_" + genre + "_song_" + str(i+1) + ".txt"
    else:
        file_name =  "generated_songs/smart_generated_" + genre + "_song.txt"

    #Save generated graph
    #snap.SaveEdgeList(G_Directed_i, file_name)

    fname = "Smart_generated_" + genre + "_songs.txt"
    return fname, chord_progression


def main(Random=False):
    for genre in ["rock", "jazz"]:
        #Instantiate datasets
        G_Multi, G_Directed, G_Undirected, id_to_chord = ld.load_genre_graphs(genre)
        generated_songs = [] #list of song graphs

        if (Random == True):
            for i in range(ITERATIONS):
                fname, chord_progression = random_walk_generation(G_Multi, i, id_to_chord, genre)
                generated_songs.append(chord_progression)
        else:
            for i in range(ITERATIONS):
                fname, chord_progression = smart_walk_generation(G_Undirected, G_Multi, id_to_chord, genre, i)
                generated_songs.append(chord_progression)

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
    main()
