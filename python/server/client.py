# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 14:32:41 2024

@author: spanj
"""
import requests

picture_json = {
  "picture": {
    "3, 3": "red",
    "3, 4": "blue",
    "3, 5": "yellow",
    "3, 6": "white",
    "4, 3": "white",
    "4, 4": "green",
    "4, 5": "green",
    "4, 6": "red",
    "5, 3": "yellow",
    "5, 4": "white",
    "5, 5": "red",
    "5, 6": "blue",
    "6, 3": "blue",
    "6, 4": "red",
    "6, 5": "yellow",
    "6, 6": "green"
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
      "color": "red",
      "angle": 0
    },
    {
      "name": "Robot5",
      "current_position": [8, 2],
      "color": "blue",
      "angle": 0
    },
    {
      "name": "Robot6",
      "current_position": [6, 9],
      "color": "green",
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

url = 'http://192.168.0.69:5000/'
response = requests.post(url + 'send_data', json=robots_json)
print(response.json())

response = requests.post(url + 'send_picture', json=picture_json)
print(response.json())

response = requests.get(url + 'get_state')
print(response.json())