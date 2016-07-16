# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup as bs
from urllib.request import urlopen

URL = "http://www.exprimeviajes.com/"

# document = urlopen(URL)

# Only for the development stage
with open('test.txt', 'r') as file:
    document = file.read()

web = bs(document, "html.parser")
sales = []

for h2 in web.findAll('h2', class_="entry-title"):
    link = h2.a['href']
    title = h2.a.text.strip().split()
    sales.append((link, int(title[title.index("EUROS") - 1])))

print(sales)