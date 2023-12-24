from collections import OrderedDict

class Cache:
    def __init__(self, capacity : int = 4096):
        self.cache = OrderedDict()
        self.capacity = capacity

    def get(self, key):
        if key not in self.cache:
            return None
        else:
            self.cache.move_to_end(key)
            return self.cache[key]
    
    def put(self, key, value):
        if key in self.cache:
            self.cache.move_to_end(key)
        
        #check while of elif
        while( len(self.cache >= self.capacity)):
            self.cache.popitem(last = False)
        
        self.cache[key] = value
    