import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Full screen dimensions
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Simple Shooting Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
GREY = (169, 169, 169)
PURPLE = (128, 0, 128)

# Game states
TITLE, PLAYING, GAME_OVER = 'TITLE', 'PLAYING', 'GAME_OVER'
game_state = TITLE

# Font settings
font = pygame.font.Font(None, 36)
title_font = pygame.font.Font(None, 74)

def reset_game():
    global player_pos, player_health, player_bullets, enemies, bullets, ammo_boxes, five_enemies_spawned, boss_spawned, super_boss_spawned, boss, super_boss
    player_pos = [WIDTH // 2, HEIGHT // 2]
    player_health = 100
    player_bullets = 20
    enemies = [create_enemy()]
    bullets = []
    ammo_boxes = []
    five_enemies_spawned = False
    boss_spawned = False
    super_boss_spawned = False
    boss = None
    super_boss = None

def create_enemy():
    return {
        'pos': [random.randint(0, WIDTH - 50), random.randint(0, HEIGHT - 50)],
        'health': 10,
        'hit_time': 0,
        'direction': [random.choice([-1, 1]), random.choice([-1, 1])],
        'shoot_time': 1000,
        'last_shoot': pygame.time.get_ticks()
    }

def create_boss():
    return {
        'pos': [random.randint(0, WIDTH - 100), random.randint(0, HEIGHT - 100)],
        'health': 50,
        'hit_time': 0,
        'direction': [random.choice([-1, 1]), random.choice([-1, 1])],
        'shoot_time': 500,
        'last_shoot': pygame.time.get_ticks()
    }

def create_super_boss():
    return {
        'pos': [random.randint(0, WIDTH - 150), random.randint(0, HEIGHT - 150)],
        'health': 100,
        'hit_time': 0,
        'direction': [random.choice([-1, 1]), random.choice([-1, 1])],
        'shoot_time': 1500,
        'last_shoot': pygame.time.get_ticks(),
        'speed': 6  # Increased speed for the super boss
    }

reset_game()

# Player settings
player_size = 50
player_color = GREEN
player_speed = 5
player_hit_time = 0

# Enemy settings
enemy_speed = 3
enemy_size = 50

# Bullet settings
bullet_speed = 7
bullet_size = 5
exploding_bullets = []

# Super boss bullet settings
super_boss_bullet_speed = 5
super_boss_bullet_size = 10  # Twice the size of regular bullets

# Ammo box settings
ammo_box_size = 20
ammo_spawn_time = 5000  # milliseconds
ammo_last_spawn = pygame.time.get_ticks()

# Melee attack settings
melee_range = 75
melee_damage = 5
melee_cooldown = 2000  # milliseconds
melee_last_attack = 0
melee_attacking = False

# Game clock
clock = pygame.time.Clock()

def draw_title_screen():
    screen.fill(WHITE)
    title_text = title_font.render("Simple Shooting Game", True, BLACK)
    instruction_text = font.render("Press SPACE to Start", True, BLACK)
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 2 - title_text.get_height() // 2 - 50))
    screen.blit(instruction_text, (WIDTH // 2 - instruction_text.get_width() // 2, HEIGHT // 2 - instruction_text.get_height() // 2 + 50))

def draw_game_over_screen(win):
    screen.fill(WHITE)
    if win:
        game_over_text = title_font.render("You Win!", True, GREEN)
    else:
        game_over_text = title_font.render("Game Over", True, RED)
    instruction_text = font.render("Press SPACE to Play Again", True, BLACK)
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - game_over_text.get_height() // 2 - 50))
    screen.blit(instruction_text, (WIDTH // 2 - instruction_text.get_width() // 2, HEIGHT // 2 - instruction_text.get_height() // 2 + 50))

def draw_player():
    if pygame.time.get_ticks() - player_hit_time < 100:
        color = YELLOW
    else:
        color = player_color
    pygame.draw.rect(screen, color, (*player_pos, player_size, player_size))
    draw_melee_cooldown()

def draw_enemies():
    for enemy in enemies:
        if pygame.time.get_ticks() - enemy['hit_time'] < 100:
            color = YELLOW
        else:
            color = RED
        pygame.draw.rect(screen, color, (*enemy['pos'], enemy_size, enemy_size))
        health_text = font.render(f"{enemy['health']}", True, BLACK)
        screen.blit(health_text, (enemy['pos'][0], enemy['pos'][1] - 20))

def draw_boss():
    if boss:
        if pygame.time.get_ticks() - boss['hit_time'] < 100:
            color = YELLOW
        else:
            color = PURPLE
        pygame.draw.rect(screen, color, (*boss['pos'], 100, 100))
        health_text = font.render(f"{boss['health']}", True, BLACK)
        screen.blit(health_text, (boss['pos'][0], boss['pos'][1] - 20))

def draw_super_boss():
    if super_boss:
        if pygame.time.get_ticks() - super_boss['hit_time'] < 100:
            color = YELLOW
        else:
            color = RED
        pygame.draw.rect(screen, color, (*super_boss['pos'], 150, 150))
        health_text = font.render(f"{super_boss['health']}", True, BLACK)
        screen.blit(health_text, (super_boss['pos'][0], super_boss['pos'][1] - 20))

def draw_bullets():
    for bullet in bullets:
        if bullet.get('hit'):
            pygame.draw.circle(screen, RED, (int(bullet['pos'][0]), int(bullet['pos'][1])), bullet['size'])
        else:
            pygame.draw.circle(screen, BLACK, (int(bullet['pos'][0]), int(bullet['pos'][1])), bullet['size'])

def draw_ammo_boxes():
    for box in ammo_boxes:
        pygame.draw.rect(screen, BLACK, (*box, ammo_box_size, ammo_box_size))

def draw_status():
    health_text = font.render(f"Health: {player_health}", True, BLACK)
    ammo_text = font.render(f"Ammo: {player_bullets}", True, BLACK)
    screen.blit(health_text, (10, 10))
    screen.blit(ammo_text, (10, 50))

def draw_melee_attack():
    if melee_attacking:
        center = (player_pos[0] + player_size // 2, player_pos[1] + player_size // 2)
        pygame.draw.circle(screen, RED, center, melee_range, 3)

def draw_melee_cooldown():
    current_time = pygame.time.get_ticks()
    if current_time - melee_last_attack < melee_cooldown:
        cooldown_ratio = (current_time - melee_last_attack) / melee_cooldown
        cooldown_width = int(player_size * cooldown_ratio)
        pygame.draw.rect(screen, GREY, (player_pos[0], player_pos[1] + player_size + 5, player_size, 10))
        pygame.draw.rect(screen, RED, (player_pos[0], player_pos[1] + player_size + 5, cooldown_width, 10))
    else:
        pygame.draw.rect(screen, GREY, (player_pos[0], player_pos[1] + player_size + 5, player_size, 10))
        pygame.draw.rect(screen, GREEN, (player_pos[0], player_pos[1] + player_size + 5, player_size, 10))

def move_player(keys_pressed):
    if keys_pressed[pygame.K_w] and player_pos[1] - player_speed > 0:
        player_pos[1] -= player_speed
    if keys_pressed[pygame.K_s] and player_pos[1] + player_speed + player_size < HEIGHT:
        player_pos[1] += player_speed
    if keys_pressed[pygame.K_a] and player_pos[0] - player_speed > 0:
        player_pos[0] -= player_speed
    if keys_pressed[pygame.K_d] and player_pos[0] + player_speed + player_size < WIDTH:
        player_pos[0] += player_speed

def move_enemies():
    for enemy in enemies:
        enemy['pos'][0] += enemy['direction'][0] * enemy_speed
        enemy['pos'][1] += enemy['direction'][1] * enemy_speed

        if enemy['pos'][0] <= 0 or enemy['pos'][0] >= WIDTH - enemy_size:
            enemy['direction'][0] = -enemy['direction'][0]
        if enemy['pos'][1] <= 0 or enemy['pos'][1] >= HEIGHT - enemy_size:
            enemy['direction'][1] = -enemy['direction'][1]

def move_boss():
    if boss:
        boss['pos'][0] += boss['direction'][0] * enemy_speed
        boss['pos'][1] += boss['direction'][1] * enemy_speed

        if boss['pos'][0] <= 0 or boss['pos'][0] >= WIDTH - 100:
            boss['direction'][0] = -boss['direction'][0]
        if boss['pos'][1] <= 0 or boss['pos'][1] >= HEIGHT - 100:
            boss['direction'][1] = -boss['direction'][1]

def move_super_boss():
    if super_boss:
        super_boss['pos'][0] += super_boss['direction'][0] * super_boss['speed']
        super_boss['pos'][1] += super_boss['direction'][1] * super_boss['speed']

        if super_boss['pos'][0] <= 0 or super_boss['pos'][0] >= WIDTH - 150:
            super_boss['direction'][0] = -super_boss['direction'][0]
        if super_boss['pos'][1] <= 0 or super_boss['pos'][1] >= HEIGHT - 150:
            super_boss['direction'][1] = -super_boss['direction'][1]

def shoot_bullet(target_pos):
    global player_bullets
    if player_bullets > 0:
        direction = [target_pos[0] - (player_pos[0] + player_size // 2), target_pos[1] - (player_pos[1] + player_size // 2)]
        length = math.hypot(*direction)
        direction = [direction[0] / length, direction[1] / length]
        bullets.append({'pos': [player_pos[0] + player_size // 2, player_pos[1] + player_size // 2], 'dir': direction, 'owner': 'player', 'hit': False, 'size': bullet_size})
        player_bullets -= 1

def move_bullets():
    for bullet in bullets[:]:
        bullet['pos'][0] += bullet['dir'][0] * bullet_speed
        bullet['pos'][1] += bullet['dir'][1] * bullet_speed
        if bullet['pos'][0] < 0 or bullet['pos'][0] > WIDTH or bullet['pos'][1] < 0 or bullet['pos'][1] > HEIGHT:
            bullets.remove(bullet)

def check_bullet_hits():
    global enemy_hit_time, boss, super_boss, five_enemies_spawned, boss_spawned, super_boss_spawned
    for bullet in bullets[:]:
        if bullet.get('hit'):
            if pygame.time.get_ticks() - bullet['hit_time'] > 200:
                bullets.remove(bullet)
            continue
        for enemy in enemies:
            if enemy['pos'][0] < bullet['pos'][0] < enemy['pos'][0] + enemy_size and enemy['pos'][1] < bullet['pos'][1] < enemy['pos'][1] + enemy_size and bullet['owner'] == 'player':
                bullet['hit'] = True
                bullet['hit_time'] = pygame.time.get_ticks()
                enemy['health'] -= 1
                enemy['hit_time'] = pygame.time.get_ticks()
                if enemy['health'] <= 0:
                    enemies.remove(enemy)
                    if not five_enemies_spawned:
                        print("Spawning five enemies")
                        enemies.extend(create_enemy() for _ in range(5))
                        five_enemies_spawned = True
        if boss:
            if boss['pos'][0] < bullet['pos'][0] < boss['pos'][0] + 100 and boss['pos'][1] < bullet['pos'][1] < boss['pos'][1] + 100 and bullet['owner'] == 'player':
                bullet['hit'] = True
                bullet['hit_time'] = pygame.time.get_ticks()
                boss['health'] -= 1
                boss['hit_time'] = pygame.time.get_ticks()
                if boss['health'] <= 0:
                    boss = None
        if super_boss:
            if super_boss['pos'][0] < bullet['pos'][0] < super_boss['pos'][0] + 150 and super_boss['pos'][1] < bullet['pos'][1] < super_boss['pos'][1] + 150 and bullet['owner'] == 'player':
                bullet['hit'] = True
                bullet['hit_time'] = pygame.time.get_ticks()
                super_boss['health'] -= 1
                super_boss['hit_time'] = pygame.time.get_ticks()
                if super_boss['health'] <= 0:
                    super_boss = None

def spawn_ammo_box():
    ammo_boxes.append([random.randint(0, WIDTH - ammo_box_size), random.randint(0, HEIGHT - ammo_box_size)])

def pick_ammo_box():
    global player_bullets
    for box in ammo_boxes[:]:
        if player_pos[0] < box[0] < player_pos[0] + player_size and player_pos[1] < box[1] < player_pos[1] + player_size:
            ammo_boxes.remove(box)
            player_bullets = 20

def enemy_shoot():
    for enemy in enemies:
        if pygame.time.get_ticks() - enemy['last_shoot'] > enemy['shoot_time']:
            direction = [player_pos[0] + player_size // 2 - (enemy['pos'][0] + enemy_size // 2), player_pos[1] + player_size // 2 - (enemy['pos'][1] + enemy_size // 2)]
            length = math.hypot(*direction)
            direction = [direction[0] / length, direction[1] / length]
            bullets.append({'pos': [enemy['pos'][0] + enemy_size // 2, enemy['pos'][1] + enemy_size // 2], 'dir': direction, 'owner': 'enemy', 'hit': False, 'size': bullet_size})
            enemy['last_shoot'] = pygame.time.get_ticks()
    if boss:
        if pygame.time.get_ticks() - boss['last_shoot'] > boss['shoot_time']:
            direction = [player_pos[0] + player_size // 2 - (boss['pos'][0] + 50), player_pos[1] + player_size // 2 - (boss['pos'][1] + 50)]
            length = math.hypot(*direction)
            direction = [direction[0] / length, direction[1] / length]
            bullets.append({'pos': [boss['pos'][0] + 50, boss['pos'][1] + 50], 'dir': direction, 'owner': 'boss', 'hit': False, 'size': bullet_size})
            bullets.append({'pos': [boss['pos'][0] + 50, boss['pos'][1] + 50], 'dir': direction, 'owner': 'boss', 'hit': False, 'size': bullet_size})
            boss['last_shoot'] = pygame.time.get_ticks()
    if super_boss:
        if pygame.time.get_ticks() - super_boss['last_shoot'] > super_boss['shoot_time']:
            direction = [player_pos[0] + player_size // 2 - (super_boss['pos'][0] + 75), player_pos[1] + player_size // 2 - (super_boss['pos'][1] + 75)]
            length = math.hypot(*direction)
            direction = [direction[0] / length, direction[1] / length]
            bullets.append({'pos': [super_boss['pos'][0] + 75, super_boss['pos'][1] + 75], 'dir': direction, 'owner': 'super_boss', 'hit': False, 'size': super_boss_bullet_size})
            super_boss['last_shoot'] = pygame.time.get_ticks()

def check_player_hit():
    global player_health, player_hit_time
    for bullet in bullets[:]:
        if bullet.get('hit'):
            if pygame.time.get_ticks() - bullet['hit_time'] > 200:
                bullets.remove(bullet)
            continue
        if player_pos[0] < bullet['pos'][0] < player_pos[0] + player_size and player_pos[1] < bullet['pos'][1] < player_pos[1] + player_size and bullet['owner'] in ['enemy', 'boss', 'super_boss']:
            bullet['hit'] = True
            bullet['hit_time'] = pygame.time.get_ticks()
            player_health -= 1
            player_hit_time = pygame.time.get_ticks()

def check_melee_hit():
    global enemy_health, enemy_hit_time, boss, super_boss, five_enemies_spawned
    center = (player_pos[0] + player_size // 2, player_pos[1] + player_size // 2)
    for enemy in enemies:
        distance = math.hypot(center[0] - enemy['pos'][0], center[1] - enemy['pos'][1])
        if distance <= melee_range:
            enemy['health'] -= melee_damage
            enemy['hit_time'] = pygame.time.get_ticks()
            if enemy['health'] <= 0:
                enemies.remove(enemy)
                if not five_enemies_spawned:
                    print("Spawning five enemies")
                    enemies.extend(create_enemy() for _ in range(5))
                    five_enemies_spawned = True
    if boss:
        distance = math.hypot(center[0] - boss['pos'][0], center[1] - boss['pos'][1])
        if distance <= melee_range + 50:  # Adjust for the larger size of the boss
            boss['health'] -= melee_damage
            boss['hit_time'] = pygame.time.get_ticks()
            if boss['health'] <= 0:
                boss = None
    if super_boss:
        distance = math.hypot(center[0] - super_boss['pos'][0], center[1] - super_boss['pos'][1])
        if distance <= melee_range + 75:  # Adjust for the larger size of the super boss
            super_boss['health'] -= melee_damage
            super_boss['hit_time'] = pygame.time.get_ticks()
            if super_boss['health'] <= 0:
                super_boss = None

def check_melee_bullet_hit():
    center = (player_pos[0] + player_size // 2, player_pos[1] + player_size // 2)
    for bullet in bullets:
        if bullet.get('hit'):
            continue
        distance = math.hypot(center[0] - bullet['pos'][0], center[1] - bullet['pos'][1])
        if distance <= melee_range:
            bullet['hit'] = True
            bullet['hit_time'] = pygame.time.get_ticks()

running = True
while running:
    clock.tick(60)
    screen.fill(WHITE)
    keys_pressed = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and game_state in [TITLE, GAME_OVER]:
            game_state = PLAYING
            reset_game()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and game_state == PLAYING:
                shoot_bullet(event.pos)
            elif event.button == 3 and game_state == PLAYING:
                current_time = pygame.time.get_ticks()
                if current_time - melee_last_attack >= melee_cooldown:
                    melee_last_attack = current_time
                    melee_attacking = True
                    check_melee_hit()
                    check_melee_bullet_hit()

    if game_state == TITLE:
        draw_title_screen()
    elif game_state == PLAYING:
        move_player(keys_pressed)
        move_enemies()
        move_boss()
        move_super_boss()
        move_bullets()
        check_bullet_hits()
        pick_ammo_box()

        # Enemy shooting
        enemy_shoot()

        # Ammo box spawning
        if pygame.time.get_ticks() - ammo_last_spawn > ammo_spawn_time:
            spawn_ammo_box()
            ammo_last_spawn = pygame.time.get_ticks()

        # Check player hit
        check_player_hit()

        # Draw everything
        draw_player()
        draw_enemies()
        draw_boss()
        draw_super_boss()
        draw_bullets()
        draw_ammo_boxes()
        draw_status()
        draw_melee_attack()

        # End melee attack animation
        if melee_attacking and pygame.time.get_ticks() - melee_last_attack > 200:
            melee_attacking = False

        # Game over conditions
        if player_health <= 0:
            game_state = GAME_OVER
            win = False
        if not enemies and not boss_spawned and five_enemies_spawned:
            boss_spawned = True
            boss = create_boss()
            print("Boss spawned")
        if boss_spawned and not boss and not super_boss_spawned:
            super_boss_spawned = True
            super_boss = create_super_boss()
            print("Super Boss spawned")
        if super_boss_spawned and not super_boss:
            game_state = GAME_OVER
            win = True

    elif game_state == GAME_OVER:
        draw_game_over_screen(win)

    pygame.display.flip()

pygame.quit()