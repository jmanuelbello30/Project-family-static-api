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

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
#get all members
def handle_members():
    
    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    response_body = {
        "family": members
    }

    return jsonify(response_body), 200

#get one member by id
@app.route('/member/<int:id>', methods=['GET'] )
def get_member_(id):
    
    if request.method == 'GET':
        member = jackson_family.get_member(id)
        if member:
            return jsonify(member), 200
        else:
            return "Petición rechazada, revise los parámetros", 400

#add member
@app.route('/member', methods=['POST'])
def create_new_member():
    member = request.json
    if member:
        new_member = jackson_family.add_member(member)
        return jsonify({"El nuevo miembro se añadió": new_member._members[-1]}), 200
    else:
        return "Petición rechazada, revise los parámetros", 400

#Delete a member
@app.route('/member/<int:id>', methods=['DELETE'])
def delete_member(id):
    deleted_member = jackson_family.delete_member(id)
    if deleted_member:
        return jsonify({"done": True}), 200
    else:
        return "Petición rechazada, revise los parámetros", 400

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)