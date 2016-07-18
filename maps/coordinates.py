# -*- coding: utf-8 -*-
import googlemaps
import os, sys
sys.path.append(os.path.join(
                os.path.dirname(
                    os.path.dirname(
                        os.path.abspath(__file__))),
                "credentials"))

from maps import api_key

def get_coordinates(location):
    gmaps = googlemaps.Client(key=api_key)
    
    geocode_res = gmaps.geocode(location)[0]
    
    return "{0},{1}".format(geocode_res['geometry']['location']['lat'],
                            geocode_res['geometry']['location']['lng'])
                            
if __name__ == "__main__":
    print(get_coordinates("Sevilla"))