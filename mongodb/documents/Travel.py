# -*- coding: utf-8 -*-
from mongoengine import Document
from mongoengine.fields import FloatField, StringField, URLField, BooleanField, DateTimeField
import re
import datetime


class Travel(Document):
    price = FloatField(required=True, min_value=0.0)
    date = DateTimeField(required=True)
    departure = StringField(required=True)
    destination = StringField(required=True)
    return_to = StringField(required=True)
    url = URLField(required=True, unique=True)
    ticket_type = StringField(required=True)
    last = BooleanField(required=True, default=False)
    distance_price = FloatField(required=True, min_value=0.0)
    distance = FloatField(required=True, min_value=0.0)
    continent = StringField(required=True)
    added = DateTimeField(required=True, default=datetime.datetime.now)