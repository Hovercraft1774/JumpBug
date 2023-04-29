import pygame
from random import choice
from scripts.settings import *
vec = pg.math.Vector2


class Spritesheet:
    #utility class for loading and parsing spritesheets
    def __init__(self,filename):
        self.spritesheet = pg.image.load(filename).convert()

    def get_image(self,x,y,width,height):
        # grab an image out of a larger spritesheet
        image = pg.Surface((width,height))
        image.blit(self.spritesheet,(0,0),(x,y,width,height)) #move the image we wanted into the corner. creates new image essentially
        image = pg.transform.scale(image,(width // 2, height // 2))
        return image


class Player(pg.sprite.Sprite):#must be a sprite inherited otherwise it won't fit in groups

    def __init__(self,game,x,y,color_key):
        super(Player,self).__init__()
        self._layer = PLAYER_LAYER #sets the draw layer of the player
        self.game = game #adds reference to the game
        self.walking = False
        self.jumping = False
        self.current_frame = 0
        self.last_update = 0
        self.color_key = color_key
        self.load_image()
        # self.player_img = pg.transform.flip(self.player_img, True, True) #this flips the image along the x,y axis
        self.image = self.standing_frames[0]

        # self.image = pg.Surface((30,40))
        # self.image.fill(img_dir)

        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.pos = vec(x,y)
        self.vel = vec(0,0)
        self.acc = vec(0,0)

        self.addToGroups()

    def load_image(self):
        self.standing_frames = [self.game.spritesheet.get_image(614,1063,120,191),
                                self.game.spritesheet.get_image(690,406,120,201)]
        for frame in self.standing_frames:
            frame.set_colorkey(self.color_key)#gets rid of black color and makes it transparent
        self.walking_frames_r = [self.game.spritesheet.get_image(678,860,120,201),
                               self.game.spritesheet.get_image(692,1458,120,207)]
        self.walking_frames_l = []
        for frame in self.walking_frames_r:
            frame.set_colorkey(self.color_key)
            self.walking_frames_l.append(pg.transform.flip(frame,True,False))
        self.jump_frames = [self.game.spritesheet.get_image(416,1660,150,181)]
        for frame in self.jump_frames:
            frame.set_colorkey(self.color_key)

    def jump(self):
        #only jump if on platform. No flying
        self.rect.y += 2
        hits = pg.sprite.spritecollide(self,self.game.platform_group,False)
        self.rect.y += 2
        if hits and not self.jumping:
            self.game.jump_sound.play()
            self.jumping = True
            self.vel.y = -PLAYER_JUMP

    def jump_cut(self):
        if self.jumping:
            if self.vel.y < -7:
                self.vel.y = -7

    def update(self):
        self.animate()
        self.acc = vec(0,PLAYER_GRAV)
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            self.acc.x = -PLAYER_ACC
        if keys[pg.K_d]:
            self.acc.x = PLAYER_ACC

    # Faster you go, the more friction applies to you, also only for the x quordinate
        self.acc.x += self.vel.x * PLAYER_FRICTION
    # acceleration changes velocity, velocity defines length moved
        self.vel += self.acc
        if abs(self.vel.x) < 0.2:
            self.vel.x = 0
    # you add the half acceleration for sake of physics
        self.pos += self.vel + 0.5 * self.acc

    # makes it so game doesn't crash when on platforms, but also wraps cleanly
        if self.pos.x > WIDTH + self.rect.width / 2:
            self.pos.x = 0 - self.rect.width / 2
        if self.pos.x < 0 - self.rect.width / 2:
            self.pos.x = WIDTH + self.rect.width / 2

        self.rect.midbottom = self.pos

    def animate(self):
        now = pygame.time.get_ticks()
        if self.vel.x != 0:
            self.walking = True
        else:
            self.walking = False

        #walk animation
        if self.walking:
            if now - self.last_update>200:
                self.last_update = now
                self.current_frame = (self.current_frame+1) % len(self.walking_frames_r)
                bottom = self.rect.bottom
                if self.vel.x >0:
                    self.image = self.walking_frames_r[self.current_frame]
                else:
                    self.image = self.walking_frames_l[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
        self.mask = pg.mask.from_surface(self.image) #makes a mask from the player image

        #idle animation
        if not self.jumping and not self.walking:
            if now-self.last_update > 400: #the 400 is milliseconds
                self.last_update = now
                self.current_frame = (self.current_frame+1) % len(self.standing_frames) #use the remainder so no integer overload
                bottom = self.rect.bottom
                self.image = self.standing_frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom



    def addToGroups(self):
        self.game.all_sprites.add(self)
        self.game.player_group.add(self)

class Cloud(pg.sprite.Sprite):
    def __init__(self,game,color_key):
        self._layer = CLOUD_LAYER  # sets the draw layer of the object
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.color_key = color_key
        self.addToGroups()
        self.image = choice(self.game.cloud_images)
        self.image.set_colorkey(self.color_key)
        self.rect = self.image.get_rect()
        scale = random.randrange(50,101)/ 100
        self.image = pg.transform.scale(self.image, (int(self.rect.width*scale),
                                                     int(self.rect.height*scale)))
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-500, -50)

    def update(self):
        if self.rect.top > HEIGHT*2:
            self.kill()

    def addToGroups(self):
        self.game.all_sprites.add(self)
        self.game.cloud_group.add(self)


class Platform(pg.sprite.Sprite):
    def __init__(self,game, x, y,color_key):
        self._layer = PLATFORM_LAYER  # sets the draw layer of the object
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.color_key = color_key
        images = [self.game.spritesheet.get_image(0, 288,380,94),
                  self.game.spritesheet.get_image(213,1662,201,100)]
        self.image = random.choice(images)
        self.image.set_colorkey(self.color_key)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # Spawn Chance out of 100 for spawning powerup
        if random.randrange(100) < POW_SPAWN_PCT:
            Powerup(self.game, self, self.color_key)
        self.addToGroups()


    def addToGroups(self):
        self.game.all_sprites.add(self)
        self.game.platform_group.add(self)


class Powerup(pg.sprite.Sprite):
    def __init__(self,game, plat, color_key):
        self._layer = POW_LAYER  # sets the draw layer of the object
        self.groups = game.all_sprites,game.powerup_group #another way to add sprites to groups
        pg.sprite.Sprite.__init__(self,self.groups)
        self.game = game
        self.plat = plat
        self.type = choice(['boost'])
        images = [self.game.spritesheet.get_image(820, 1805, 71, 70)]
        self.image = random.choice(images)
        self.image.set_colorkey(color_key)
        self.rect = self.image.get_rect()
        self.rect.centerx = self.plat.rect.centerx
        self.rect.bottom = self.plat.rect.top -5

    def update(self):
        self.rect.bottom = self.plat.rect.top - 5
        if not self.game.platform_group.has(self.plat):
            self.kill()




