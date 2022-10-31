class RoundRobin:
    def __init__(self, keys):
        self.keys = keys
        self.index = -1
 
    def next(self):
        self.index = (self.index + 1) % len(self.keys)
        return self.keys[self.index]
 

