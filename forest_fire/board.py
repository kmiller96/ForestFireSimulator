from copy import deepcopy

from .objects import EmptyTile


class Board:
    
    def __init__(self, x, y):
        self.xdim = x
        self.ydim = y
        self.state = [[EmptyTile()] * x for _ in range(y)]
    
    def __getitem__(self, coords):
        x, y = coords
        return self.state[y][x]
    
    def __setitem__(self, coords, value):
        x, y = coords
        self.state[y][x] = value

    def __str__(self):
        board_string = ''
        for row in self.state:
            row_string = ''
            for cell in row:
                row_string += str(cell)
            board_string += row_string + '\n'

        board_string,_ = board_string.rsplit('\n', 1)  # Removes last instance of \n character
        return str(board_string)
    
    def adjacent(self, x0, y0, distance=1):
        x_range = range(x0 - distance, x0 + distance + 1)
        y_range = range(y0 - distance, y0 + distance + 1)

        adjacent_coords = [(x, y) for x in x_range for y in y_range]
        valid_adjacent_coords = []

        filters = [
            lambda x, y: x == x0 and y == y0,
            lambda x, y: x >= self.xdim or x < 0,
            lambda x, y: y >= self.ydim or y < 0,
        ]

        for x, y in adjacent_coords:
            if any([should_filter(x, y) for should_filter in filters]):
                continue
            else:
                valid_adjacent_coords.append((x, y))

        return valid_adjacent_coords
    
    def copy(self):
        return deepcopy(self)
        
    def enumerate(self):
        for y, row in enumerate(self.state):
            for x, cell in enumerate(row):
                yield ((x, y), cell)
    
    def find_all(self, object_type):
        coordinate_list = []

        for coordinate, cell in self.enumerate():
            if isinstance(cell, object_type):
                coordinate_list.append(coordinate)
        
        return coordinate_list
