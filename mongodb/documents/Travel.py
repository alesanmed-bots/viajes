# -*- coding: utf-8 -*-
from mongoengine import Document
from mongoengine.fiedls import FloatField
from mongoengine.fiedls import StringField
import re


class Travel(Document):
    price = FloatField(required=True, min_value=0.0)
    date = StringField(required=True,
                       regex=re.compile("^(0[1-9]|[12][0-9]|3[01])-\
                       (0[1-9]|1[012])-(19|20)\d\d$"))