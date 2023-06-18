# Подключить нужные модули
from random import randint 
from pygame import *
import os

init() 


# Глобальные переменные (настройки)
win_width = 1280 
win_height = 720
#pygame.mixer.init()
#pygame.mixer.music.load('1.mp3')
#pygame.mixer.music.play()

# класс-родитель для других спрайтов
class GameSprite(sprite.Sprite):
  # конструктор класса
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        # Вызываем конструктор класса (Sprite):
        sprite.Sprite.__init__(self)

        # каждый спрайт должен хранить свойство image - изображение
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.width = size_x
        self.height = size_y

        # каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
 
  # метод, отрисовывающий героя на окне
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
f=0
#класс-наследник для спрайта-игрока (управляется стрелками)
class Player(GameSprite):
    def update_l_r(self):
        global f
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
            f=1
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
            f=0
    def update_a_d(self):
        keys = key.get_pressed()
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_height - 80:
            self.rect.y += self.speed

#класс-наследник для спрайта-врага (перемещается сам)
class Enemy(GameSprite): 
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed, side='left'):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y, player_speed)        
        self.side = side
    
    def update(self):
        global side
        if self.side == 'right':
            self.rect.x -= self.speed
        if self.side == 'left':
            self.rect.x += self.speed

window = display.set_mode((win_width, win_height))
display.set_caption("Arcada")

m=os.path.join(os.path.abspath(__file__ + "/.."),"images/fon.jpg") # абсолютый путь
background = transform.scale(image.load(m), (win_width, win_height))

# во время игры пишем надписи размера 40
font2 = font.Font(None, 40)
font1 = font.Font(None, 80)
win = font1.render('YOU WIN!', True, (255, 255, 255))
lose = font1.render('YOU LOSE!', True, (180, 0, 0))

items = sprite.Group()
#Персонажи игры:
level=['                              ',
'                             d         ',
'   t                                   ',
'r           l     r       o  d    l ',
' -----/ -            / ------/         ' ,
'                                       l  ',
'   r          l                         ',
'              r      l                    ',
'   r          o   c  o       /         ',
'      /     /-------/                 ',
'               l                        ',
'                                       ', 
'    r          l      r       /         l  ',
'r    s               r                l ',
'               l        k       c       ',
'--------------      ------------------  ',
]
platforms = []
stairs=[]
coins=[]
monsters=[]
blocks_r=[]
blocks_l=[]
manas = sprite.Group() # группа що клонує атакуючі шари


k_door = False # чи підібрано ключ для дверей

o_chest = False # чи відкрита скриня

c_count = 0 # лічильник монет
x=0
y=0
for r in level:
        for c in r:
            if c == 'r':
                n = GameSprite('images/nothing.png',x, y, 40, 80 ,0)# нічого
                blocks_r.append(n)
                items.add(n)
            if c == 'l':
                n = GameSprite('images/nothing.png',x, y, 40, 80 ,0) 
                blocks_l.append(n)
                items.add(n)
            if c == '-':
                platform = GameSprite('images/Rectangle 2.png',x, y, 40, 40 ,0)# платформа
                platforms.append(platform)
                items.add(platform)
            if c=='s':
                hero = Player('images/hero.png', x, y,80,80, 4) # головний персонаж
                items.add(hero)
            if c=='c':
                monster = Enemy('images/monster.png', x, y,40,40, 2,'left')# ворог
                monsters.append(monster)
                items.add(monster)
            if c=='k':
                key_k = Player('images/key.png', x, y,70,30, 0) # предмет без якого не буде виграшу
                items.add(key_k)
            if c=='d':
                door = Player('images/box2.png', x, y,60,60, 0) # фінальний спрайт
                items.add(door)
            if c=='o':
                coin = Player('images/coin.png', x, y,50,50, 0) # предмети що збираємо
                coins.append(coin)
                items.add(coin)
            if c=='/':
                stair = Player('images/ladder.png', x, y,100,220, 0) # драбинка
                stairs.append(stair)
                items.add(stair)
            if c=='t':
                t = Player('images/box.png', x, y,80,80, 0) # предмет, що додає більше балів
                items.add(t)
            x +=40
        y+=40
        x = 0
mana=GameSprite("images/nothing.png",hero.rect.x+20,hero.rect.y+10,50,50,0)# предмет, що вбиває

game = True
finish = False
clock = time.Clock()
FPS = 60




#музыка
mixer.init()
#mixer.music.load('1.mp3')
#mixer.music.play()
game_over=''
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
    if finish != True:
        window.blit(background,(0, 0))
        items.draw(window)
        
        if f==1:
            hero.image=transform.scale(image.load("images/hero2.png"), (hero.width, hero.height))
        else:
            hero.image=transform.scale(image.load("images/hero.png"), (hero.width, hero.height))
        for monster in monsters:
            monster.update()

# перевірка зіткнень

# торкання країв платформи зліва
        for r in blocks_r: 
            if sprite.collide_rect(hero, r):
                hero.rect.x = r.rect.x + hero.width # для героя
            for monster in monsters:
                if sprite.collide_rect(monster, r): # для ворогів
                    monster.side = 'left'
# торкання країв платформи справа
        for l in blocks_l: 
            if sprite.collide_rect(hero, l):
                hero.rect.x = l.rect.x - hero.width
            for monster in monsters:
                if sprite.collide_rect(monster, l):
                    monster.side = 'right'
        hero.update_l_r() # рух вліво і вправо
        # піднімаємось по драбинам
        for s in stairs:                 
            if sprite.collide_rect(hero, s):
                hero.update_a_d()
            
                if hero.rect.y <= (s.rect.y - 100): # умова, щоб гравець не піднімався вище платформи
                    hero.rect.y = s.rect.y - 100
            
                if hero.rect.y >= (s.rect.y + 190): # умова, щоб гравець не спускався нижче платформи
                    hero.rect.y = s.rect.y +190  


        for c in coins:  # збирає монети
            if sprite.collide_rect(hero, c):
                c_count += 1
                coins.remove(c)
                items.remove(c)
        if sprite.collide_rect(hero,t) and c_count==2: # якщо зібрав 2 монети можеш видкрити скриню клавішою е
            keys = key.get_pressed()
            if keys[K_e]:
                c_count += 10
                items.remove(t)
        if sprite.collide_rect(hero,key_k):# взяти ключ
            keys = key.get_pressed()
            if keys[K_e]:
                k_door=True
                items.remove(key_k)
                
        if sprite.collide_rect(hero,door) and k_door:# торкання дверей, кінець гри(слідуючий рівень)
            game_over='win'
            finish=False
    # знищуємо ворогів
        for monster in monsters:
            keys = key.get_pressed()       
            if keys[K_SPACE]:   
                if  sprite.collide_rect(monster, hero):
                    monster.rect.y = -150 # якщо не перемістити ворога за межі екрану, його привид може вбити грваця
                    
            if sprite.collide_rect(hero, monster):
                game_over='lose'
                finish=False
                
        coin_c = font2.render('coins: ' + str(c_count), True,(246,249,128))
        window.blit(coin_c, (40, 0))

    if game_over=='win':
        window.fill((0,0,0))
        window.blit(win,(400,300))
    elif game_over=='lose':
        window.fill((0,0,0))
        window.blit(lose,(400,300))
    display.update()
    clock.tick(FPS)
