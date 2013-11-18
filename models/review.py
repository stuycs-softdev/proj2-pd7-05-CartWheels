# Models and Collections for reviews
from models.base import Collection, Model
from settings import REVIEW_COLLECTION


class ReviewModel(Model):

    def __init__(self, db, fs, collection, obj):
        super(ReviewModel, self).__init__(db, fs, collection, obj)
        self.text = obj['text']
        self.rating = obj['rating']
        self.user = obj['user']
        self.cart_id = obj['cart_id']


class Review(Collection):

    def __init__(self):
        super(Review, self).__init__(REVIEW_COLLECTION, ReviewModel)

    def insert(self, **kwargs):
        return super(Review, self).insert(**kwargs)
