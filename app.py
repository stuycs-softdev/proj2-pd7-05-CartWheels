#!/usr/local/bin/python
from flask import Flask, render_template, session, redirect, request, url_for
from bson import ObjectId
from models import Collection, Cart, User, Review
from settings import SECRET_KEY, STORE_FILE
import json


app = Flask(__name__)
app.secret_key = SECRET_KEY
models = Collection()
carts = Cart()
users = User()
reviews = Review()

f = open(STORE_FILE)
api_key = f.readlines()[0].strip()
f.close()


# Base function, renders the template with the api key as input
@app.route('/')
def home():
    r = reviews.get_by_date()
    recs = carts.sort_by([('rating', -1), ('date', -1)])
    if request.method == 'POST':
        key = request.form['key']
        val = request.form['val']
        kwargs = {}
        kwargs[key] = val
        recs = carts.sort_by([('rating', -1)], **kwargs)
    if not 'username' in session:
        return render_template('index.html', user=None, reviews=r,
                               recommendations=recs[:20], API_KEY=api_key)
    else:
        user = users.find_one(username=session['username'])
        return render_template('index.html', user=user, reviews=r, 
                               recommendations=recs[:20], API_KEY=api_key)



# Register
@app.route('/register',methods=['GET','POST'])
def register():
    if 'username' in session:
        return redirect(url_for('home'))
    if request.method == 'GET':
        return render_template('register.html')
    if users.exists(request.form['username']):
        return render_template('register.html', error='Username already exists')
    if request.form['password'] != request.form['confirm']:
        return render_template('register.html', error='Passwords do not match')
    session['username'] = request.form['username']
    users.insert(username=request.form['username'],
            password=request.form['password'])
    return redirect(url_for('home'))


# Login
@app.route('/login',methods=['GET','POST'])
def login():
    if 'username' in session:
        return redirect(url_for('home'))
    if request.method == 'GET':
        return render_template('login.html')
    u = users.find_one(username=request.form['username'],
            password=request.form['password'])
    if not u:
        return render_template('login.html',
                error='Incorrect username or password')
    session['username'] = request.form['username']
    return redirect(url_for('home'))


# Logout
@app.route('/logout')
def logout():
    if 'username' in session:
        session.pop('username')
    return redirect(url_for('home'))


# For the user to change personal information
@app.route('/changeinfo', methods=['GET', 'POST'])
def changeinfo():
    if 'username' not in session:
        return redirect(url_for('home'))
    if request.method == 'GET':
        return render_template('changeinfo.html',user=session['username'])
    u = users.find_one(username=session['username'])
    error = None
    usererror = None
    passerror = None
    usersuccess = None
    pwsuccess = None
    if u.password == request.form['oldpw']:
        if request.form['newuser']:
            if not u.change_username(request.form['oldpw'],
                    request.form['newuser']):
                usererror = 'Username change unsuccessful.'
            else:
                session['username'] = request.form['newuser']
                usersuccess = 'Username successfully changed to: ' + request.form['newuser']
        if request.form['newpw']:
            if not u.change_password(request.form['oldpw'], request.form['newpw'],
                    request.form['confirm']):
                passerror= 'Passwords do not match.'
            else:
                pwsuccess= 'Password successfully changed.'
    else:
        error = 'Incorrect password'
    return render_template('changeinfo.html', user=session['username'],error=error, usererror=usererror, passerror=passerror, usersuccess=usersuccess, pwsuccess=pwsuccess)


# Cart page
@app.route('/carts/<string:cid>', methods=['GET', 'POST'])
def cart_page(cid):
    c = carts.find_one(_id=ObjectId(cid))
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
    return render_template('cart.html', target_cart=c, user=None)


# Reviews ordered by date
@app.route('/newest-reviews/<int:page>')
def new_reviews(page):
    r = reviews.get_by_date()
    start = (page - 1) * 20
    end = page * 20
    if 'username' in session:
        u = users.find_one(username=session['username'])
        return render_template('reviews.html', reviews=r[start:end], page=page, user=u)
    return render_template('reviews.html', reviews=r[start:end], page=page, user=None)

# Carts ordered by rating
@app.route('/top-carts/<int:page>')
def recommendations(page):
    recs = carts.sort_by([('rating', -1), ('date', -1)])
    start = (page - 1) * 20
    end = page * 20
    if 'username' in session:
        u = users.find_one(username=session['username'])
        return render_template("recommendations.html", recommendations=recs[start:end], page=page, user=u)
    return render_template("recommendations.html", recommendations=recs[start:end], page=page, user=None)


# Search by tag
@app.route('/search/<int:page>')
def search(page):
    t = request.args.get('tag')
    results = carts.get_by_tag(t)
    start = (page - 1) * 20
    end = page * 20
    if 'username' in session:
        u = users.find_one(username=session['username'])
        return render_template('search.html', carts=results[start:end], page=page, t=t, u=u)
    return render_template('search.html', carts=results[start:end], page=page, t=t, u=None)



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
        r['date'] = r['date'].strftime('%A, %B %d')
        r['_id'] = str(r['_id'])
        for image in r['images']:
            image['date'] = image['date_added'].strftime('%A, %B %d')
            image['_id'] = str(image['_id'])
        for tag in r['tags']:
            tag['date'] = tag['date'].strftime('%A, %B %d')
            tag['_id'] = str(tag['_id'])
    # Return results as an array
    data = {'results': results}
    return json.dumps(data)


# Get image by id
@app.route('/_image/<image_id>')
def serve_image(image_id):
    image = models.fs.get(ObjectId(image_id))
    data = image.read()
    image.close()
    return data


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
