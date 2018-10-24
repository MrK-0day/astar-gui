import pygame as pg
import math

ARA = 1

ADJACENTS = {"rook"   : [(1,0),(-1,0),(0,1),(0,-1)],
             "queen"  : [(1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)],
             "knight" : [(1,-2),(1,2),(-1,-2),(-1,2),(2,1),(2,-1),(-2,1),(-2,-1)]}

def rook(x,y):
    (x1,y1) = x
    (x2,y2) = y
    return math.sqrt(abs(x1-x2)**2 + abs(y1-y2)**2)
def queen(x,y):
    (x1,y1) = x
    (x2,y2) = y
    a,b = abs(x1-x2),abs(y1-y2)
    return max(a,b)
def knight(x,y):
    (x1,y1) = x
    (x2,y2) = y
    a,b = abs(x1-x2),abs(y1-y2)
    return max((a//2+a%2),(b//2+b%2))

HEURISTICS = {"rook"   : rook,
              "queen"  : queen,
              "knight" : knight}

class Star(object):
    def __init__(self,start,end,move_type,barriers):
        self.start,self.end = start,end
        self.moves = ADJACENTS[move_type]
        self.heuristic = HEURISTICS[move_type]
        self.barriers = barriers
        self.setup()

    def setup(self):
        self.closed_set = set((self.start,))
        self.open_set   = set()
        self.came_from = {}
        self.gx = {self.start:0}
        self.hx = {}
        self.fx = {}
        self.current = self.start
        self.current = self.follow_current_path()
        self.solution = []
        self.solved = False

    def get_neighbors(self):
        neighbors = set()
        for (i,j) in self.moves:
            check = (self.current[0]+i,self.current[1]+j)
            if check not in (self.barriers|self.closed_set):
                neighbors.add(check)
        return neighbors

    def follow_current_path(self):
        next_cell = None
        for cell in self.get_neighbors():
            tentative_gx = self.gx[self.current]+1
            if cell not in self.open_set:
                self.open_set.add(cell)
                tentative_best = True
            elif cell in self.gx and tentative_gx < self.gx[cell]:
                tentative_best = True
            else:
                tentative_best = False

            if tentative_best:
                x,y = abs(self.end[0]-cell[0]),abs(self.end[1]-cell[1])
                self.came_from[cell] = self.current
                self.gx[cell] = tentative_gx
                self.hx[cell] = ARA * self.heuristic(cell,self.end)
                self.fx[cell] = self.gx[cell]+self.hx[cell]
                if not next_cell or self.fx[cell]<self.fx[next_cell]:
                    next_cell = cell
        return next_cell

    def get_path(self,cell):
        if cell in self.came_from:
            self.solution.append(cell)
            self.get_path(self.came_from[cell])

    def evaluate(self):
        if self.open_set and not self.solved:
            for cell in self.open_set:
                if (self.current not in self.open_set) or (self.fx[cell]<self.fx[self.current]):
                    self.current = cell
            if self.current == self.end:
                self.get_path(self.current)
                self.solved = True
            self.open_set.discard(self.current)
            self.closed_set.add(self.current)
            self.current = self.follow_current_path()
        elif not self.solution:
            self.solution = "NO SOLUTION"