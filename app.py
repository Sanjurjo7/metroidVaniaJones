# INITIALIZATION
import pygame, math, sys, spritesheet, itertools
from pygame.locals import *

screen = pygame.display.set_mode((1024,768))
clock = pygame.time.Clock()
transp = (255,0,255)

class CharSprite(pygame.sprite.Sprite):
    GRAVITY = 2
    MAX_DOWN_SPEED = 100
    RUN_SPEED = 10
    JUMP_FORCE = -14
    spritesheetJ = spritesheet.Spritesheet('JonesSheet.png')

    def __init__(self, image, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = self.spritesheetJ.image_at((128,0,32,64))
        self.position = position
        self.direction = 'right'
        self.rect = self.image.get_rect()
        self.rect.center = self.position
        self.dx, self.dy = 0,0
        self.speed = (0,0)
        self.fall = True
        self.curr_anim = []
        self.frame = 0

    def update(self, deltat):
        # SIMULATION
        # FIXME: This is a placeholder for collision
        if self.dy >= 0 and self.position[1] >= 580:
            if self.dy > 0 or self.dy < -14:
                self.idle('right')
        # Gravity as a constant falling force
        if self.fall:
            self.dy += self.GRAVITY
            if self.dy > self.MAX_DOWN_SPEED:
                self.dy = self.MAX_DOWN_SPEED
            self.anim_cycle('jump', 'right')

        # Calculate speed vectors
        self.speed = (self.dx,self.dy)
        x, y = self.position
        self.position = tuple(map(sum,zip((x,y),self.speed)))
       
        # Gather image and ready display
        # FIXME: Images display and refresh too quickly
        self.image = self.curr_anim[self.frame]
        self.frame += 1
        self.frame = self.frame%len(self.curr_anim)
        self.rect = self.image.get_rect()
        self.rect.center = self.position

    def anim_cycle(self, name, direction):
        animations = {
            'idle': [
                (0,0,32,64),(32,0,32,64),
                (64,0,32,64),(96,0,32,64)],
            'jump': [
                (288,0,32,64),(320,0,32,64),
                (352,0,32,64),(382,0,32,64)],
            'run': [
                (480, 0, 32, 64),(512,0,32,64),(544,0,32,64),
                (576,0,32,64),(608,0,32,64),] }
        # FIXME: this code isn't causing the images to flip?
        self.curr_anim = self.spritesheetJ.images_at(
            animations[name], colorkey=transp)
        if direction == 'left':
            self.curr_anim = self.spritesheetJ.imagesR_at(animations[name], colorkey=transp)
        self.frame = 0

    def idle(self, direction):
        if self.fall:
            self.fall = False
            self.dy = 0
        self.dx = 0
        self.anim_cycle('idle', 'right')

    def run(self, direction):
        # ANIMATION GATHER
        if self.position[0] < 1200:
            for i in range(self.RUN_SPEED):
                if direction == 'left':
                    self.dx -= 1
                    self.anim_cycle('run', 'left')
                else:
                    self.dx += 1
                    self.anim_cycle('run', 'right')

    def jump(self, direction):
        if not self.fall:
            self.dy += self.JUMP_FORCE
            self.fall = True

# CREATE CHARACTER AND RUN
rect = screen.get_rect()
character = CharSprite('idle', rect.center)
p_group = pygame.sprite.RenderPlain(character)
while 1:
    # USER INPUT
    deltat = clock.tick(10)
    for event in pygame.event.get():
        if not hasattr(event, 'key'): continue
        down = event.type == KEYDOWN
        if event.type == KEYDOWN:
            if event.key == K_w: character.jump('right')
            if event.key == K_d: character.run('right')
            if event.key == K_a: character.run('left')
        if event.type == KEYUP:
            if event.key == K_a: character.idle('left')
            if event.key == K_d: character.idle('right')
        if event.key == K_ESCAPE: sys.exit(0)

    # RENDERING
    screen.fill((0,10,8))
    p_group.draw(screen)
    p_group.update(deltat)
    pygame.display.flip()
