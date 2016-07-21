# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup as bs
import locale
import urllib.request
import os, sys
import re
import time
sys.path.append(os.path.join(
                os.path.dirname(
                    os.path.dirname(
                        os.path.abspath(__file__))),
                "maps"))
from coordinates import get_coordinates
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

def is_number(string):
    try:
        int(string)
        return True
    except ValueError:
        return False

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
    
    if date_p.text.strip() == "":
        date_p = travel_page.find(
                        "div",
                        class_="entry-content").find_all("p")[3]

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
    """
    
    if ";" in travel['destination']:
        destination_coord = get_coordinates(
                            travel['destination'].split(';')[0].strip())
    elif "," in travel['destination']:
        destination_coord = get_coordinates(
                                travel['destination'].split(',')[0].strip())
    else:
        destination_coord = get_coordinates(
                                travel['destination'].strip())
    
    if ";" in travel['departure']:
        departure_coord = get_coordinates(
                                travel['departure'].split(';')[0].strip())
    elif "," in travel['departure']:
        departure_coord = get_coordinates(
                                travel['departure'].split(',')[0].strip())
    else:
        departure_coord = get_coordinates(
                                travel['departure'].strip())
                                
    print("{0}: {1}".format(travel['departure'], departure_coord))
    print("{0}: {1}".format(travel['destination'], destination_coord))
    
    travel['distance'] = get_distance([departure_coord,
                                        destination_coord]) / 1000
        
    travel['price'] = price
    travel['distance_price'] = travel['price'] / travel['distance']
    travel['date'] = time.strftime("%d-%m-%Y", travel_date)
    travel['url'] = travel_url
    
    print("--------------------------------")
    return travel
    
        
if __name__ == "__main__":
    print(parse_travel(
    "http://www.exprimeviajes.com/chollo-bali-vuelos-12-noches-por-496-euros/", 150))