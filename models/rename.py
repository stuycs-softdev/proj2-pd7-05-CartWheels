# Models and Collections for name guesses
from models.base import Collection, Model
from models.cart import Cart
from settings import RENAME_COLLECTION


class RenameModel(Model):

    def __init__(self, db, fs, collection, obj):
        super(RenameModel, self).__init__(db, fs, collection, obj)
        self.name = obj['name']
        self.cart_id = obj['cart_id']
        self.count = obj['count']

    def increment(self, uid):
        self.count += 1
        self.collection.update({'_id': self.get_id()}, count=self.count)

    def approve(self):
        carts = Cart()
        carts.update({'_id': self.cart_id}, owner=self.name)
        self.collection.remove(cart_id=self.cart_id)


class Rename(Collection):

    def __init__(self):
        super(Rename, self).__init__(RENAME_COLLECTION, RenameModel)

    def insert(self, **kwargs):
        return super(Rename, self).insert(count=0, **kwargs)
