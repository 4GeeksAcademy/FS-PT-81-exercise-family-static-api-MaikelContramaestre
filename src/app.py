"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

jackson_family.add_member({
    'name':'juanito',
    'age': 34,
    'id': 34,
    'lucky_number' :[34]
})


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def handle_hello():

    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    response_body = {
        "hello": "world",
        "family": members
    }

    return jsonify(response_body), 200
@app.route('/members', methods=['POST'])
def handle_add():
    data = request.json
    if 'name' not in data or 'age' not in data or 'lucky_number' not in data:
        return jsonify({'msg': 'Faltan datos por agregar'}), 400    
    response = jackson_family.add_member(data)
    print (data)
    return jsonify({'msg': response}), 200

@app.route('/members/<int:member_id>' , methods=['DELETE'])
def handle_delete(member_id):
    member = jackson_family.get_member(member_id)
    if member:
        jackson_family.delete_member(member_id)
        return jsonify({"message": f"Usuario con ID {member_id} eliminado."}), 200
    else:
         return jsonify({"error": "Usuario no encontrado"}), 404

@app.route('/members/<int:member_id>', methods=['GET'])
def handle_find(member_id):

    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_member(member_id)
    response_body = {
        
        "family": members
    }

    return jsonify(response_body), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
