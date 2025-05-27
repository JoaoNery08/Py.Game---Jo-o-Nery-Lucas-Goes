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