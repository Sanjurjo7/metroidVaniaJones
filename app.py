import pygame, math, sys, spritesheet, character
from pygame.locals import *

# INITIALIZATION
screen_size = HEIGHT, WIDTH = 640,480
screen = pygame.display.set_mode(screen_size)
clock = pygame.time.Clock()

class Collideable (pygame.sprite.Sprite):
    # TODO: This code could be abstracted and extracted
    def __init__ (self, image_loc, position):
        pygame.sprite.Sprite.__init__(self)
        self.sprites = spritesheet.Spritesheet(image_loc)
        self.image = self.sprites.image_at(
                (0,352,64,32), colorkey=-1)
        self.rect = self.image.get_rect()
        self.position = position
        self.direction = 'right'
        self.rect.center = self.position

# CREATE CHARACTER AND PLATFORMS AND GROUP THEM 
rect = screen.get_rect()

# player created with the character.py file
player = character.CharSprite('assets/JonesSheet.png', rect.center)

platform = Collideable('assets/JonesSheet.png', (
    rect.center[0], rect.center[1]+200))
platform2 = Collideable('assets/JonesSheet.png', (
    rect.center[0]+100, rect.center[1] + 100))

p_group = pygame.sprite.Group()
p_group.add(player)

c_group = pygame.sprite.Group()
c_group.add(platform, platform2)

while 1:
    # USER INPUT
    deltat = clock.tick(30)
    for event in pygame.event.get():
        if not hasattr(event, 'key'): continue
        down = event.type == KEYDOWN
        if event.type == KEYDOWN:
            # d-pad keys
            if event.key == K_w: pass
            if event.key == K_d: player.run('right')
            if event.key == K_a: player.run('left')
            if event.key == K_s: pass
            # letter buttons (X,Y,A,B)
            if event.key == K_i: player.jump()
            if event.key == K_u: pass
            if event.key == K_j: pass
            if event.key == K_k: pass
            # shoulder keys
            if event.key == K_y: pass
            if event.key == K_o: pass
            # select and start
            if event.key == K_p: pass
            if event.key == K_h: pass
        if event.type == KEYUP:
            if event.key == K_a: player.idle()
            if event.key == K_d: player.idle()
        if event.key == K_ESCAPE: sys.exit(0)

    # RENDERING
    screen.fill((0,10,8))
    hit = pygame.sprite.spritecollide(player,c_group, False)
    c_group.draw(screen)
    p_group.draw(screen)
    p_group.update(deltat,hit)
    pygame.display.flip()
