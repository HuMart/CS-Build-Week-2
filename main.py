import sys
from maze import Maze

print("starting the treasure hunt")
api_key = input("insert your key")

direction = input("enter the direction:")

world = Maze(api_key, command=direction)
world.move_to_room(direction)