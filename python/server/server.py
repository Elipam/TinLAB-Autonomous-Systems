# -*- coding: utf-8 -*-
"""
Created on Thu May 30 13:38:09 2024

@author: spanj
"""

from flask import Flask, request, jsonify, render_template
import threading
import requests
import time

class grid():
    def __init__(self):
        self.makeGrid()

class RobotServer:
    def __init__(self):
        self.app = Flask(__name__)
        self.ipList = []
        self.robotDict = {}
        self.setup_routes()

    def setup_routes(self):
        @self.app.route('/send_data', methods=['POST'])
        def receive_data():
            data = request.json
            print("Received Data:")
            if (data['robots']):
                for robot in data['robots']:
                    self.robotDict[robot['name']] = [robot['current_position'], robot['goal'], robot['direction']]
            print(self.robotDict)
            return jsonify({'message': 'Data received successfully'})

        @self.app.route('/robot_signup', methods=['POST'])
        def receive_signup():
            data = request.json
            self.ipList.append(data["ip"])
            print("Received Data:", data)
            return jsonify({'message': 'Signup received successfully'})

        @self.app.route('/robot_step', methods=['GET'])
        def send_right():
            return 200

        @self.app.route('/')
        def home():
            return render_template('index.html')

    def run_flask_app(self):
        self.app.run(host='0.0.0.0', port=5000)

if __name__ == '__main__':
    server = RobotServer()

    # Start Flask app in a separate thread
    flask_thread = threading.Thread(target=server.run_flask_app)
    flask_thread.daemon = True
    flask_thread.start()
    time.sleep(2)

    # Temp, only here to wait before testing 
    while not server.ipList:
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
    server.ipList[0] = "127.0.0.1" + ":5000"
    url = 'http://' + server.ipList[0] + '/send_data'
    try:
        response = requests.post(url, json=data)
    except Exception as e:
        print("Failed to send POST request:", e)

    print(response.json())

    # Keep the main thread alive if necessary
    while True:
        time.sleep(1)

