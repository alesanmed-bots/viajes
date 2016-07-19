# -*- coding: utf-8 -*-

from pymongo import MongoClient

def connect():
    client = MongoClient()
    db = client.travel_bot
    
    return client, db
    
def disconnect(client):
    client.close()
    
def get_last_to_check():
    client, db = connect()
    
    last_to_check = db.last_travel.find({}, limit=1)[0]
    
    disconnect(client)    
    
    return last_to_check
    
def update_last_to_check(travel):
    client, db = connect()
    
    db.last_travel.remove({})
    
    db.last_travel.insert_one(travel)
    