import json
import requests
import sys
import time

rooms = ["?"] * 500

URL = "https://lambda-treasure-hunt.herokuapp.com/api/adv/move/"
HEADERS = {"Authorization": "Token 5eb6cf7b74fecb698b5a9d227cce7f23d013bedd"}
def map_graph():
    visited = set()
    opposites = {"n":"s", "s":"n", "e":"w", "w":"e"}

    init = requests.get(url = "https://lambda-treasure-hunt.herokuapp.com/api/adv/init/", headers = HEADERS)
    init_response = json.loads(init.text)
    print(init_response["messages"])
    time.sleep(init_response["cooldown"])

    current_room = init_response["room_id"]
    previous_room = "?"

    init_exits = {"n": "?", "s": "?", "e": "?", "w": "?",}

    for i in init_response["exits"]:
        init_exits[i] = i

    rooms[current_room] = init_response.copy()
    rooms[current_room]["exits"] = init_exits.copy()

    directions = []
    path = []

    for i in init_response["exits"]:
        directions.append({"room_id": current_room, "direction": i})

    dead_end = False
    

    while len(directions) > 0:
        go_back = False
        if dead_end:
            print("dead end")

        visited.add(current_room)
        previous_room = current_room
        direction = directions.pop()

        while current_room != direction["room_id"] and len(path) > 0:

            go_back = True
            print(f"Going back {len(path)}")
            back = path.pop()
            if rooms[current_room]:
                print(rooms[current_room]["exits"][opposites[back]])
                r = requests.post(url = URL, headers = HEADERS, json = {"direction": opposites[back], "next_room_id": f"{rooms[current_room]['exits'][opposites[back]]}"})
                res = json.loads(r.text)
                time.sleep(res["cooldown"])
                print(res)
                
            else:
                r = requests.post(url = URL, headers = HEADERS, json = {"direction": opposites[back]})
                res = json.loads(r.text)
            # print(res["messages"])
            print(res["errors"])
            print(res["cooldown"])
            current_room = res["room_id"]
            previous_room = current_room
            time.sleep(res["cooldown"])

        if len(path) == 0 and current_room != direction["room_id"]:
            print(previous_room)
            print(direction)
            print(current_room)

            with open("map.txt", "w") as map_file:
                map_file.write(f"{init_response}")
                map_file.write(f"\n")
                map_file.write(f"{direction}")
                map_file.write(f"\n")
                map_file.write(f"{current_room}")
                map_file.write(f"\n")
                map_file.write(f"{rooms}")
                map_file.write(f"/n")
                # map_file.write
            print("Exit")
            exit()
    
        print(f"Progress: {len(visited)}")

        path.append(direction["direction"])
        r = requests.post(url = URL, headers = HEADERS, json = {"direction": direction["direction"]})
        res = json.loads(r.text)

        print(f"Room ID: {res['room_id']}")
        print(res["messages"])
        print(res["errors"])
        print(res["cooldown"])
        time.sleep(res["cooldown"])

        current_room = res["room_id"]
        print(current_room)

        if res["room_id"] not in visited:
            exits = {"e": "?", "w": "?", "n": "?", "s": "?"}    

            for i in res["exits"]:
                exits[i] = i
            rooms[res["room_id"]] = res.copy()
            rooms[res["room_id"]]["exits"] = exits.copy()

            for i in res["exits"]:
                if opposites[i] != direction["direction"]:
                    directions.append({"room_id": res["room_id"], "direction": i})          
    
        rooms[int(previous_room)]["exits"][direction["direction"]] = current_room
        rooms[int(current_room)]["exits"][opposites[direction["direction"]]] = previous_room

        if current_room in visited and go_back is False:
            dead_end = True
            print("Again here?? ")
            print(f"current: {rooms[current_room]}")
            print(f"previous: {rooms[previous_room]}")
            print("I'll try to reverse one room")
            print(f"Going back... {len(path)}")
            back = path.pop()

            if rooms[current_room]:
                print(rooms[current_room]["exits"][opposites[back]])
                r = requests.post(url = URL, headers = HEADERS, json = {"direction": opposites[back], "next_room_id": f"{rooms[current_room]['exits'][opposites[back]]}"})
                res = json.loads(r.text)
                print(res)
        
            else:
                r = requests.post(url = URL, headers = HEADERS, json = {"direction": opposites[back]})
                res = json.loads(r.text)

            print(res["messages"])
            print(res["errors"])
            print(res["cooldown"])
            current_room = res["room_id"]
            previous_room = current_room
            time.sleep(res["cooldown"])

        with open("map.txt", "w") as map_file:
            map_file.write(rooms.__str__())

map_graph()


