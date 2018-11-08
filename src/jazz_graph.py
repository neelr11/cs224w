import snap

from jazz_parser import parser
from jazz_parser import chord
from jazz_parser import util
import json

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
    edges_by_song = []
    chord_set_by_song = []

    for song in chord_songs:
        song_edges = []
        song_chords = set()
        for i in range(len(song)-1):
            c1 = parse_chord(song[i])
            c2 = parse_chord(song[i+1])
            if c1 != c2:
                edges.append((c1, c2))
                song_edges.append((c1, c2))

            chord_set.add(c1)
            chord_set.add(c2)

            song_chords.add(c1)
            song_chords.add(c2)
        edges_by_song.append(song_edges)
        chord_set_by_song.append(song_chords)


    return sorted(chord_set), edges, edges_by_song, chord_set_by_song

if __name__=='__main__':

    chord_set, edges, edges_by_song, chord_set_by_song = read_data()
    G = snap.PNEANet.New()

    chords_dict = {}
    labels = snap.TIntStrH()
    for i, c in enumerate(chord_set):
        labels[i] = c
        chords_dict[c] = i
        G.AddNode(i)

    for edge in edges:
        G.AddEdge(chords_dict[edge[0]], chords_dict[edge[1]])

    with open('chords_dict_jazz.txt', 'w') as file:
        file.write(json.dumps(chords_dict))
    snap.SaveEdgeList(G, "../data/genre_graphs/jazz_graph/jazz_graph.txt", "Save as tab-separated list of edges")

    print 'num chords', G.GetNodes()
    print 'num edges', len(edges)

    # save graphs by song
    for i in range(len(chord_set_by_song)):
        G = snap.PNEANet.New()
        chords = chord_set_by_song[i]
        edges = edges_by_song[i]
        for id,c in enumerate(chord_set):
            G.AddNode(id)
        for edge in edges:
            G.AddEdge(chords_dict[edge[0]], chords_dict[edge[1]])
        snap.SaveEdgeList(G, "../data/song_graphs/jazz_graphs/" + str(i) + ".txt", "Save as tab-separated list of edges")
