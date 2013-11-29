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
@app.route('/')
def home():
    return render_template('index.html', API_KEY=api_key)


# Register
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


# Login
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


# Logout
@app.route('/logout')
def logout():
    if 'username' in session:
        session.pop('username')
    return redirect(url_for('home'))


# For the user to change personal information
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


# Cart page
@app.route('/carts/<cid>', methods=['GET', 'POST'])
def cart(cid):
    c = carts.find_one(_id=ObjectId(cid))
    u = None
    if 'username' in session:
        u = users.find_one(username=session['username'])
    if request.method == 'POST':
        if request.form['btn'] == 'Submit':
            rating = int(request.form['review_rating'])
            text = request.form['review_text']
            c.add_review(user=u.username, text=text, rating=rating)
        elif request.form['btn'] == 'Upload':
            f = request.files['file']
            c.add_image(f, request.form['img_label'])
        else:
            c.add_tag(request.form['tag_label'])
    return render_template('cart.html', target_cart=c, user=u)


# Tag page
@app.route('/carts/<label>')
def tag(label):
    pass


# Serves the data from the backend to the frontend js using json module
@app.route('/_data')
def serve_data():
    # Get iterable copy of args
    rargs = request.args.copy()
    kwargs = {}
    # Copy request args into a copy
    for k in rargs.keys():
        kwargs[k] = rargs[k]
    objs = carts.find(**kwargs)
    results = [o._obj for o in objs]
    # Remove incompatible types
    for r in results:
        r.pop('date', None)
        r['_id'] = str(r['_id'])
    # Return results as an array
    data = {'results': results}
    return json.dumps(data)


# Get image by id
@app.route('/_image/<image_id>')
def serve_image(image_id):
    image = carts.fs.get(ObjectId(image_id))
    data = image.read()
    image.close()
    return data


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
