import pygame
import math
from parametros import *
from sys import exit
import random
import json
import os

pygame.init()

# Window setup
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Z-Killer')
clock = pygame.time.Clock()

# Load images
background = pygame.image.load(r'Py.Game---Jo-o-Nery-Lucas-Goes\assets\image\Background\background0.png').convert_alpha()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
game_over_image = pygame.image.load(r'Py.Game---Jo-o-Nery-Lucas-Goes\assets\image\Background\game_over.png').convert_alpha()
game_over_image = pygame.transform.scale(game_over_image, (WIDTH, HEIGHT))
start_screen_image = pygame.image.load(r'Py.Game---Jo-o-Nery-Lucas-Goes\assets\image\Background\inicio.png').convert_alpha()
start_screen_image = pygame.transform.scale(start_screen_image, (WIDTH, HEIGHT))
start_button_image = pygame.image.load(r'Py.Game---Jo-o-Nery-Lucas-Goes\assets\image\Background\Start.png').convert_alpha()
start_button_image = pygame.transform.scale(start_button_image, (200, 100))
character_select_button_image = pygame.image.load(r'Py.Game---Jo-o-Nery-Lucas-Goes\assets\image\Background\character_select.png').convert_alpha()
character_select_button_image = pygame.transform.rotozoom(character_select_button_image, 0, 1.2)
character_select_button_image = pygame.transform.scale(character_select_button_image, (200, 100))
ranking_button_image = pygame.image.load(r'Py.Game---Jo-o-Nery-Lucas-Goes\assets\image\Background\ranking.png').convert_alpha()
ranking_button_image = pygame.transform.scale(ranking_button_image, (200, 100))

pygame.mixer.music.load(r'Py.Game---Jo-o-Nery-Lucas-Goes\assets\sound\apocalypse.mp3')  
pygame.mixer.music.set_volume(0.8)
game_over_music = pygame.mixer.Sound(r'Py.Game---Jo-o-Nery-Lucas-Goes\assets\sound\go_effect.mp3') 
game_over_music.set_volume(0.5)
shoot_sound = pygame.mixer.Sound(r'Py.Game---Jo-o-Nery-Lucas-Goes\assets\sound\shot.mp3')
shoot_sound.set_volume(0.1)
music_loaded = True

BOSS_IMAGE_PATH = r'Py.Game---Jo-o-Nery-Lucas-Goes\assets\image\Personagens\Boss\alba_boss.png'
ULTRA_BOSS_IMAGE_PATH = r'Py.Game---Jo-o-Nery-Lucas-Goes\assets\image\Personagens\Boss\UltraBoss.png'

POWERUP_IMAGES = {
    'health': pygame.image.load(r'Py.Game---Jo-o-Nery-Lucas-Goes\assets\image\PowerUps\health.png').convert_alpha(),
    'immunity': pygame.image.load(r'Py.Game---Jo-o-Nery-Lucas-Goes\assets\image\PowerUps\immunity.png').convert_alpha(),
    'nuke': pygame.image.load(r'Py.Game---Jo-o-Nery-Lucas-Goes\assets\image\PowerUps\nuke.png').convert_alpha(),
    'speed': pygame.image.load(r'Py.Game---Jo-o-Nery-Lucas-Goes\assets\image\PowerUps\speed.png').convert_alpha(),
    'extra_life': pygame.image.load(r'Py.Game---Jo-o-Nery-Lucas-Goes\assets\image\PowerUps\extra_life.png').convert_alpha()
}

for key in POWERUP_IMAGES:
    POWERUP_IMAGES[key] = pygame.transform.scale(POWERUP_IMAGES[key], (80,80))

POWERUP_SPAWN_CHANCE = 0.25  
POWERUP_SPAWN_INTERVAL = 30000  # 30 segundos
POWERUP_IMMUNITY_DURATION = 10000  # 10 segundos 

