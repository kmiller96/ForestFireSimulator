from random import random, randint, sample

from forest_fire import objects


class RandomTreeGrowthEngine:
    """Randomly adds a new tree to the board."""
    
    def __init__(self, growth_probability=1.0):
        self.growth_probability = float(growth_probability)

    def step(self, board):
        if random() <= self.growth_probability:
            x = randint(0, board.xdim - 1)
            y = randint(0, board.ydim - 1)

            board[x, y] = objects.Tree()
        
        return board


class InverseDensityTreeGrowthEngine:
    """Spawns new trees inversely proportional to the density of the forest."""

    def __init__(self, decay_factor=2):
        self.decay_factor = float(decay_factor)
    
    def step(self, board):
        try:
            ntrees = len(board.find_all(objects.Tree))
            threshold = 1 / (self.decay_factor ** ntrees)
        except OverflowError as e:
            return board  # Number is so small it should be zero.

        if random() <= threshold:
            x = randint(0, board.xdim - 1)
            y = randint(0, board.ydim - 1)

            board[x, y] = objects.Tree()
        
        return board
            

class ProximityTreeGrowthEngine:
    """Tries to grow more trees around existing trees."""

    def __init__(self, distance = 1, max_growth_per_step = 1):
        self.seed_distance = int(distance)
        self.max_growth = int(max_growth_per_step)

    def step(self, board):
        new_trees_coords = []

        for (x, y), cell in board.enumerate():
            if isinstance(cell, objects.Tree):
                propogated_trees = board.adjacent(x0=x, y0=y, distance=self.seed_distance)
                new_trees_coords.extend(propogated_trees)
        
        if len(set(new_trees_coords)) > self.max_growth:
            new_trees_coords = sample(
                list(set(new_trees_coords)),  # Removes duplicate coordinates
                self.max_growth
            )
        
        for (x, y) in new_trees_coords:
            if isinstance(board[x, y], objects.Fire):
                continue  # Can't put a tree where a fire is currently.
            else:
                board[x, y] = objects.Tree()
        return board

