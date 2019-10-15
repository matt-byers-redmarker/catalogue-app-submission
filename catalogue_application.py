# Table imports from database
from database_setup import Base, Category, CategoryItem, User

# Imports for querying data from database
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, joinedload
from sqlalchemy import create_engine

# Flask imports
from flask import Flask, jsonify, request, url_for, abort, g, render_template, make_response, flash, redirect, session as login_session
from flask_httpauth import HTTPBasicAuth

# Google Oauth imports
from google.oauth2 import id_token
from google.auth.transport import requests

# Other python imports
import httplib2
import string
import random
import json

# Connecting to and setting up database
auth = HTTPBasicAuth()
engine = create_engine('sqlite:///MBitemCatalog.db', connect_args={"check_same_thread": False})
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
app = Flask(__name__)


# END IMPORTS -----------------


# GOOGLE client ID for oauth
CLIENT_ID = json.loads(open('client_secrets.json', 'r').read())['web']['client_id']


# User Helper Functions
def createUser(login_session):
    newUser = User(username=login_session['username'], email=login_session['email'], picture=login_session['picture'])
    session.add(newUser) 
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


# Global query variables
categories = session.query(Category)
items = session.query(CategoryItem)
creator = getUserInfo(CategoryItem.user_id)


# Login and authentication
@app.route('/logout/')
def logout():
    if "username" in login_session:
        g.current_user = None
        flash("LoggedOut Successfully!", "success")
        del login_session['token']
        print('deleted token')
        del login_session['guser_id']
        print('deleted guser_id')
        del login_session['username']
        print('deleted unsername')
        del login_session['email']
        print('deleted email')
        del login_session['picture']
        print('deleted guser_id')
        return redirect('/')
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html')


@app.route('/oauth/google/', methods = ['POST'])
def googleLogin():
    try:
        if request.form['id_token']:
            token = request.form['id_token']
            # Specify the CLIENT_ID of the app that accesses the backend:
            idinfo = id_token.verify_oauth2_token(token, requests.Request(), CLIENT_ID)
            if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                raise ValueError('Wrong issuer.')

            # ID token is valid. Create login session with user info.
            login_session['guser_id'] = idinfo['sub']
            login_session['username'] = idinfo['name']
            login_session['picture'] = idinfo['picture']
            login_session['email'] = idinfo['email']
            print('Added login sessions for user: ' + login_session['username'])

            #see if user exists, if it doesn't make a new one
            user = session.query(User).filter_by(email=idinfo['email']).first()
            if not user:
                user_id = createUser(login_session)
                login_session['user_id'] = user_id # the out put of the createUser function is the user ID
                print("User added with name: " + login_session['username'] + " and email: " + login_session['email'])
            else:
                print ("User already added")

            if not login_session.get('token'):
                print('--------------Flashed Logged In----------------------')
                flash("LoggedIn User: {}!".format(idinfo['name']), "success")
            login_session['token'] = user.generate_auth_token(600)
            print('Login session token: ' + str(login_session['token']))

    except ValueError:
        print("Invalid token passed")
        pass

    return idinfo

# @app.route('/gdisconnect')
# def gdisconnect():
#     access_token = login_session.get('access_token')
#     if access_token is None:
#         print 'Access Token is None'
#         response = make_response(json.dumps('Current user not connected.'), 401)
#         response.headers['Content-Type'] = 'application/json'
#         return response
#     print 'In gdisconnect access token is %s', access_token
#     print 'User name is: '
#     print login_session['username']
#     url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']
#     h = httplib2.Http()
#     result = h.request(url, 'GET')[0]
#     print 'result is '
#     print result
#     if result['status'] == '200':
#         del login_session['access_token']
#         del login_session['gplus_id']
#         del login_session['username']
#         del login_session['email']
#         del login_session['picture']
#         response = make_response(json.dumps('Successfully disconnected.'), 200)
#         response.headers['Content-Type'] = 'application/json'
#         return response
#     else:
#         response = make_response(json.dumps('Failed to revoke token for given user.', 400))
#         response.headers['Content-Type'] = 'application/json'
#         return response



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
    if "username" not in login_session:
        return redirect('/login')
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
    if "username" not in login_session:
        return redirect('/login')
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
    if "username" not in login_session:
        return redirect('/login')
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
