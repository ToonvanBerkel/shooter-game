import pygame 
import random

enemy_size = 50
enemy_speed = 3

def create_enemy(WIDTH, HEIGHT):
    return {
        'pos': [random.randint(0, WIDTH - enemy_size), random.randint(0, HEIGHT - enemy_size)],
        'direction': [random.choice([-1, 1]), random.choice([-1, 1])],
        'health': 20
    }

def move_enemies(enemies, WIDTH, HEIGHT):
    for enemy in enemies:
        enemy['pos'][0] += enemy['direction'][0] * enemy_speed
        enemy['pos'][1] += enemy['direction'][1] * enemy_speed

        if enemy['pos'][0] <= 0 or enemy['pos'][0] >= WIDTH - enemy_size:
            enemy['direction'][0] *= -1
        if enemy['pos'][1] <= 0 or enemy['pos'][1] >= HEIGHT - enemy_size:
            enemy['direction'][1] *= -1
