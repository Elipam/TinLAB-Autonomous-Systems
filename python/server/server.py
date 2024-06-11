# -*- coding: utf-8 -*-
"""
Created on Thu May 30 13:38:09 2024

@author: spanj
"""

from flask import Flask, request, jsonify, render_template
import threading
import requests
import time

app = Flask(__name__)

ipList = []
robotDict = {}

@app.route('/send_data', methods=['POST'])
def receive_data():
    data = request.json
    print("Received Data:")
    if (data['robots']):
        for robot in data['robots']:
            robotDict[robot['name']] = [robot['current_position'], robot['goal'], robot['direction']]
    print(robotDict)
    return jsonify({'message': 'Data received successfully'})

@app.route('/robot_signup', methods=['POST'])
def receive_signup():
    data = request.json
    ipList.append(data["ip"])
    print("Received Data:", data)
    return jsonify({'message': 'Signup received successfully'})

@app.route('/robot_step', methods=['GET'])
def send_right():
    return 200

@app.route('/')
def home():
    return render_template('index.html')

def run_flask_app():
    app.run(host='0.0.0.0', port=5000)

if __name__ == '__main__':
    # Start Flask app in a separate thread
    flask_thread = threading.Thread(target=run_flask_app)
    flask_thread.daemon = True
    flask_thread.start()

    # Give Flask app some time to start
    time.sleep(2)

    while (ipList == []):
        time.sleep(1)

    # Now you can send a request using the requests library
    data = {
        "robots": [
            {
                "name": "Robot1",
                "current_position": [1, 1],
                "goal": [3, 4],
                "direction": 12
            },
            {
                "name": "Robot2",
                "current_position": [0, 0],
                "goal": [5, 6],
                "direction": 12
            },
            {
                "name": "Robot3",
                "current_position": [5, 8],
                "goal": [5, 2],
                "direction": 12
            }
        ]
    }
    ipList[0] = "127.0.0.1" + ":5000"
    url = 'http://' + ipList[0] + '/send_data'
    try:
        response = requests.post(url, json=data)
    except Exception as e:
        print("Failed to send POST request:", e)

    print(response.json())

    # Keep the main thread alive if necessary
    while True:
        time.sleep(1)

