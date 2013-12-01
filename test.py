from models import *
from bson import ObjectId


carts = Cart()
users = User()
revs = Review()
tags = Tag()
renames = Rename()


u = users.insert(username='Ben', password='goose')
c = carts.find_one(_id=ObjectId('52952ef7421aa93b89efcc0e'))
r = c.add_review(u.username, text='Great place to chow down!', rating=4.5)
t = tags.insert(label='chow')

t.attach(c.get_id())
