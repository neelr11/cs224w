import chord
import numpy as np
import parser
import re
from collections import defaultdict
import operator

duration_dict = {
  '1': 1,
  '2': .5,
  '4': .25,
  '8': .125,
  '16': .0625,
  '2.': .75,
  '2..': .875,
  '4.': .375,
  '8.': .1875,
  '8*5': .625,
}

def make_bigrams(arr):
  bigrams = defaultdict(list)
  for i in range(len(arr)-1):
    bigrams[arr[i]].append(arr[i+1])
  return bigrams

def get_start_probs(songs, chord_classes):
  starting_chord_counts = defaultdict(int)
  for song in songs:
    starting_chord_counts[song.chord_measures[0][0]] += 1
  for c in chord_classes:
    starting_chord_counts[c] += 1
  start_probs = np.zeros(len(chord_classes))
  total = sum([starting_chord_counts[c] for c in chord_classes])
  for c in starting_chord_counts:
    start_probs[chord_classes.index(c)] = starting_chord_counts[c] * 1. / total
  return start_probs

def get_transition_probs(songs, chord_classes):
  chords = get_chords(songs)
  bigrams = make_bigrams(chords)
  # laplace smoothing
  # for c in bigrams:
  #   for transition_c in chord_classes:
  #     bigrams[c].append(transition_c)
  trans_probs = np.zeros((len(chord_classes), len(chord_classes)))
  for c in chord_classes:
    transitions = bigrams[c]
    transition_probs = [transitions.count(x) + 1 for x in chord_classes]
    transition_probs = [x * 1. / sum(transition_probs) for x in transition_probs]
    trans_probs[chord_classes.index(c)] = transition_probs
  return trans_probs

def strip_duration_from_chord(token):
  if token == 'START' or token == 'END':
    return token
  pattern = '([a-z]*)([\',]*)([?!>-]*)([\d.*]*)(.*)'
  result = re.match(pattern, token)
  note, octave, style, duration, remaining = result.group(1,2,3,4,5)
  token = note + remaining
  return token

def strip_durations_from_chords(chords):
  for i in range(len(chords)):
    chords[i] = strip_duration_from_chord(chords[i])

def get_note_classes_from_note_groups(note_groups):
  notes = []
  for note_g in note_groups:
    notes.extend(note_g)
  return list(sorted(set(notes)))

def strip_duration(token):
  if token == 'START' or token == 'END':
    return token
  pattern = '([a-z]*)([\',]*)([?!>-]*)([\d.*]*)(.*)'
  result = re.match(pattern, token)
  note, octave, style, duration, remaining = result.group(1,2,3,4,5)
  if ':' in token: # chord (style is always empty)
    token = note + remaining
  else: # note - remove extras
    token = note + octave
  return token

def strip_durations_from_note_groups(note_groups):
  for note_g in note_groups:
    for i in range(len(note_g)):
      note_g[i] = strip_duration(note_g[i])
      

def get_notes_under_chords(songs):
  note_groups = []
  lengths = []
  for song in songs:
    prev_length = len(note_groups)
    for note_m, chord_m in zip(song.note_measures, song.chord_measures):
      if note_m[0] == 'START' or note_m[0] == 'END':
        note_groups.append(note_m)
        continue
      chord_i = 0
      note_i = 0
      note_group = []
      while note_i < len(note_m) and chord_i < len(chord_m):
        note_group.append(note_m[note_i])
        note_time = sum([get_time(note_m[i]) for i in range(note_i+1)])
        chord_time = sum([get_time(chord_m[i]) for i in range(chord_i+1)])
        if note_time >= chord_time:
          note_groups.append(note_group[:])
          chord_i += 1
          if note_time == chord_time:
            note_group = []
          else:
            note_group = [note_m[note_i]]
        note_i += 1

      # for note_i in range(len(note_m)):
      #   note_group.append(note_m[note_i])
      #   note_time += get_time(note_m[note_i])
      #   # print note_group
      #   # print note_time, chord_time
      #   if note_time >= chord_time:
      #     note_groups.append(note_group[:])
      #     chord_i += 1
      #     if chord_i < len(chord_m):
      #       chord_time += get_time(chord_m[chord_i])
      #     else:
      #       break
      #     # print note_group
      #     note_group = []
      #     if note_time == chord_time:
      #       note_i += 1
      #     else:
      #       # if note_i < len(note_m):
      #       #   note_time += get_time(note_m[note_i])
      #   else:
      #     note_i += 1
          # if note_i < len(note_m):
          #   note_time += get_time(note_m[note_i])
      if note_i == len(note_m):
        for _ in range(chord_i, len(chord_m)):
          # print note_group
          note_groups.append([note_m[-1]])
      if chord_i == len(chord_m):
        for i in range(note_i, len(note_m)):
          note_groups[-1].append(note_m[i])
    lengths.append(len(note_groups) - prev_length)
  return note_groups, lengths

