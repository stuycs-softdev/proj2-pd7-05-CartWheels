# Models and Collections for tags
from models.base import Collection, Model
from settings import TAG_COLLECTION


class TagModel(Model):

    def __init__(self, db, fs, collection, obj):
        super(TagModel, self).__init__(db, fs, collection, obj)
        self.label = obj['label']
        self.carts = obj['carts']

    # Add a cart which has this tag
    def add_cart(self, cart_id):
        self.carts.append(cart_id)
        self.collection.update({'_id': self.get_id()}, carts=self.carts)

    # Get carts by tag


class Tag(Collection):

    def __init__(self):
        super(Tag, self).__init__(TAG_COLLECTION, TagModel)

    def insert(self, **kwargs):
        return super(Tag, self).insert(carts=[], **kwargs)
