from flask import Blueprint, request, jsonify
from database import query_db

items_bp = Blueprint('items', __name__)

@items_bp.route('/items', methods=['POST'])
def add_item():
    data = request.get_json()
    if not data or 'name' not in data or 'quantity' not in data:
        return jsonify({'error': 'Invalid input'}), 400
    
    query_db("INSERT INTO Item (name, quantity) VALUES (?, ?)", 
             (data['name'], data['quantity']))
    return jsonify({"message": "Item added"}), 201

@items_bp.route('/items', methods=['GET'])
def get_items():
    items = query_db("SELECT * FROM Item")
    return jsonify([dict(item) for item in items])

@items_bp.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    data = request.get_json()
    if not data or 'quantity' not in data:
        return jsonify({'error': 'Invalid input'}), 400
    
    query_db("UPDATE Item SET quantity = ? WHERE item_id = ?", 
             (data['quantity'], item_id))
    return jsonify({"message": "Item updated"})

@items_bp.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    query_db("DELETE FROM Item WHERE item_id = ?", (item_id,))
    return jsonify({"message": "Item deleted"})
