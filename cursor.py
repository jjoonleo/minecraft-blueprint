from block import *

class Cursor:
    def __init__(self, clickState = False, block = Block("grass_block_side",1), layer = 0):
        self.clickState = clickState
        self.block = block
        self.layer = layer
        pass
    
    
