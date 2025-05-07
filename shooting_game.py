import pygame 
import random
import math
from levels import level1
from Logic.player import move_player, player_size
from Logic.enemy import move_enemies, enemy_size

# Initialize Pygame
pygame.init()

info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Simple Shooting Game")

WHITE, BLACK = (255, 255, 255), (0, 0, 0)
RED, GREEN, YELLOW = (255, 0, 0), (0, 255, 0), (255, 255, 0)
GREY, PURPLE = (169, 169, 169), (128, 0, 128)
TITLE, PLAYING, GAME_OVER, FINISHED = 'TITLE', 'PLAYING', 'GAME_OVER', 'FINISHED'
font, title_font = pygame.font.Font(None, 36), pygame.font.Font(None, 74)

bullet_speed, bullet_size = 7, 5

clock = pygame.time.Clock()
game_state = TITLE
player_color = GREEN

def reset_game():
    global player_pos, player_health, enemies, bullets
    player_pos = [WIDTH // 2, HEIGHT // 2]
    player_health = 100
    bullets.clear()
    enemies.clear()
    enemies.extend(level1.load_level(WIDTH, HEIGHT))

def draw_title_screen():
    screen.fill(WHITE)
    title_text = title_font.render("Simple Shooting Game", True, BLACK)
    instruction_text = font.render("Press SPACE to Start", True, BLACK)
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 2 - title_text.get_height() // 2 - 50))
    screen.blit(instruction_text, (WIDTH // 2 - instruction_text.get_width() // 2, HEIGHT // 2 - instruction_text.get_height() // 2 + 50))

def draw_finished_screen():
    screen.fill(WHITE)
    finished_text = title_font.render("Level Complete!", True, GREEN)
    restart_text = font.render("Press SPACE to Play Again", True, BLACK)
    screen.blit(finished_text, (WIDTH // 2 - finished_text.get_width() // 2, HEIGHT // 2 - 50))
    screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 50))

def draw_health_bar(x, y, health, max_health, width=50, height=5):
    pygame.draw.rect(screen, GREY, (x, y - 10, width, height))
    health_width = int(width * (health / max_health))
    pygame.draw.rect(screen, RED, (x, y - 10, health_width, height))

def draw_gameplay():
    pygame.draw.rect(screen, player_color, (*player_pos, player_size, player_size))
    draw_health_bar(player_pos[0], player_pos[1], player_health, 100, player_size)

    for enemy in enemies:
        pygame.draw.rect(screen, RED, (*enemy['pos'], enemy_size, enemy_size))
        draw_health_bar(enemy['pos'][0], enemy['pos'][1], enemy['health'], 20, enemy_size)

    for bullet in bullets:
        pygame.draw.circle(screen, BLACK, (int(bullet['pos'][0]), int(bullet['pos'][1])), bullet_size)

def move_bullets():
    global player_health
    for bullet in bullets[:]:
        bullet_hit = False
        bullet['pos'][0] += bullet['dir'][0] * bullet_speed
        bullet['pos'][1] += bullet['dir'][1] * bullet_speed

        if bullet['pos'][0] < 0 or bullet['pos'][0] > WIDTH or bullet['pos'][1] < 0 or bullet['pos'][1] > HEIGHT:
            bullets.remove(bullet)
            continue

        for enemy in enemies:
            ex, ey = enemy['pos']
            if ex < bullet['pos'][0] < ex + enemy_size and ey < bullet['pos'][1] < ey + enemy_size:
                enemy['health'] -= 5
                if enemy['health'] <= 0:
                    enemies.remove(enemy)
                bullet_hit = True
                break

        if bullet_hit:
            bullets.remove(bullet)
            continue

        if bullet.get('source') != 'player':
            px, py = player_pos
            if px < bullet['pos'][0] < px + player_size and py < bullet['pos'][1] < py + player_size:
                player_health -= 5
                bullets.remove(bullet)

def shoot_bullet(target):
    dx, dy = target[0] - (player_pos[0] + player_size // 2), target[1] - (player_pos[1] + player_size // 2)
    dist = math.hypot(dx, dy)
    if dist == 0:
        return
    dx, dy = dx / dist, dy / dist
    bullets.append({
        'pos': [player_pos[0] + player_size // 2, player_pos[1] + player_size // 2],
        'dir': [dx, dy],
        'source': 'player'
    })

enemies, bullets = [], []
reset_game()

running = True
while running:
    clock.tick(60)
    screen.fill(WHITE)
    keys_pressed = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and game_state in [TITLE, GAME_OVER, FINISHED]:
            game_state = PLAYING
            reset_game()
        elif event.type == pygame.MOUSEBUTTONDOWN and game_state == PLAYING:
            if event.button == 1:
                shoot_bullet(event.pos)

    if game_state == TITLE:
        draw_title_screen()
    elif game_state == PLAYING:
        move_player(keys_pressed, player_pos, WIDTH, HEIGHT)
        move_enemies(enemies, WIDTH, HEIGHT)
        move_bullets()
        draw_gameplay()
        if not enemies:
            game_state = FINISHED
    elif game_state == FINISHED:
        draw_finished_screen()

    pygame.display.flip()

pygame.quit()
