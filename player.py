import json
import time
import random
import requests
from cpu import CPU

URL = "https://lambda-treasure-hunt.herokuapp.com/api/adv"
HEADERS = {"Authorization": "Token 5eb6cf7b74fecb698b5a9d227cce7f23d013bedd"}

map = []

with open("map.txt", "r" ) as f:
    for line in f:
        # print(line)
        map = json.loads(line)

    # print(f"first room: {map[0]}")

def look_for_shop(gold):
    queue = []
    visited = set()
    init = requests.get(url= f"{URL}/init/", headers= HEADERS)
    init_res = json.loads(init.text)
    time.sleep(init_res['cooldown'])
    current_room = init_res['room_id']
    queue.append([map[current_room]])
    

    while len(queue)> 0:
        path = queue.pop()
        vertex = path[-1]

        if vertex['room_id'] not in visited:
            print(vertex['title'])
            visited.add(vertex['room_id'])
            if vertex['title'] == "Shop":
                directions = []
                for i in range(0, len(path)-1):
                    for x in path[i]['exits']:
                        if path[i]['exits'][x] == path[i + 1]['room_id']:
                            directions.append({"direction": x, "id": path[i + 1]['room_id']})
                
                for i in directions:
                    r = requests.post(url = f"{URL}/move/", headers = HEADERS, json = {"direction": i["direction"], "next_room_id": f"{i['id']}"})
                    res = json.loads(r.text)
                    print(res)
                    time.sleep(res['cooldown'])
                break

            for i in vertex['exits']:
                if vertex['exits'][i] is not None and vertex['exits'][i] not in visited:
                    new_path = list(path)
                    new_path.append(map[vertex["exits"][i]])
                    queue.insert(0, new_path)
    
    r = requests.post(url = f"{URL}/status/", headers = HEADERS)
    res = json.loads(r.text)
    gold = res['gold']
    print(res)
    time.sleep(res['cooldown'])

    if len(res["inventory"]) > 0:
        for i in range(0, len(res["inventory"])):
            if "treasure" in res["inventory"][i]:
                r = requests.post(url = f"{URL}/sell/", headers = HEADERS, json = {"name": res["inventory"][i]})
                result = json.loads(r.text)
                print(f"{result}")
                time.sleep(result['cooldown'])

                r = requests.post(url = f"{URL}/sell/", headers = HEADERS, json = {"name": res["inventory"][i], "confirm":"yes"})
                result = json.loads(r.text)
                print(f"RESULT: {result}")
                time.sleep(result['cooldown'])

                

def look_for_gold():
    opposites = {
        "n": "s",
        "s": "n",
        "e": "w",
        "w": "e"
    }
    init = requests.get(url = f"{URL}/init/",  headers = HEADERS)
    init_res = json.loads(init.text)
    time.sleep(init_res['cooldown'])
    current_room_id = init_res['room_id']
    current_room = init_res
      
    
    status = requests.post(url = f"{URL}/status/", headers = HEADERS)
    status_res = json.loads(status.text)
    strength = status_res["strength"]
    encumbrance = status_res["encumbrance"]
    time.sleep(status_res["cooldown"])  

    visited = ()
    ready_for_sale = False
    last_move = None
    
    
    while ready_for_sale is False:
        directions = []
        for i in map[current_room_id]["exits"]:
            if map[current_room_id]['exits'][i] is not None:
                if last_move is None or i not in opposites[last_move]:
                    directions.append(i)
        if len(directions) == 0:
            break
        print(directions)
        choice = random.randrange(0, len(directions))
        last_move = directions[choice]
        if len(current_room['items']) > 0:
            for i in current_room['items']:
                if "treasure" in i:
                    item = requests.post(url = f"{URL}/examine/", headers = HEADERS, json = {"name":i})
                    item_res = json.loads(item.text)
                    print(item_res)
                    weight = item_res["weight"]
                    time.sleep(item_res["cooldown"])

                if weight <= strength - encumbrance:
                    encumbrance += weight
                    grab = requests.post(url = f"{URL}/take/", headers = HEADERS, json = {"name": i})
                    grab_res = json.loads(grab.text)
                    time.sleep(grab_res['cooldown'])
                    if encumbrance == strength:
                        ready_for_sale = True
                    break
                else:
                    ready_for_sale = True

        r = requests.post(url = f"{URL}/move/", headers = HEADERS, json = {"direction": last_move, "next_room_id": f"{map[current_room_id]['exits'][last_move]}"})
        room_res = json.loads(r.text)
        print(room_res)
        current_room = room_res
        current_room_id = room_res['room_id']
        time.sleep(room_res["cooldown"])



