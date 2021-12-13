import os
from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from db import db
from resources.user import UserRegister
from security import authenticate, identity
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # flask_sqlalchemy is an extension of sqlalchemy library

uri = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = uri  # 3 slashes mean data.db resides in root dir of project(where our code runs)
# With line 9, we have turned off tracker of flask_sqlalchemy, as sqlalchemy is already tracking modifications in model objs 
app.secret_key = 'prakhar'
api = Api(app)
db.init_app(app)

@app.before_first_request  
def create_tables():
    db.create_all()  # Before the first req gets processed, this will create data.db and all the databases within it(by looking at all the models we have defined, it will know wich tables to create)

# JWT creates a new endpoint /auth. So when we call /auth with username & password, JWT sends it to our authenticate func, which authenticates the user
# Once authenticate func succesfully authenticates user, JWT returns us an auth token(which it makes by doing some encryption on userid)
# So the next time you send req, you send this token, JWT decrypts it into a payload having userid, which it passes to identify func
# If identity func returns non None val, JWT understand that token was valid and user is correct
jwt = JWT(app, authenticate, identity)  

api.add_resource(Store, '/store/<string:name>')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(StoreList, '/stores')

if __name__ == '__main__':
    app.run(port=5000, debug = True)