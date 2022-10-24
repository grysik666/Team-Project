import math

class Data:
    def __init__(self, centre, house):
        self.centre = centre
        self.house = house

    def distance(self):
        return math.sqrt((self.centre[0]-self.house[0])^2+(self.centre[1]-self.house[1])^2)

