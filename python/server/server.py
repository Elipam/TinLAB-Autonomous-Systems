from flask import Flask, request, jsonify, render_template
import threading
import requests
import time

class Pathfinding:
    def __init__(self, width=13, height=10):
        self.robots = {}
        self.robots_move = {}
        self.robots_step = {'robots':[]}
        self.picture = {}
        self.possible_moves = [(1,0), (0,1), (-1,0), (0,-1), (0,0)]
        self.width = width
        self.height = height
        self.current_grid = self.make_grid()
        self.goal_grid = self.make_grid()

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

    def determine_goal(self, color, current_position):
        min_heuristic = float('inf')
        closest_goal = None
        
        for key, value in self.picture.items():
            if value[0] == color and not value[1]:
                goal = [int(num.strip()) for num in key.split(',')]
                h = self.heuristic(current_position, goal)
                if h < min_heuristic:
                    min_heuristic = h
                    closest_goal = goal
        
        if closest_goal:
            # Mark the closest goal as checked
            key = ','.join(map(str, closest_goal))
            self.picture[key] = [color, True]
            print(f"Determine_goal {closest_goal}")
            return closest_goal
        
        return [-1, -1]
    
    def quick_move(self):
        self.robots_move = {'robots':[]}
        next_grid = [row[:] for row in self.current_grid]
        for key, value in self.robots.items():
            pos, goal, color, direction = value
            x, y = pos
            if goal == [-1, -1]:
                goal = self.determine_goal(color, pos)
                print(f"quick_move {goal}")
                if goal == [-1, -1]:
                    next_grid[y][x] = key
                    self.robots_move['robots'].append({"name":key, "current_position":[x, y], "next_position":[x, y]}) 
                    continue
            min_heuristic = float('inf')
            best_move = None
            for move in self.possible_moves:
                next_x, next_y = x + move[0], y + move[1]
                if not (0 <= next_y < len(next_grid) and 0 <= next_x < len(next_grid[0])):
                    continue
                if next_grid[next_y][next_x] != 0 and next_grid[next_y][next_x] != key:
                    continue
                h = self.heuristic((next_x, next_y), goal)
                if h < min_heuristic:
                    min_heuristic = h
                    best_move = move

            if best_move == None:
                move = [0,0]
            if best_move:
                next_x, next_y = x + best_move[0], y + best_move[1]
                next_grid[next_y][next_x] = key
                self.robots_move['robots'].append({"name":key, "current_position":[x, y], "next_position":[next_x, next_y], "angle": direction})
                
                self.robots_step = {'robots':[]}
                self.robots_step['robots'].append({"name":key, "next_steps":self.determine_steps(best_move, direction)}) 

        return self.robots_move
    
    def determine_steps(self, move, angle):
        # Determine the target direction based on the move
        target_direction = None
        if move == (0, 0):
            return ["WAIT"]
        elif move == (1, 0):  # Right
            target_direction = "right"
        elif move == (0, 1):  # Up
            target_direction = "up"
        elif move == (-1, 0):  # Left
            target_direction = "left"
        elif move == (0, -1):  # Down
            target_direction = "down"

        # Get the current direction
        current_direction = self.get_direction(angle)
        
        # Determine the turning direction
        turns = []
        if current_direction != target_direction:
            directions_order = ["up", "right", "down", "left"]
            current_index = directions_order.index(current_direction)
            target_index = directions_order.index(target_direction)

            # Calculate the shortest turn direction
            if (target_index - current_index) % 4 == 1:
                turns.append("TURN_RIGHT")
            elif (target_index - current_index) % 4 == 3:
                turns.append("TURN_LEFT")
            elif (target_index - current_index) % 4 == 2:
                turns.append("TURN_RIGHT")
                turns.append("TURN_RIGHT")
            else:
                turns.append("TURN_LEFT")
                turns.append("TURN_LEFT")

        return turns + ["MOVE_FORWARD"]
    
    def get_direction(self, angle):
        directions = {
        "up": (315, 360, 0, 45),
        "right": (45, 135),
        "down": (135, 225),
        "left": (225, 315)
    }
        if (angle >= directions["up"][0] and angle < directions["up"][1]) or (angle >= directions["up"][2] and angle <= directions["up"][3]):
            return "up"
        elif angle >= directions["right"][0] and angle < directions["right"][1]:
            return "right"
        elif angle >= directions["down"][0] and angle < directions["down"][1]:
            return "down"
        elif angle >= directions["left"][0] and angle < directions["left"][1]:
            return "left"

class RobotServer:
    def __init__(self, pathfinding_instance):
        self.app = Flask(__name__)
        self.ip_list = []
        self.board = pathfinding_instance
        self.setup_routes()
        self.state = "initial_state"

    def setup_routes(self):
        @self.app.route('/send_data', methods=['POST'])
        def receive_data():
            data = request.json
            print("Received Data:")
            if 'robots' in data:
                for robot in data['robots']:
                    if all(key in robot for key in ('name', 'color', 'current_position', 'angle')):
                        if robot['name'] not in self.board.robots:
                            goal = self.board.determine_goal(robot['color'], robot['current_position'])
                        else:
                            goal = self.board.robots[robot['name']][1]
                            last_pos = self.board.robots[robot['name']][0]
                            self.board.current_grid[last_pos[1]][last_pos[0]] = 0
                        self.board.robots[robot['name']] = [robot['current_position'], goal, robot['color'], robot['angle']]
                        new_pos = robot['current_position']
                        self.board.current_grid[new_pos[1]][new_pos[0]] = robot['name']
                                  
                    else:
                        print({'message': 'Data received successfully but keys are weird'})
                        print(data)    
            else:
                print(f"This is not a robots this is {data}")
                return jsonify({'message': 'Data received but not processed'})
            # print(f"received {data} own {self.board.robots}")
            return jsonify({'message': 'Data received successfully'})

        @self.app.route('/get_data', methods=['GET'])
        def send_data():
            client_ip = request.remote_addr
            print(f"Next step requested from IP: {client_ip}")
            data = self.board.quick_move()
            # print(f"Sending to simulation {data}")
            return jsonify(data)

        @self.app.route('/send_picture', methods=['POST'])
        def receive_picture():
            data = request.json
            if 'picture' in data:
                transformed_picture = {
                    coords: [color, False] for coords, color in data['picture'].items()
                }   
                self.board.picture = transformed_picture
                # self.board.determine_goal()
                return jsonify({"message": "Picture received successfully"})
            print(data)
            return jsonify({"message": "Picture received, but no picture data found"})

        @self.app.route('/')
        def index():
            return render_template('index.html', state=self.state)

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

    picture_json = {
        'picture': {
            '3, 3': 'red', 
            '3, 4': 'green', 
            '3, 5': 'blue', 
            '3, 6': 'red', 
            '4, 3': 'blue', 
            '4, 4': 'red', 
            '4, 5': 'green', 
            '4, 6': 'blue', 
            '5, 3': 'red', 
            '5, 4': 'green', 
            '5, 5': 'blue', 
            '5, 6': 'red', 
            '6, 3': 'green', 
            '6, 4': 'blue', 
            '6, 5': 'red', 
            '6, 6': 'green'
        }
    }

    url = 'http://127.0.0.1:5000/'
    response = requests.post(url + 'send_picture', json=picture_json)
    # Keep the main thread alive, ctrl and c to interrupt
    while True:
        time.sleep(1)