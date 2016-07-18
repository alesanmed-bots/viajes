# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup as bs
import locale
import urllib.request
import os, sys
import time
sys.path.append(os.path.join(
                os.path.dirname(
                    os.path.dirname(
                        os.path.abspath(__file__))),
                "maps"))
from coordinates import get_coordinates
from distance import get_distance
from tools.user_agent import get_user_agent

def parse_travel(travel_url, price):
    if type(travel_url) != str:
        raise ValueError("travel_url is not a String object")
    print(travel_url)
    
    locale.setlocale(locale.LC_TIME, "es_ES.utf8")
        
    req = urllib.request.Request(
                    travel_url,
                    data=None,
                    headers= {
                        'User-Agent': get_user_agent()
                        }
                    )
    
    document = urllib.request.urlopen(req)
    # Only for the development stage
    # with open('tools/test.txt', 'r') as file:
    #    document = file.read()
        
    travel_page = bs(document, 'html.parser')
    
    content = travel_page.find(
                        "div",
                        class_="entry-content").find_all("div")[1].find_all("p")
    
    date_p = travel_page.find(
                        "div",
                        class_="entry-content").find_all("p")[2]
                        
    date = date_p.text.split(":")[-1].split("(")[0].strip().split("-")[-1].strip()
    print(date)
    date = time.strptime(date, "%B %Y")
    print(date)
    
    travel = {}
    for p in content:
        if "Ciudad de salida" in p.text:
            travel['departure'] = p.text.split(":")[-1].strip().split("(")[0].strip()
        elif "Ciudad de destino" in p.text:
            travel['destination'] = p.text.split(":")[-1].strip().split("(")[0].strip()
        elif "Ciudad de regreso" in p.text:
            travel['return_to'] = p.text.split(":")[-1].strip().split("(")[0].strip()
        elif "Tipo de billete" in p.text:
            travel['ticket_type'] = p.text.split(":")[-1].strip()
            
            
    """
    This is only made for getting the coordinates of first city, the travel map
    is NEVER modified
    if ";" in travel['destination']:
        destination_coord = get_coordinates(
                            travel['destination'].split(';')[0].strip())
    elif "," in travel['destination']:
        destination_coord = get_coordinates(
                                travel['destination'].split(',')[0].strip())
        
    if ";" in travel['departure']:
        departure_coord = get_coordinates(
                                travel['departure'].split(';')[0].strip())
    elif "," in travel['departure']:
        departure_coord = get_coordinates(
                                travel['departure'].split(',')[0].strip())
    
    travel['distance'] = get_distance([departure_coord,
                                        destination_coord]) / 1000
    """
        
    travel['price'] = price
    
    print("--------------------------------")
    return travel
    
        
if __name__ == "__main__":
    print(parse_travel(
    "http://www.exprimeviajes.com/vuelos-baratos-a-amsterdam-por-30-euros-el-trayecto/", 150))