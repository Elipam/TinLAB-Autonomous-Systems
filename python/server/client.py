# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 14:32:41 2024

@author: spanj
"""
import requests

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

url = 'http://192.168.0.4:5000/send_data'
response = requests.post(url, json=data)

print(response.json())
