import pygame
import sys
from config import *
import keyboard
import objects

pygame.init()
screen = pygame.display.set_mode((GUI_W, GUI_H))
clock = pygame.time.Clock()
game_over = False
graph = objects.Graph(screen)
b1 = objects.Button(100, 20, 40, 30, gui=screen, text="Node")
node_for_attachment = None

while not game_over:

    screen.fill((255, 255, 255))
    pygame.draw.line(screen, (0, 0, 0), (0, 60), (GUI_W, 60))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mX, mY = pygame.mouse.get_pos()

            if mY - NODE_RADIUS >= 60:

                # if b1 is in node state
                if b1.text == "Node":
                    graph.add_node(mX, mY)
                
                elif b1.text == "Attach":
                    # if were on a node
                    for n in graph.nodes:
                        if n.clicked(mX, mY):
                            if node_for_attachment is not None:
                                if n==node_for_attachment:
                                # check if the edge exists
                                    pass
                                elif n.value == node_for_attachment.value != "":
                                    print("Can't connect graph of same values")
                                elif not graph.edgeExists(n, node_for_attachment):
                                    graph.add_edge(node_for_attachment, n)
                                else:
                                    print("attachment already exists")
                                node_for_attachment = None
                            else:
                                node_for_attachment = n

            elif b1.clicked(mX, mY):
                if b1.state == 1:b1.deactivate();b1.text = "Node";node_for_attachment = None
                else: b1.activate();b1.text = "Attach"
    
    if keyboard.is_pressed("f"):
        graph.color()
    if keyboard.is_pressed("c"):
        graph.clear()

    graph.draw(selected=node_for_attachment)
    b1.draw()
    
    pygame.display.update()
    clock.tick(60)
    