class BaseTileObject:
    character = "?"
    flammable = False 

    def __str__(self):
        return str(self.character)


class EmptyTile(BaseTileObject):
    character = "."
    

class Tree(BaseTileObject):
    character = "T"
    flammable = True 


class Fire(BaseTileObject):
    character = "&"