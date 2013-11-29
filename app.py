#!/usr/local/bin/python
from flask import Flask, render_template, session, redirect, request, url_for
from bson import ObjectId
from models import Cart, User
from settings import SECRET_KEY, STORE_FILE
import json


app = Flask(__name__)
app.secret_key = SECRET_KEY
carts = Cart()
users = User()


f = open(STORE_FILE)
api_key = f.readlines()[0].strip()
f.close()


# Base function, renders the template with the api key as input
'''Map for the home function for the GET method:
    I. Check if the username is in session
        1) If it is...
            i. grab the user from the database
                - u = users.find_one(username=session['username'])
            ii. render the template, and pass the user as an argument
                - render_template('index.html', ..., user=u)
        2) If it isn't
            i. render the template as normal
                - render_template('index.html', ...)
TODO: render the template with a list of trending food carts, or reviews'''
@app.route('/')
def home():
    return render_template('index.html', API_KEY=api_key)


@app.route('/register',methods=['GET','POST'])
def register():
    if 'username' in session:
        return redirect(url_for('home'))
    if request.method == 'GET':
        return render_template('register.html')
    if users.exists(request.form['username']):
        return render_template('register.html',error='Username already exists')
    if request.form['password'] != request.form['confirm']:
        return render_template('register.html',error='Passwords do not match')
    session['username'] = request.form['username']
    users.insert(username=request.form['username'],password=request.form['password'])
    return redirect(url_for('home'))


@app.route('/login',methods=['GET','POST'])
def login():
    if 'username' in session:
        return redirect(url_for('home'))
    if request.method == 'GET':
        return render_template('login.html')
    u = users.find_one(username=request.form['username'], password=request.form['password'])
    if not u:
        return render_template('login.html', error='Incorrect username or password')
    session['username'] = request.form['username']
    return redirect(url_for('home'))


@app.route('/logout')
def logout():
    if 'username' in session:
        session.pop('username')
    return redirect(url_for('home'))


@app.route('/changeinfo',methods=['GET','POST'])
def changeinfo():
    if 'username' not in session:
        return redirect(url_for('home'))
    if request.method == 'GET':
        return render_template('changeinfo.html')

    u = users.find_one(username=session['username'])
    error = None
    usererror = None
    passerror = None

    if u.password == request.form['oldpw']:
        if request.form['newuser']:
            if not u.change_username(request.form['oldpw'],
                    request.form['newuser']):
                usererror = 'Username change unsuccessful.'
            else:
                session['username'] = request.form['newuser']
        if request.form['newpw']:
            if not u.change_password(request.form['oldpw'], request.form['newpw'],
                    request.form['confirm']):
                passerror= 'Passwords do not match.'
    else:
        error = 'Incorrect password'
    return render_template('changeinfo.html', error=error, usererror=usererror, passerror=passerror)


# Review page
'''Map for the user function for the GET method:
    I. Grab the review from the database
        - target_rev = reviews.find_one(_id=rid)
    II. Check if a review exists (use if target_review is not None) with the given id
        1) If it does...
            i. Check if the username is in session
                - if it is...
                    * grab the user from the database
                        - u = users.find_one(username=session['username'])
                    * render the template with the user and the target_review to the function
                        - render_template('index.html', ..., target_review=target_review, u=u)
                - if it isn't
                    * render the template with the target_review
                        - render_template('index.html', ..., target_review=target_review, u=None)
TODO: Implement POST method'''
@app.route('/reviews/<id>')
def review(rid):
    pass


# Cart page
'''Map for the cart function for the GET method:
    I. Grab the cart from the database
        - target_cart = carts.find_one(_id=cid)
    II. Check if a cart exists (use if target_cart is not None) with the given id
        1) If it does...
            i. Check if the username is in session
                - if it is...
                    * grab the user from the database
                        - u = users.find_one(username=session['username'])
                    * render the template with the user and the cart to the function
                        - render_template('index.html', ..., target_cart=target_cart, u=u)
                - if it isn't
                    * render the template with the target_cart
                        - render_template('index.html', ..., target_cart=target_cart, u=None)
TODO: Implement POST method'''
@app.route('/carts/<cid>', methods=['GET', 'POST'])
def cart(cid):
    c = carts.find_one(_id=ObjectId(cid))
    u = None
    if 'username' in session:
        u = users.find_one(username=session['username'])
    if request.method == 'POST':
        rating = int(request.form['review_rating'])
        text = request.form['review_text']
        c.add_review(user=u.username, text=text, rating=rating)
    return render_template('cart.html', target_cart=c, user=u)


# Tag page
'''Map for the tag function
    I. Grab the tag from the database
        - tag = tags.find_one(label=label)
    II. Check if the tag exists (use if target is not None)
        i. Check if the username is in session
            - if it is...
                * grab the user from the database
                    - u = users.find_one(username=session['username'])
                * render the template with the user and the tag passed to the function
                    - render_template('index.html', ..., tag=tag, u=u)
            - if it isn't
                * render the template with the tag
                    - render_template('index.html', ..., tag=tag, u=None)
TODO: Implement POST method'''
@app.route('/carts/<label>')
def tag(label):
    t = tags.find_one(label=ObjectId(label))
    u = None
    if 'username' in session:
        u = users.find_one(username=session['username'])
        return render_template('tag.html', tag=t, user=u.username)
    else:
        return render_template('tag.html', tag=tag, user=u)
    

# Serves the data from the backend to the frontend js using json module
@app.route('/_data')
def serve_data():
    rargs = request.args.copy()
    kwargs = {}
    for k in rargs.keys():
        kwargs[k] = rargs[k]

    objs = carts.find(**kwargs)
    results = [o._obj for o in objs]

    for r in results:
        r.pop('date', None)
        r['_id'] = str(r['_id'])

    data = {'results': results}
    return json.dumps(data)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
