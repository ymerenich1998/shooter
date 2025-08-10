import pygame as pg
from random import randint


class GameSprite(pg.sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, player_width=65, player_height=65):
        super().__init__()
        self.image = pg.transform.scale(pg.image.load(player_image), (player_width, player_height))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def draw(self, surface: pg.Surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def update(self, left_bound: int, right_bound: int):
        keys = pg.key.get_pressed()
        if (keys[pg.K_LEFT] or keys[pg.K_a]) and self.rect.x > left_bound:
            self.rect.x -= self.speed
        if (keys[pg.K_RIGHT] or keys[pg.K_d]) and self.rect.x < right_bound:
            self.rect.x += self.speed

    def fire(self, bullets_group: pg.sprite.Group, bullet_image: str):
        bullet = Bullet(bullet_image, self.rect.centerx, self.rect.top, 10, 15, 20)
        bullets_group.add(bullet)


class Enemy(GameSprite):
    def update(self, screen_height: int, respawn_x_min: int, respawn_x_max: int) -> bool:
        self.rect.y += self.speed
        if self.rect.y > screen_height:
            self.rect.y = -self.rect.height
            self.rect.x = randint(respawn_x_min, respawn_x_max)
            return True
        return False


class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()


class Boom(GameSprite):
    def __init__(self, frames_dir: str, x: int, y: int, speed: int = 0, w: int = 65, h: int = 65):
        super().__init__(f"{frames_dir}/1.png", x, y, speed, w, h)
        self._frames_dir = frames_dir
        self._n = 1
        self._max = 16 

    def update(self):
        self._n += 1
        if self._n > self._max:
            self.kill()
            return

        img = pg.image.load(f"{self._frames_dir}/{self._n}.png")
        if img.get_size() != (self.rect.w, self.rect.h):
            img = pg.transform.scale(img, (self.rect.w, self.rect.h))
        self.image = img
