from __main__ import api
from flask import request, jsonify
import dsb


@api.route('/auth')
def auth():
    user = request.args.get('user')
    if not user:
        return jsonify({'error': 'missing query parameter: user'})

    password = request.args.get('password')
    if not password:
        return jsonify({'error': 'missing query parameter: password'})

    return jsonify(dsb.auth(user, password))


@api.route('/get')
def get():
    auth_id = request.args.get('authid')
    if not auth_id:
        return jsonify({'error': 'missing query parameter: authid'})

    table_id = request.args.get('tableid')
    if not table_id:
        table_id = ""

    return jsonify(dsb.get(auth_id, table_id))
