import pygame
from random import randint

class State:
    transitions = []
    def __init__(self, name: str, position: list[int]):
        self.name = name
        self.position = pygame.Rect(position[0]-80,position[1]-20,160,40)
        self.color = pygame.Color(randint(50,225),randint(50,225),randint(50,225))
    def draw(self, screen: pygame.Surface):
        pygame.draw.rect(screen, self.color, self.position, border_radius=5)


class Transition:
    def __init__(self, toState: State):
        self.toState = toState



# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
running = True

def draw(objs):
    for drawObj in objs:
        drawObj.draw(screen)

def selection(objs):
    mousepos = pygame.mouse.get_pos()
    for i, drawObj in reversed(list(enumerate(objs))):
        if drawObj.position.collidepoint(mousepos):
            pygame.draw.rect(screen, "steelblue1", drawObj.position, width=2, border_radius=5)
            return i   

drawables = []
selected = None

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                drawables.append(State("Testing", pygame.mouse.get_pos()))
    
    # fill the screen with a color to wipe away anything from last frame
    screen.fill("beige")
    draw(drawables)
    selected = selection(drawables)
    # flip() the display to put your work on screen
    pygame.display.flip()
pygame.quit()