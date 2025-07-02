from flask import Blueprint, request, jsonify

items_bp = Blueprint('items', __name__)

items = []

@items_bp.route('/items', methods=['POST'])
def add_item():
    data = request.get_json()
    
    if not data or 'id' not in data or 'name' not in data or \
       'quantity' not in data:
        return jsonify({'error': 'Invalid input'}), 400
    
    items.append(data)
    
    return jsonify({"message": "Item added", "item": data}), 201

@items_bp.route('/items', methods=['GET'])
def get_items():
    return jsonify(items)

@items_bp.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    data = request.get_json()
    
    if not data or 'quantity' not in data:
        return jsonify({'error': 'Invalid input'}), 400
    
    for item in items:
        if item['id'] == item_id:
            item.update(data)
            return jsonify({
                "message": "Item updated",
                "item": item
            })
    return jsonify({"error": "Item not found"}), 404

@items_bp.route('/items/<int:item_id>', methods=['PATCH'])
def patch_item(item_id):
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    for item in items:
        if item['id'] == item_id:
            item.update(data)
            return jsonify({
                'message': 'Item updated (partially)',
                'item': item
            })
    return jsonify({'error': 'Item not found'}), 404

@items_bp.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    for item in items:
        if item['id'] == item_id:
            items.remove(item)
            return jsonify({"message": "Item deleted"})
    return jsonify({'error': 'Item not found'}), 404