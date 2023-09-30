from pygame import *

color = (200,255,255)
win_width = 600
win_height = 500
window = display.set_mode((win_width,win_height))
window.fill(color)

clock = time.Clock()
FPS = 60
game = True

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

    display.update()
    clock.tick(FPS)


from pygame import *
from random import randint
from time import time as timer 

lost = 0
score = 0
max_lost = 3
goal = 10 
lives = 3
num_fire = 0
rel_time=False


class GameSprite(sprite.Sprite):
    def __init__(self, img, speed, x, y, sizex, sizey):
        super().__init__()
        self.image = transform.scale(image.load(img), (sizex,  sizey))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))



class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_RIGHT]  and self.rect.x < 635:
           self.rect.x += 10
        if keys[K_LEFT] and self.rect.x > 0:
            self.rect.x  -= 10

    def fire(self):
        bullet = Bullet("bullet.png", -15, self.rect.centerx, self.rect.top, 15, 20)
        bullets.add(bullet)


class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y > 500 :
            self.rect.y = 0
            self.rect.x = randint(80,700)
            lost = lost + 1



class Bullet(GameSprite):
    def update(self):
        self.rect.y +=self.speed
        if self.rect.y < 0:
            self.kill()


        


window = display.set_mode((700, 500))
display.set_caption("Shooter game")

background = transform.scale(image.load("galaxy.jpg"), (700, 500))


mixer.init()
mixer.music.load("space.ogg")
mixer.music.play()

fire_sound  = mixer.Sound("fire.ogg")

font.init()
style = font.Font(None, 36)


player = Player("rocket.png", 10, 4, 420, 65, 65)
enemys = sprite.Group()
for e in range(1,6):
    enemy = Enemy("ufo.png", randint(1,3), randint(80,700), 0, 80, 50)
    enemys.add(enemy)


asteroids = sprite.Group()
for a in range(1,3):
    asteroid = Enemy("asteroid.png", randint(1,3), randint(80, 500), 0, 80, 50)
    asteroids.add(asteroid)



bullets = sprite.Group()



clock = time.Clock()
FPS = 60

font.init()
font = font.Font(None, 70)
win = font.render("YOU WON", True, (255, 215, 0))
lose1 = font.render("YOU LOST", True, (255, 215, 0))
game = True
finish = False
while game :
    for e in event.get():
        if e.type == QUIT:
            game = False

        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if  num_fire < 5 and rel_time == False:
                    fire_sound.play()
                    player.fire()
                    num_fire += 1
                if num_fire >= 5 and rel_time == False:
                    ti = timer()
                    rel_time = True




    if not finish:
        window.blit(background, (0,0))

        text_lose = style.render("Missed:" + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10,20))

        text_win = style.render("Score:" + str(score), 1, (255,255,255))
        window.blit(text_win, (10,40))

        text_lives = style.render("Lives:" + str(lives), 1, (255, 255, 255))
        window.blit(text_lives, (10,60))

        player.update()
        player.reset()

        enemys.update()
        enemys.draw(window)

        asteroids.update()
        asteroids.draw(window)

        

        bullets.update()
        bullets.draw(window)

        sprites_list = sprite.groupcollide(enemys, bullets, True, True)
        for s in sprites_list:
            score += 1
            enemy = Enemy("ufo.png", randint(1,10), randint(80,700), 0, 80, 50)
            enemys.add(enemy)

        if sprite.spritecollide(player, enemys, False) or sprite.spritecollide(player, asteroids, False):
            sprite.spritecollide(player, enemys, True)
            sprite.spritecollide(player, asteroids, True)
            lives -=1

        if rel_time == True:
            tt = timer()
            if tt - ti<= 3:
                text_re = style.render("Wait, reload", 1, (255, 0, 0))
                window.blit(text_re, (260, 460))
            else:
                num_fire = 0
                rel_time = False

        if lives == 0 or lost >= max_lost:
            finish = True
            window.blit(lose1, (200,200))

        if score >= 10:
            finish = True
            window.blit(win, (200,200))



    display.update()
    clock.tick(FPS)


