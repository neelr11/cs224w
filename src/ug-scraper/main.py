import sys
from genre_scraper import get_page_urls
from song_scraper import scrape_song
import urllib2

genres = ['Rock', 'Country', 'Pop']
genre_to_id = {
    'Rock': 4,
    'Country': 49,
    'Pop': 14,
}



def get_urls():
    # Need to redo this for Electronic etc....****
    for genre in genres:
        get_page_urls('https://www.ultimate-guitar.com/explore?genres[]='+str(genre_to_id[genre]), genre)


def main(genre, starting_song):
    num_urls = 0
    with open('../data/song_ids.txt', 'r') as f2:
        song_ids = [int(song_id.strip()) for song_id in f2.readlines()]
    print("**********************")
    print("Starting genre: %s" % genre)

    song_id_file = open('../data/song_ids.txt', 'a')

    with open('../data/song_urls/'+genre+'.txt', 'r') as f:
        song_urls = [song_url.strip() for song_url in f.readlines()]
        num_songs = len(song_urls)
        i = starting_song
        for j in range(starting_song, len(song_urls)):
            song_id = scrape_song(song_urls[j], song_ids, '../data/song_chords/'+genre+'/')
            if song_id != -1:
                song_ids.append(song_id)
                num_urls += 1
                song_id_file.write("%i\n" % song_id)

            print('Song %i...(%f) done with genre %s' % (i, float(i)/num_songs, genre))
            i += 1
            print num_urls
    song_id_file.close()

#Pass one of the genres in the above list
if __name__ == "__main__":
    #get_urls()
    main(sys.argv[1], int(sys.argv[2]))
