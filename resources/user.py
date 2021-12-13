import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel
# Our user info will reside in DB. When authenticate/indetity func wants a user by name or id, we search for corresponding
# info in DB, create an object using that and return it

# Resource for User sign-up
class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', 
                    type = str,
                    required = True,
                    help = 'This field cannot be left blank'
        )
    parser.add_argument('password', 
                    type = str,
                    required = True,
                    help = 'This field cannot be left blank'
        )


    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message":"A user with that name already exists"}, 400  # Bad request

        user = UserModel(**data)  # **data means passing username=data['username], password=data['password]
        user.save_to_db()
        
        return {"message":"User created successfully"}, 201
        


