import requests
from bs4 import BeautifulSoup
import urlparse
import json


url = "https://www.walmart.com/ip/54649026"
result = requests.get(url)
soup = BeautifulSoup(result.text, "html.parser")

# This will look for a meta tag with the og:image property
og_image = (soup.find('meta', property='og:image') or
                    soup.find('meta', attrs={'name': 'og:image'}))
if og_image and og_image['content']:
    print og_image['content']
    print ''

# This will look for a link tag with a rel attribute set to 'image_src'
thumbnail_spec = soup.find('link', rel='image_src')
if thumbnail_spec and thumbnail_spec['href']:
    print thumbnail_spec['href']
    print ''


def getLst():
    image = """<img src="%s"><br />"""
    tlist=[]
    for img in soup.findAll("img", src=True):
        tlist+=[img["src"]]
    return tlist

image = """<img src="%s"><br />"""
for img in soup.findAll("img", src=True):
   print img["src"]#image % urlparse.urljoin(url, img["src"])
   print ''
