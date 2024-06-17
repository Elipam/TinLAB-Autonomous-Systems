from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

state = "initial_state"

@app.route('/')
def index():
    return render_template('index.html', state=state)

@app.route('/button_pressed', methods=['POST'])
def button_pressed():
    try:
        command = request.form['command']

        if command == 'MOVE_FORWARD':
            MoveForward(1)
        elif command == 'MOVE_BACKWARD':
            MoveBackward(1)
        elif command == 'MOVE_LEFT':
            MoveLeft(1)
        elif command == 'MOVE_RIGHT':
            MoveRight(1)
        else:
            return jsonify({'error': 'Invalid command'}), 400

        global state
        state = command
        print(f"State updated to: {state}")

        return jsonify({'message': f'Command {command} executed successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/get_state', methods=['GET'])
def get_state():
    return jsonify({'state': state})

def MoveForward(duration):
    print(f"Moving forward for {duration} seconds")

def MoveBackward(duration):
    print(f"Moving backward for {duration} seconds")

def MoveLeft(duration):
    print(f"Turning left for {duration} seconds")

def MoveRight(duration):
    print(f"Turning right for {duration} seconds")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
