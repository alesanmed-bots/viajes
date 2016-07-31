# -*- coding: utf-8 -*-
from mongoengine.connection import connect as mongo_connect
from mongoengine.connection import disconnect as mongo_disconnect
from mongodb.documents.Travel import Travel

def connect():
    mongo_connect('Viajes')
    
def disconnect():
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
    print(travel)
    to_save = Travel(**travel)
    
    to_save.save()