# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 14:32:41 2024

@author: spanj
"""
import requests

picture_json = {
  "picture": {
    "3, 3": "white",
    "3, 4": "white",
    "3, 5": "white",
    "3, 6": "white",
    "4, 3]": "white"
  }
}

robots_json = {
  "robots": [
    {
      "name": "Robot1",
      "current_position": [1, 1],
      "color": "white",
      "direction": 12
    },
    {
      "name": "Robot2",
      "current_position": [0, 0],
      "color": "white",
      "direction": 12
    },
    {
      "name": "Robot3",
      "current_position": [5, 8],
      "color": "white",
      "direction": 12
    }
  ]
}

url = 'http://192.168.0.69:5000/'
response = requests.post(url + 'send_picture', json=picture_json)

print(response.json())

response = requests.post(url + 'send_data', json=robots_json)
print(response.json())