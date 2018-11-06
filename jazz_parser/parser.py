import os
import re
import sys
import pickle

flats_to_sharps = {
  'aeses': 'g',
  'beses': 'a',
  'ceses': 'ais',
  'deses': 'c',
  'eeses': 'd',
  'feses': 'dis',
  'geses': 'f',
  'des': 'cis',
  'ees': 'dis',
  'ges': 'fis',
  'aes': 'gis',
  'bes': 'ais',
  'eis': 'f',
  'eis': 'f',
  'bis': 'c',
  'ces': 'b',
  'fes': 'e',
  # 'cis': 'des',
  # 'dis': 'ees',
  # 'fis': 'ges',
  # 'gis': 'aes',
  # 'ais': 'bes',
}

# key_order = ['c','des','d','ees','e','f','ges','g','aes','a','bes','b']
key_order = ['c', 'cis', 'd', 'dis', 'e', 'f', 'fis', 'g', 'gis', 'a', 'ais', 'b']

class Song:
  key = ''
  chord_measures = []
  note_measures = []

def strip_duration(token):
  pattern = '([a-z]*)([\',]*)([?!>-]*)([\d.*]*)(.*)'
  result = re.match(pattern, token)
  note, octave, style, duration, remaining = result.group(1,2,3,4,5)
  if ':' in token: # chord (style is always empty)
    token = note + remaining
  else: # note - remove extras
    token = note + octave
  return token

def strip_octave(token):
  pattern = '([a-z]*)([\',]*)([\d.]*)'
  result = re.match(pattern, token)
  note, octave, duration = result.group(1,2,3)
  if len(octave) == 0:
    return token
  return note + duration

def remove_empty_measures(songs):
  for song in songs:
    new_chord_measures = []
    new_note_measures = []
    for chord_m, note_m in zip(song.chord_measures, song.note_measures):
      if len(chord_m) != 0 and len(note_m) != 0:
        new_chord_measures.append(chord_m)
        new_note_measures.append(note_m)
    song.chord_measures = new_chord_measures
    song.note_measures = new_note_measures

def re_add_durations(notes):
  new_notes = []
  prev_duration = '4'
  for note in notes:
    pattern = '([a-z]*)([\',]*)([\d.]*)'
    result = re.match(pattern, note)
    note, octave, duration = result.group(1,2,3)
    if len(duration) == 0:
      duration = prev_duration
    else:
      prev_duration = duration
    new_notes.append(note + octave + duration)
  return new_notes

def interpret_token(token):
  if token[0] == 'R':
    token = 'r' + token[1:] # I had token[0] = 'r' it was a gnarly bug
  pattern = '([a-z]*)([\',]*)([?!>-]*)([\d.*]*)(.*)'
  result = re.match(pattern, token)
  note, octave, style, duration, remaining = result.group(1,2,3,4,5)
  if duration == '.': # hot bug fix
    duration = ''
  if len(duration) == 0:
    if interpret_token.prev_duration != None: # janky static variable to track last used duration
      duration = interpret_token.prev_duration
    else:
      duration = str(4)
  if ':' in token: # chord (style is always empty)
    token = note + duration + remaining
  else: # note - remove extras
    token = note + octave + duration
  interpret_token.prev_duration = duration
  return token

def is_invalid_token(token):
  if '\\' in token or '{' in token or '}' in token \
  or token[0].isdigit() or token[0] == 's' \
  or 'volta' in token or 'Fine' in token or '#' in token or '%' in token \
  or token[0] == '"' \
  or token[0] not in ['a','b','c','d','e','f','g','|','r','R'] \
  or 'end' in token or 'faster' in token or 'break' in token \
  or 'al' in token:
    return True
  return False

def clean_token(token):
  for char in ['"','[',']','(',')','/']: # / gets rid of alternate bass notes
    if char in token:
      token = token[:token.index(char)]
  return token

def parse_tokens(line, type):
  measures = []
  measure = []
  tokens = line.split()
  for i in range(len(tokens)):
    token = tokens[i]
    if '%%' in token:
      return measures
    # if '\\partial' in token: # skip partial measures
    #   return measures
    if is_invalid_token(token):
      continue
    if token == '|':
      measures.append(measure)
      measure = []
    else:
      token = clean_token(token)
      token = interpret_token(token)
      if '*' in token: # multiple measures
        index = token.index('*')
        if token[index - 1] == '1' or token[index - 1] == '.':
          n = int(token[index+1])
          token = token[:index]+token[index+2:]
          for _ in range(n-1):
            measure.append(token)
            measures.append(measure)
            measure = []
      elif '1.' in token: # measure and a half
        index = token.index('1')
        measure.append(token[:index+1]+token[index+2:])
        measures.append(measure)
        measure = []
        token = token[:index]+'2'+token[index+2:]
      measure.append(token)
  return measures

