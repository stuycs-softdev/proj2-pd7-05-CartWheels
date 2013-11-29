# Application
SECRET_KEY = "}. 2}MpuI3J[yYGg8*b9jL&;%Lyt(WhxxhlFaoadm}sQjaVF+/z`vs~#qd@ Spd8"
STORE_FILE = "store.info"

# Mongodb
DB_NAME = 'cartwheels'
COLLECTIONS = {
        'User': 'users',
        'Cart': 'carts',
        'Tag': 'tags',
        'Review': 'reviews',
        'Rename': 'rename',
        'Collection': 'ignore'
        }

IGNORE_ATTRS = ['_obj', 'collection', 'fs', 'db']

# Elasticsearch
ES_REPEAT = 5
