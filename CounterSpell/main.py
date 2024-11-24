import pygame
from pygame.locals import *
import pickle
from os import path

pygame.init()

pygame.init()
pygame.mixer.init()
pygame.mixer.music.load('sfx/main.wav')
pygame.mixer.music.play(-1)
                        
win = 0
timer_font = pygame.font.Font(None, 38)
timer_sec = 10
timer_text = timer_font.render("10", True, (0, 0, 0))
timer = pygame.USEREVENT + 1                                                
pygame.time.set_timer(timer, 1000)

screen_width = 800
screen_height = 800

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Platformer')

tile_size = 40
game_over = 0
collect = False
level = 3
max_levels = 3


# load images
sun_img = pygame.image.load('img/sun_img.png')
bg_img = pygame.image.load('img/bgpic.png')
dark = pygame.image.load('img/dark.png')


def draw_grid():
    for line in range(0, 21):
        # pygame.draw.line(screen, (255, 255, 255), (0, line * tile_size), (screen_width, line * tile_size))
        # pygame.draw.line(screen, (255, 255, 255), (line * tile_size, 0), (line * tile_size, screen_height))
        break

class Player():
    def __init__(self, x, y):
        img = pygame.image.load('img/happy.png')
        self.image = pygame.transform.scale(img, (tile_size, tile_size * 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.jumped = False
    def update(self, game_over):
        if timer_sec == 0:
            self.image = pygame.transform.scale(pygame.image.load('img/angry.png'), (tile_size, tile_size * 2))
        else:
            self.image = pygame.transform.scale(pygame.image.load('img/happy.png'), (tile_size, tile_size * 2))
        dx = 0
        dy = 0

        if game_over == 0:

            #get key presses
            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE] and self.jumped == False:
                self.jumped = True
                self.vel_y = -15
            if key[pygame.K_d]:
                dx += 3
            if key[pygame.K_a]:
                dx -= 3

            #add gravity
            self.vel_y += 1
            if self.vel_y > 10:
                self.vel_y = 10
            dy += self.vel_y
            
            #check for collision
            for tile in world.tile_list:
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0

                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height): 
                    if self.vel_y < 0:
                        dy = tile[1].bottom - self.rect.top
                        self.vel_y = 0
                    elif self.vel_y >= 0:
                        dy = tile[1].top - self.rect.bottom
                        self.vel_y = 0
                        self.jumped = False

            if pygame.sprite.spritecollide(self, spike_group, False):
                game_over = -1
            if pygame.sprite.spritecollide(self, exit_group, False):
                game_over = -1
                win = 1

            #update player position
            self.rect.x += dx
            self.rect.y += dy


        #draw player on screen
        screen.blit(self.image, self.rect)
        pygame.draw.rect(screen, (34, 52, 139), self.rect, 2)

        if timer_sec == 0:
            screen.blit(dark, (self.rect.x - 750, self.rect.y - 750))

        return game_over

class World():
    def __init__(self, data):
        self.tile_list = []

        #load images
        dirt_img = pygame.image.load('img/dirt_img.png')
        grass_img = pygame.image.load('img/grass_img.png')
        spike_img = pygame.image.load('img/spike_img.png')

        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(dirt_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 2:
                    img = pygame.transform.scale(grass_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 3:
                    img = pygame.transform.scale(spike_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 6:
                    spike = Spike(col_count * tile_size, row_count * tile_size + (tile_size // 2))
                    spike_group.add(spike)
                if tile == 7:
                    coin = Coin(col_count * tile_size + (tile_size // 2), row_count * tile_size + (tile_size // 2))
                    coin_group.add(coin)
                if tile == 8:
                    exit = Exit(col_count * tile_size + tile_size, row_count * tile_size)
                    exit_group.add(exit)
                
                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])
            pygame.draw.rect(screen, (34, 52, 139), tile[1], 1)

class Spike(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		img = pygame.image.load('img/spikes-1.png')
		self.image = pygame.transform.scale(img, (tile_size, tile_size // 2))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

class Exit(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		img = pygame.image.load('img/portal.png')
		self.image = pygame.transform.scale(img, (tile_size, tile_size))
		self.rect = self.image.get_rect()
		self.rect.x = x - 40
		self.rect.y = y

class Coin(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		img = pygame.image.load('img/sanity-1.png')
		self.image = pygame.transform.scale(img, (tile_size // 2, tile_size // 2))
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)

if path.exists(f'level{level}_data'):   
    pickle_in = open(f'level{level}_data', 'rb')
    world_data = pickle.load(pickle_in)
else:
    pickle_in = open('endscreen', 'rb')
    world_data = pickle.load(pickle_in)

player = Player(100, screen_height - 120)
spike_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()
world = World(world_data)

run = True

while run: 


    if win == 1:
        win = pygame.image.load('img/win.png')
        screen.blit(win, (screen_width // 2, screen_height // 2))
        pygame.mixer.music.stop()
        pygame.mixer.music.load('sfx/finaltrack.wav')
        pygame.mixer.music.play(-1)

    screen.blit(bg_img, (0, 0))

    world.draw()

    if game_over == 0:
            
        if pygame.sprite.spritecollide(player, coin_group, True):
            timer_sec = 10
            timer_text = timer_font.render(str(timer_sec), True, (0, 0, 0))
            collect = True         

    spike_group.draw(screen)
    coin_group.draw(screen)
    exit_group.draw(screen)

    game_over = player.update(game_over)

    draw_grid()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == timer:    # checks for timer event
            if game_over == 0:
                if timer_sec > 0:
                    timer_sec -= 1
                    timer_text = timer_font.render(str(timer_sec), True, (0, 0, 0))
                else:
                    if collect:
                        pygame.time.set_timer(timer, 10)
                        collect = False
                    else:
                        pass
    screen.blit(timer_text, (screen_width // 2, screen_height * .1 ))
    pygame.display.update()

pygame.quit()