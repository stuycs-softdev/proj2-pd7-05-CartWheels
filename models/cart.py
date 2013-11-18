# Models and Collections for carts
from models.base import Collection, Model
from models.review import Review
from models.tag import Tag
from settings import CART_COLLECTION


class CartModel(Model):

    def __init__(self, db, fs, collection, obj):
        super(CartModel, self).__init__(db, fs, collection, obj)
        self.lat = obj['lat']
        self.lng = obj['lng']
        self.street = obj['street']
        self.address = obj['address']
        self.zip_code = obj['zip_code']
        self.borough = obj['borough']
        self.owner = obj['owner']
        self.revs = obj['revs']
        self.tags = obj['tags']

    # Assign a value to the image_id
    def add_image(self, image_id):
        self.image_id = image_id

    # Get the image from GridFS
    def get_image(self, image_id):
        return self.fs.get(self.image_id)

    # Adds a review under the users page
    def add_review(self, user, **kwargs):
        if not user in self.revs:
            self.revs.append(user)
            self.collection.update({'_id': self.get_id()}, revs=self.revs)
            return self.reviews.insert(cart_id=self.get_id(), **kwargs)
        return False

    # Get blog reviews made by this user, and with other arguments
    def get_reviews(self, **kwargs):
        reviews = Review()
        return reviews.find(cart_id=self.get_id(), **kwargs)

    # Add a tag
    def tag(self, label):
        tags = Tag()
        t = tags.find_one(text=label)
        if t is None:
            tags.insert(text=label)

        if t.get_id() not in self.tags:
            t.add_cart(self.get_id())
            self.tags.append(t.get_id())
            self.collection.update({'_id': self.get_id()}, tags=self.tags)
            return True
        return False

    # Get tags for the cart
    def get_tags(self, **kwargs):
        tags = Tag()
        results = [tags.find_one(_id=i) for i in self.tags]
        return results


class Cart(Collection):

    def __init__(self):
        super(Cart, self).__init__(CART_COLLECTION, CartModel)

    def insert(self, **kwargs):
        return super(Cart, self).insert(revs=[], tags=[], **kwargs)
