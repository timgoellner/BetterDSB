from __main__ import api
from flask import request, jsonify
import dsb

@api.route('/auth')
def auth():
  user = request.args.get('user')
  if (not user):
    return jsonify({ 'error': 'missing argument: user' })

  password = request.args.get('password')
  if (not password):
    return jsonify({ 'error': 'missing argument: password' })

  return jsonify(dsb.auth(user, password))