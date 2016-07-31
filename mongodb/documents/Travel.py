# -*- coding: utf-8 -*-
from mongoengine import Document
from mongoengine.fields import FloatField, StringField, URLField, BooleanField
import re


class Travel(Document):
    price = FloatField(required=True, min_value=0.0)
    date = StringField(required=True,
                       regex=re.compile("^(0[1-9]|[12][0-9]|3[01])-(0[1-9]|1[012])-(19|20)\d\d$"))
    departure = StringField(required=True)
    destination = StringField(required=True)
    return_to = StringField(required=True)
    url = URLField(required=True, unique=True)
    ticket_type = StringField(required=True)
    last = BooleanField(required=True, default=False)
    distance_price = FloatField(required=True, min_value=0.0)
    distance = FloatField(required=True, min_value=0.0)
    continent = StringField(required=True)