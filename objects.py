import pygame
from config import *
import random


class Graph:
    def __init__(self, gui):
        
        self.nodes = []
        self.edges = []
        self.gui = gui
        self.num_colors=3
        
    def resetGraph(self):
        self.nodes = []
        self.edges = []
        
    def draw(self, selected=None):
        # draws each node and its edges
        # for some orientation, draws each node at its location and edges connecting each node
        for e in self.edges:
            e.draw(self.gui)
        for n in self.nodes:
            n.draw(self.gui,selected=selected)
    
    def create_random_graph(self, num_nodes=10, num_attachments=10):
        
        self.resetGraph()
        num_nodes = min(40, num_nodes)
        while(len(self.nodes) < num_nodes):
            randX = random.randint(0, GUI_W)
            randY = random.randint(0, GUI_H)
            self.add_node(randX, randY)

        for i in range(num_attachments):
            randX = random.randint(0, GUI_W)
            randY = random.randint(0, GUI_H)
            self.add_edge(self.nodes[random.randint(0, len(self.nodes) - 1)], self.nodes[random.randint(0, len(self.nodes) - 1)])
    def add_node(self, x, y):
        # Check for node collisions
        r = NODE_RADIUS
        if y - NODE_RADIUS <= 60:
            return
        for n in self.nodes: # if the node is within 2r of another node, don't place it
            if n.x-2*r <= x <= n.x+2*r and n.y-2*r <= y <= n.y+2*r:
                print("Can't place node there.")
                return
        # else, place the node
        self.nodes.append(Node(x, y))

    def add_edge(self, N1, N2):
        # add an edge between N1 and N2
        self.edges.append(Edge(N1, N2))
        N1.neighbors.append(N2)
        N2.neighbors.append(N1)
    
    def edgeExists(self, N1, N2):

        # checks if an edge exists between N1 and N2
        for e in self.edges:
            if (e.v1 == N1 and e.v2 == N2) or (e.v1 == N2 and e.v2 == N1): # check for both permutations
                return True
        return False
    

    def color(self):
            for node in self.nodes:
                if node.color == WHITE:
                    # check if it has any limitations on its neighhbors
                    # map of colors and if they can apply to this node
                    colors = list(COLORS.items())
                    
                    for n in node.neighbors:
                        for z in range(len(colors)):
                            if n is not False and colors[z] is not False and n.color == colors[z][1]: colors[z] = False # type: ignore
                    # find an available color
                    for c in colors:
                        if c is not False and c[0] != -1 and int(c[0]) <= self.num_colors-1: # if the color is available and it is in the bounds of num_colors
                            # set my color to c[0]
                            node.set(c[0])
                            break
    def clear(self):
        # reset all nodes' colors
        for node in self.nodes:
            node.set(-1)

class Node:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.color = WHITE
        self.neighbors = []
        self.vX = 0 # velocity of a node at a given point
        self.vY = 0
    
    def draw(self, gui,selected=None):
        # draws a specific node at a specific location and if it is a selected node or not
        if self == selected:
            pygame.draw.circle(gui, SELECTED, [self.x, self.y], NODE_RADIUS)
        else:
            pygame.draw.circle(gui, self.color, [self.x, self.y], NODE_RADIUS)
        pygame.draw.circle(gui, BLACK, [self.x, self.y], NODE_RADIUS, 2)


    def clicked(self, mX, mY):
        # if a mouse x and y is inside a node's bounds (clicked)
        return self.x - NODE_RADIUS <= mX <= self.x+NODE_RADIUS and self.y - NODE_RADIUS <= mY <= self.y+NODE_RADIUS
    
    def set(self, val):
        # sets a value of a node and its color
        self.color = COLORS[val]

class Edge:
    def __init__(self, v1:Node, v2:Node):
        self.v1 = v1
        self.v2 = v2
        # references to its 2 vertices

    def draw(self, gui):
        # draws a specific edge at a specific location
        pygame.draw.line(gui, BLACK, (self.v1.x, self.v1.y),(self.v2.x, self.v2.y))

    


class Button:
    def __init__(self, x, y, w, h, states:list, colors:dict, gui=None):

        self.x = x
        self.y = y
        self.w = w
        self.h = h
                
        self.gui = gui
        self.states = states # default button
        self.colors = colors
        self.state = 0
        self.text = self.states[0]


    def set_states(self, states, colors=None):
        self.states = states
        if colors != None:
            self.colors = colors

    def clicked(self, mX, mY):
        return self.x <= mX <= self.x + self.w and self.y <= mY <= self.y+self.h
    
    def draw(self):
        assert self.gui != None
        pygame.draw.rect(self.gui, self.colors[self.state], [self.x, self.y, self.w, self.h])
        pygame.draw.rect(self.gui, BLACK, [self.x, self.y, self.w, self.h], 2)
        # draw the text on
        text = pygame.font.Font('freesansbold.ttf', 10).render(self.text, True, (0, 0, 0))
        self.gui.blit(text, (self.x+self.w//max(2,len(self.text)), self.y+self.h//max(2, len(self.text)-1)))

    def set(self, s:str):
        if s in self.states: self.state = self.states.index(s)
        self.color = self.colors[self.state]
        self.text = self.states[self.state]

    def setNext(self):
        self.state = (self.state + 1) % len(self.states)
        self.color = self.colors[self.state]
        self.text = self.states[self.state]

    def setPrev(self):
        if self.state == 0:
            self.state = len(self.states) - 1
        else:
            self.state = (self.state - 1)
        self.color = self.colors[self.state]
        self.text = self.states[self.state]