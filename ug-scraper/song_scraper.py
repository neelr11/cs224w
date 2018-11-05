
from bs4 import BeautifulSoup
import urllib2
import re
import json
from page_scraper import get_page_object

#Scrapes a song and saves key and chord progressions to a .txt file


# Scrape a song and save it to a txt file in the following format:
# Line 1 - Key
# Lines 2-end: Chord progression
# Return song_id if success
# Return -1 if
#   - Song not in 'Standard' Tuning
#   - Key not given
#   - Not a Chords tab
#   - Song id already seen
#   - Miscellaneous Parsing error
def scrape_song(url, song_ids, path):
    print("**************")
    song_obj = get_page_object(url)
    if song_obj == None:
        print('Could not find song object')
        return -1
    song_name, artist_name, tab_type, song_id, key, tuning, tab_content = get_song_data(song_obj)
    print('Song \'%s\' found' % song_name)
    if int(song_id) in song_ids:
        print('Song \'%s\' already parsed' % song_name)
        return -1
    if key == None:
        print('Song \'%s\' no given key' % song_name)
        return -1
    if tab_type != "Chords":
        print('Song \'%s\' not chords' % song_name)
        return -1
    if tuning != "Standard":
        print('Song \'%s\' not standard tuning' % song_name)
        return -1

    print('Song \'%s\' chords being saved!' % song_name)
    chords = re.findall('\[ch\](.*?)\[\/ch\]', tab_content)
    save_chords_to_txt(chords, key, song_name, artist_name, path)
    return int(song_id)

def save_chords_to_txt(chords, key, song_name, artist_name, path):
    file_name = "".join([c for c in song_name+'-'+artist_name if c.isalpha() or c.isdigit() or c==' ' or c=='-']).rstrip()
    with open(path + file_name, 'w') as f:
        f.write("Key:%s\n" % key)
        for i in range(len(chords)-1):
            f.write("%s\t%s\n" % (chords[i], chords[i+1]))

def get_song_data(song_obj):
    song_name = (song_obj[u'data'][u'tab'][u'song_name'])
    artist_name = (song_obj[u'data'][u'tab'][u'artist_name'])
    tab_type = (song_obj[u'data'][u'tab'][u'type'])
    song_id = (song_obj[u'data'][u'tab'][u'song_id'])

    meta = song_obj[u'data'][u'tab_view'][u'meta']
    if u'tonality' not in meta: key = None
    else: key = (song_obj[u'data'][u'tab_view'][u'meta'][u'tonality'])
    if u'tuning' not in meta: tuning = None
    else: tuning = (song_obj[u'data'][u'tab_view'][u'meta'][u'tuning'][u'name'])
    tab_content = (song_obj[u'data'][u'tab_view'][u'wiki_tab'][u'content'])
    return song_name, artist_name, tab_type, song_id, key, tuning, tab_content
