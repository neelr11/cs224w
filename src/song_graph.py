from load_song_graphs import load_song_graphs
import snap
import random

genre = 'rock'
graphs, id_to_chord = load_song_graphs(genre)

labels = snap.TIntStrH()
for id in id_to_chord:
    labels[id] = id_to_chord[id]

snap.DrawGViz(graphs[random.randint(0, len(graphs)-1)], snap.gvlNeato, genre+'.png', genre + ' song chords', labels)
