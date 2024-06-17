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

    def determine_goals(self):
        print(self.robots)
        print(self.picture)

    def quick_move(self):
        self.robots_move = {'robots':[]}
        next_grid = self.make_grid()
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
        self.last_command = None  # Variabele voor de laatste opdracht
        self.setup_routes()

        # Start een aparte thread voor periodiek printen van last_command
        self.start_print_last_command_thread()

    def start_print_last_command_thread(self):
        def print_last_command():
            while True:
                print(f"Last Command: {self.last_command}")
                time.sleep(1)  # Wacht 1 seconde voordat de volgende print wordt uitgevoerd

        # Maak een nieuwe thread voor de print_last_command functie
        self.print_last_command_thread = threading.Thread(target=print_last_command)
        self.print_last_command_thread.daemon = True  # Stel in als daemon thread
        self.print_last_command_thread.start()  # Start de thread

    def send_command_to_pico(self, command_data):
        try:
            pico_url = 'http://192.168.0.25:5000/get_data_for_microcontroller'
            response = requests.post(pico_url, json=command_data)
            print(f"Response from Pico: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"Failed to send command to Pico: {e}")

    def setup_routes(self):
        @self.app.route('/send_data', methods=['POST'])
        def receive_data():
            data = request.json
            print("Received Data:", data)
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
            return 'OK', 200
            
        @app.route('/button_pressed', methods=['POST'])
        def button_pressed():
            global last_command
            command = request.form['command']
            
            if command == 'MOVE_FORWARD':
                last_command = 'MOVE_FORWARD'
            elif command == 'MOVE_BACKWARD':
                last_command = 'MOVE_BACKWARD'
            elif command == 'MOVE_LEFT':
                last_command = 'MOVE_LEFT'
            elif command == 'MOVE_RIGHT':
                last_command = 'MOVE_RIGHT'
            else:
                return jsonify({'error': 'Invalid command'}), 400
            
            return jsonify({'message': f'Command {command} received successfully'})

        @app.route('/get_last_command', methods=['GET'])
        def get_last_command():
            global last_command
            if last_command:
                return jsonify({'command': last_command})
            else:
                return jsonify({'error': 'No command received yet'})

        @self.app.route('/')
        def home():
            return render_template('index.html')

    def run_flask_app(self):
        self.app.run(host='0.0.0.0', port=5000)

if __name__ == '__main__':
    grid = Pathfinding()
    server = RobotServer(grid)

    # Start Flask app in een aparte thread
    flask_thread = threading.Thread(target=server.run_flask_app)
    flask_thread.daemon = True
    flask_thread.start()
    time.sleep(2)

    # Temp, alleen om te wachten voor testen
    while not server.ip_list:
        time.sleep(1)

    # Nu kun je een verzoek sturen met behulp van de requests library
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
    server.ip_list.append("192.168.0.25:5000") 
    url = f'http://{server.ip_list[0]}/send_data'
    try:
        response = requests.post(url, json=data)
    except Exception as e:
        print("Failed to send POST request:", e)

    print(response.json())

    grid.print_grid()
    # Houd de hoofdthread actief indien nodig
    while True:
        time.sleep(1)
