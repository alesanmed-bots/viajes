# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
import os, sys
sys.path.append(os.path.join(
                os.path.dirname(
                    os.path.dirname(
                        os.path.abspath(__file__))),
                "maps"))
from coordinates import get_coordinates
from distance import get_distance

def parse_travel(travel_url):
    if type(travel_url) != str:
        raise ValueError("travel_url is not a String object")
        
    # document = urlopen(travel_url)
    # Only for the development stage
    with open('test.txt', 'r') as file:
        document = file.read()
        
    travel_page = bs(document, 'html.parser')
    
    content = travel_page.find(
                        "div",
                        class_="entry-content").find_all("div")[1].find_all("p")
    
    travel = {}
    for p in content:
        if "Ciudad de salida" in p.text:
            travel['departure'] = p.text.split(":")[-1].strip()
        elif "Ciudad de destino" in p.text:
            travel['destination'] = p.text.split(":")[-1].strip()
        elif "Ciudad de regreso" in p.text:
            travel['return_to'] = p.text.split(":")[-1].strip()
        elif "Tipo de billete" in p.text:
            travel['ticket_type'] = p.text.split(":")[-1].strip()
    
    departure_coord = get_coordinates(travel['departure'])
    destination_coord = get_coordinates(travel['destination'])
    
    travel['distance'] = get_distance([departure_coord,
                                        destination_coord]) / 1000
    print(travel)
    
        
if __name__ == "__main__":
    parse_travel(
    "http://www.exprimeviajes.com/santorini-vuelos-7-noches-por-194-euros/")