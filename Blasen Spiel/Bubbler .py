import pygame                                                               #Imported pygame
import os   
import time      
import sys                                                           
from pygame.constants import(K_ESCAPE, MOUSEBUTTONDOWN, QUIT, K_p )
from random import randint 


class Settings:
    w_width = 1024
    w_height = 768
    w_border = 20
    pygame.display.set_caption("Bubbler")
    file_path = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(file_path, "Pictures")
    sound_path = os.path.join(file_path, "Sound" )

class Background(object):
    def __init__(self, filename):
        self.backgrounda = pygame.image.load(os.path.join(Settings.image_path, filename))
        self.image = pygame.image.load(os.path.join(Settings.image_path, "hintergrund.png")).convert() #Legt das Bild fest
        self.rect = self.image.get_rect()  

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Blase(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.durchmesser = 40
        self.image_orig = pygame.image.load(os.path.join(Settings.image_path,"Blase.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image_orig, (self.durchmesser, self.durchmesser))
        self.rect = self.image.get_rect()
        self.rect.left = randint(Settings.w_border, Settings.w_width - Settings.w_border)
        self.rect.top = randint(Settings.w_border, Settings.w_height - (Settings.w_border * 2))
        self.cd = pygame.time.get_ticks()
        self.cds = 500
        self.ran = pygame.time.get_ticks()

    def update(self):
        self.scale_up()

    def cooldown_scale(self):
        return pygame.time.get_ticks() >= self.cd

    def scale_up(self):
        if self.cooldown_scale():
            self.durchmesser += randint(1, 4)
            c = self.rect.center
            self.image = pygame.transform.scale(self.image_orig, (self.durchmesser, self.durchmesser))
            self.rect = self.image.get_rect()
            self.rect.center = c
            self.cd = pygame.time.get_ticks() + self.cds
            if self.durchmesser > 100:
                pygame.quit()




    def events(self):
        pass
 
    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Score(object):
    def __init__(self):
        self.black = 0,0,0
        self.count = 0
        self.font = pygame.font.SysFont("comicsans",35, True , True)
        self.text = self.font.render("Score : "+str(self.count),1,self.black)

    def show_score(self, screen):
        screen.blit(self.text,(540 ,10))


    def score_up(self):
        self.count += 1
        self.text = self.font.render("Score : "+str(self.count),1,self.black)

class Cursor(object):
    def __init__(self):
        self.cursorx = pygame.image.load(os.path.join(Settings.image_path, "cursor.png")).convert_alpha()
        self.cursor  = pygame.transform.scale(self.cursorx, (50, 50))
        self.rect = self.cursor.get_rect()

    def drawmouse(self, screen):
        pygame.mouse.set_visible(False)
        screen.blit(self.cursor,(pygame.mouse.get_pos()))


class Game(object):
    def __init__(self):
        self.screen = pygame.display.set_mode((Settings.w_width, Settings.w_height))
        self.clock = pygame.time.Clock()
        self.runn = False
        self.score = Score()
        self.background = Background("hintergrund.png")
        self.all_blasen = pygame.sprite.Group()
        self.sound1 = pygame.mixer.Sound(os.path.join(Settings.sound_path, "Click.wav"))
        self.sound2 = pygame.mixer.Sound(os.path.join(Settings.sound_path, "pop.wav"))
        self.music = pygame.mixer.music.load(os.path.join(Settings.sound_path, "music.mp3"))
        self.blase_cd = pygame.time.get_ticks()
        self.blase_cds = 1000
        self.cursor = Cursor()
        self.k = 1
        self.ram = pygame.time.get_ticks()

    def run(self):
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(-1)
        self.runn = True
        self.pause = False
        
        while self.runn:
            self.clock.tick(60)
            self.watch_for_events()

            if not self.pause:
                self.events()
                self.all_blasen.update()
                self.draw()
                pygame.mixer.music.unpause()
                pygame.mouse.set_visible(False)
            
            if self.pause:
                pygame.mixer.music.pause()
                pygame.mouse.set_visible(True)

    def blase_cooldown(self):
        return pygame.time.get_ticks() >= self.blase_cd

    def events(self):
        for i in range(1):
            if self.blase_cooldown():
                if self.blase_cd > 1000:
                    self.blase_cd -=5
                if len(self.all_blasen)< 5:
                    self.all_blasen.add(Blase())
                    self.blase_cd = pygame.time.get_ticks() + self.blase_cds
                    self.k += 1
    
    
    def draw(self):
        self.background.draw(self.screen)
        self.all_blasen.draw(self.screen)
        self.score.show_score(self.screen)
        self.cursor.drawmouse(self.screen)
    
        pygame.display.flip()

    def watch_for_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.runn = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.pause = not self.pause 

            if event.type == MOUSEBUTTONDOWN:
                self.sound1.play()
                for all_blasen in self.all_blasen:
                    if all_blasen.rect.collidepoint(event.pos):
                        self.sound2.play()
                        all_blasen.kill()        
                        self.score.score_up()

if __name__ == '__main__':
    os.environ['SDL_VIDEO_WINDOWS_POS'] = "50, 1100"
    pygame.init()
    game = Game()
    game.run()
    pygame.quit()