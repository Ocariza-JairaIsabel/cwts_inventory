from flask import Blueprint, request, jsonify
from database import query_db

logs_bp = Blueprint('logs', __name__)

@logs_bp.route('/logs', methods=['POST'])
def add_log():
    data = request.get_json()
    required_fields = {'item_id', 'type', 'qty', 'date'}
    if not data or not required_fields.issubset(data):
        return jsonify({'error': 'Invalid input'}), 400
    
    item = query_db("SELECT * FROM Item WHERE item_id = ?", 
                    (data['item_id'],), one=True)

    if not item:
        return jsonify({"error": "Item not found"}), 404

    current_qty = item['quantity']
    qty = data['qty']

    if data['type'] == 'IN':
        new_qty = current_qty + qty
    elif data['type'] == 'OUT':
        if qty > current_qty:
            return jsonify({"error": "Not enough stock"}), 400
        new_qty = current_qty - qty
    else:
        return jsonify({"error": "Invalid type"}), 400

    query_db("INSERT INTO Log (item_id, type, qty, date) VALUES (?, ?, ?, ?)",
             (data['item_id'], data['type'], qty, data['date']))
    query_db("UPDATE Item SET quantity = ? WHERE item_id = ?", 
             (new_qty, data['item_id']))

    return jsonify({"message": "Log recorded and inventory updated"}), 201

@logs_bp.route('/logs', methods=['GET'])
def get_logs():
    logs = query_db("""
        SELECT Log.log_id, Item.name, Log.type, Log.qty, Log.date
        FROM Log JOIN Item ON Log.item_id = Item.item_id
        ORDER BY Log.date DESC
    """)
    return jsonify([dict(log) for log in logs])

@logs_bp.route('/logs/<int:log_id>', methods=['DELETE'])
def delete_log(log_id):
    query_db("DELETE FROM Log WHERE log_id = ?", (log_id,))
    return jsonify({"message": "Log deleted"})
