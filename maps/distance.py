# -*- coding: utf-8 -*-
import numpy as np
from geopy.distance import vincenty

def get_distance(coords):
    assert len(coords) == 2
    
    return vincenty(coords[0], coords[1]).meters
    
if __name__ == "__main__":
    print(get_distance([(41.3850639,2.1734035), (37.3890924,-5.9844589)]))