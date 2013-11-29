# Models and Collections for tags
from models.base import Collection, Model
from settings import TAG_COLLECTION


''' Format for an insert would be:
    tags.insert(label=...)
'''
class TagModel(Model):

    def __init__(self, db, fs, collection, obj):
        super(TagModel, self).__init__(db, fs, collection, obj)


class Tag(Collection):

    def __init__(self):
        super(Tag, self).__init__(TAG_COLLECTION, TagModel)

    def insert(self, **kwargs):
        return super(Tag, self).insert(count=0, **kwargs)
