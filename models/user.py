# Models and Collections for users
from models.base import Collection, Model
from models.review import Review
from settings import USER_COLLECTION


class UserModel(Model):

    def __init__(self, db, fs, collection, obj):
        super(UserModel, self).__init__(db, fs, collection, obj)
        self.username = obj['username']
        self.password = obj['password']
        self.reviews = Review()

    # Change password with authentication
    def change_password(self, oldpass, newpass):
        if oldpass == self.password:
            self.password = newpass
            self.collection.update({'_id': self.get_id()}, password=newpass)
            return True
        return False

    # assign a value to the image_id
    def add_image(self, image_id):
        self.image_id = image_id

    # get the image from GridFS
    def get_image(self, image_id):
        return self.fs.get(self.image_id)

    # Get blog reviews made by this user, and with other arguments
    def get_reviews(self, **kwargs):
        return self.reviews.find(user=self.username, **kwargs)


class User(Collection):

    def __init__(self):
        super(User, self).__init__(USER_COLLECTION, UserModel)

    def insert(self, **kwargs):
        return super(User, self).insert(**kwargs)

    # Checks if a specific user exists
    def exists(self, username):
        return self.find_one(username=username) is not None
