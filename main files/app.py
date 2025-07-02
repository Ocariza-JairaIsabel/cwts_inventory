from flask import Flask, request, jsonify
import sqlite3
import os

app = Flask(__name__)
DB = 'database.db'

# --- Initialize DB from schema.sql ---
def init_db():
    if not os.path.exists(DB):
        with sqlite3.connect(DB) as conn:
            with open('schema.sql', 'r') as f:
                conn.executescript(f.read())

init_db()

# --- Helper for queries ---
def query_db(query, args=(), one=False):
    with sqlite3.connect(DB) as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.execute(query, args)
        result = cur.fetchall()
        conn.commit()
        return (result[0] if result else None) if one else result

# --- ROUTES ---

# CREATE item
@app.route('/items', methods=['POST'])
def add_item():
    data = request.get_json()
    query_db("INSERT INTO Item (name, quantity) VALUES (?, ?)", (data['name'], data['quantity']))
    return jsonify({"message": "Item added"}), 201

# READ all items
@app.route('/items', methods=['GET'])
def get_items():
    items = query_db("SELECT * FROM Item")
    return jsonify([dict(item) for item in items])

# UPDATE item
@app.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    data = request.get_json()
    query_db("UPDATE Item SET quantity = ? WHERE item_id = ?", (data['quantity'], item_id))
    return jsonify({"message": "Item updated"})

# DELETE item
@app.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    query_db("DELETE FROM Item WHERE item_id = ?", (item_id,))
    return jsonify({"message": "Item deleted"})

# CREATE log (and adjust item quantity)
@app.route('/logs', methods=['POST'])
def add_log():
    data = request.get_json()
    item = query_db("SELECT * FROM Item WHERE item_id = ?", (data['item_id'],), one=True)

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

    # Add log and update item quantity
    query_db("INSERT INTO Log (item_id, type, qty, date) VALUES (?, ?, ?, ?)",
             (data['item_id'], data['type'], qty, data['date']))
    query_db("UPDATE Item SET quantity = ? WHERE item_id = ?", (new_qty, data['item_id']))

    return jsonify({"message": "Log recorded and inventory updated"}), 201

# READ all logs (with item name)
@app.route('/logs', methods=['GET'])
def get_logs():
    logs = query_db("""
        SELECT Log.log_id, Item.name, Log.type, Log.qty, Log.date
        FROM Log JOIN Item ON Log.item_id = Item.item_id
        ORDER BY Log.date DESC
    """)
    return jsonify([dict(log) for log in logs])

# DELETE log
@app.route('/logs/<int:log_id>', methods=['DELETE'])
def delete_log(log_id):
    query_db("DELETE FROM Log WHERE log_id = ?", (log_id,))
    return jsonify({"message": "Log deleted"})

# --- Run Server ---
if __name__ == '__main__':
    app.run(debug=True)
