import sys
from genre_scraper import get_page_urls
from song_scraper import scrape_song
import urllib2

genres = ['Rock', 'Electronic', 'Country', 'Pop']

# for genre in genres:
#     get_page_urls('https://www.ultimate-guitar.com/explore?genres[]='+str(genre_to_id[genre]), genre)

def main():
    num_urls = 0
    song_ids = []
    for genre in genres:
        print("**********************")
        print("Starting genre: %s" % genre)
        with open('../data/song_urls/'+genre+'.txt', 'r') as f:
            song_urls = [song_url.strip() for song_url in f.readlines()]
            num_songs = len(song_urls)
            i = 0
            for song_url in song_urls:
                song_id = scrape_song(song_url, song_ids, '../data/song_chords/'+genre+'/')
                if song_id != -1:
                    song_ids.append(song_id)
                    num_urls += 1
                print('Song %i...(%f) done with genre %s' % (i, float(i)/num_songs, genre))
                i += 1
                break
                print num_urls

#Pass one of the genres in the above list
if __name__ == "__main__":
    main()
