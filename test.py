from models import *


carts = Cart()
users = User()
revs = Review()
tags = Tag()
guesses = NameGuess()


u = users.insert(username='Ben', password='goose')
c = carts.find_one(owner='UNKNOWN')
r = c.add_review(u.username, text='Great place to chow down!', rating=4.5)
t = tags.insert(label='chow')

t.attach(c.get_id())
for ca in t.get_carts():
    for rev in ca.get_reviews():
        print rev.text

t.detach(c.get_id())
print len(t.get_carts())

#n = guesses.insert(name='RAFIQI\'S HALAL', cart_id=c.get_id())
#n.approve()
#c = carts.find_one(_id=c.get_id())
#print c.owner

users.remove_all()
revs.remove_all()
tags.remove_all()
guesses.remove_all()
