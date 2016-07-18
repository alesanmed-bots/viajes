# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup as bs
import urllib.request
from tools.parse_travel import parse_travel
from tools.user_agent import get_user_agent
import time

URL = "http://www.exprimeviajes.com/"

"""
req = urllib.request.Request(
                    URL,
                    data=None,
                    headers= {
                        'User-Agent': get_user_agent()
                        }
                    )
document = urllib.request.urlopen(req)
"""

# Only for the development stage
with open('test.txt', 'r') as file:
    document = file.read()

web = bs(document, "html.parser")
sales = []

for h2 in web.findAll('h2', class_="entry-title"):
    link = h2.a['href']
    title = h2.a.text.strip().split()
    price = int(title[title.index("EUROS") - 1])
    sales.append(parse_travel(link, price))
    time.sleep(3)

print(sales)