
from bs4 import BeautifulSoup
import urllib2
from page_scraper import get_page_object


# For each genre, scrape all Chords tab URLs and save them to a file
# URLs can then be used by song_scraper to scrape the chords.

genre_url_prefix = 'https://www.ultimate-guitar.com/explore?genres[]='
genre_url_suffix = '&order=hitstotal_desc&type[]=Chords'
genre_to_id = {
    'Rock': 4,
    'Country': 49,
    'Pop': 14,
}

# Gets max 1000 songs
def get_page_urls(url, genre):
    print("**********")
    print("Parsing URLS for genre %s" % genre)
    song_obj = get_page_object(genre_url_prefix+str(genre_to_id[genre])+genre_url_suffix)
    num_songs = song_obj[u'data'][u'totalResults']
    print('Num songs: %i' %num_songs)
    numPagesToScrape = num_songs/50 + 1
    if numPagesToScrape > 20: numPagesToScrape = 20
    numTabs = 0
    tab_urls = []
    for i in range(numPagesToScrape):
        url = genre_url_prefix+str(genre_to_id[genre])+genre_url_suffix
        if i > 0: url += "&page=" + str(i+1)
        song_obj = get_page_object(url)
        tabs = song_obj[u'data'][u'data'][u'tabs']
        for tab in tabs:
            if tab['type_name'] == "Chords":
                tab_urls.append(tab['tab_url'])
                numTabs += 1
    with open('../data/song_urls/'+genre+'.txt', 'w') as f:
        for tab_url in tab_urls:
            f.write(tab_url+"\n")

    print('Total Tabs for genre %s: %i' % (genre, numTabs))
    #print (song_obj)
