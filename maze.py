import sys
import requests
import json
from map_builder import Map

class Maze:

    def __init__(self, key, mapJson = [], command = ''):
        self.api_key = key
        self.url = "https://lambda-treasure-hunt.herokuapp.com/api/adv/"
        self.headers = {"Content-Type": "application/json", "Authorization": "Token" + self.api_key}

        self.map = Map()

        self.command = command
        self.pl_name = "",
        self.pl_cooldown = 0,
        self.pl_encumbrance = 0,
        self.pl_strength = 0,
        self.pl_speed = 0,
        self.pl_gold = 0,
        self.pl_inventory = [],
        self.pl_status = [],
        self.pl_error = [],
        self.pl_message = []

    def get_status(self):

        res = requests.get(self.url + "init", headers=self.headers)
        data = res.json()
        self.map.add_to_map(data)
        print(data["room_id"], "exits:", data["exits"])

    def add_to_map(self, room=None):
        if self.command:
            url = "https://lambda-treasure-hunt.herokuapp.com/api/adv/move/"
            r = requests.post(url, headers=self.headers,  json={"direction": self.command})
            new_room = r.json()
            print("New room:", new_room["cooldown"])
            self.map.add_to_map(new_room)
        else:
                print("Not working")

    def move_to_room(self, direction):
        url = "https://lambda-treasure-hunt.herokuapp.com/api/adv/move/"
        r = requests.post(url, headers=self.headers, json={"direction": direction})
        next_room = r.json()
        print(next_room["room_id"])