def get_time(token):
  duration = get_duration(token)
  time = duration_dict[duration]
  return time

def get_duration(token):
  token_list = [token]
  _, durations_list = separate_durations(token_list)
  return durations_list[0]

def extract_features(songs):
  note_measures = get_note_measures(songs)
  note_classes = get_note_classes(songs)
  X = np.zeros((len(note_measures),12))
  for i,m in enumerate(note_measures):
    for note in m:
      if note != 'r':
        X[i,note_classes.index(note)] += 1
  return X

def extract_labels(songs):
  chords = get_first_chords(songs)
  chord_classes = list(sorted(set(chords)))
  y = np.zeros(len(chords))
  for i,c in enumerate(chords):
    y[i] = chord_classes.index(c)
  return y

def separate_durations(tokens):
  pitches = []
  durations = []
  for token in tokens:
    if token == 'START' or token == 'END':
      pitches.append(token)
      durations.append(token)
      continue
    pattern = '([a-z]*)([\',?!>-]*)([\d.*]*)(.*)'
    result = re.match(pattern, token)
    pitch, style, duration, remaining = result.group(1,2,3,4)
    pitches.append(pitch)
    durations.append(duration)
  return pitches, durations

def remove_weird_notes(notes):
  new_notes = []
  for note in notes:
    if note == 'START' or note == 'END':
      new_notes.append(note)
      continue
    pattern = '([a-z]*)([\',?!>-]*)([\d.*]*)(.*)'
    result = re.match(pattern, note)
    pitch, style, duration, remaining = result.group(1,2,3,4)
    if duration == '.' or duration == '5':
      continue
    if duration == '3':
      note = pitch + style + '2.' + remaining
    new_notes.append(note)
  return new_notes

def get_chord_counts(songs):
  chords = defaultdict(int)
  for song in songs:
    for m in song.chord_measures:
      for i in range(len(m)):
        chords[m[i]] += 1
  return chords

def get_chords(songs):
  chords = []
  for song in songs:
    for m in song.chord_measures:
      chords.extend(m)
  return chords

def get_chord_songs(songs):
  arr = []
  for song in songs:
    x = []
    for m in song.chord_measures:
      for c in m:
        x.append(c)
    arr.append(x)
  return arr

def get_first_chords(songs):
  chords = []
  for song in songs:
    for m in song.chord_measures:
      chords.append(m[0])
  return chords

def get_chord_measures(songs):
  chords = []
  for song in songs:
    for m in song.chord_measures:
      chords.append(m)
  return chords

def get_chord_classes(songs):
  chords = get_chords(songs)
  return list(sorted(set(chords)))

def get_note_counts(songs):
  notes = defaultdict(int)
  for song in songs:
    for m in song.note_measures:
      for i in range(len(m)):
        notes[m[i]] += 1
  return notes

def get_notes(songs):
  notes = []
  for song in songs:
    for m in song.note_measures:
      notes.extend(m)
  return notes

def get_note_measures(songs):
  notes = []
  for song in songs:
    for m in song.note_measures:
      notes.append(m)
  return notes

def get_note_classes(songs):
  notes = get_notes(songs)
  return list(sorted(set(notes)))

def main():
  songs = parser.parse(no_durations=True, no_octaves=True)
  chord.substitute_chords(songs)

  # for song in reversed(songs):
  #   for c, n in zip(song.chord_measures, song.note_measures):
  #     print c, n

  chords = get_chord_counts(songs)


  for k,v in sorted(chords.items(), key=operator.itemgetter(1)):
    print '{}\t\t{}'.format(k,v)

  top_chords = [k for k,v in sorted(chords.items(), key=operator.itemgetter(1))]
  print top_chords[-17:]

  # print len(set(chords)), sum(chords[x] for x in chords)
  # print len(set(notes)), len(notes)

  # notes = get_notes(songs)
  # for note in sorted(set(notes)):
  #   print note


if __name__=='__main__':
  main()
