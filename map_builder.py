# import json


# class Map:

#     def __init__(self):

#         self.data = {}
#         self.map_file()

#     def map_file(self):
#         with open("map.txt") as js_file:
#             self.data = json.load(js_file)
#             print(self.data)

#     def add_to_map(self, new_room):

#         roomID = new_room["room_id"]

#         if str(roomID) in self.data:
#             print("Existing room")
#         else:
#             new_room = {
#                 "title": new_room["title"],
#                 "room_id": new_room["room_id"],
#                 "elevation": new_room["elevation"],
#                 "coordinates": new_room["coordinates"],
#                 "terrain": new_room["terrain"],
#                 "exits": new_room["exits"],
#                 "messages": new_room["messages"],
#             }

#             self.data[roomID] = new_room
            
#             with open("map.txt", 'w') as new_file:
#                 json.dump(self.data, new_file)

#             self.map_file()

