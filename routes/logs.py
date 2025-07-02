from flask import Blueprint, request, jsonify
from routes.items import items 

logs_bp = Blueprint('logs', __name__)
logs = []

@logs_bp.route('/logs', methods=['POST'])
def add_log():
    data = request.get_json()
    required = {'item_id', 'type', 'qty', 'date'}

    if not data or not required.issubset(data):
        return jsonify({'error': 'Invalid input'}), 400

    if data['type'] not in ('IN', 'OUT'):
        return jsonify({'error': 'Invalid type'}), 400

    for item in items:
        if item['id'] == data['item_id']:
            if data['type'] == 'IN':
                item['quantity'] += data['qty']
            elif data['type'] == 'OUT':
                if item['quantity'] < data['qty']:
                    return jsonify({
                        'error': 'Not enough stock to remove'
                    }), 400
                item['quantity'] -= data['qty']
            break
    else:
        return jsonify({'error': 'Item not found'}), 404

    logs.append(data)
    return jsonify({
        'message': 'Log recorded and inventory updated',
        'log': data
    }), 201

@logs_bp.route('/logs', methods=['GET'])
def get_logs():
    return jsonify(logs)

@logs_bp.route('/logs/<int:log_id>', methods=['PUT'])
def update_log(log_id):
    data = request.get_json()
    required = {'item_id', 'type', 'qty', 'date'}

    if not data or not required.issubset(data):
        return jsonify({'error': 'Invalid input'}), 400

    if data['type'] not in ('IN', 'OUT'):
        return jsonify({'error': 'Invalid type'}), 400

    for i, log in enumerate(logs):
        if log.get('id') == log_id:
            logs[i] = data
            return jsonify({
                'message': 'Log fully updated',
                'log': data
            })
    return jsonify({'error': 'Log not found'}), 404

@logs_bp.route('/logs/<int:log_id>', methods=['PATCH'])
def patch_log(log_id):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    if 'type' in data and data['type'] not in ('IN', 'OUT'):
        return jsonify({'error': 'Invalid type'}), 400

    if 'item_id' in data:
        return jsonify({
            'error': 'Changing item_id is not allowed in patch'
        }), 400

    for log in logs:
        if log.get('id') == log_id:
            log.update(data)
            return jsonify({
                'message': 'Log updated (partially)',
                'log': log
            })
    return jsonify({'error': 'Log not found'}), 404

@logs_bp.route('/logs/<int:log_id>', methods=['DELETE'])
def delete_log(log_id):
    for log in logs:
        if log.get('id') == log_id:
            logs.remove(log)
            return jsonify({'message': 'Log deleted'})
    return jsonify({'error': 'Log not found'}), 404



# TODO DAY 3 - Ocariza:
# - Add error handling and input validation for log endpoints