from flask import Flask, request, jsonify
from waitress import serve

api = Flask(__name__)

import routes

if __name__ == '__main__':
  serve(api, listen='127.0.0.1:120')
