import pygame
import math
from parametros import *
from sys import exit
import random
import json
import os

pygame.init()

#Tela config
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Z-Killer')
clock = pygame.time.Clock()

#Imagens
background = pygame.image.load('assets/image/Background/background0.png').convert_alpha()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
game_over_image = pygame.image.load('assets/image/Background/game_over.png').convert_alpha()
game_over_image = pygame.transform.scale(game_over_image, (WIDTH, HEIGHT))
start_screen_image = pygame.image.load('assets/image/Background/inicio.png').convert_alpha()
start_screen_image = pygame.transform.scale(start_screen_image, (WIDTH, HEIGHT))
start_button_image = pygame.image.load('assets/image/Background/Start.png').convert_alpha()
start_button_image = pygame.transform.scale(start_button_image, (200, 100))
character_select_button_image = pygame.image.load(r'assets\image\Background\character_select.png').convert_alpha()
character_select_button_image = pygame.transform.rotozoom(character_select_button_image, 0, 1.2)
character_select_button_image = pygame.transform.scale(character_select_button_image, (200, 100))
ranking_button_image = pygame.image.load(r'assets\image\Background\ranking.png').convert_alpha()
ranking_button_image = pygame.transform.scale(ranking_button_image, (200, 100))

pygame.mixer.music.load(r'assets\sound\apocalypse.mp3')  
pygame.mixer.music.set_volume(0.8)
game_over_music = pygame.mixer.Sound(r'assets\sound\go_effect.mp3') 
game_over_music.set_volume(0.5)
shoot_sound = pygame.mixer.Sound(r'assets\sound\shot.mp3')
shoot_sound.set_volume(0.1)
music_loaded = True

BOSS_IMAGE_PATH = r'assets\image\Personagens\Boss\alba_boss.png'
ULTRA_BOSS_IMAGE_PATH = r'assets\image\Personagens\Boss\UltraBoss.png'

POWERUP_IMAGES = {
    'health': pygame.image.load(r'assets\image\PowerUps\health.png').convert_alpha(),
    'immunity': pygame.image.load(r'assets\image\PowerUps\immunity.png').convert_alpha(),
    'nuke': pygame.image.load(r'assets\image\PowerUps\nuke.png').convert_alpha(),
    'speed': pygame.image.load(r'assets\image\PowerUps\speed.png').convert_alpha(),
    'extra_life': pygame.image.load(r'assets\image\PowerUps\extra_life.png').convert_alpha()
}

for key in POWERUP_IMAGES:
    POWERUP_IMAGES[key] = pygame.transform.scale(POWERUP_IMAGES[key], (80,80))

POWERUP_SPAWN_CHANCE = 0.25  
POWERUP_SPAWN_INTERVAL = 30000  # 30 segundos
POWERUP_IMMUNITY_DURATION = 10000  # 10 segundos 

character_configs = {
    'musculoso': {
        'image': pygame.image.load(r'assets/image/Personagens/Masculino/musculoso.png').convert_alpha(),
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
        'image': pygame.image.load(r'assets\image\Personagens\Masculino\nerd.png').convert_alpha(),
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
        'image': pygame.image.load(r'assets\image\Personagens\Masculino\flash.png').convert_alpha(),
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
        'image': pygame.image.load(r'assets\image\Personagens\Masculino\mendel_ofc.png').convert_alpha(),
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

#Partes do jogo
START_SCREEN = 0
GAME_ACTIVE = 1
GAME_OVER = 2
CHARACTER_SELECT = 3
GET_PLAYER_NAME = 4
SHOW_RANKING = 5
game_state = START_SCREEN

#Pontuação
score = 0
player_name = ""
font = pygame.font.Font(None, 36)
title_font = pygame.font.Font(None, 72)
ranking_font = pygame.font.Font(None, 48)

selected_character = 'musculoso'  

last_powerup_spawn_time = 0

#Ranking
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
        self.health_bar_full = pygame.transform.rotozoom(pygame.image.load('assets/image/Personagens/HUD/Health/full.png').convert_alpha(), 0, 0.5)
        self.health_bar_75 = pygame.transform.rotozoom(pygame.image.load('assets/image/Personagens/HUD/Health/75.png').convert_alpha(), 0, 0.5)
        self.health_bar_50 = pygame.transform.rotozoom(pygame.image.load('assets/image/Personagens/HUD/Health/50.png').convert_alpha(), 0, 0.5)
        self.health_bar_25 = pygame.transform.rotozoom(pygame.image.load('assets/image/Personagens/HUD/Health/25.png').convert_alpha(), 0, 0.5)

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
    def init(self, x, y, angle, speed, damage, scale, lifetime):
        super().init()
        self.image = pygame.image.load('assets/image/Weapons/small_dot.png').convert_alpha()
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
    def init(self, position):
        super().init(enemy_group, all_sprites)
        self.image = pygame.image.load('assets/image/Enemies/Zombie/0.png').convert_alpha()
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
    def init(self, position, wave):
        super().init(enemy_group, all_sprites)
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

