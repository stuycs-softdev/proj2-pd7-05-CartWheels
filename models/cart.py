# Models and Collections for carts
from datetime import datetime
from models.base import Collection, Model
from models.review import Review
from models.tag import Tag


''' Format for an insert would be:
    carts.insert(lat=...,lng=...street=...,address=...,zip_code=...,
        borough=...,owner=...)
'''
class CartModel(Model):

    def __init__(self, db, fs, collection, obj):
        super(CartModel, self).__init__(db, fs, collection, obj)

    # Adds image associated with the cart
    def add_image(self, image_file, label):
        image_id = self.fs.put(image_file.read())
        img = {'_id': image_id, 'date_added': datetime.now(), 'label': label}
        self.images.append(img)
        self.save()

    # Adds tag to cart
    def add_tag(self, label):
        tags = Tag()
        t = tags.find_one(label=label)
        if not t:
            t = tags.insert(label=label)
        if not any(d['label'] == label for d in self.tags):
            t.count += 1
            t.save()
            t._obj.pop('count')
            self.tags.append(t._obj)
            self.save()
            return True
        return False

    # Adds a review under the users page
    def add_review(self, user, **kwargs):
        reviews = Review()
        ratings = [r.rating for r in self.get_reviews()]
        self.rating = sum(ratings) / len(ratings)
        self.save()
        return reviews.insert(cart_id=self.get_id(), user=user, **kwargs)

    # Get blog reviews made by this user, and with other arguments
    def get_reviews(self, **kwargs):
        reviews = Review()
        return reviews.find(cart_id=self.get_id(), **kwargs)


class Cart(Collection):

    def __init__(self):
        super(Cart, self).__init__(CartModel)

    def insert(self, **kwargs):
        return super(Cart, self).insert(tags=[], images=[], rating=-1, **kwargs)

    # Get by tag function
    def get_by_tag(self, label):
        self.to_objects(self.objects.find({}, {'tags': {'$elemMatch':
            {'label': label}}}))
