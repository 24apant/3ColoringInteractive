import pygame
import sys
from config import *
import keyboard
import objects

pygame.init()
screen = pygame.display.set_mode((GUI_W, GUI_H))
clock = pygame.time.Clock()

game_over = False
top_line_h = 60 # separates the buttons and graph
dragging = False # node that we refer to for dragging
node_for_attachment = None # Node that we refer to when attaching


graph = objects.Graph(screen)


# Current Mode of the graph
ModeButton = objects.Button(100, 20, 40, 30, ["Node", "Attach", "Drag"], {0:LIGHT_BLUE, 1:YELLOW, 2:GREEN}, gui=screen)


# Buttons managing number of colors
num_colors_button = objects.Button(200, 20, 40, 30, ["2", "3", "4", "5", "6", "7", "8"], COLORS, gui=screen)
num_colors_button.set("3")
graph.num_colors = int(num_colors_button.text)

# Buttons for increasing, decreasing the number of colors and clearing graph
down_button = objects.Button(250, 20, 40, 30, ["-"], {0:RED}, gui=screen)
up_button = objects.Button(300, 20, 40, 30, ["+"], {0:GREEN}, gui=screen)
clearGraphButton = objects.Button(400, 20, 40, 30, ["Clear"], {0:ORANGE}, gui=screen)

# Create Random Graph Button
random_graph_button = objects.Button(450, 20, 40, 30, ["Rand"], {0:LIGHT_BLUE}, gui=screen)

while not game_over:

    screen.fill((255, 255, 255))
    pygame.draw.line(screen, (0, 0, 0), (0, top_line_h), (GUI_W, top_line_h))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONUP:
            dragging = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mX, mY = pygame.mouse.get_pos()

            if mY - NODE_RADIUS >= 60:

                # if b1 is in node state
                if ModeButton.text == "Node":
                    graph.add_node(mX, mY)
                
                elif ModeButton.text == "Attach":
                    # if were on a node
                    for n in graph.nodes:
                        if n.clicked(mX, mY):
                            if node_for_attachment is not None:
                                if n==node_for_attachment:
                                # check if the edge exists
                                    pass
                                elif n.color == node_for_attachment.color != WHITE:
                                    print("Can't connect graph of same values")
                                elif not graph.edgeExists(n, node_for_attachment):
                                    graph.add_edge(node_for_attachment, n)
                                else:
                                    print("attachment already exists")
                                node_for_attachment = None
                            else:
                                node_for_attachment = n
                elif ModeButton.text == "Drag":
                    if dragging == False:
                        for n in graph.nodes:
                            if n.clicked(mX, mY):
                                dragging = n
            
            

            elif ModeButton.clicked(mX, mY):
                ModeButton.setNext()
            elif down_button.clicked(mX, mY):
                num_colors_button.setPrev()
                graph.num_colors = int(num_colors_button.text)
            elif up_button.clicked(mX, mY):
                num_colors_button.setNext()
                graph.num_colors = int(num_colors_button.text)
            elif clearGraphButton.clicked(mX, mY):
                graph.resetGraph()
            elif random_graph_button.clicked(mX, mY):
                graph.create_random_graph(990, 80)
    

    if dragging is not False:
        mX, mY = pygame.mouse.get_pos()
        dragging.vX += (mX - dragging.x) // 8
        dragging.vY += (mY - dragging.y) // 8

        
        if dragging.vX < 0:
                dragging.vX = max(-2*NODE_RADIUS, dragging.vX)
        else:
                dragging.vX = min(2*NODE_RADIUS, dragging.vX)

        if dragging.vY < 0:
                dragging.vY = max(2*-NODE_RADIUS, dragging.vY)
        else:
                dragging.vY = min(2*NODE_RADIUS, dragging.vY)


    for n in graph.nodes:
        if n.vX != 0:
            if n.vX < 0: n.vX +=1
            else: n.vX -= 1
        if n.vY != 0:
            if n.vY < 0: n.vY +=1
            else: n.vY -= 1
        

        # check for out of bounds, 
        if(n.x + NODE_RADIUS >= GUI_W) or (n.x - NODE_RADIUS <= 0):
            n.vX *= -1
        if(n.y + NODE_RADIUS >= GUI_H) or (n.y - NODE_RADIUS <= top_line_h):
            n.vY *= -1

        
        n.x += n.vX
        n.y += n.vY

        n.x = min(GUI_W-NODE_RADIUS, n.x); n.x = max(NODE_RADIUS, n.x)
        n.y = min(GUI_H-NODE_RADIUS, n.y); n.y = max(top_line_h+NODE_RADIUS, n.y)
        

    if keyboard.is_pressed("f"):
        graph.color()
    if keyboard.is_pressed("c"):
        graph.clear()
    if keyboard.is_pressed("g"):
        graph.create_random_graph(990, 80)

    graph.draw(selected=node_for_attachment)
    ModeButton.draw()
    num_colors_button.draw()
    down_button.draw()
    up_button.draw()
    clearGraphButton.draw()
    random_graph_button.draw()

    
    pygame.display.update()
    clock.tick(30)
    