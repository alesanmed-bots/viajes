# -*- coding: utf-8 -*-
from mongoengine.connection import connect as mongo_connect
from mongoengine.connection import disconnect as mongo_disconnect
from mongodb.documents.Travel import Travel
import logging

logger = logging.getLogger('viajes.transactions');

def connect(env):
    if env == "dev":
        mongo_connect('Viajes')
    else:
        mongo_connect('Viajes', host="viajes_db", port=27017)
    
def disconnect(env):
    mongo_disconnect('Viajes')

def get_last_to_check():
    last_to_check = Travel.objects(last=True).first()
    
    last_url = None

    if last_to_check is not None:    
        last_url = last_to_check.url
        
    return last_url
    
def update_last_to_check(travel_url):
    Travel.objects(last=True).update_one(set__last=False)
    
    Travel.objects(url=travel_url).update_one(set__last=True)
    
def save_travel(travel):
    logger.debug("Saving travel {0}".format(travel['url']))
    to_save = Travel(**travel)
    
    to_save.save()