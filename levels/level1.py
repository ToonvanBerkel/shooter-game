from Logic.enemy import create_enemy

def load_level(WIDTH, HEIGHT):
    return [create_enemy(WIDTH, HEIGHT) for _ in range(5)]
