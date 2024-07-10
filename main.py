import pygame
from random import randint
import numpy as np

class State:
    def __init__(self, name: str, position: list[int]):
        self.name = name
        self.position = pygame.Rect(position[0]-80,position[1]-20,160,40)
        self.color = pygame.Color(randint(75,225),randint(50,225),randint(50,225))
        self.transitions = []
    def draw(self, screen: pygame.Surface):
        pygame.draw.rect(screen, self.color, self.position, border_radius=5)


class Transition:
    def __init__(self, toState: int):
        self.toState = toState
    def draw(self, screen: pygame.Surface, fromPos, toStateCpy: State):
        toPos = toStateCpy.position.center
        slope = np.subtract(fromPos, toPos)
        perp = 10*([-slope[1], slope[0]] / np.linalg.norm([-slope[1], slope[0]]))
        
        pygame.draw.line(screen, "snow", np.add(fromPos, perp), np.add(toStateCpy.position.center, perp), width=4)

pygame.init()
screen = pygame.display.set_mode((1280, 720))
running = True

def draw(objs, selected, selected_2):
    for drawObj in objs:
        for transition in drawObj.transitions:
            transition.draw(screen, drawObj.position.center, objs[transition.toState])
    for drawObj in objs:
        drawObj.draw(screen)
    if (selected != None):
        pygame.draw.rect(screen, "steelblue1", objs[selected].position, width=2, border_radius=5)
    if (selected_2 != None):
        pygame.draw.rect(screen, "coral", objs[selected_2].position, width=2, border_radius=5)

def selection(objs):
    mousepos = pygame.mouse.get_pos()
    for i, drawObj in reversed(list(enumerate(objs))):
        if drawObj.position.collidepoint(mousepos):
            return i   

states = []
selected = None
selected_2 = None
mode = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if mode == 2 and selected_2 != None and selected != selected_2:
                states[selected].transitions.append(Transition(selected_2))
            mode = 0
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and mode == 0:
                states.append(State("Testing", pygame.mouse.get_pos()))
            if event.key == pygame.K_g and selected != None:
                mode = 1
            if event.key == pygame.K_w and selected != None:
                mode = 2
            if event.key == pygame.K_RETURN:
                mode = 0
    
    screen.fill("darkslategray")
    if mode == 0:
        selected = selection(states)
        selected_2 = None
    if mode == 1:
        states[selected].position.center = pygame.mouse.get_pos()
    if mode == 2:
        selected_2 = selection(states)
        pygame.draw.line(screen, "snow3", states[selected].position.center, pygame.mouse.get_pos(), width=4)
    draw(states, selected, selected_2)
    pygame.display.flip()
pygame.quit()