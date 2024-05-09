from __main__ import api
from flask import request, jsonify
import dsb

@api.route('/auth')
def auth():
  user = request.args.get('user')
  if (not user):
    return jsonify({ 'error': 'missing query parameter: user' })

  password = request.args.get('password')
  if (not password):
    return jsonify({ 'error': 'missing query parameter: password' })

  return jsonify(dsb.auth(user, password))

@api.route('/get')
def get():
  authid = request.args.get('authid')
  if (not authid):
    return jsonify({ 'error': 'missing query parameter: authid' })

  if (request.data): request_body = request.json
  else: request_body = {}

  return jsonify(dsb.get(authid, request_body))