import load_genre_graphs as ld
import analysis
import snap
import random

ITERATIONS = 100
MAX_SONG_LENGTH = 100

for genre in ["rock", "jazz"]:
    #G_Multi, G_Directed, _, id_to_chord = analysis.main(genre)
    G_Multi, G_Directed, _, id_to_chord = ld.load_genre_graphs(genre)
    generated_songs = [] #list of song graphs
    for i in range(ITERATIONS):
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
            node_dsts = snap.TIntV() #dstNodeID to count (edges to that dstNodeID)
            neighbors = [node.GetNbrNId(x) for x in xrange(node.GetOutDeg())]
            dstID = random.choice(neighbors)
            if not G_Directed_i.IsNode(dstID): #if edge dst isn't a node in G_Directed_i, add it
                G_Directed_i.AddNode(dstID)
            G_Directed_i.AddEdge(nodeID, dstID)
            node = G_Multi.GetNI(dstID)
            length += 1

        #add last chord to list
        chord_progression.append(id_to_chord[nodeID])

        generated_songs.append(chord_progression)
        file_name = "generated_" + genre + "_song_" + str(i) + ".txt"
        snap.SaveEdgeList(G_Directed_i, file_name)

    fname = "Generated_" + genre + "_songs.txt"
    f = open(fname, "w")
    index = 1
    for song in generated_songs:
        f.write(str(index) + ". ")
        for chord in song:
            f.write(str(chord) + " ")
        f.write("\n")
        index += 1