def change_name():
    queue = []
    visited = set()
    init = requests.get(url = f"{URL}/init/",  headers = HEADERS)
    init_res = json.loads(init.text)
    time.sleep(init_res["cooldown"])
    current_room = init_res['room_id']
    queue.append([map[current_room]])

    while len(queue) > 0:
        path = queue.pop()
        vertex = path[-1]
        if vertex["room_id"] not in visited:
            
            print(vertex['title'])
            visited.add(vertex["room_id"])
            
            if vertex["title"] == "Pirate Ry's":
                directions = []
                for i in range(0, len(path)-1):
                    for x in path[i]["exits"]:
                        if path[i]["exits"][x] == path[i + 1]["room_id"]:
                            directions.append({"direction": x, "id": path[i + 1]['room_id']})
                
                for i in directions:
                    r = requests.post(url = f"{URL}/move/", headers = HEADERS, json = {"direction": i["direction"], "next_room_id": f"{i['id']}"})
                    res = json.loads(r.text)
                    print(res)
                    time.sleep(res["cooldown"])
                break

            for i in vertex["exits"]:
                if vertex["exits"][i] is not None and vertex["exits"][i] not in visited:
                    new_path = list(path)
                    new_path.append(map[vertex["exits"][i]])
                    queue.insert(0, new_path)
    
    new_name = "Lame Pirate"
    r = requests.post(url = f"{URL}/status/", headers = HEADERS)
    res = json.loads(r.text)
    print(res)
    time.sleep(res['cooldown'])    
    if res["gold"] >= 1000:
        r = requests.post(url = f"{URL}/change_name/", headers = HEADERS, json = {"name": f"{new_name}", "confirm": "aye"})
        result = json.loads(r.text)
        print(result)
        # time.sleep(res["cooldown"]
    else:
        print("You need more gold")

def look_for_coordenates(coord):
    queue = []
    visited = set()
    init = requests.get(url = f"{URL}/init/",  headers = HEADERS)
    init_res = json.loads(init.text)
    time.sleep(init_res["cooldown"])
    current_room = init_res['room_id']
    queue.append([map[current_room]])

    while len(queue) > 0:
        path = queue.pop()
        vertex = path[-1]

        if vertex["room_id"] not in visited:
            print(vertex["title"])
            visited.add(vertex["room_id"])
            if vertex["coordinates"] == coord:
                directions = []
                for i in range(0, len(path)-1):
                    for x in path[i]["exits"]:
                        if path[i]["exits"][x] == path[i + 1]["room_id"]:
                            directions.append({"direction": x, "id": path[i + 1]["room_id"]})
                
                for i in directions:
                    r = requests.post(url = f"{URL}/move/", headers = HEADERS, json = {"direction": i["direction"], "next_room_id": f"{i['id']}"})
                    res = json.loads(r.text)
                    print(res)
                    time.sleep(res["cooldown"])
                break

            for i in vertex["exits"]:
                if vertex["exits"][i] is not None and vertex["exits"][i] not in visited:
                    new_path = list(path)
                    new_path.append(map[vertex["exits"][i]])
                    queue.insert(0, new_path)


    



# look_for_gold()
# look_for_shop(1000)
# change_name()
 
end = requests.get(url = "https://lambda-treasure-hunt.herokuapp.com/api/bc/get_balance/", headers = HEADERS)
end_res = json.loads(end.text)
print(end_res)
# look_for_coordenates("(63,61)")
# pray = requests.post(url = f"{URL}/pray/", headers = HEADERS)
# pray_res = json.loads(pray.text)
# time.sleep(pray_res["cooldown"])


# look_for_coordenates( "(52,52)") 
# well = requests.post(url = f"{URL}/examine/", headers = HEADERS, json = {"name": "well"})
# well_res = well.json()
# with open("well.txt", "w") as outfile:
#     outfile.write(well_res['description'][39:])
# outfile.close()
# cpu = CPU()
# cpu.load('well.txt')
# time.sleep(well_res['cooldown'])
# run_mine = ''.join(cpu.run()[23:])
# print(run_mine)

        

    
       


# find_by_coord("(51,60)")  