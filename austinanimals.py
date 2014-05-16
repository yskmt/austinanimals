import tweepy

from bs4 import BeautifulSoup
from urllib2 import urlopen, Request

import re

import pdb

consumer_key = "QgUvx8L4wcyhVbD7X2GkXwyYT"
consumer_secret = "dwRK6TtYsTAALzOSBWhmpujC4eoeVzqYxzfono0irO8B8bvwzL"

access_token = "19383289-bSwFXjI56RLY0HD4fNmHB1TH48Zy32VWwkN8mcbsl"
access_token_secret = "WbXrw6fwI7tADxmLifd2HMFSb7r29QW3Dk9z39HCF2SWH"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)


## Get the tweets from austinanimals and extract url
austinanimals_timeline = api.user_timeline(id="austinanimals", count=10)
tinyuri_urls = []

for i in range(len(austinanimals_timeline)):
    txt =  austinanimals_timeline[i].text
    search_result = re.search(r'(http.*)', txt)

    if search_result:
        tinyuri_urls.append(search_result.group(1))



def make_soup(url):
    # need to set user-agent
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = Request(url,headers=hdr)
    page = urlopen(req)

    return BeautifulSoup(page, "lxml")

# empty object to hold pet information
class petClass:
    pass

def get_pet_info(url):
    'Obtain pet information and return the list of petClass objects'

    soup = make_soup(url)

    textbody = soup.find("div", id="text")

    if textbody==None:
        # url_redirect = re.search(r'url=(.+)\"\s',str(soup.find("meta", attrs={'content': re.compile('url')}))).group(1)

        pdb.set_trace()
        url_redirect = re.search(r'url=(.+)\"\s', \
                                 str(soup.find("meta", attrs={'http-equiv': re.compile(r'(r|R)efresh')}))).group(1)

        print "url_redirect = " + url_redirect

        soup = make_soup(url_redirect)

    # pdb.set_trace()
    # print textbody
    text_contents = textbody.contents

    pets = []
    for i in range(len(text_contents)/2):
        petregex = re.search(r'(\d+\))(.+):.*(CAT|DOG)(.*)', text_contents[i*2])
        petID = petregex.group(2)
        pettype = petregex.group(3)
        petdesc = petregex.group(4).split(',')
        addr = 'N/A'

        petinfo = []
        for j in range(len(petdesc)):
            if (len(petdesc[j]) != 0) or (re.match('\s+',petdesc[j]) != None):
                addr_re = re.search(r'found at (.*)',petdesc[j])
                if addr_re:
                    addr = addr_re.group(1)
                else:
                    petinfo.append(petdesc[j])

        link =  text_contents[i*2+1].string

        pet = petClass() 
        pet.petID = petID
        pet.pet_type = pettype
        pet.addr = addr.replace('/', ' and ') + ' TX' # +'Austin'
        pet.petinfo = petinfo
        pet.link = link

        # geocoding using Google V3 API
        g = geocoders.GoogleV3(api_key='AIzaSyB7LvwvLJN0l04rFfHbIyUBsqi61vP6qWA')
        place, (lat, lng) = g.geocode(pet.addr)  

        pet.place = place
        pet.lat = lat
        pet.lng = lng



        pets.append(pet)

    return pets


A = []
for i in range(len(tinyuri_urls)):
    A += get_pet_info(tinyuri_urls[i])

for pt in A:
    print pt.petID
    print pt.pet_type
    print pt.addr
    print pt.petinfo
    print pt.link 
    print pt.place
    print pt.lat 
    print pt.lng

