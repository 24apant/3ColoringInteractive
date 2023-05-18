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
dragging = False
top_line_h = 60
r = NODE_RADIUS


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
                elif b1.text == "Drag":
                    if dragging == False:
                        for n in graph.nodes:
                            if n.clicked(mX, mY):
                                dragging = n
            
            

            elif b1.clicked(mX, mY):
                if b1.state == 2:b1.set_node();b1.text = "Node";node_for_attachment = None
                elif b1.state == 0:b1.set_drag();b1.text="Drag";node_for_attachment = None
                else: b1.set_attach();b1.text = "Attach"
    

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

    graph.draw(selected=node_for_attachment)
    b1.draw()
    
    pygame.display.update()
    clock.tick(24)
    