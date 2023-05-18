import pygame
import config

from config import *


class Graph:
    def __init__(self, gui):
        self.nodes = []
        self.edges = []
        self.gui = gui
    def draw(self,selected=None):
        # draws each node and its edges
        # for some orientation, draws each node at its location and edges connecting each node
        for e in self.edges:
            e.draw(self.gui)
        for n in self.nodes:
            n.draw(self.gui,selected=selected)
    
    def add_node(self, x, y):
        # Check for node collisions
        r = config.NODE_RADIUS
        for n in self.nodes:
            if n.x-2*r <= x <= n.x+2*r and n.y-2*r <= y <= n.y+2*r:
                print("Can't place node there.")
                return
        self.nodes.append(Node(x, y))
    def add_edge(self, N1, N2):
        self.edges.append(Edge(N1, N2))
        N1.neighbors.append(N2)
        N2.neighbors.append(N1)
    
    def edgeExists(self, N1, N2):
        for e in self.edges:
            if (e.v1 == N1 and e.v2 == N2) or (e.v1 == N2 and e.v2 == N1):
                return True
        return False
    

    def color(self):
            for node in self.nodes:
                if node.value == "":
                    # check if it has any limitations on its neighhbors
                    # map of colors and if they can apply to this node
                    colors = {"True":True,"Buffer":True ,"False":True}
                    for n in node.neighbors:
                        if n.value in colors: colors[n.value] = False
                    # find an available color
                    for c in colors.items():
                        if c[1] == True:
                            # set my color to c[0]
                            node.set(c[0])
    def clear(self):
        for node in self.nodes:
            node.set("")

class Node:
    def __init__(self, x: int, y: int):
        self.value = ""
        self.x = x
        self.y = y
        self.color = config.WHITE
        self.neighbors = []
        self.vX = 0
        self.vY = 0
    
    def draw(self, gui,selected=None):
        if self == selected:
            pygame.draw.circle(gui, SELECTED, [self.x, self.y], config.NODE_RADIUS)
        else:
            pygame.draw.circle(gui, self.color, [self.x, self.y], config.NODE_RADIUS)
        pygame.draw.circle(gui, config.BLACK, [self.x, self.y], config.NODE_RADIUS, 2)
    def clicked(self, mX, mY):
        return self.x - NODE_RADIUS <= mX <= self.x+NODE_RADIUS and self.y - NODE_RADIUS <= mY <= self.y+NODE_RADIUS
    
    def set(self, val):
        # sets a value - parameter checking to make sure the input is valid
        if val == "True":
            self.color=config.GREEN
        elif val == "False":
            self.color=config.RED
        elif val == "Buffer":
            self.color = config.BLUE
        elif val == "":
            self.color = (255, 255, 255)
        else:
            raise BaseException("Value '" + val + "' not valid.")
        self.value = val

class Edge:
    def __init__(self, v1:Node, v2:Node):
        self.v1 = v1
        self.v2 = v2
    def draw(self, gui):
        # draws a specific edge at a specific location
        pygame.draw.line(gui, config.BLACK, (self.v1.x, self.v1.y),(self.v2.x, self.v2.y))

    


class Button:
    def __init__(self, x, y, w, h, text="", gui=None):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = LIGHT_BLUE
        self.text = text
        self.gui = gui
        self.state = 1

    def clicked(self, mX, mY):
        return self.x <= mX <= self.x + self.w and self.y <= mY <= self.y+self.h
    def draw(self):
        assert self.gui != None
        pygame.draw.rect(self.gui, self.color, [self.x, self.y, self.w, self.h])
        pygame.draw.rect(self.gui, BLACK, [self.x, self.y, self.w, self.h], 2)
        # draw the text on
        text = pygame.font.Font('freesansbold.ttf', 10).render(self.text, True, (0, 0, 0))
        self.gui.blit(text, (self.x+self.w//len(self.text), self.y+self.h//(len(self.text)-1)))

    def set_node(self):
        self.state = 1
        self.color = LIGHT_BLUE
    def set_attach(self):
        self.state = 0
        self.color = YELLOW
    def set_drag(self):
        self.state = 2
        self.color = GREEN