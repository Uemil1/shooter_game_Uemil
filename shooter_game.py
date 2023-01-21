from pygame import *
from random import randint
font.init()
font1 = font.Font(None, 80)
win = font1.render('YOU WIN!', True, (255, 255, 255))
lose = font1.render('YOU LOSE', True, (180, 0, 0))
font2 = font.Font(None, 36)

lost = 0
max_lost = 10
score = 0
max_score = 15

img_bullet = 'Objects/bullet.png'
img_back = 'Fons/Fon1.png'
img_hero = 'Personages/Player3.png'
img_enemy = 'Personages/Voin1.png'

finish = False
game = True
clock = time.Clock()

win_width = 800
win_height = 600



class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        key_pressed = key.get_pressed()
        if key_pressed[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if key_pressed[K_DOWN] and self.rect.y < win_height - 80:
            self.rect.y += self.speed
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.right, self.rect.centery+5, 20, 15, 15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.x -= self.speed
        global lost
        if self.rect.x <= 0:
            self.rect.y = randint(80, win_height - 80)
            self.rect.x = win_width
            lost = lost + 1
class Bullet(GameSprite):
    def update(self):
        self.rect.x += self.speed
        if self.rect.x > win_width:
            self.kill()

window = display.set_mode((win_width, win_height))
display.set_caption('shooter_game')
hero = Player(img_hero, 5, win_height - 100, 80, 100, 5)
background = transform.scale(image.load(img_back), (win_width, win_height))

bullets = sprite.Group()
enemyes = sprite.Group()
for i in range (1, 6):
    enemy = Enemy(img_enemy, win_width, randint(80, win_width - 80), 80, 50, randint(3, 4))
    enemyes.add(enemy)


while game:
    for e in event.get():
            if e.type == QUIT:
                game = False
            elif e.type == KEYDOWN:
                if e.key == K_SPACE:
                    hero.fire()
                    
    if finish != True:
        window.blit(background, (0, 0))
        hero.reset()
        hero.update()
        enemyes.draw(window)
        enemyes.update()
        
        bullets.draw(window)
        bullets.update()

        collides = sprite.groupcollide(enemyes, bullets, True, True)
        for c in collides:
            score = score + 1
            enemy = Enemy(img_enemy, win_width, randint(80, win_width - 80), 80, 50, randint(3, 4))
            enemyes.add(enemy)
        if sprite.spritecollide(hero, enemyes, False) or lost >= max_lost:
            finish = True
            window.blit(lose, (200,200))
        if lost >= max_lost:
            finish = True
            window.blit(lose, (200,200))
        if score >= max_score:
            finish = True
            window.blit(win, (200,200))
        text = font2.render('Счет: ' + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))
        text_lose  = font2.render('Пропущено: ' + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 60))


        display.update()
        clock.tick(40)
    time.delay(30)