character_configs = {
    'musculoso': {
        'image': pygame.image.load(r'Py.Game---Jo-o-Nery-Lucas-Goes\assets\image\Personagens\Masculino\musculoso.png').convert_alpha(),
        'speed': 6,
        'health': 150,
        'bullet_speed': 30,
        'bullet_cooldown': 20,
        'bullet_damage': 1,
        'bullet_scale': 1,
        'size': 0.07,
        'bullet_lifetime': 1000
    },
    'nerd': {
        'image': pygame.image.load(r'Py.Game---Jo-o-Nery-Lucas-Goes\assets\image\Personagens\Masculino\nerd.png').convert_alpha(),
        'speed': 6,
        'health': 100,
        'bullet_speed': 40,
        'bullet_cooldown': 10,
        'bullet_damage': 0.5,
        'bullet_scale': 1,
        'size': 0.15,
        'bullet_lifetime': 125
    },
    'flash': {
        'image': pygame.image.load(r'Py.Game---Jo-o-Nery-Lucas-Goes\assets\image\Personagens\Masculino\flash.png').convert_alpha(),
        'speed': 12,
        'health': 80,
        'bullet_speed': 14,
        'bullet_cooldown': 25,
        'bullet_damage': 1,
        'bullet_scale': 1,
        'size': 0.1,
        'bullet_lifetime': 800
    },
    'mendel': {
        'image': pygame.image.load(r'Py.Game---Jo-o-Nery-Lucas-Goes\assets\image\Personagens\Masculino\mendel_ofc.png').convert_alpha(),
        'speed': 10,
        'health': 50,
        'bullet_speed': 10,
        'bullet_cooldown': 5,
        'bullet_damage': 0.5,
        'bullet_scale': 0.8,
        'size': 0.06,
        'bullet_lifetime': 500
    }
}

# Game states
START_SCREEN = 0
GAME_ACTIVE = 1
GAME_OVER = 2
CHARACTER_SELECT = 3
GET_PLAYER_NAME = 4
SHOW_RANKING = 5
game_state = START_SCREEN

# Score
score = 0
player_name = ""
font = pygame.font.Font(None, 36)
title_font = pygame.font.Font(None, 72)
ranking_font = pygame.font.Font(None, 48)

selected_character = 'musculoso'  

last_powerup_spawn_time = 0

# Ranking system
RANKING_FILE = 'ranking.json'

def load_ranking():
    if not os.path.exists(RANKING_FILE):
        return []
    try:
        with open(RANKING_FILE, 'r') as f:
            return json.load(f)
    except:
        return []

def save_ranking(ranking):
    with open(RANKING_FILE, 'w') as f:
        json.dump(ranking, f)

def add_to_ranking(name, score):
    ranking = load_ranking()
    ranking.append({'name': name, 'score': score})
    ranking.sort(key=lambda x: x['score'], reverse=True)
    ranking = ranking[:10]
    save_ranking(ranking)
    return ranking

