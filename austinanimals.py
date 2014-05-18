import tweepy
from geopy import geocoders
from bs4 import BeautifulSoup
from urllib2 import urlopen, Request

import json

import re

import pdb

consumer_key = "QgUvx8L4wcyhVbD7X2GkXwyYT"
consumer_secret = "dwRK6TtYsTAALzOSBWhmpujC4eoeVzqYxzfono0irO8B8bvwzL"

access_token = "19383289-bSwFXjI56RLY0HD4fNmHB1TH48Zy32VWwkN8mcbsl"
access_token_secret = "WbXrw6fwI7tADxmLifd2HMFSb7r29QW3Dk9z39HCF2SWH"

lat_ofs = 5e-4
lng_ofs = 5e-4

# empty object to hold pet information
class petClass:
    def __init__(self):
        self.addr = None
        self.lat = None
        self.link = None
        self.image_link = None
        self.lng = None
        self.petID = None
        self.pet_type = None
        self.petinfo = None
        self.place = None


def make_soup(url):
    # need to set user-agent
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = Request(url,headers=hdr)
    page = urlopen(req)

    return BeautifulSoup(page, "lxml")

def get_pet_image(url):

    image_link = ''
    soup = make_soup(url)

    if soup:
        table = soup.find('table')
    if table:
        image_link = table.find('img')

    # to be used outside from petharbor
    return str(image_link).replace('src=\"', 'src=\"http://www.petharbor.com/')

def geocode(g, addr):

    # try Texas
    results = g.geocode(addr+' Texas', exactly_one=False)

    for place, (lat, lng) in results:
        if re.search(r'(Austin|Lakeway|Llano|Del Valle|Manor|Driftwood)', place):
            # print "%s: %.5f, %.5f" % (place, lat, lng)  
            return place, (lat, lng)

    for place, (lat, lng) in results:
        if re.search(r'TX', place):
            return place, (lat, lng)

    # try Austin TX
    results = g.geocode(addr+' Austin, Texas', exactly_one=False)

    for place, (lat, lng) in results:
        if re.search(r'(Austin|Lakeway|Llano|Del Valle|Manor|Driftwood)', place):
            # print "%s: %.5f, %.5f" % (place, lat, lng)  
            return place, (lat, lng)

    for place, (lat, lng) in results:
        if re.search(r'TX', place):
            return place, (lat, lng)


    return results[0]

def get_pet_info(url):
    'Obtain pet information and return the list of petClass objects'

    soup = make_soup(url)

    textbody = soup.find("div", id="text")

    if textbody==None:
        # url_redirect = re.search(r'url=(.+)\"\s',str(soup.find("meta", attrs={'content': re.compile('url')}))).group(1)

        url_redirect = re.search(r'url=(.+)\"\s', \
                                 str(soup.find("meta", attrs={'http-equiv': re.compile(r'(r|R)efresh')}))).group(1)

        print "url_redirect = " + url_redirect

        soup = make_soup(url_redirect)
        textbody = soup.find("div", id="text")


    # print textbody
    text_contents = textbody.contents

    # geocoding using Google V3 API
    g = geocoders.GoogleV3(api_key='AIzaSyB7LvwvLJN0l04rFfHbIyUBsqi61vP6qWA')

    pets = []
    for i in range(len(text_contents)/2):
        petregex = re.search(r'(\d+\))(.+):.*(DOG|CAT|BIRD)(.*)', text_contents[i*2])

        if petregex:
            pet = petClass() 

            petID = petregex.group(2).replace(' ','')
            pettype = petregex.group(3).replace(' ','')
            petdesc = petregex.group(4).split(',')
            addr = ''

            petinfo = []
            for j in range(len(petdesc)):
                if (len(petdesc[j]) != 0) or (re.match('\s+',petdesc[j]) != None):
                    addr_re = re.search(r'found at (.*)',petdesc[j])
                    if addr_re:
                        addr = addr_re.group(1)
                        pet.addr = addr.replace('/', ' and ')

                        place, (lat, lng) = geocode(g, pet.addr)  
                        pet.place = place
                        pet.lat = lat + lat_ofs* (random.random())
                        pet.lng = lng + lng_ofs* (random.random())
                    else:
                        petinfo.append(petdesc[j].strip())

            link =  text_contents[i*2+1].string
            image_link = get_pet_image(link)

            if any([a==None for a in [petID, pettype, petdesc]]):
                print petregex

            pet.petID = petID
            pet.pet_type = pettype
            pet.petinfo = petinfo
            pet.link = link
            pet.image_link = image_link

            pets.append(pet)

        else:
            print "regex failed!"

    return pets


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

A = []
for i in range(len(tinyuri_urls)):
    A += get_pet_info(tinyuri_urls[i])

for pt in A:
    # print pt.petID
    # print pt.pet_type
    # print pt.addr
    # print pt.petinfo
    # print pt.link 
    print pt.place
    # print pt.lat 
    # print pt.lng


with open('pets.js', 'w') as f:
    f.write('var pet_arr = [];\n')
    for i in range(len(A)):
        f.write('pet_arr.push({0:s});\n'.format(json.dumps(A[i].__dict__)))



# # geocoding using Google V3 API
# g = geocoders.GoogleV3(api_key='AIzaSyB7LvwvLJN0l04rFfHbIyUBsqi61vP6qWA')


