# Models and Collections for tags
from models.base import Collection, Model
from models.cart import Cart
from settings import TAG_COLLECTION


class TagModel(Model):

    def __init__(self, db, fs, collection, obj):
        super(TagModel, self).__init__(db, fs, collection, obj)
        self.label = obj['label']
        self.carts = obj['carts']

    # Add a cart which has this tag
    def attach(self, cart_id):
        if cart_id not in self.carts:
            self.carts.append(cart_id)
            self.update(carts=self.carts)
            carts = Cart()
            c = carts.find_one(_id=cart_id)
            if not self.label in c.tags:
                c.tags.append(self.label)
            c.update(tags=c.tags)

    # Remove a cart which has this tag
    def detach(self, cart_id):
        if cart_id in self.carts:
            self.carts.remove(cart_id)
            self.update(carts=self.carts)
            carts = Cart()
            c = carts.find_one(_id=cart_id)
            if self.label in c.tags:
                c.tags.remove(self.label)
            c.update(tags=c.tags)

    # Get carts by tag
    def get_carts(self):
        carts = Cart()
        return [carts.find_one(_id=cid) for cid in self.carts]

    # Get amount of times used
    def count(self):
        return len(self.carts)


class Tag(Collection):

    def __init__(self):
        super(Tag, self).__init__(TAG_COLLECTION, TagModel)

    def insert(self, **kwargs):
        return super(Tag, self).insert(carts=[], **kwargs)
