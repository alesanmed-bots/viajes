# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup as bs
import locale
import urllib.request
import os, sys
import re
import time
import logging
sys.path.append(os.path.join(
                os.path.dirname(
                    os.path.dirname(
                        os.path.abspath(__file__))),
                "maps"))
from coordinates import get_coordinates, get_continent
from distance import get_distance
from tools.user_agent import get_user_agent
from datetime import date

months = [
    "diciembre",
    "noviembre",
    "octubre",
    "septiembre",
    "agosto",
    "julio",
    "junio",
    "mayo",
    "abril",
    "marzo",
    "febrero",
    "enero",
]

logger = logging.getLogger('viajes.parse_travel')

def is_number(string):
    try:
        int(string)
        return True
    except ValueError:
        return False

def parse_travel(travel_url, price):
    if type(travel_url) != str:
        raise ValueError("travel_url is not a String object")
    
    logger.DEBUG(travel_url)
    
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
        elif "Fechas" in p.text:
            travel['date'] = parse_date(p)
            
            
    """
    This is only made for getting the coordinates of first city, the travel map
    is NEVER modified
    """
    
    destination = "";
    if ";" in travel['destination']:
        destination = travel['destination'].split(';')[0].strip()
    elif "," in travel['destination']:
        destination = travel['destination'].split(',')[0].strip()
    else:
        destination = travel['destination'].strip()
    
    destination_coord = get_coordinates(destination);
    
    destination_continent = get_continent(destination);
    
    if ";" in travel['departure']:
        departure_coord = get_coordinates(
                                travel['departure'].split(';')[0].strip())
    elif "," in travel['departure']:
        departure_coord = get_coordinates(
                                travel['departure'].split(',')[0].strip())
    else:
        departure_coord = get_coordinates(
                                travel['departure'].strip())
                            
    travel['distance'] = get_distance([departure_coord,
                                        destination_coord]) / 1000
        
    travel['price'] = price
    travel['distance_price'] = travel['price'] / travel['distance']
    travel['url'] = travel_url
    travel['continent'] = destination_continent
    
    return travel

def parse_date(date_p):
    travel_date = date_p.text.split(":")[-1].split("(")[0].strip()
    
    
    if "–" in travel_date:    
        travel_date = travel_date.split("–")[-1].strip()
    elif "-" in travel_date:
        travel_date = travel_date.split("-")[-1].strip()
    
    pattern = re.compile("[^\w']")
    travel_date = pattern.sub(' ', travel_date)
    
    travel_date = travel_date.lower().split()
    
    travel_date_str = ""
    for month in months:
        try:
            index = travel_date.index(month)
            if is_number(travel_date[index-1]) and \
                    int(travel_date[index-1]) <= 31:
                travel_date_str += " " + travel_date[index-1]
            else:
                travel_date_str += " 28"
            
            travel_date_str += " " + month
            
            try:
                if is_number(travel_date[index+1]):
                    travel_date_str += " " + travel_date[index+1]
            except IndexError:
                travel_date_str += " " + str(date.today().year)
            
            break
        except ValueError:
            continue

    travel_date_str = travel_date_str.strip()
    
    travel_date = time.strptime(travel_date_str, "%d %B %Y")
    
    return time.strftime("%d-%m-%Y", travel_date)
    
        
if __name__ == "__main__":
    print(parse_travel(
    "http://www.exprimeviajes.com/chollo-vuelos-baratos-a-colombia-por-solo-359-euros/", 150))