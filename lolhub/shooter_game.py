#Создай собственный Шутер!

from typing import Any
from pygame import *
from random import randint
window = display.set_mode((700, 500))
display.set_caption('догонялки')
font.init()
background =transform.scale(image.load('galaxy.jpg'),(700, 500))
clock = time.Clock()
FPS = 60
score = 0
lose = 0
def reset(self):
    window.blit(self.image, (self.rect.x, self.y))

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, 
                 player_y, player_speed, 
                 player_width, player_height):
        super().__init__()
        self.image = transform.scale(image.load(player_image),
                                      (player_width, player_height))
        self.speed = player_speed
        self.rect  = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_s] and self.rect.y < 400:
            self.rect.y += self.speed

        if keys_pressed[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed

        if keys_pressed[K_d] and self.rect.x < 560:
            self.rect.x += self.speed

        if keys_pressed[K_w] and self.rect.y > 0:
            self.rect.y -= self.speed

    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, 
                        self.rect.top, 5, 10, 20) 
        bullets.add(bullet)

class Enemy(GameSprite):
    move = 'left'
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y > 700:
            self.rect.y = 0
            self.rect.x = randint(0, 640)
            lost = lost + 1
   
aliens = sprite.Group()
for i in range(5):
    y = 0
    x = randint(0, 700)
    speed = randint(1, 5)
    enemy = Enemy('asteroid.png', x, y, speed, 60, 65)
    aliens.add(enemy)

class Bullet(GameSprite):
    move = 'up' 
    def update(self):
        self.rect.y -= self.speed 
        if self.rect.y > 700:
            self.kill()

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
kick = mixer.Sound('fire.ogg')
kick.play

bullets = sprite.Group()
player = Player('rocket.png', 100, 100, 5, 100, 100)
x = randint(0, 700)
enemy = Enemy('asteroid.png', x, 0, 10, 50, 50)

dad = 0
lost = 0

font.init()
font1 = font.SysFont('Arial', 36)
font2 = font.SysFont('Arial', 70)
win = font2.render('YOU WIN', True, (0, 128, 0))
win = True

loss = font2.render('YOU LOSE!', True, (255, 0, 0))
player = Player('rocket.png', 310, 410, 10, 75, 75)
x = randint(0, 700)
enemy = Enemy('asteroid.png', x, 0, 10, 75, 75)
bullet = Bullet('bullet.png', 310, 410, 10, 75, 75)

game = True
finished = False

while game:

    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                player.fire()

    if not finished:
        sprite_list = sprite.groupcollide(aliens, bullets, True, True)

        for alien in sprite_list:
                dad += 1 
                x = randint(0, 800)
                y = randint(0, 100)
                enemy = Enemy('asteroid.png', x, y, speed, 60, 65)
                aliens.add(enemy)

        window.blit(background,(0, 0))

        bullets.update()
        bullets.draw(window)
        player.reset()
        player.update()
        aliens.draw(window)
        aliens.update()


        if score >= 10:
            win = font1.render('You win!', True, (255, 215, 0))
            window.blit(win, (350, 350))
            finish = True

        if lost >= 5:
            lose = font1.render('You lose!', True, (255, 215, 0))
            window.blit(lose, (350, 350))
            finish = True

        text_lose = font1.render('Пропущено:' + str(lost), 1, (255, 255, 255))
        text_dad = font1.render('Убито:' + str(dad), 1, (255, 255, 255))
        window.blit(text_lose, (25, 25))
        window.blit(text_dad, (25, 50))

    clock.tick(FPS)
    display.update()