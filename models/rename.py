# Models and Collections for name guesses
from models.base import Collection, Model
from models.cart import Cart
from settings import RENAME_COLLECTION


''' Format for an insert would be:
    rnames.insert(name=...,cart_id=...)
'''
class RenameModel(Model):

    def __init__(self, db, fs, collection, obj):
        super(RenameModel, self).__init__(db, fs, collection, obj)

    def increment(self, uid):
        self.count += 1
        self.save()

    def approve(self):
        carts = Cart()
        c = carts.find_one(_id=self.cart_id)
        c.owner = self.name
        c.save()
        self.collection.remove(cart_id=self.cart_id)


class Rename(Collection):

    def __init__(self):
        super(Rename, self).__init__(RENAME_COLLECTION, RenameModel)

    def insert(self, **kwargs):
        return super(Rename, self).insert(count=0, **kwargs)
