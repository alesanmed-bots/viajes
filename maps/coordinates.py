# -*- coding: utf-8 -*-
import googlemaps
import os, sys
if os.path.relpath(".", "..") != "viajes":
    sys.path.append(os.path.join(
                    os.path.dirname(
                        os.path.dirname(
                            os.path.abspath(__file__))),
                    "credentials"))
    from maps import api_key
else:
    from credentials.maps import api_key
    
from maps.continents import continents

def get_coordinates(location):
    gmaps = googlemaps.Client(key=api_key)
    
    geocode_res = gmaps.geocode(location)[0]
    
    return (geocode_res['geometry']['location']['lat'],
            geocode_res['geometry']['location']['lng'])

def get_continent(location):
    coordinates = get_coordinates(location).split(',')
    
    gmaps = googlemaps.Client(key=api_key)
    address = gmaps.reverse_geocode((coordinates[0], coordinates[1]))
    
    return continents[address[0]['address_components'][-2]['short_name']]

if __name__ == "__main__":
    print(get_continent("Sevilla"))