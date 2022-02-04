import logging
import numpy as np
from collections import defaultdict
from enum import IntEnum

logging.basicConfig(level=logging.DEBUG, 
    format='%(asctime)s - %(levelname)s: %(message)s')
#logging.disable(logging.CRITICAL)

class Direction(IntEnum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

class NodeStatus(IntEnum):
    CLEAN = 0
    WEAKENED = 1
    INFECTED = 2
    FLAGGED = 3

def read_input(filepath):

    with open(filepath) as file: 
        text = file.read()
   
    data = defaultdict(int)
    
    rows = text.split()
    center = len(rows) // 2

    for row_idx, row in enumerate(rows):
        for col_idx, node in enumerate(row):
            if node == '#':
                # row gives position on y-axis, col gives position on x-axis
                # up: decrease in row_idx, right: increase in col_idx
                data[(col_idx, -row_idx)] = 2
    
    return data, center


def change_direction(direction, turn_direction):

    if turn_direction == 'RIGHT':
        direction = (direction+1)%4
    elif turn_direction == 'LEFT': 
        direction = (direction-1)%4
    elif turn_direction == 'REVERSE':
        direction = (direction+2)%4
    else:
        raise Exception(f'turn_direction "{turn_direction}" is not supported')

    return direction


def main():

    data, m = read_input('../input/input_day22.txt')
    
    x, y = m, -m
    direction = Direction.UP    
    n = 10000000
    infections = 0

    for i in range(n):

        # turn right is current node is infected, otherwise turn left
        if data[(x,y)] == NodeStatus.CLEAN:
            direction = change_direction(direction,'LEFT')
        elif data[(x,y)] == NodeStatus.WEAKENED:
            infections += 1 # weakened node will become infected
        elif data[(x,y)] == NodeStatus.INFECTED:
            direction = change_direction(direction,'RIGHT')
        elif data[(x,y)] == NodeStatus.FLAGGED:
            direction = change_direction(direction,'REVERSE')
        else:
            raise Exception('node status is invalid')

        # modify the state of the current node
        data[(x,y)] = (data[(x,y)] + 1) % 4
                  
        # virus carrier moves forward one step
        if direction == Direction.UP:
            y += 1
        elif direction == Direction.RIGHT:
            x += 1
        elif direction == Direction.DOWN:
            y -= 1
        elif direction == Direction.LEFT:
            x -= 1
        else:
            raise Exception('invalid direction')


    print(f'Number of bursts that caused an infection: {infections}.')


if __name__ == '__main__':
    main()