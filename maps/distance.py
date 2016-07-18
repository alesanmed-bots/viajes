# -*- coding: utf-8 -*-
import googlemaps
import numpy as np
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

def get_distance(coords):
    assert len(coords) == 2
    
    gmaps = googlemaps.Client(key=api_key)
    
    res = gmaps.distance_matrix(coords, coords)
    
    coords_len = len(coords)
    distance_matrix = np.empty((coords_len, coords_len))
    
    for row, dict in enumerate(res['rows']):
        for column, element in enumerate(dict['elements']):
            distance_matrix[row, column] = element['distance']['value']
    
    return distance_matrix[0, 1]
    
if __name__ == "__main__":
    print(get_distance(["41.3850639,2.1734035", "37.3890924,-5.9844589"]))