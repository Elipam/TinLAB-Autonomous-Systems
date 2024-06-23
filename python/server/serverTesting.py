"""
Program to test server endpoints and formats.
First run server.py, either on the same pc or more like the actual use case on another pc with local ip 192.168.0.69
Then run serverTesting.py (this file) and compare outputs with the comments
"""
import requests

picture_json = {
  "picture": {
    "3, 3": "red",
    "3, 4": "blue",
    "3, 5": "green",
    "3, 6": "red",
    "4, 3": "red",
    "4, 4": "green",
    "4, 5": "green",
    "4, 6": "red",
    "5, 3": "blue",
    "5, 4": "green",
    "5, 5": "red",
    "5, 6": "blue",
    "6, 3": "blue",
    "6, 4": "red",
    "6, 5": "blue",
    "6, 6": "green"
  }
}


robots_json = {
    "robots": [
        {
        "name": "Robot1",
        "current_position": [1, 1],
        "color": "green",
        "angle": 0
        },
        {
        "name": "Robot2",
        "current_position": [0, 0],
        "color": "green",
        "angle": 0
        }
    ]
}

ip = '127.0.0.1'
# ip = '192.168.0.69'
url = 'http://' + ip + ':5000/'

response = requests.post(url + 'send_picture', json=picture_json)
print(response.json())
response = requests.post(url + 'send_data', json=robots_json)
print(response.json())

response = requests.get(url + 'get_data')
print(response.json())
# "robots": [
#   {
#     "name": "Robot1",
#     "current_position": [1, 1],
#     "next_position": [1, 2],
#   },
#   {
#     "name": "Robot2",
#     "current_position": [2, 1],
#     "next_position": [2, 2],
#   }
# ]


response = requests.get(url + 'get_state')
print(response.json())
# {
#     "name": "Robot1",
#     "next_steps": ['TURN_RIGHT', 'MOVE_FORWARD', 'TURN_LEFT']
# },
# {
#     "name": "Robot2",
#     "next_steps": ['TURN_RIGHT', 'MOVE_FORWARD', 'TURN_LEFT']
# }