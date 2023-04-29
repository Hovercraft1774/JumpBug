from scripts.settings import *
from scripts.player import *





class Mob(pg.sprite.Sprite):
    def __init__(self, game, color_key):
        self._layer = MOB_LAYER  # sets the draw layer of the object
        self.groups = game.all_sprites, game.mob_group  # another way to add sprites to groups
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image_up = self.game.spritesheet.get_image(566,510,122,139)
        self.image_up.set_colorkey(color_key)
        self.image_down = self.game.spritesheet.get_image(568,1534,122,135)
        self.image_down.set_colorkey(color_key)
        self.image = self.image_up
        self.rect = self.image.get_rect()
        self.rect.centerx = choice([-100, WIDTH+100])
        self.vx = random.randrange(1,4) #enemy speed
        if self.rect.centerx > WIDTH:
            self.vx *= -1
        self.rect.y = random.randrange(HEIGHT/2)
        self.vy = 0
        self.dy = 0.5

    def update(self):
        self.rect.x += self.vx
        self.vy += self.dy
        if self.vy > 3 or self.vy < -3:
            self.dy *= -1
        center = self.rect.center
        if self.dy <0:
            self.image = self.image_up
        else:
            self.image = self.image_down
        self.rect = self.image.get_rect()
        self.mask = pg.mask.from_surface(self.image) #creates mask, you can also create masks after rectangle collisions to help with lag
        self.rect.center = center
        self.rect.y += self.vy
        if self.rect.left > WIDTH +100 or self.rect.right < -100:
            self.kill()


