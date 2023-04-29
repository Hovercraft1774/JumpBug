#Jump Bug (Tyler Johnson)


import pygame as pg
import random
from scripts.settings import *
from scripts.player import *
from scripts.enemy import *

class Game:
    def __init__(self):
        # initialize game window, etc
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.font_name = pg.font.match_font(FONT_NAME) #gets the closest font to given for each different operating system



    def load_data(self):
        #load high score
        with open(HS_FILE,'r') as f:
            try:
                self.highscore = int(f.read())
            except:
                self.highscore = 0

        #load spritesheet image
        self.spritesheet = Spritesheet(SPRITESHEET)
        #Cloud images
        self.cloud_images = []
        for i in range(1,4):
            self.cloud_images.append(pg.image.load(os.path.join(backgroundSprites, 'cloud{}.png'.format(i))).convert())
        #load sounds
        self.jump_sound = pg.mixer.Sound(jump_sound_effect)
        self.boost_sound = pg.mixer.Sound(boost_sound_effect)
        self.jump_sound.set_volume(0.1)
        self.boost_sound.set_volume(0.1)


    def new(self):
        # start a new game
        self.score = 0
        self.all_sprites = pg.sprite.LayeredUpdates() #allows for varrying draw times for layers.
        self.player_group = pg.sprite.Group()
        self.platform_group = pg.sprite.Group()
        self.cloud_group = pg.sprite.Group()
        self.powerup_group = pg.sprite.Group()
        self.mob_group = pg.sprite.Group()
        self.player = Player(self,60, HEIGHT-100,DEFAULT_COLOR)
        for plat in PLATFORM_LIST:
            Platform(self,*plat,DEFAULT_COLOR) #star stands for explode. It takes all the parts of a list and splits them up
        self.mob_timer = 0
        pg.mixer.music.load(default_music)
        pg.mixer.music.set_volume(0.1)
        for i in range(10):
            c = Cloud(self, DEFAULT_COLOR)
            c.rect.y += 500
        self.run()


    def run(self):
        # Game Loop
        pg.mixer.music.play(loops=-1) #loops the music infinitely
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
        pg.mixer.music.fadeout(500) #makes the music fade instead of stop

    def events(self):
        # Game Loop - events
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    pg.quit()
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.jump()
            if event.type == pg.KEYUP:
                if event.key == pg.K_SPACE:
                    self.player.jump_cut()

    def update(self):
        # Game Loop - Update
        self.all_sprites.update()

        #spawn a mob?
        now = pg.time.get_ticks()
        if now-self.mob_timer > 5000 + random.choice([-1000,-500, 0, 500, 1000]): #changing the spawn time slightly for enemies
            self.mob_timer = now
            Mob(self, DEFAULT_COLOR)

        #check platform collisions
        if self.player.vel.y > 0: # makes it so that it doesn't interupt movement when coming through the bottom
            hits = pg.sprite.spritecollide(self.player,self.platform_group,False)
            if hits:
                lowest = hits[0]
                for hit in hits:
                    if hit.rect.bottom > lowest.rect.bottom:
                        lowest = hit
                if self.player.pos.x < lowest.rect.right +10 and\
                    self.player.pos.x > lowest.rect.left-10:
                    if self.player.pos.y < lowest.rect.centery: #only snap to bottom if feet are above platform
                        self.player.pos.y = lowest.rect.top
                        self.player.vel.y = 0
                        self.player.jumping = False

        #if the player is in the top 1/4 of the screen scroll screen
        if self.player.rect.top <= HEIGHT/4:
            if random.randrange(100) < 10:
                Cloud(self,DEFAULT_COLOR)
            self.player.pos.y  += max(abs(self.player.vel.y), 2)#gets the absolute value of the player
            for cloud in self.cloud_group:
                cloud.rect.y += max(abs(self.player.vel.y / 2), 2)
            for plat in self.platform_group:
                plat.rect.y += max(abs(self.player.vel.y),2) #absolute value
                if plat.rect.y >= HEIGHT:
                    plat.kill()
                    self.score += 10
            for mob in self.mob_group:
                mob.rect.y += max(abs(self.player.vel.y),2) #absolute value
                if mob.rect.y >= HEIGHT:
                    mob.kill()

        #if player hits a mob
        mob_hits = pg.sprite.spritecollide(self.player,self.mob_group,False, pg.sprite.collide_mask)
        if mob_hits:
            self.playing = False

        #if player hits a powerup
        pow_hits = pg.sprite.spritecollide(self.player,self.powerup_group,True)
        for pow in pow_hits:
            if pow.type == "boost":
                self.boost_sound.play()
                self.player.vel.y += -BOOST_POWER
                self.player.jumping = False

        #Death
        if self.player.rect.top > HEIGHT:
            for sprite in self.all_sprites:
                sprite.rect.y -=max(self.player.vel.y,10) #use the max so that you don't fall too slow or fast
                if sprite.rect.bottom < -10:
                    sprite.kill()
            if len(self.platform_group) == 0:
                self.playing = False

        #spawn new platforms to keep same average number
        while len(self.platform_group) < 6:
            width = random.randrange(50,100)
            p = Platform(self,random.randrange(0,WIDTH-width),
                         random.randrange(-75, -35), DEFAULT_COLOR)


    def draw(self):
        # Game Loop - draw
        self.screen.fill(BG_COLOR)
        self.all_sprites.draw(self.screen)
        self.screen.blit(self.player.image, self.player.rect)
        self.draw_text(str(self.score),22,WHITE,WIDTH/2, 15)
        # *after* drawing everything, flip the display
        pg.display.flip()

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    pg.quit()
                if event.type == pg.KEYDOWN:
                    waiting = False


    def show_start_screen(self):
        # game splash/start screen
        pg.mixer.music.load(title_music)
        pg.mixer.music.play(loops=-1)
        pg.mixer.music.set_volume(0.1)
        self.screen.fill(BG_COLOR)
        self.draw_text(TITLE, 65, WHITE, WIDTH/2, HEIGHT/4+100)
        self.draw_text("Use WASD to move, Space to jump",22, WHITE, WIDTH/2,HEIGHT*3/4-50)
        self.draw_text("Press a key to play", 22, WHITE, WIDTH/2, HEIGHT*3/4)
        self.draw_text("High Score = "+str(self.highscore), 30, WHITE, WIDTH/2, HEIGHT*1/6)
        pg.display.flip()
        self.wait_for_key()
        pg.mixer.music.fadeout(500)

    def show_go_screen(self):
        # game over/continue
        pg.mixer.music.load(title_music)
        pg.mixer.music.play(loops=-1)
        pg.mixer.music.set_volume(0.1)
        self.screen.fill(BG_COLOR)
        self.draw_text("GAME OVER", 45, RED, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Score: "+ str(self.score), 22, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Press a key to play again", 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        if self.score > self.highscore:
            self.highscore = self.score
            self.draw_text("NEW HIGH SCORE", 22, WHITE, WIDTH/2, HEIGHT/2 +40)
            with open(HS_FILE,'w') as f:
                f.write(str(self.score))
        else:
            self.draw_text("High Score = " + str(self.highscore), 30, WHITE, WIDTH/2, HEIGHT/2 +40)
        pg.display.flip()
        self.wait_for_key()

    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name,size)
        text_surface = font.render(text,True,color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        self.screen.blit(text_surface, text_rect)