class Player(pygame.sprite.Sprite):
    def __init__(self, character_type='musculoso'):
        super().__init__()
        config = character_configs[character_type]
        self.pos = pygame.math.Vector2(player_start_x, player_start_y)
        self.character_type = character_type
        self.image = pygame.transform.rotozoom(config['image'], 95, config['size'])
        self.base_player_image = self.image
        self.hitbox_rect = self.base_player_image.get_rect(center=self.pos)
        self.rect = self.hitbox_rect.copy()
        self.mask = pygame.mask.from_surface(self.image)  # Collision mask
        self.speed = config['speed']
        self.original_speed = self.speed
        self.shoot = False
        self.shoot_cooldown = 0
        self.bullet_cooldown = config['bullet_cooldown']
        self.gun_barrel_offset = pygame.math.Vector2(GUN_BARREL_OFFSET_X, GUN_BARREL_OFFSET_Y)
        self.max_health = config['health']
        self.current_health = config['health']
        self.invincible_timer = 0
        self.alive = True
        self.angle = 0
        self.bullet_speed = config['bullet_speed']
        self.bullet_damage = config['bullet_damage']
        self.bullet_scale = config['bullet_scale']
        self.bullet_lifetime = config['bullet_lifetime']
        
        # Powerup status
        self.extra_lives = 0
        self.max_extra_lives = 2
        self.is_immune = False
        self.immune_timer = 0
        self.speed_boost_timer = 0
        self.speed_boost_active = False

        # Health bars
        self.health_bar_full = pygame.transform.rotozoom(pygame.image.load(r'Py.Game---Jo-o-Nery-Lucas-Goes\assets\image\Personagens\HUD\Health\full.png').convert_alpha(), 0, 0.5)
        self.health_bar_75 = pygame.transform.rotozoom(pygame.image.load(r'Py.Game---Jo-o-Nery-Lucas-Goes\assets\image\Personagens\HUD\Health\75.png').convert_alpha(), 0, 0.5)
        self.health_bar_50 = pygame.transform.rotozoom(pygame.image.load(r'Py.Game---Jo-o-Nery-Lucas-Goes\assets\image\Personagens\HUD\Health\50.png').convert_alpha(), 0, 0.5)
        self.health_bar_25 = pygame.transform.rotozoom(pygame.image.load(r'Py.Game---Jo-o-Nery-Lucas-Goes\assets\image\Personagens\HUD\Health\25.png').convert_alpha(), 0, 0.5)

    def draw_health_bar(self, window):
        if self.current_health > 75:
            window.blit(self.health_bar_full, (0, 0))
        elif self.current_health > 50:
            window.blit(self.health_bar_75, (0, 0))
        elif self.current_health > 25:
            window.blit(self.health_bar_50, (0, 0))
        else:
            window.blit(self.health_bar_25, (0, 0))

    def take_damage(self, damage_percent=0.2):
        if self.invincible_timer == 0 and self.alive and not self.is_immune:
            damage_amount = self.max_health * damage_percent
            self.current_health -= damage_amount
            self.invincible_timer = 60
            if self.current_health <= 0:
                if self.extra_lives > 0:
                    self.extra_lives -= 1
                    self.current_health = self.max_health
                else:
                    self.current_health = 0
                    self.alive = False
                    self.kill()

    def activate_powerup(self, powerup_type):
        if powerup_type == 'health':
            self.current_health = self.max_health
        elif powerup_type == 'immunity':
            self.is_immune = True
            self.immune_timer = pygame.time.get_ticks() + POWERUP_IMMUNITY_DURATION
        elif powerup_type == 'nuke':
            for enemy in enemy_group:
                enemy.kill()
        elif powerup_type == 'speed':
            self.speed = self.original_speed * 2  # 100% mais rápido
            self.speed_boost_active = True
            self.speed_boost_timer = pygame.time.get_ticks() + POWERUP_IMMUNITY_DURATION
        elif powerup_type == 'extra_life':
            if self.extra_lives < self.max_extra_lives:
                self.extra_lives += 1

    def player_rotation(self):
        if not self.alive:
            return
            
        self.mouse_coords = pygame.mouse.get_pos()
        self.mouse_player_x = (self.mouse_coords[0] - self.hitbox_rect.centerx)
        self.mouse_player_y = (self.mouse_coords[1] - self.hitbox_rect.centery)
        self.angle = math.degrees(math.atan2(self.mouse_player_y, self.mouse_player_x))
        self.image = pygame.transform.rotate(self.base_player_image, -self.angle)
        self.rect = self.image.get_rect(center=self.hitbox_rect.center)
        self.mask = pygame.mask.from_surface(self.image)

    def user_input(self):
        if not self.alive:
            return
            
        self.speed_x = 0
        self.speed_y = 0

        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.speed_y = -self.speed
        if keys[pygame.K_s]:
            self.speed_y = self.speed
        if keys[pygame.K_d]:
            self.speed_x = self.speed
        if keys[pygame.K_a]:
            self.speed_x = -self.speed

        if self.speed_x != 0 and self.speed_y != 0:
            self.speed_x /= math.sqrt(2)
            self.speed_y /= math.sqrt(2)

        if pygame.mouse.get_pressed()[0] or keys[pygame.K_SPACE]:
            self.is_shooting()
            self.shoot = True
        else:
            self.shoot = False

    def is_shooting(self):
        if self.shoot_cooldown == 0 and self.alive:
            self.shoot_cooldown = self.bullet_cooldown
            spawn_bullet_pos = self.pos + self.gun_barrel_offset.rotate(-self.angle)
            bullet = Bullet(spawn_bullet_pos[0], spawn_bullet_pos[1], self.angle, 
                          self.bullet_speed, self.bullet_damage, 
                          self.bullet_scale, self.bullet_lifetime)
            bullet_group.add(bullet)
            all_sprites.add(bullet)
            shoot_sound.play()  

    def move(self):
        if not self.alive:
            return
            
        self.pos += pygame.math.Vector2(self.speed_x, self.speed_y)
        self.pos.x = max(self.hitbox_rect.width // 2, min(self.pos.x, WIDTH - self.hitbox_rect.width // 2))
        self.pos.y = max(self.hitbox_rect.height // 2, min(self.pos.y, HEIGHT - self.hitbox_rect.height // 2))
        self.hitbox_rect.center = self.pos
        self.rect.center = self.hitbox_rect.center

    def update(self):
        if not self.alive:
            return
            
        current_time = pygame.time.get_ticks()
        if self.is_immune and current_time > self.immune_timer:
            self.is_immune = False
        
        if self.speed_boost_active and current_time > self.speed_boost_timer:
            self.speed = self.original_speed
            self.speed_boost_active = False
            
        self.user_input()
        self.move()
        self.player_rotation()

        if self.invincible_timer > 0:
            self.invincible_timer -= 1

        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, angle, speed, damage, scale, lifetime):
        super().__init__()
        self.image = pygame.image.load(r'Py.Game---Jo-o-Nery-Lucas-Goes\assets\image\Weapons\small_dot.png').convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 180, scale)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.mask = pygame.mask.from_surface(self.image)
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = speed
        self.damage = damage
        self.x_speed = math.cos(self.angle * (2 * math.pi / 360)) * self.speed
        self.y_speed = math.sin(self.angle * (2 * math.pi / 360)) * self.speed
        self.bullet_lifetime = lifetime
        self.spawn_time = pygame.time.get_ticks()

    def bullet_movement(self):
        self.x += self.x_speed
        self.y += self.y_speed
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

        for enemy in enemy_group:
            offset_x = enemy.rect.x - self.rect.x
            offset_y = enemy.rect.y - self.rect.y
            if self.mask.overlap(enemy.mask, (offset_x, offset_y)):
                enemy.take_damage(self.damage)
                self.kill()

        if pygame.time.get_ticks() - self.spawn_time > self.bullet_lifetime:
            self.kill()

    def update(self):
        self.bullet_movement()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__(enemy_group, all_sprites)
        self.image = pygame.image.load(r'Py.Game---Jo-o-Nery-Lucas-Goes\assets\image\Enemies\Zombie\0.png').convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 0, 0.4)
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.mask = pygame.mask.from_surface(self.image) 
        self.direction = pygame.math.Vector2()
        self.speed = ENEMY_SPEED
        self.position = pygame.math.Vector2(position)
        self.health = 1
        self.damage_cooldown = 60

    def take_damage(self, damage=1):
        global score
        self.health -= damage
        if self.health <= 0:
            score += ENEMY_POINTS
            self.kill()

    def deal_damage_to_player(self):
        if player.alive and self.damage_cooldown <= 0:
            offset_x = player.rect.x - self.rect.x
            offset_y = player.rect.y - self.rect.y
            if self.mask.overlap(player.mask, (offset_x, offset_y)):
                player.take_damage()
                self.damage_cooldown = 60

    def chase_player(self):
        if not player.alive:
            return
            
        player_vector = pygame.math.Vector2(player.hitbox_rect.center)
        enemy_vector = pygame.math.Vector2(self.rect.center)
        if (player_vector - enemy_vector).length() > 0:
            self.direction = (player_vector - enemy_vector).normalize()
            self.position += self.direction * self.speed
            self.rect.center = self.position

    def update(self):
        self.chase_player()
        self.deal_damage_to_player()
        if self.damage_cooldown > 0:
            self.damage_cooldown -= 1

