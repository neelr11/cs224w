import rock_graph
import jazz_graph

rock_chords, _ = rock_graph.read_data()
jazz_chords, _ = jazz_graph.read_data()

print rock_chords
print jazz_chords
intersection = set(rock_chords).intersection(set(jazz_chords))
print sorted(intersection)
print sorted(set(rock_chords) - intersection)