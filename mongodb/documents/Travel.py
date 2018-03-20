# -*- coding: utf-8 -*-
from mongoengine import Document
from mongoengine.fields import FloatField, StringField, URLField, BooleanField, DateTimeField
import re
import datetime


class Travel(Document):
    price = FloatField(min_value=0.0, default=0.0)
    date = DateTimeField()
    departure = StringField()
    destination = StringField()
    return_to = StringField()
    url = URLField()
    ticket_type = StringField()
    last = BooleanField(default=False)
    distance_price = FloatField(min_value=0.0, default=0.0)
    distance = FloatField(min_value=0.0, default=0.0)
    continent = StringField()
    added = DateTimeField(default=datetime.datetime.now)