# Models and Collections for carts
from models.base import Collection, Model
from models.review import Review
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

    # Assign a value to the image_id
    def add_image(self, image_id):
        self.image_id = image_id

    # Get the image from GridFS
    def get_image(self, image_id):
        return self.fs.get(self.image_id)

    # Adds a review under the users page
    def add_review(self, user, **kwargs):
        reviews = Review()
        return reviews.insert(cart_id=self.get_id(), user=user, **kwargs)

    # Get blog reviews made by this user, and with other arguments
    def get_reviews(self, **kwargs):
        reviews = Review()
        return reviews.find(cart_id=self.get_id(), **kwargs)


class Cart(Collection):

    def __init__(self):
        super(Cart, self).__init__(CART_COLLECTION, CartModel)

    def insert(self, **kwargs):
        return super(Cart, self).insert(**kwargs)
