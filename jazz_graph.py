import snap

from jazz_parser import parser
from jazz_parser import chord
from jazz_parser import util

from collections import Counter

lilypond_to_our_schema = {
    'c': 'C',
    'cis': 'Db',
    'd': 'D',
    'dis': 'Eb',
    'e': 'E',
    'f': 'F',
    'fis': 'Gb',
    'g': 'G',
    'gis': 'Ab',
    'a': 'A',
    'ais': 'Bb',
    'b': 'B',
}

def parse_chord(chord):
    if ':' in chord:
        chord = lilypond_to_our_schema[chord[:chord.index(':')]] + chord[chord.index(':')+1:]
    else:
        chord = lilypond_to_our_schema[chord]
    return chord

def read_data():  
    songs = parser.parse(no_durations=True, remove_empties=True, no_octaves=True)
    chord.clean_up_chords(songs)
    chord_songs = util.get_chord_songs(songs)

    chord_set = set()
    edges = []

    for song in chord_songs:
        for i in range(len(song)-1):
            c1 = parse_chord(song[i])
            c2 = parse_chord(song[i+1])
            if c1 != c2:
                edges.append((c1, c2))

            chord_set.add(c1)
            chord_set.add(c2)

    return sorted(chord_set), edges

if __name__=='__main__':

    chord_set, edges = read_data()

    G = snap.PNGraph.New()

    chords_dict = {}
    labels = snap.TIntStrH()
    for i, c in enumerate(chord_set):
        labels[i] = c
        chords_dict[c] = i
        G.AddNode(i)

    for edge in edges:
        G.AddEdge(chords_dict[edge[0]], chords_dict[edge[1]])

    print 'num chords', G.GetNodes()
    print 'num edges', len(edges)
    print 'num unique edges', G.GetEdges()

    snap.DrawGViz(G, snap.gvlNeato, 'jazz.png', 'jazz chords', labels)
