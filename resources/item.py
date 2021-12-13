from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', 
                    type = float,
                    required = True,
                    help = 'This field cannot be left blank'
        )
    parser.add_argument('store_id', 
                    type = int,
                    required = True,
                    help = 'Every item needs a store_id'
        )


    @jwt_required()   # Makes it compulsory for user to verify JWT before making get call
    def get( self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {"message": "Item not found"}, 404

    
    def post(self, name):
        item = ItemModel.find_by_name(name) # can also do Item.find_by_name instead of self.find.. 
        if item:
            return {"message" : "An item with name {} already exists".format( name )}, 400   # 400 is for bad request. Sending 400 as its user's fault 

        # Whenever your request sends json payload as a body, you can access that through request.get_json, but if there is no body sent,
        #or the content-type in headers is inappropriate, the below line will fail
        #data = request.get_json()
        data = Item.parser.parse_args()   
        item = ItemModel(name, **data)  # **data is equivalent to data['price'], data['store_id]
        
        try:
            item.save_to_db()
        except:
            return {"message":"An error occurred inserting the item"}, 500  # 500 is Internal server error
        return item.json(), 201

    
    def delete(self, name):

        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        return {'message': 'Item deleted'}
    
    
    def put(self, name):
        # Put method is meant to be idempotent, meaning that if you call it 10 times, output will still be the same
        # So it sees if the obj exists, if it doesn't, it makes new obj, else simply updates
        
        data = Item.parser.parse_args()  # With this and the above code,we can filter out data corresponding to 'price' out of the whole JSON payload, others will be dropped

        #data = request.get_json() If you do this, the whole JSON payload(body sent by user) will be assigned to data
        item = ItemModel.find_by_name(name)
        if not item:
            item = ItemModel(name, **data)
            
        else:
            item.price = data['price']
            item.store_id = data['store_id']
        
        item.save_to_db()
           
        return item.json()





class ItemList(Resource):
    def get(self):
        
        return {'items' : [ x.json() for x in ItemModel.query.all() ] }

