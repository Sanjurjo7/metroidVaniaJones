# INITIALIZATION
import pygame, math, sys, spritesheet
from pygame.locals import *

screen = pygame.display.set_mode((1024,768))
clock = pygame.time.Clock()

class CharSprite(pygame.sprite.Sprite):
    GRAVITY = (0,2)
    MAX_FORWARD_SPEED = (10,0)
    MAX_DOWN_SPEED = (0,100)
    RUN_SPEED = (2,0)
    JUMP_FORCE = (0,-14)
    spritesheet = spritesheet.Spritesheet('JonesSheet.png')

    def __init__(self, image, position):
        pygame.sprite.Sprite.__init__(self)
        self.src_image = self.spritesheet.image_at((0,0,32,64))
        self.position = position
        self.speed = (0,0)
        self.direction = 'right'
        self.image = self.src_image
        self.rect = self.src_image.get_rect()
        self.jump = False
        self.rect.center = self.position

    def update(self, deltat):
        # SIMULATION
        if self.position[1] < 480:
            self.speed = tuple(map(sum,zip(self.speed,self.GRAVITY)))
            if self.speed[1] > self.MAX_DOWN_SPEED[1]:
                self.speed[1] = self.MAX_DOWN_SPEED[1]
        elif self.jump and self.speed[1] == 0:
            self.speed = tuple(map(sum,zip(self.speed,self.JUMP_FORCE)))
        else:
            self.speed = (0,0)
        x, y = self.position
        self.position = tuple(map(sum,zip((x,y),self.speed)))
        if self.speed == (0,0):
            self.jump = False
            self.src_image = self.spritesheet.image_at((0,0,32,64))
        elif self.speed != 0:
            self.src_image = self.spritesheet.image_at((320,0,32,64))
        # Gather image and ready display
        self.image = pygame.transform.flip(self.src_image,False,False )
        self.rect = self.image.get_rect()
        self.rect.center = self.position

    def run(self, direction):
        if self.position[0] < 600:
            self.speed = tuple(map(sum,zip(self.speed,self.RUN_SPEED)))

    def jump(self, direction):
        pass

# CREATE CHARACTER AND RUN
rect = screen.get_rect()
character = CharSprite('idle', rect.center)
p_group = pygame.sprite.RenderPlain(character)
while 1:
    # USER INPUT
    deltat = clock.tick(30)
    for event in pygame.event.get():
        if not hasattr(event, 'key'): continue
        down = event.type == KEYDOWN
        if event.type == KEYDOWN:
            if event.key == K_w: character.jump = True
            if event.key == K_d: character.run('right')
            if event.key == K_a: character.run('left')
        if event.key == K_ESCAPE: sys.exit(0)

    # RENDERING
    screen.fill((0,0,0))
    p_group.draw(screen)
    p_group.update(deltat)
    p_group.draw(screen)
    pygame.display.flip()
