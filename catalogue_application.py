from database_setup import Base, Category, CategoryItem, User

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, joinedload
from sqlalchemy import create_engine

from flask import Flask, jsonify, request, url_for, abort, g, render_template, make_response, flash, redirect, session as login_session
from flask_httpauth import HTTPBasicAuth

# from oauth2client.client import flow_from_clientsecrets
# from oauth2client.client import FlowExchangeError

from google.oauth2 import id_token
from google.auth.transport import requests

import httplib2
import requests
import string
import random
import json

auth = HTTPBasicAuth()

engine = create_engine('sqlite:///MBitemCatalog.db', connect_args={"check_same_thread": False})

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
app = Flask(__name__)


CLIENT_ID = json.loads(open('client_secrets.json', 'r').read())['web']['client_id']

categories = session.query(Category)
items = session.query(CategoryItem)

# Login and authentication
@app.route('/login/')
def login():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html')


@app.route('/oauth/<provider>', methods = ['POST'])
def login2(provider):
    #STEP 1 - Parse the auth code
    auth_code = request.json.get('auth_code')
    print("Step 1 - Complete, received auth code %s" % auth_code)
    if provider == 'google':
        #STEP 2 - Exchange for a token, https://developers.google.com/identity/sign-in/web/backend-auth
        try:
            # Specify the CLIENT_ID of the app that accesses the backend:
            idinfo = id_token.verify_oauth2_token(token, requests.Request(), CLIENT_ID)
            if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                raise ValueError('Wrong issuer.')
            # ID token is valid. Get the user's Google Account ID from the decoded token.
            userid = idinfo['sub']
        except ValueError:
            return("Invalid token")
            pass
          
        # Check that the access token is valid.
        access_token = credentials.access_token
        url = ('https://oauth2.googleapis.com/tokeninfo?id_token={}'.format(access_token))
        h = httplib2.Http()
        result = json.loads(h.request(url, 'GET')[1])
        # If there was an error in the access token info, abort.
        if result.get('error') is not None:
            response = make_response(json.dumps(result.get('error')), 500)
            response.headers['Content-Type'] = 'application/json'
            
        print("Step 2 Complete! Access Token: {}".format(credentials.access_token))

        #STEP 3 - Find User or make a new one
        #Get user info
        h = httplib2.Http()
        userinfo_url =  "https://www.googleapis.com/oauth2/v1/userinfo"
        params = {'access_token': credentials.access_token, 'alt':'json'}
        answer = requests.get(userinfo_url, params=params)
      
        data = answer.json()

        name = data['name']
        picture = data['picture']
        email = data['email']
        
        #see if user exists, if it doesn't make a new one
        user = session.query(User).filter_by(email=email).first()
        if not user:
            user = User(username = name, picture = picture, email = email)
            session.add(user)
            session.commit()

        #STEP 4 - Make token
        token = user.generate_auth_token(600)
        #STEP 5 - Send back token to the client 
        return jsonify({'token': token.decode('ascii')})
    else:
        return 'Unrecoginized Provider'


# Start app routes
# Add JSON endpoints here
@app.route('/catalogue.json/')
def cataloguesJSON():
    catalogue = session.query(Category).options(joinedload(Category.items)).all()
    return jsonify(Catalog = [dict(c.serialize,
        items = [i.serialize for i in c.items])
        for c in categories
    ])


@app.route('/category/<int:category_id>.json/')
def categoryJSON(category_id):
    category = categories.filter_by(id=category_id).one()
    return jsonify(Category=category.serialize)


@app.route('/categories.json/')
def categoriesJSON():
    allCategories = categories.all()
    return jsonify(Categories=[c.serialize for c in allCategories])


@app.route('/category/<int:category_id>/items.json/')
def categoryItemsJSON(category_id):
    categoryItems = items.filter_by(id=category_id).all()
    return jsonify(items=[i.serialize for i in categoryItems])


@app.route('/category/item/<int:item_id>.json/')
def itemJSON(item_id):
    item = items.filter_by(id=item_id).one()
    return jsonify(categoryItem=item.serialize)


# Add regular app routes here
@app.route('/')
@app.route('/catalogue/')
def catalogues():
    return render_template('catalogue.html', categories=categories, items=items)


@app.route('/category/<int:category_id>/')
def category(category_id):
    category = categories.filter_by(id=category_id).one()
    item_list = items.filter_by(category_id=category_id)
    count_items = len(items.filter_by(category_id=category_id).all())
    return render_template('category.html', categories=categories, category=category, count_items=count_items, items=item_list)


@app.route('/category/item/<int:item_id>/')
def item(item_id):
    item = items.filter_by(id=item_id).one()
    print("item id is " + str(item_id))
    return render_template('item.html', item_id=item_id, item=item)


@app.route('/category/<int:category_id>/newitem/', methods=['GET', 'POST'])
def newItem(category_id):
    if request.method == 'POST':
        if request.form['name']:
            name = request.form['name']
        if request.form['description']:
            description = request.form['description']
        newItem = CategoryItem(name=name, description=description, category_id=category_id)
        session.add(newItem)
        session.commit()
        flash("New Category item created!")
        return redirect(url_for('category', category_id=category_id))
    else:
        return render_template('newItem.html', category_id=category_id)


@app.route('/category/item/<int:item_id>/edit/', methods=['GET', 'POST'])
def editItem(item_id):
    editedItem = items.filter_by(id=item_id).one()
    if request.method == 'POST':
        if request.form['updatedName']:
            editedItem.name = request.form['updatedName']
        if request.form['updatedDescription']:
            editedItem.description = request.form['updatedDescription']
        session.add(editedItem)
        session.commit()
        flash(str(editedItem.name) + " updated!", "success")
        return redirect(url_for('category', category_id=editedItem.category_id))
    else:
        return render_template('edititem.html', item_id=item_id, item=editedItem)


@app.route('/category/item/<int:item_id>/delete/', methods=['GET', 'POST'])
def deleteItem(item_id):
    itemToDelete =  items.filter_by(id=item_id).one()
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash("Category item deleted!", "danger")
        return redirect(url_for('category', category_id=itemToDelete.category_id))
    else:
        return render_template('deleteItem.html', item_id=item_id, item=itemToDelete)


# ADD OAUTH


if __name__ == '__main__':
    app.debug = True
    app.config['SECRET_KEY'] = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(32))
    app.run(host='0.0.0.0', port=8000)
