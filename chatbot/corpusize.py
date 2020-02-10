#############################################################
# Make a raw text file a corpus for training in json format #
#############################################################

from bs4 import BeautifulSoup as bsoup
import requests as req

r = req.get('http://bay12games.com/dwarves')
print(r.text)

print('a')
