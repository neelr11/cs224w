from bs4 import BeautifulSoup
import json
import requests
import urllib2

#Scrape a UG page and return the JSON object that contains relevant HTML data for the page

#window.UGAPP.store.page stores page data
SONG_OBJ_NAME = 'window.UGAPP.store.page'

# Returns None if parsing error or page object not found
def get_page_object(url):
    print (url)
    song_obj = None
    try:
        print("Parsing url %s" % url)
        headers = {'User-Agent':'Mozilla/5.0'}
        req = urllib2.Request(url,headers=headers)
        page = urllib2.urlopen( req )
    except (urllib2.HTTPError, urllib2.URLError), e:
        print ('Parsing Error')
        return song_obj

    soup = BeautifulSoup(page, 'html.parser')
    script_tags = soup.find_all('script')
    found_tag = False

    for script_tag in script_tags:
        if SONG_OBJ_NAME in script_tag.text:
            song_obj = get_song_object(script_tag.text)
            found_tag = True
            break
    if not found_tag:
        print('Error on %s, could not find song object' % url)
    return song_obj

# clean up and return json object
def get_song_object(script_tag_text):
    script_tag_text = script_tag_text.strip()
    script_tag_text = script_tag_text.replace("window.UGAPP.store.page =", "")
    script_tag_text = script_tag_text[:-1]
    return (json.loads(script_tag_text))
