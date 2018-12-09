import load_genre_graphs as ld
import analysis
import snap
import random

ITERATIONS = 100
OUT_THRESHOLD = 0.7
MAX_SONG_LENGTH = 100


def random_walk_generation(G_Multi, node, i):
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


def smart_walk_generation(G_Multi, clusters, node, i = ""):
    #MUST GET FROM NEEL
    clusters = Neel.get_clusters(genre) #List of sers of node IDs
    visited = set()
    chord_progression = []
    length = 0

    #instantiate song graph
    G_Directed_i = snap.TNGraph.New() #song graph i

    #Get node in largest cluster
    #1. Get index of largest element of clusters
    cluster_index = argmax([len(x) for x in clusters])
    # Choose randomly from this
    node = random.choice(clusters[cluster_index])

    G_Directed_i.AddNode(node.GetId())
    visited.add(node.GetId())

    #while not at last node in the song
    while node.GetOutDeg() > 0 and length < MAX_SONG_LENGTH:
        nodeID = node.GetId()
        chord_progression.append(id_to_chord[nodeID])
        rand = random.choice(0, 1)

        #With probability X stay within cluster
        if rand < OUT_THRESHOLD:
            dstID = random.choice(clusters[cluster_index])

        else:
            neighbors = [node.GetNbrNId(x) for x in xrange(node.GetOutDeg())]
            dstID = random.choice(clusters[cluster_index].union([visited, neighbors]))
            if dstID not in clusters[cluster_index]:
                cluster_index = [x for x in clusters where dstID in x][0]

            if not G_Directed_i.IsNode(dstID): #if edge dst isn't a node in G_Directed_i, add it
                G_Directed_i.AddNode(dstID)
            G_Directed_i.AddEdge(nodeID, dstID)
            node = G_Multi.GetNI(dstID)
            length += 1

    #add last chord to list
    chord_progression.append(id_to_chord[nodeID])

    if i:
        file_name = "generated_songs/smart_generated_" + genre + "_song_" + str(i+1) + ".txt"
    else:
        file_name =  "generated_songs/smart_generated_" + genre + "_song.txt"

    snap.SaveEdgeList(G_Directed_i, file_name)

    fname = "Random_generated_" + genre + "_songs.txt"
    return fname, chord_progression


def main(Random=True):
    for genre in ["rock, jazz"]:
        #Instantiate datasets
        G_Multi, G_Directed, _, id_to_chord = ld.load_genre_graphs(genre)

        if (Random == True):
            generated_songs = [] #list of song graphs
            for i in range(ITERATIONS):
                fname, chord_progression = random_walk_generation(G_Multi, node, i)
                generated_songs.append(chord_progression)
        else:
            fname, chord_progression = smart_walk_generation(G_Multi, node)

        #Save generated song
        f = open(fname, "w")
        index = 1
        for song in generated_songs:
            f.write(str(index) + ". ")
            for chord in song:
                f.write(str(chord) + " ")
            f.write("\n")
            index += 1
