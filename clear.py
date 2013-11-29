#!/usr/local/bin/python
from models import *
from settings import COLLECTIONS

models = Collection()

for key in COLLECTIONS:
    val = COLLECTIONS[key]
    if val != 'ignore':
        models.db[val].drop()

models.db.fs.drop()
