import pygame
from random import randint
import numpy as np

class State:
    def __init__(self, name: str, position: list[int]):
        self.name = name
        self.position = pygame.Rect(position[0]-80,position[1]-20,160,40)
        self.color = pygame.Color(randint(200,255),randint(50,162),randint(50,100))
        self.transitions = []
    def draw(self, screen: pygame.Surface, font: pygame.font.SysFont):
        pygame.draw.rect(screen, self.color, self.position, border_radius=5)
        text = font.render(self.name, True, "snow")
        text_rect = text.get_rect(center=self.position.center)   
        screen.blit(text, text_rect)


class Transition:
    def __init__(self, toState: int):
        self.toState = toState
        self.clickBox = None
        self.selected = False
    def draw(self, screen: pygame.Surface, fromPos, toStateCpy: State):
        toPos = toStateCpy.position.center
        slope = np.subtract(fromPos, toPos)
        norm = np.linalg.norm(np.subtract(fromPos, toPos))
        slope = slope/norm
        perp = [-10*slope[1], 10*slope[0]]
        arrowPos = fromPos-((norm/2)*slope)+perp
        pygame.draw.line(screen, "steelblue1" if self.selected else "snow", np.add(fromPos, perp), np.add(toStateCpy.position.center, perp), width=4)
        self.clickBox = pygame.draw.polygon(screen, "steelblue1" if self.selected else "snow", [arrowPos, arrowPos+(10*slope)-perp, arrowPos+(10*slope)+perp])

pygame.init()
screen = pygame.display.set_mode((1280, 720))
font = pygame.font.SysFont(None, 24)
running = True

def draw(objs, selected, selected_2):
    for drawObj in objs:
        for transition in drawObj.transitions:
            transition.draw(screen, drawObj.position.center, objs[transition.toState])
    for drawObj in objs:
        drawObj.draw(screen, font)
    if (selected != None):
        pygame.draw.rect(screen, "steelblue1", objs[selected].position, width=2, border_radius=5)
    if (selected_2 != None):
        pygame.draw.rect(screen, "coral", objs[selected_2].position, width=2, border_radius=5)

def selection(objs):
    mousepos = pygame.mouse.get_pos()
    for i, drawObj in reversed(list(enumerate(objs))):
        if drawObj.position.collidepoint(mousepos):
            return i

def tr_selection(objs):
    mousepos = pygame.mouse.get_pos()
    for i, drawObj in enumerate(objs):
        for j, transition in enumerate(drawObj.transitions):
            if transition.clickBox.collidepoint(mousepos):
                return (i, j)   

states = []
selected = None
selected_2 = None
selected_tr = None
mode = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if mode == 2 and selected_2 != None and selected != selected_2:
                states[selected].transitions.append(Transition(selected_2))
            if mode == 0 and selected != None:
                mode = 1
            elif mode == 0:
                if selected_tr != None:
                    states[selected_tr[0]].transitions[selected_tr[1]].selected = False
                    selected_tr == None
                selected_tr = tr_selection(states)
                if selected_tr != None:
                    states[selected_tr[0]].transitions[selected_tr[1]].selected = True
            else:
                mode = 0
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and mode == 0:
                states.append(State("Testing", pygame.mouse.get_pos()))
            elif event.key == pygame.K_g and selected != None:
                mode = 1
            elif event.key == pygame.K_w and selected != None:
                mode = 2
            elif event.key == pygame.K_RETURN:
                mode = 0
    
    screen.fill(pygame.Color(38,70,83))
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