# -*- coding: utf-8 -*-
"""
Created on Thu May 30 13:38:09 2024

@author: spanj
"""
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/send_data', methods=['POST'])
def receive_data():
    data = request.json
    # Process received data
    print("Received Data:", data)
    return jsonify({'message': 'Data received successfully'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
