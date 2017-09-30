# INITIALIZATION
import pygame, math, sys, spritesheet
from pygame.locals import *

screen = pygame.display.set_mode((1024,768))
clock = pygame.time.Clock()

class CharSprite(pygame.sprite.Sprite):
    GRAVITY = 2
    MAX_DOWN_SPEED = 100
    RUN_SPEED = 2
    JUMP_FORCE = -14
    spritesheet = spritesheet.Spritesheet('JonesSheet.png')

    def __init__(self, image, position):
        pygame.sprite.Sprite.__init__(self)
        self.src_image = self.spritesheet.image_at((0,0,32,64))
        self.position = position
        self.direction = 'right'
        self.image = self.src_image
        self.rect = self.src_image.get_rect()
        self.jump_t = False
        self.rect.center = self.position
        self.dx, self.dy = 0,0
        self.speed = (0,0)
        self.fall = True

    def update(self, deltat):
        # SIMULATION
        if self.position[1] == 580:
            self.fall = False
            if self.dy > 0 or self.dy < -14:
                self.dy = 0
        if self.fall:
            self.dy += self.GRAVITY
            if self.dy > self.MAX_DOWN_SPEED:
                self.dy = self.MAX_DOWN_SPEED

        self.speed = (self.dx,self.dy)
        x, y = self.position
        self.position = tuple(map(sum,zip((x,y),self.speed)))
        if self.speed == (0,0):
            self.src_image = self.spritesheet.image_at((0,0,32,64))
        elif self.speed != 0:
            self.src_image = self.spritesheet.image_at((320,0,32,64))
        # Gather image and ready display
        self.image = pygame.transform.flip(self.src_image,False,False )
        self.rect = self.image.get_rect()
        self.rect.center = self.position

    def run(self, direction):
        if self.position[0] < 1200:
            self.dx += self.RUN_SPEED
        run_cycle = [
            (480,0,32,64), (512,0,32,64), (544,0,32,64),
            (576,0,32,64), (608,0,32,64), (640,0,32,64)]

    def jump(self, direction):
        if not self.jump_t and self.dy == 0:
            self.dy += self.JUMP_FORCE
            self.fall = True

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
            if event.key == K_w: character.jump('right')
            if event.key == K_d: character.run('right')
        if event.key == K_ESCAPE: sys.exit(0)

    # RENDERING
    screen.fill((0,0,0))
    p_group.draw(screen)
    p_group.update(deltat)
    p_group.draw(screen)
    pygame.display.flip()