class BossEnemy(pygame.sprite.Sprite):
    def __init__(self, position, wave):
        super().__init__(enemy_group, all_sprites)
        self.image = pygame.image.load(BOSS_IMAGE_PATH).convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 0, 0.7)

        self.rect = self.image.get_rect()
        self.rect.center = position
        self.mask = pygame.mask.from_surface(self.image)  
        self.direction = pygame.math.Vector2()
        self.speed = ENEMY_SPEED * 1.4  
        self.position = pygame.math.Vector2(position)
        self.health = 50 + (wave // 5 - 1) * 10 
        self.damage_cooldown = 60
        self.wave = wave

    def take_damage(self, damage=1):
        global score
        self.health -= damage
        if self.health <= 0:
            score += BOSS_POINTS * (self.wave // 5) 
            self.kill()

    def deal_damage_to_player(self):
        if player.alive and self.damage_cooldown <= 0:
            offset_x = player.rect.x - self.rect.x
            offset_y = player.rect.y - self.rect.y
            if self.mask.overlap(player.mask, (offset_x, offset_y)):
                player.take_damage(1)  
                self.damage_cooldown = 60

    def chase_player(self):
        if not player.alive:
            return
            
        player_vector = pygame.math.Vector2(player.hitbox_rect.center)
        enemy_vector = pygame.math.Vector2(self.rect.center)
        if (player_vector - enemy_vector).length() > 0:
            self.direction = (player_vector - enemy_vector).normalize()
            self.position += self.direction * self.speed
            self.rect.center = self.position

    def update(self):
        self.chase_player()
        self.deal_damage_to_player()
        if self.damage_cooldown > 0:
            self.damage_cooldown -= 1

class UltraBoss(pygame.sprite.Sprite):
    def __init__(self, position, wave):
        super().__init__(enemy_group, all_sprites)
        self.image = pygame.image.load(ULTRA_BOSS_IMAGE_PATH).convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 0, 1.0)  
        
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.mask = pygame.mask.from_surface(self.image)
        self.direction = pygame.math.Vector2()
        self.speed = ENEMY_SPEED * 1.2  
        self.position = pygame.math.Vector2(position)
        self.health = 75 + (wave // 10 - 1) * 25  
        self.damage_cooldown = 30  
        self.wave = wave
        self.damage_per_hit = 1

    def take_damage(self, damage=1):
        global score
        self.health -= damage
        if self.health <= 0:
            score += BOSS_POINTS * (self.wave // 5) * 3 
            self.kill()

    def deal_damage_to_player(self):
        if player.alive and self.damage_cooldown <= 0:
            offset_x = player.rect.x - self.rect.x
            offset_y = player.rect.y - self.rect.y
            if self.mask.overlap(player.mask, (offset_x, offset_y)):
                player.take_damage(1)
                self.damage_cooldown = 30

    def chase_player(self):
        if not player.alive:
            return
            
        player_vector = pygame.math.Vector2(player.hitbox_rect.center)
        enemy_vector = pygame.math.Vector2(self.rect.center)
        if (player_vector - enemy_vector).length() > 0:
            self.direction = (player_vector - enemy_vector).normalize()
            self.position += self.direction * self.speed
            self.rect.center = self.position

    def update(self):
        self.chase_player()
        self.deal_damage_to_player()
        if self.damage_cooldown > 0:
            self.damage_cooldown -= 1

class Powerup(pygame.sprite.Sprite):
    def __init__(self, powerup_type):
        super().__init__()
        self.powerup_type = powerup_type
        self.image = POWERUP_IMAGES[powerup_type]
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(50, WIDTH - 50)
        self.rect.y = -50
        self.speed = 3
        
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > HEIGHT:
            self.kill()
        
        if player.alive and self.rect.colliderect(player.hitbox_rect):
            player.activate_powerup(self.powerup_type)
            self.kill()

def spawn_wave(wave):
    if wave % 10 == 0:  # UltraBoss wave (a cada 10 waves)
        ultra_boss = UltraBoss((random.randint(-200, WIDTH + 200), random.randint(-200, -50)), wave)
        all_sprites.add(ultra_boss)
        enemy_group.add(ultra_boss)
    elif wave % 5 == 0:  # Boss wave (a cada 5 waves)
        boss = BossEnemy((random.randint(-200, WIDTH + 200), random.randint(-200, -50)), wave)
        all_sprites.add(boss)
        enemy_group.add(boss)
    else:
        num_zombies = wave * 3
        for _ in range(num_zombies):
            side = random.choice(["left", "right", "top", "bottom"])
            
            if side == "left":
                x = random.randint(-200, -50)
                y = random.randint(-200, HEIGHT + 200)
            elif side == "right":
                x = random.randint(WIDTH + 50, WIDTH + 200)
                y = random.randint(-200, HEIGHT + 200)
            elif side == "top":
                x = random.randint(-200, WIDTH + 200)
                y = random.randint(-200, -50)
            elif side == "bottom":
                x = random.randint(-200, WIDTH + 200)
                y = random.randint(HEIGHT + 50, HEIGHT + 200)

            zombie = Enemy((x, y))
            all_sprites.add(zombie)
            enemy_group.add(zombie)

def draw_score(window, score):
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    window.blit(score_text, (WIDTH - 200, 10))

def draw_wave(window, wave):
    wave_text = font.render(f"Wave: {wave}", True, (255, 255, 255))
    window.blit(wave_text, (WIDTH - 200, 50))

def draw_extra_lives(window, player):
    life_icon = pygame.transform.scale(POWERUP_IMAGES['extra_life'], (80, 80))
    for i in range(player.extra_lives):
        window.blit(life_icon, (10 + i * 35, HEIGHT - 90))

def show_character_select():
    global selected_character, game_state
    
    window.blit(start_screen_image, (0, 0))

    title_text = font.render("Select Your Character", True, (255, 255, 255))
    window.blit(title_text, (WIDTH//2 - title_text.get_width()//2, 50))
    
    # Character options
    character_rects = {}
    x_positions = [WIDTH/5, WIDTH * 2/5, WIDTH * 3/5, WIDTH * 4/5] 
    for i, (char_name, config) in enumerate(character_configs.items()):
        scaled_img = pygame.transform.scale(config['image'], (150, 150))
        rect = scaled_img.get_rect(center=(x_positions[i], HEIGHT//2))
        window.blit(scaled_img, rect)
        character_rects[char_name] = rect
        
        if char_name == selected_character:
            pygame.draw.rect(window, (0, 255, 0), rect, 3)
    
    # Back button
    back_button_rect = pygame.Rect(50, HEIGHT - 100, 200, 50)
    pygame.draw.rect(window, (255, 0, 0), back_button_rect)
    back_text = font.render("Back", True, (255, 255, 255))
    window.blit(back_text, (back_button_rect.centerx - back_text.get_width()//2, 
                          back_button_rect.centery - back_text.get_height()//2))
    
    pygame.display.update()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if music_loaded:
                    pygame.mixer.music.stop()
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                
                for char_name, rect in character_rects.items():
                    if rect.collidepoint(mouse_pos):
                        selected_character = char_name
                        reset_game(selected_character)
                        return START_SCREEN
                
                if back_button_rect.collidepoint(mouse_pos):
                    return START_SCREEN
                    
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return START_SCREEN

def show_start_screen():
    if music_loaded:
        pygame.mixer.music.play(-1)  # Tocar música em loop
    
    window.blit(start_screen_image, (0, 0))
    
    # Start button
    start_button_rect = start_button_image.get_rect(center=(WIDTH//2, HEIGHT//2))
    window.blit(start_button_image, start_button_rect)
    
    # Character select button
    char_select_button_rect = character_select_button_image.get_rect(center=(WIDTH//2, HEIGHT//2 + 110))
    window.blit(character_select_button_image, char_select_button_rect)
    
    # Ranking button
    ranking_button_rect = ranking_button_image.get_rect(center=(WIDTH//2, HEIGHT//2 + 220))
    window.blit(ranking_button_image, ranking_button_rect)
    
    pygame.display.update()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if music_loaded:
                    pygame.mixer.music.stop()
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if start_button_rect.collidepoint(mouse_pos):
                    return GET_PLAYER_NAME
                if char_select_button_rect.collidepoint(mouse_pos):
                    return CHARACTER_SELECT
                if ranking_button_rect.collidepoint(mouse_pos):
                    return SHOW_RANKING
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if music_loaded:
                        pygame.mixer.music.stop()
                    pygame.quit()
                    exit()
                waiting = False
    return GAME_ACTIVE

def show_get_player_name():
    global player_name
    
    input_active = True
    input_text = ""
    
    while input_active:
        window.blit(start_screen_image, (0, 0))

        title_text = title_font.render("Enter Your Name", True, (255, 255, 255))
        window.blit(title_text, (WIDTH//2 - title_text.get_width()//2, HEIGHT//3))

        input_rect = pygame.Rect(WIDTH//2 - 150, HEIGHT//2, 300, 50)
        pygame.draw.rect(window, (255, 255, 255), input_rect, 2)

        text_surface = font.render(input_text, True, (255, 255, 255))
        window.blit(text_surface, (input_rect.x + 10, input_rect.y + 10))

        submit_button = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 + 80, 200, 50)
        pygame.draw.rect(window, (0, 255, 0), submit_button)
        submit_text = font.render("Start Game", True, (0, 0, 0))
        window.blit(submit_text, (submit_button.centerx - submit_text.get_width()//2, 
                                submit_button.centery - submit_text.get_height()//2))
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if music_loaded:
                    pygame.mixer.music.stop()
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if submit_button.collidepoint(event.pos):
                    if input_text.strip() != "":
                        player_name = input_text.strip()
                        if music_loaded:
                            pygame.mixer.music.stop()
                        reset_game(selected_character)
                        return GAME_ACTIVE
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if input_text.strip() != "":
                        player_name = input_text.strip()
                        if music_loaded:
                            pygame.mixer.music.stop()
                        reset_game(selected_character)
                        return GAME_ACTIVE
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    if len(input_text) < 15:  # Limite de caracteres
                        input_text += event.unicode
                if event.key == pygame.K_ESCAPE:
                    return START_SCREEN
    
    return GAME_ACTIVE

def show_ranking():
    ranking = load_ranking()
    
    window.blit(start_screen_image, (0, 0))

    title_text = title_font.render("TOP 10 PLAYERS", True, (255, 255, 255))
    window.blit(title_text, (WIDTH//2 - title_text.get_width()//2, 50))

    for i, entry in enumerate(ranking[:10]):  
        name = entry['name']
        score = entry['score']
        rank_text = ranking_font.render(f"{i+1}. {name}: {score}", True, (255, 255, 255))
        window.blit(rank_text, (WIDTH//2 - rank_text.get_width()//2, 150 + i * 50))
    
    back_button = pygame.Rect(WIDTH//2 - 100, HEIGHT - 100, 200, 50)
    pygame.draw.rect(window, (255, 0, 0), back_button)
    back_text = font.render("Back", True, (255, 255, 255))
    window.blit(back_text, (back_button.centerx - back_text.get_width()//2, 
                          back_button.centery - back_text.get_height()//2))
    
    pygame.display.update()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if music_loaded:
                    pygame.mixer.music.stop()
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.collidepoint(event.pos):
                    return START_SCREEN
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return START_SCREEN

def show_game_over_screen():
    if music_loaded:
        pygame.mixer.music.stop()
        game_over_music.play()
    
    window.blit(game_over_image, (0, 0))
    final_score_text = font.render(f"Final Score: {score}", True, (255, 255, 255))
    window.blit(final_score_text, (WIDTH // 2 - 100, HEIGHT // 2 + 200))
    
    if player_name:
        add_to_ranking(player_name, score)
    
    pygame.display.update()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if music_loaded:
                    game_over_music.stop()
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if music_loaded:
                        game_over_music.stop()
                    pygame.quit()
                    exit()
                waiting = False
    if music_loaded:
        game_over_music.stop()
    reset_game(selected_character)
    return START_SCREEN

def reset_game(character_type='musculoso'):
    global all_sprites, bullet_group, enemy_group, player, score, wave, powerup_group, last_powerup_spawn_time
    
    all_sprites = pygame.sprite.Group()
    bullet_group = pygame.sprite.Group()
    enemy_group = pygame.sprite.Group()
    powerup_group = pygame.sprite.Group()
    
    player = Player(character_type)
    all_sprites.add(player)
    score = 0
    wave = 1
    last_powerup_spawn_time = 0
    spawn_wave(wave)

all_sprites = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
powerup_group = pygame.sprite.Group()

player = Player(selected_character)
all_sprites.add(player)

wave = 1
spawn_wave(wave)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            if music_loaded:
                pygame.mixer.music.stop()
            running = False

    if game_state == START_SCREEN:
        game_state = show_start_screen()
    elif game_state == CHARACTER_SELECT:
        game_state = show_character_select()
    elif game_state == GET_PLAYER_NAME:
        game_state = show_get_player_name()
    elif game_state == SHOW_RANKING:
        game_state = show_ranking()
    elif game_state == GAME_ACTIVE:
        if len(enemy_group) == 0 and player.alive:
            wave += 1
            spawn_wave(wave)

        current_time = pygame.time.get_ticks()
        if (current_time - last_powerup_spawn_time > POWERUP_SPAWN_INTERVAL and 
            random.random() < POWERUP_SPAWN_CHANCE and len(powerup_group) == 0):
            last_powerup_spawn_time = current_time
            powerup_type = random.choice(['health', 'immunity', 'nuke', 'speed', 'extra_life'])
            powerup = Powerup(powerup_type)
            powerup_group.add(powerup)
            all_sprites.add(powerup)

        window.blit(background, (0, 0))
        all_sprites.draw(window)
        all_sprites.update()
        
        if player.alive:
            player.draw_health_bar(window)
            draw_score(window, score)
            draw_wave(window, wave)
            draw_extra_lives(window, player) 
        else:
            game_state = GAME_OVER
    elif game_state == GAME_OVER:
        game_state = show_game_over_screen()
    
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
exit()