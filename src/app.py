from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson import ObjectId
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


app = Flask(__name__)

uri = "mongodb+srv://davidstudiodev:2648@mycluster.crtme.mongodb.net/?retryWrites=true&w=majority&appName=MyCluster"

client = MongoClient(uri, server_api=ServerApi('1'))

db = client['shop']
products = db['products']


@app.route('/read', methods=['GET'])
def getProduct():
    query = list(products.find())
       
    for product in query:
        product['_id'] = str(product['_id'])
       
    return jsonify('Products:', query)

@app.route('/add', methods=['POST'])
def addProduct():
   
    newProduct = {
        'name': request.json['name'],
        'price': request.json['price'],
        'category': request.json['category'],
        'stock': request.json['stock']
    }
    
    query = products.insert_one(newProduct)
    return jsonify('Message: ', 'Product Add {}'.format(newProduct))
   

@app.route('/update/<string:id>', methods=['PUT'])
def updateProduct(id):
       query = products.find_one({'_id': ObjectId(id)})
       
       updateProduct = request.json
       queryUdpate = products.update_one({'_id': ObjectId(id)}, {'$set': updateProduct})
       
       return jsonify('Product updated.')
   
   
@app.route('/delete/<string:id>', methods=['DELETE'])
def deleteProduct(id):
       
       query = products.delete_one({'_id': ObjectId(id)})
       if query:
           return jsonify('Product deleted.')
             
       return 'Delete'
   
if __name__ == '__main__':
    app.run() 
   