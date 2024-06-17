# -*- coding: utf-8 -*-
"""
Created on Thu May 30 13:38:09 2024

@author: spanj
"""

from flask import Flask, request, jsonify, render_template
import threading
import requests
import time

class Pathfinding:
    def __init__(self, width=13, height=10):
        self.robots = {}
        self.robots_move = {}
        self.picture = {}
        self.possible_moves = [(1,0), (0,1), (-1,0), (0,-1), (0,0)]
        self.width = width
        self.height = height
        self.current_grid = self.make_grid()
        self.goal_grid = self.make_grid()
        #self.initialize_grids()

    def heuristic(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def make_grid(self):
        return [[0 for _ in range(self.width)] for _ in range(self.height)]

    def print_grid(self, grid=None):
        if grid is None:
            grid = self.current_grid
        print(f"+{len(grid[0])*'-'*2+'-'}+")
        for row in grid:
            print('|', end='')
            for element in row:
                print(f" {element}", end='')
            print(' |')
        print(f"+{len(grid[0])*'-'*2+'-'}+")

    def initialize_grids(self):
        for key, value in self.current_positions.items():
            row, col = value
            self.current_grid[col][row] = key
        for key, value in self.goal_positions.items():
            row, col = value
            self.goal_grid[col][row] = key

    def determine_goals(self):
        print(self.robots)
        print(self.picture)

    def algorithm(self):
        next_grid = self.make_grid()
        for key, value in self.current_positions.items():
            row, col = value
            if value == self.goal_positions[key]:
                next_grid[col][row] = key
                continue
            min_heuristic = float('inf')
            best_move = None
            for move in self.possible_moves:
                next_row, next_col = row + move[0], col + move[1]
                if not (0 <= next_row < len(next_grid) and 0 <= next_col < len(next_grid[0])):
                    continue
                if next_grid[next_col][next_row] != 0:
                    continue
                h = self.heuristic((next_row, next_col), self.goal_positions[key])
                if h < min_heuristic:
                    min_heuristic = h
                    best_move = move
            if best_move:
                next_row, next_col = row + best_move[0], col + best_move[1]
                next_grid[next_col][next_row] = key
                self.current_positions[key] = (next_row, next_col)

        self.print_grid(next_grid)
        if next_grid == self.goal_grid:
            return
        self.algorithm()
    
    def quick_move(self):
        self.robots_move = {'robots':[]}
        next_grid = self.make_grid()
        print(self.robots)
        for key, value in self.robots.items():
            pos, goal, color, direction = value
            x, y = pos
            min_heuristic = float('inf')
            best_move = None
            for move in self.possible_moves:
                next_x, next_y = x + move[0], y + move[1]
                if not (0 <= next_y < len(next_grid) and 0 <= next_x < len(next_grid[0])):
                    continue
                if next_grid[next_y][next_x] != 0:
                    continue
                h = self.heuristic((next_x, next_y), goal)
                if h < min_heuristic:
                    min_heuristic = h
                    best_move = move
            if best_move:
                next_x, next_y = x + best_move[0], y + best_move[1]
                next_grid[next_y][next_x] = key
                self.robots_move['robots'].append({"name":key, "current_position":[x, y], "next_position":[next_x, next_y]}) 
        print(self.robots_move['robots'])
        return self.robots_move

class RobotServer:
    def __init__(self, pathfinding_instance):
        self.app = Flask(__name__)
        self.ip_list = []
        self.board = pathfinding_instance
        self.setup_routes()

    def setup_routes(self):
        @self.app.route('/send_data', methods=['POST'])
        def receive_data():
            data = request.json
            print("Received Data:")
            if 'robots' in data:
                for robot in data['robots']:
                    if all(key in robot for key in ('name', 'color', 'current_position', 'angle')):
                        self.board.robots[robot['name']] = [robot['current_position'], [12, 0], robot['color'], robot['angle']]
                    else:
                        print({'message': 'Data received successfully but keys are weird'})
                        print(data)
            else:
                print(f"This is not a robots this is {data}")
                return jsonify({'message': 'Data received but not processed'})
            print(f"received {data} own {self.board.robots}")
            return jsonify({'message': 'Data received successfully'})

        @self.app.route('/get_data', methods=['GET'])
        def send_data():
            client_ip = request.remote_addr
            print(f"Next step requested from IP: {client_ip}")
            data = self.board.quick_move()
            print(f"Sending to simulation {data}")
            return jsonify(data)

        @self.app.route('/send_picture', methods=['POST'])
        def receive_picture():
            data = request.json
            if 'picture' in data:
                self.board.picture = data['picture']
                self.board.determine_goals()
                return jsonify({"message": "Picture received successfully"})
            print(data)
            return jsonify({"message": "Picture received, but no picture data found"})
        
        @self.app.route('/robot_signup', methods=['POST'])
        def receive_signup():
            data = request.json
            self.ip_list.append(data["ip"])
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
    grid = Pathfinding()
    server = RobotServer(grid)

    # Start Flask app in a separate thread
    flask_thread = threading.Thread(target=server.run_flask_app)
    flask_thread.daemon = True
    flask_thread.start()
    time.sleep(2)

    # Temp, only here to wait before testing 
    while not server.ip_list:
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
    server.ip_list[0] = "127.0.0.1" + ":5000"
    url = 'http://' + server.ip_list[0] + '/send_data'
    try:
        response = requests.post(url, json=data)
    except Exception as e:
        print("Failed to send POST request:", e)

    print(response.json())

    grid.print_grid()
    # Keep the main thread alive if necessary
    while True:
        time.sleep(1)