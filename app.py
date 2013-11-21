#!/usr/local/bin/python
from flask import Flask, render_template, session, redirect, request, url_for
from models import Cart
from settings import SECRET_KEY, STORE_FILE
import json


app = Flask(__name__)
app.secret_key = SECRET_KEY
carts = Cart()

f = open(STORE_FILE)
api_key = f.readlines()[0].strip()
f.close()


# Base function, renders the template with the api key as input
"""Map for the home function for the GET method:
    I. Check if the username is in session
        1) If it is...
            i. grab the user from the database
                - u = users.find_one(username=session['username'])
            ii. render the template, and pass the user as an argument
                - render_template("index.html", ..., user=u)
        2) If it isn't
            i. render the template as normal
                - render_template("index.html", ...)
TODO: render the template with a list of trending food carts, or reviews"""
@app.route("/")
def home():
    return render_template('index.html', API_KEY=api_key)


# Review page
"""Map for the user function for the GET method:
    I. Grab the review from the database
        - target_rev = reviews.find_one(_id=uid)
    II. Check if a review exists (use if target_review is not None) with the given id
        1) If it does...
            i. Check if the username is in session
                - if it is...
                    * grab the user from the database
                        - u = users.find_one(username=session['username'])
                    * render the template with the user and the target_review to the function 
                        - render_template("index.html", ..., target_review=target_review, u=u)
                - if it isn't
                    * render the template with the target_review
                        - render_template("index.html", ..., target_review=target_review, u=None)
TODO: Implement POST method"""
@app.route("/reviews/<id>")
def review(rid):
    pass


# Cart page
"""Map for the cart function for the GET method:
    I. Grab the cart from the database
        - target_cart = carts.find_one(_id=cid)
    II. Check if a cart exists (use if target_cart is not None) with the given id
        1) If it does...
            i. Check if the username is in session
                - if it is...
                    * grab the user from the database
                        - u = users.find_one(username=session['username'])
                    * render the template with the user and the cart to the function 
                        - render_template("index.html", ..., target_cart=target_cart, u=u)
                - if it isn't
                    * render the template with the target_cart
                        - render_template("index.html", ..., target_cart=target_cart, u=None)
TODO: Implement POST method"""
@app.route("/carts/<cid>")
def cart(cid):
    pass


# Tag page
"""Map for the tag function
    I. Grab the tag from the database
        - tag = tags.find_one(label=label)
    II. Check if the tag exists (use if target is not None)
        i. Check if the username is in session
            - if it is...
                * grab the user from the database
                    - u = users.find_one(username=session['username'])
                * render the template with the user and the tag passed to the function 
                    - render_template("index.html", ..., tag=tag, u=u)
            - if it isn't
                * render the template with the tag
                    - render_template("index.html", ..., tag=tag, u=None)
TODO: Implement POST method"""
@app.route("/carts/<label>")
def tag(label):
    pass


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
