# Sprite classes for Fox Jump - game
import pygame as pg
from settings import *
from random import choice
vec = pg.math.Vector2


class Spritesheet:
    # loading sprites
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()

    def get_image(self, x, y, width, height):
        # grab an image out of a spritesheet
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        image = pg.transform.scale(image, (width * 3, height * 3))
        return image


class Player(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.walking = False
        self.jumping = False
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.image = self.idle_frames[0]
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.pos = vec(40, HEIGHT - 70)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

    def load_images(self):
        # idle frames
        self.idle_frames = [self.game.spritesheet.get_image(7, 24, 18, 22),
                            self.game.spritesheet.get_image(41, 25, 19, 21),
                            self.game.spritesheet.get_image(74, 26, 21, 20),
                            self.game.spritesheet.get_image(6, 59, 19, 21)]
        for frame in self.idle_frames:
            frame.set_colorkey(BLACK)
            # walk frames
        self.walk_frames_r = [self.game.spritesheet.get_image(7, 92, 18, 22),
                              self.game.spritesheet.get_image(41, 91, 20, 22),
                              self.game.spritesheet.get_image(77, 92, 18, 22),
                              self.game.spritesheet.get_image(113, 11, 18, 22),
                              self.game.spritesheet.get_image(114, 44, 17, 22),
                              self.game.spritesheet.get_image(113, 79, 18, 22)]
        self.walk_frames_l = []
        for frame in self.walk_frames_r:
            frame.set_colorkey(BLACK)
            self.walk_frames_l.append(pg.transform.flip(frame, True, False))
        # jump frames
        self.jump_frames_r = [self.game.spritesheet.get_image(40, 57, 23, 21),
                              self.game.spritesheet.get_image(76, 55, 21, 22)]
        self.jump_frames_l = []
        for frame in self.jump_frames_r:
            frame.set_colorkey(BLACK)
            self.jump_frames_l.append(pg.transform.flip(frame, True, False))

    def jump_cut(self):
        if self.jumping:
            if self.vel.y < -3:
                self.vel.y = -5

    def jump(self):
        self.rect.y += 2
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.y -= 2
        if hits and not self.jumping:
            self.game.jump_sound.play()
            self.jumping = True
            self.vel.y = -PLAYER_JUMP

    def update(self):
        self.animate()
        self.acc = vec(0, PLAYER_GRAV)
        self.vx = 0
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.acc.x = -PLAYER_ACC
        if keys[pg.K_RIGHT]:
            self.acc.x = PLAYER_ACC

        # apply friction
        self.acc.x += self.vel.x * PLAYER_FRICTION
        # equations of motion
        self.vel += self.acc
        if abs(self.vel.x) < 0.5:
            self.vel.x = 0
        self.pos += self.vel + 0.5 * self.acc
        # moves sprite from one side of the screen to another when edge reached
        # add and substract half the width to look smoother
        if self.pos.x > WIDTH + self.rect.width / 2:
            self.pos.x = 0 - self.rect.width / 2
        if self.pos.x < 0 - self.rect.width / 2:
            self.pos.x = WIDTH + self.rect.width / 2

        self.rect.midbottom = self.pos

    def animate(self):
        now = pg.time.get_ticks()
        # check if we are walking
        if self.vel.x != 0:
            self.walking = True
        else:
            self.walking = False
        # show jumping animation if we're jumping
        if self.jumping:
            if self.vel.y < 0 and self.vel.x > 0:
                self.image = self.jump_frames_r[0]
                self.walking = False
        if self.jumping:
            if self.vel.y > 0 and self.vel.x > 0:
                self.image = self.jump_frames_r[1]
                self.walking = False
        if self.jumping:
            if self.vel.y < 0 and self.vel.x < 0:
                self.image = self.jump_frames_l[0]
                self.walking = False
        if self.jumping:
            if self.vel.y > 0 and self.vel.x < 0:
                self.image = self.jump_frames_l[1]
                self.walking = False
        # show walking animation
        if self.walking:
            if now - self.last_update > 100:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.walk_frames_l)
                bottom = self.rect.bottom
                if self.vel.x > 0:
                    self.image = self.walk_frames_r[self.current_frame]
                else:
                    self.image = self.walk_frames_l[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
        # show idle animation
        if not self.jumping and not self.walking:
            if now - self.last_update > 150:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.idle_frames)
                bottom = self.rect.bottom
                self.image = self.idle_frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom


class Platform(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        images = [self.game.spritesheet.get_image(1, 1, 61, 11),
                  self.game.spritesheet.get_image(64, 1, 31, 11)]
        self.image = choice(images)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y