# INITIALIZATION
import pygame, math, sys, spritesheet
from pygame.locals import *

screen_size = HEIGHT, WIDTH = 640,480
screen = pygame.display.set_mode(screen_size)
clock = pygame.time.Clock()

class CharSprite(pygame.sprite.Sprite):
    GRAVITY = 2
    MAX_DOWN_SPEED = 100
    RUN_SPEED = 10
    JUMP_FORCE = -20

    def __init__(self, image_loc, position):
        pygame.sprite.Sprite.__init__(self)
        self.sprites = spritesheet.Spritesheet(image_loc)
        self.image = self.sprites.image_at(
                (128,0,32,64),colorkey=-1)
        self.rect = self.image.get_rect()
        self.position = position
        self.direction = 'right'
        self.rect.center = self.position
        self.dx, self.dy = 0,0
        self.speed = (0,0)
        self.fall = True
        self.curr_anim = []
        self.frame = 0

    def update(self, deltat, collisions):
        # SIMULATION
        # FIXME: This does not properly handle collisions
        if collisions and self.dy > 0:
            self.fall = False
            self.dy = 0
            self.anim_cycle('idle')
        # Gravity as a constant falling force
        if not collisions:
            self.dy += self.GRAVITY
            if self.dy > self.MAX_DOWN_SPEED:
                self.dy = self.MAX_DOWN_SPEED
            self.anim_cycle('jump')

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

    def anim_cycle(self, name):
        animations = {
            'idle': [
                (0,0,32,64),(32,0,32,64),
                (64,0,32,64),(96,0,32,64)],
            'jump': [
                (288,0,32,64),(320,0,32,64),
                (352,0,32,64),(382,0,32,64)],
            'run': [
                (480, 0, 32, 64),(512,0,32,64),(544,0,32,64),
                (576,0,32,64),(608,0,32,64),],
            'fall': [
                (288,0,32,64)]}
        self.curr_anim = self.sprites.images_at(
            animations[name], colorkey=-1)
        if self.direction == 'left':
            self.curr_anim = self.sprites.imagesR_at(
                animations[name], colorkey=-1)
        self.frame = 0

    def idle(self):
        # FIXME: This is very buggy, and stops unintended things.
        for i in range(self.RUN_SPEED):
            if self.direction == 'left':
                self.dx += 1 
            else:
                self.dx -= 1
        self.anim_cycle('idle')

    def run(self, direction):
        for i in range(self.RUN_SPEED):
            if direction == 'left':
                self.dx -= 1
                self.direction = 'left'
                self.anim_cycle('run')
            else:
                self.dx += 1
                self.direction = 'right'
                self.anim_cycle('run')

    def jump(self):
        if not self.fall:
            self.dy += self.JUMP_FORCE
            self.fall = True
            self.anim_cycle('jump')

class Collideable (pygame.sprite.Sprite):
    def __init__ (self, image_loc, position):
        pygame.sprite.Sprite.__init__(self)
        self.sprites = spritesheet.Spritesheet(image_loc)
        self.image = self.sprites.image_at(
                (0,352,64,64), colorkey=-1)
        self.rect = self.image.get_rect()
        self.position = position
        self.direction = 'right'
        self.rect.center = self.position

# CREATE CHARACTER PLATFORMS AND GROUP THEM 
rect = screen.get_rect()
character = CharSprite('assets/JonesSheet.png', rect.center)
platform = Collideable('assets/JonesSheet.png', (rect.center[0], rect.center[1]+200)) 
platform2 = Collideable('assets/JonesSheet.png', (rect.center[0]+100, rect.center[1] + 100))
p_group = pygame.sprite.Group()
p_group.add(character)
c_group = pygame.sprite.Group()
c_group.add(platform)
c_group.add(platform2)
while 1:
    # USER INPUT
    deltat = clock.tick(30)
    for event in pygame.event.get():
        if not hasattr(event, 'key'): continue
        down = event.type == KEYDOWN
        if event.type == KEYDOWN:
            if event.key == K_w: character.jump()
            if event.key == K_d: character.run('right')
            if event.key == K_a: character.run('left')
        if event.type == KEYUP:
            if event.key == K_a: character.idle()
            if event.key == K_d: character.idle()
        if event.key == K_ESCAPE: sys.exit(0)

    # RENDERING
    screen.fill((0,10,8))
    hit = pygame.sprite.spritecollide(character,c_group, False)
    c_group.draw(screen)
    p_group.draw(screen)
    p_group.update(deltat,hit)
    pygame.display.flip()
