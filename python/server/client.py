# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 14:32:41 2024

@author: spanj
"""
import json
import time
import requests

picture_json = {
  "picture": {
    "3, 3": "Red",
    "3, 4": "Blue",
    "3, 5": "Green",
    "3, 6": "Red",
    "4, 3": "Red",
    "4, 4": "Green",
    "4, 5": "Green",
    "4, 6": "Red",
    "5, 3": "Blue",
    "5, 4": "Green",
    "5, 5": "Red",
    "5, 6": "Blue",
    "6, 3": "Blue",
    "6, 4": "Red",
    "6, 5": "Blue",
    "6, 6": "Green"
  }
}


robots_json = {
  "robots": [
    {
      "name": "Robot1",
      "current_position": [1, 1],
      "color": "white",
      "angle": 0
    },
    {
      "name": "Robot2",
      "current_position": [0, 0],
      "color": "white",
      "angle": 0
    },
    {
      "name": "Robot3",
      "current_position": [5, 8],
      "color": "white",
      "angle": 0
    },
    {
      "name": "Robot4",
      "current_position": [3, 7],
      "color": "Red",
      "angle": 0
    },
    {
      "name": "Robot5",
      "current_position": [8, 2],
      "color": "Blue",
      "angle": 0
    },
    {
      "name": "Robot6",
      "current_position": [6, 9],
      "color": "Green",
      "angle": 0
    },
    {
      "name": "Robot7",
      "current_position": [2, 3],
      "color": "yellow",
      "angle": 0
    },
    {
      "name": "Robot8",
      "current_position": [9, 1],
      "color": "purple",
      "angle": 0
    },
    {
      "name": "Robot9",
      "current_position": [4, 4],
      "color": "orange",
      "angle": 0
    },
    {
      "name": "Robot10",
      "current_position": [7, 5],
      "color": "pink",
      "angle": 0
    },
    {
      "name": "Robot11",
      "current_position": [0, 6],
      "color": "gray",
      "angle": 0
    },
    {
      "name": "Robot12",
      "current_position": [5, 5],
      "color": "black",
      "angle": 0
    },
    {
      "name": "Robot13",
      "current_position": [9, 9],
      "color": "brown",
      "angle": 0
    },
    {
      "name": "Robot14",
      "current_position": [2, 8],
      "color": "cyan",
      "angle": 0
    },
    {
      "name": "Robot15",
      "current_position": [8, 3],
      "color": "magenta",
      "angle": 0
    },
    {
      "name": "Robot16",
      "current_position": [1, 9],
      "color": "lime",
      "angle": 0
    }
  ]
}

url = 'http://192.168.0.25:5000/'
# response = requests.post(url + 'send_data', json=robots_json)
# print(response.json())

# response = requests.post(url + 'send_picture', json=picture_json)
# print(response.json())

# response = requests.post(url + 'set_state', {'state': 'MOVE_FORWARD'})
# print(response.json())

robot_actions = {
    'robots': [
        {
            "name": "Robot1",
            "next_steps": ['MOVE_RIGHT', 'WAIT', 'MOVE_FORWARD']
        },
        {
            "name": "Robot2",
            "next_steps": ['MOVE_RIGHT', 'WAIT', 'MOVE_FORWARD']
        }
    ]
}

while True:
    # POST-aanvraag naar de 'set_state' route
    response = requests.post(url + 'set_state', json=robot_actions)
    if response.status_code == 200:
        try:
            data = response.json()
        except json.JSONDecodeError:
            print("Failed to decode JSON from response")
    else:
        print(f"POST request failed with status {response.status_code}")
    
    time.sleep(4)
