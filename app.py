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


@app.route("/")
def home():
    return render_template('index.html', API_KEY=api_key)


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
