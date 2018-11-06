import re

chords_dict = {
  '6': ['6.9'],
  '7': ['7.9', '9', '11', '13', '7.13', '9-', '7.9-', '7.9+', '7.11', '7.11+', 'sus4.9', '7.5-.9+', '7.5-.9-', '7~', '7.4', '5.11', '9.11+', 'sus4.7'],
  'maj7': ['maj7.9', 'maj7.11+', 'maj9'],
  'm7': ['m', 'm6', 'm9', 'm7.9', 'm11', 'm7.11', 'm7.9-', 'm7+', 'm6.9'],
  'm7.5-': ['7.3-.5-.9-.11-.13-', '7.3-.5-.9-.11-.13-'],
  'dim7': ['dim'],
  '7.5+': ['5+', 'aug', '7.5+', '7.5+.9-', '7.9-.5+', '5+.9', '5+9', '9.5+', '7.5+.9+', '5+7'],
}

chords_dict2 = {
  'c:maj7': ['c', 'c:', 'c:6'],
  'cis:7': ['cis', 'cis:6'],
  'd:7': ['d', 'd:6'],
  'dis:7': ['dis', 'dis:6'],
  'e:7': ['e', 'e:6'],
  'f:maj7': ['f', 'f:6', 'f:maj1'],
  'fis:7': ['fis', 'fis:6'],
  'g:7': ['g', 'g:6'],
  'gis:7': ['gis', 'gis:6'],
  'a:7': ['a', 'a:6'],
  'ais:7': ['ais', 'ais:6'],
  'b:7': ['b', 'b:6'],
}

chords_dict3 = {
  '6': [],
  '6.9': [],
  '7': ['7~'],
  '5.11': [],
  'sus4.7': ['7.4'],
  '7.5-.9+': [],
  '7.5-.9-': [],
  '7.5+': ['5+7'],
  '7.5+.9': ['5+.9', '5+9', '9.5+'],
  '7.5+.9-': [],
  '7.9-.5+': [],
  '7.5+.9+': [],
  '9-': ['7.9-'],
  '9+': ['7.9+'],
  '9': ['7.9'],
  '9.11+': [],
  'sus4.9': [],
  '11': ['7.11'],
  '11+': ['7.11+'],
  '13': ['7.13'],
  'maj7': [],
  'maj9': ['maj7.9'],
  'maj7.11+': [],
  'm': [],
  'm6': [],
  'm6.9': [],
  'm7': [],
  'm7.5+': ['m7+'],
  'm7.9-': ['m7.9-'],
  'm9': [],
  'm11': ['m7.11'],
  '7.3-.5-.9-.11-.13-': [],
  'dim': [],
  'dim7': [],
  'aug': ['5+'],
}

def clean_up_chord(token):
  if token == 'c,':
    token = 'c'
  pattern = '([a-z]*)([\',?!>-]*)([\d.*]*)(.*)'
  result = re.match(pattern, token)
  note, style, duration, remaining = result.group(1,2,3,4)
  for chord in chords_dict3:
    if remaining[1:] in chords_dict3[chord]:
      token = note + duration + ':' + chord
  if token[len(token)-1] == ':':
    token = token[:-1]
  return token

def clean_up_chords(songs):
  for song in songs:
    for m in song.chord_measures:
      for i in range(len(m)):
        m[i] = clean_up_chord(m[i])

def substitute_chord(token):
  pattern = '([a-z]*)([\',?!>-]*)([\d.*]*)(.*)'
  result = re.match(pattern, token)
  note, style, duration, remaining = result.group(1,2,3,4)
  for chord in chords_dict:
    if remaining[1:] in chords_dict[chord]:
      token = note + duration + ':' + chord
  for chord in chords_dict2:
    if token in chords_dict2[chord]:
      token = chord
  return token

def substitute_chords_from_list(chords):
  for i in range(len(chords)):
    chords[i] = substitute_chord(chords[i])

def substitute_chords(songs):
  for song in songs:
    for m in song.chord_measures:
      for i in range(len(m)):
        m[i] = substitute_chord(m[i])
