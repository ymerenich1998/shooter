from pygame import *
from random import randint
from sprites import Player, Enemy, Bullet, Boom

init()

win_width = 700
win_height = 500
win = display.set_mode((win_width, win_height))
display.set_caption("Space Shooter")
bg = transform.scale(image.load("./assets/galaxy.jpg"), (win_width, win_height))

clock = time.Clock()

mixer.init()
mixer.music.load("./assets/sounds/space.ogg")
mixer.music.set_volume(0.1)
mixer.music.play(-1)

fire_sound = mixer.Sound("./assets/sounds/fire.ogg")
fire_sound.set_volume(0.1)

font.init()
stat_font = font.SysFont("Arial", 24)
result_font = font.SysFont("Arial", 36)
life_font = font.SysFont("Arial", 72)

win_text = result_font.render("You win!", True, (0, 255, 0))
lose_text = result_font.render("You lose!", True, (255, 0, 0))

run = True
finished = False
max_ammo = 10

def start_game():
    global finished, player, lost, enemies, score, bullets, ammo, life, booms, asteroids
    finished = False
    lost = 0
    score = 0
    ammo = 10
    life = 3

    player = Player("./assets/rocket.png", 300, 400, 5, 80, 80)

    enemies = sprite.Group()
    asteroids = sprite.Group()
    bullets = sprite.Group()
    booms = sprite.Group()

    for _ in range(5):
        enemy = Enemy("./assets/ufo.png", randint(80, win_width - 80), randint(-100, -40), randint(1, 3), 80, 40)
        enemies.add(enemy)
    for _ in range(3):
        asteroid = Enemy("./assets/asteroid.png", randint(80, win_width - 80), randint(-100, -40), randint(1, 3), 80, 40)
        asteroids.add(asteroid)

    win.fill((0, 0, 0))

start_game()

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                run = False
            if e.key == K_r:
                start_game()
            if e.key == K_SPACE:
                if ammo > 0 and not finished:
                    player.fire(bullets, "./assets/bullet.png")
                    ammo -= 1
                    fire_sound.play()
        if e.type == MOUSEBUTTONDOWN:
            if e.button == 1 and ammo > 0 and not finished:
                player.fire(bullets, "./assets/bullet.png")
                ammo -= 1
                fire_sound.play()

    if not finished:
        win.blit(bg, (0, 0))

        # HUD
        text_score = stat_font.render(f"Score: {score}", True, (255, 255, 255))
        text_lost = stat_font.render(f"Lost: {lost}", True, (255, 255, 255))
        text_life = life_font.render(f"{life}", True, (123, 225, 100))
        win.blit(text_score, (10, 10))
        win.blit(text_lost, (10, 50))
        win.blit(text_life, (650, 10))

        if life <= 0 or lost >= 10:
            finished = True
            win.blit(lose_text, (win_width // 2 - lose_text.get_width() // 2,
                                 win_height // 2 - lose_text.get_height() // 2))
        if score >= 30:
            finished = True
            win.blit(win_text, (win_width // 2 - win_text.get_width() // 2,
                                win_height // 2 - win_text.get_height() // 2))

        player.update(5, win_width - 80)

        for enemy in list(enemies):
            if enemy.update(win_height, 80, win_width - 80):
                lost += 1
        for asteroid in list(asteroids):
            asteroid.update(win_height, 80, win_width - 80)

        bullets.update()
        booms.update()

        player.draw(win)
        enemies.draw(win)
        bullets.draw(win)
        booms.draw(win)
        asteroids.draw(win)

        for enemy in sprite.groupcollide(enemies, bullets, True, True):
            score += 1
            if ammo < max_ammo and randint(0, 1) == 1:
                ammo += 1
            booms.add(Boom("./assets/boom", enemy.rect.x - 10, enemy.rect.y - 10, 0, 80, 80))
            enemies.add(Enemy("./assets/ufo.png", randint(80, win_width - 80), randint(-100, -40), randint(1, 3), 80, 40))

        for asteroid in sprite.groupcollide(asteroids, bullets, True, True):
            if ammo < max_ammo and randint(0, 1) == 1:
                ammo += 1
            booms.add(Boom("./assets/boom", asteroid.rect.x - 10, asteroid.rect.y - 10, 0, 80, 80))
            asteroids.add(Enemy("./assets/asteroid.png", randint(80, win_width - 80), randint(-100, -40), randint(1, 2), 80, 40))

        for enemy in list(enemies):
            if sprite.collide_rect(player, enemy):
                booms.add(Boom("./assets/boom", player.rect.x - 10, player.rect.y - 10, 0, 80, 80))
                life -= 1
                enemy.kill()
                enemies.add(Enemy("./assets/ufo.png", randint(80, win_width - 80), randint(-100, -40), randint(1, 3), 80, 40))
                player.rect.x, player.rect.y = 300, 400

        for asteroid in list(asteroids):
            if sprite.collide_rect(player, asteroid):
                booms.add(Boom("./assets/boom", player.rect.x - 10, player.rect.y - 10, 0, 80, 80))
                life -= 1
                asteroid.kill()
                asteroids.add(Enemy("./assets/asteroid.png", randint(80, win_width - 80), randint(-100, -40), randint(1, 3), 80, 40))
                player.rect.x, player.rect.y = 300, 400

        if ammo > 0:
            ammo_text = stat_font.render(f"Ammo: {ammo}", True, (255, 255, 0))
        else:
            ammo_text = stat_font.render("Out of Ammo!", True, (255, 0, 0))
        win.blit(ammo_text, (10, 90))

        if time.get_ticks() % 120 == 0 and ammo < max_ammo:
            ammo += 1

    display.update()
    clock.tick(60)