def convert_key(token):
  for note in flats_to_sharps:
    if note in token:
      return flats_to_sharps[note] + token[len(note):]
  return token

def convert_flats_chords(token):
  for note in flats_to_sharps:
    if note in token:
      return flats_to_sharps[note] + token[len(note):]
  return token

def convert_flats(token):
  for note in flats_to_sharps:
    if note in token and not token[len(note)].isalpha():
      if note == 'ces' or note == 'ceses':
        if "'" in token:
          index = token.index("'")
          token = token[:index] + token[index+1:]
        else:
          token = token[:len(note)] + ',' + token[len(note):]
      return flats_to_sharps[note] + token[len(note):]
  return token

def transpose_token(token, offset):
  if token[0] == 'R':
    token[0] = 'r'
  if token[0] == 'r':
    return token
  pattern = '([a-z]*)(.*)'
  result = re.match(pattern, token)
  note, remaining = result.group(1,2)
  i = key_order.index(note)
  if i >= offset:
    new_note = key_order[i-offset]
  else:
    new_note = key_order[i+12-offset]
  return new_note + remaining

def strip_durations(songs):
  for song in songs:
    for measure in song.chord_measures:
      for i in range(len(measure)):
        measure[i] = strip_duration(measure[i])
    for measure in song.note_measures:
      for i in range(len(measure)):
        measure[i] = strip_duration(measure[i])

def strip_chord_durations(songs):
  for song in songs:
    for measure in song.chord_measures:
      for i in range(len(measure)):
        measure[i] = strip_duration(measure[i])

def strip_octaves(note_measures):
  for measure in note_measures:
    for i in range(len(measure)):
      measure[i] = strip_octave(measure[i])

def transpose_chords(songs):
  # convert to all sharps
  for song in songs:
    key, majmin = song.key.split()
    song.key = convert_flats_chords(key) + ' ' + majmin
    for measure in song.chord_measures:
      for i in range(len(measure)):
        measure[i] = convert_flats_chords(measure[i])

  # convert to relative major
  for song in songs:
    key = song.key.split()[0]
    if song.key.split()[1] == '\\minor':
      i = key_order.index(key)
      if i >= 9:
        key = key_order[i-9]
      else:
        key = key_order[i+3]
    song.key = key

  # transpose
  for song in songs:
    key = song.key
    offset = key_order.index(key)
    for measure in song.chord_measures:
      for i in range(len(measure)):
        measure[i] = transpose_token(measure[i], offset)

def transpose_notes(note_measures, old_key, no_octaves):
  key = old_key.split()[0]
  key = convert_key(key)
  if old_key.split()[1] == '\\minor':
    i = key_order.index(key)
    if i >= 9:
      key = key_order[i-9]
    else:
      key = key_order[i+3]

  offset = key_order.index(key)
  if offset >= 6:
    key = key + ','

  # convert flats
  for measure in note_measures:
    for i in range(len(measure)):
      measure[i] = convert_flats(measure[i])

def parse(no_durations=False, no_octaves=False, remove_empties=False, special=False):

  songs = []
  path = './openbook/src/openbook/'
  for filename in os.listdir(path):
    song = Song()
    f = open(path + filename)
    lines = f.readlines()
    read_chords = False
    read_melody = False
    chord_measures = []
    note_measures = []
    for line in lines:
      if '\\endChords' in line or 'endif' in line:
        read_chords = False
        interpret_token.prev_duration = None
      if read_chords:
        chord_measures.extend(parse_tokens(line, 'chords'))
      if '\\startChords' in line and len(chord_measures) == 0:
        read_chords = True
      if 'endif' in line:
        read_melody = False
        interpret_token.prev_duration = None
      if read_melody:
        note_measures.extend(parse_tokens(line, 'notes'))
      if '\\key' in line and len(note_measures) == 0:
        song.key = line[line.index(' ')+1:-1]
        read_melody = True
      if "attributes['title']" in line:
        song.title = line[line.index('=')+1:-1]

    song.chord_measures = chord_measures

    songs.append(song)

  transpose_chords(songs)

  strip_chord_durations(songs)

  return songs
