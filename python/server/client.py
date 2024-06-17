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
    "4, 3": "white"
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
    },
    {
      "name": "Robot4",
      "current_position": [3, 7],
      "color": "red",
      "direction": 6
    },
    {
      "name": "Robot5",
      "current_position": [8, 2],
      "color": "blue",
      "direction": 3
    },
    {
      "name": "Robot6",
      "current_position": [6, 9],
      "color": "green",
      "direction": 9
    },
    {
      "name": "Robot7",
      "current_position": [2, 3],
      "color": "yellow",
      "direction": 2
    },
    {
      "name": "Robot8",
      "current_position": [9, 1],
      "color": "purple",
      "direction": 4
    },
    {
      "name": "Robot9",
      "current_position": [4, 4],
      "color": "orange",
      "direction": 7
    },
    {
      "name": "Robot10",
      "current_position": [7, 5],
      "color": "pink",
      "direction": 1
    },
    {
      "name": "Robot11",
      "current_position": [0, 6],
      "color": "gray",
      "direction": 5
    },
    {
      "name": "Robot12",
      "current_position": [5, 5],
      "color": "black",
      "direction": 8
    },
    {
      "name": "Robot13",
      "current_position": [9, 9],
      "color": "brown",
      "direction": 11
    },
    {
      "name": "Robot14",
      "current_position": [2, 8],
      "color": "cyan",
      "direction": 10
    },
    {
      "name": "Robot15",
      "current_position": [8, 3],
      "color": "magenta",
      "direction": 0
    },
    {
      "name": "Robot16",
      "current_position": [1, 9],
      "color": "lime",
      "direction": 13
    }
  ]
}

url = 'http://192.168.0.69:5000/'
response = requests.post(url + 'send_data', json=robots_json)
print(response.json())

response = requests.post(url + 'send_picture', json=picture_json)
print(response.json())

response = requests.get(url + 'get_data')
print(response.json())