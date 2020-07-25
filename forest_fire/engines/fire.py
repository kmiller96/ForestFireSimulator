from random import random, randint, choice

from forest_fire import objects

class RandomFireSourceEngine:
    """Randomly ignites a fire somewhere in the forest."""

    def __init__(self, probability=0.2, min_trees_before_ignition=0.2):
        self.probability = float(probability)
        self.min_trees = float(min_trees_before_ignition)
    
    def step(self, board):
        trees = board.find_all(objects.Tree)
        ntrees = len(trees)

        if self.min_trees < 1:
            min_n_trees = int(board.xdim * board.ydim * self.min_trees)
        else:
            min_n_trees = int(self.min_trees)

        if random() <= self.probability and ntrees > min_n_trees:
            (x, y) = choice(trees)
            board[x, y] = objects.Fire()
        return board


class FireSpreadEngine:
    """Spreads the fire in a realistic way."""

    def __init__(self, spread_probability=1.0, spread_distance=1):
        self.spread_probability = float(spread_probability)
        self.spread_distance = int(spread_distance)
    
    def step(self, board):
        fires = board.find_all(objects.Fire)

        potential_fires = []
        for (x, y) in fires:
            spread_cells = board.adjacent(x0=x, y0=y, distance=self.spread_distance)
            potential_fires.extend(spread_cells) 
        
        for (x, y) in set(potential_fires):
            if random() <= self.spread_probability and board[x, y].flammable:
                board[x, y] = objects.Fire()
        
        return board


class FireExtinguishEngine:

    def __init__(self, burnout_time):
        self.burnout_time = int(burnout_time)
        self._previous_boards = []
    
    def step(self, board):
        if len(self._previous_boards) < self.burnout_time:
            pass  # No previous state so nothing to compare.

        else:
            previous_board = self._previous_boards.pop()
            previous_fires = previous_board.find_all(objects.Fire)
            for (x, y) in previous_fires:
                board[x, y] = objects.EmptyTile()

        self._previous_boards.insert(0, board.copy()) 
        return board    