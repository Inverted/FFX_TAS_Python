from players.base import Player
import memory

class LuluImpl(Player):
    
    def __init__(self):
        super().__init__("Lulu", 5, [0, 20, 21, 1])
        
Lulu = LuluImpl()