import pygame as pg
from random import randint
from pathlib import Path

class GameSprite(pg.sprite.Sprite):
    def __init__(self, image_path: str, x: int, y: int, speed: int, w=65, h=65):
        super().__init__()
        self.image = pg.transform.scale(pg.image.load(image_path), (w, h))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = speed

    def draw(self, surface: pg.Surface) -> None:
        surface.blit(self.image, self.rect)

class Bullet(GameSprite):
    def update(self) -> None:
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill()

class Player(GameSprite):
    def __init__(self, image_path, x, y, speed, w, h, bullets_group: pg.sprite.Group, bullet_image: str):
        super().__init__(image_path, x, y, speed, w, h)
        self._bullets = bullets_group
        self._bullet_image = bullet_image

    def update(self, left_bound: int, right_bound: int) -> None:
        keys = pg.key.get_pressed()
        if (keys[pg.K_LEFT] or keys[pg.K_a]) and self.rect.x > left_bound:
            self.rect.x -= self.speed
        if (keys[pg.K_RIGHT] or keys[pg.K_d]) and self.rect.x < right_bound:
            self.rect.x += self.speed

    def fire(self) -> Bullet:
        bullet = Bullet(self._bullet_image, self.rect.centerx, self.rect.top, 10, 15, 20)
        self._bullets.add(bullet)
        return bullet  # зручно, якщо захочеш реагувати у main (звук тощо)

class Enemy(GameSprite):
    def update(self, screen_h: int, respawn_x_range=(80, 620), on_miss=None) -> None:
        self.rect.y += self.speed
        if self.rect.top > screen_h:
            self.rect.y = -self.rect.height
            self.rect.x = randint(*respawn_x_range)
            if on_miss:
                on_miss()  # інкремент втрат робимо з main

class Boom(pg.sprite.Sprite):
    _frames_cache: dict[tuple[str, tuple[int, int] | None], list[pg.Surface]] = {}

    def __init__(self, frames_dir: str, x: int, y: int, scale: tuple[int, int] | None = (65, 65)):
        super().__init__()
        self.frames = self._load_frames(frames_dir, scale)
        self.index = 0
        self.image = self.frames[self.index]
        self.rect = self.image.get_rect(topleft=(x, y))

    @classmethod
    def _load_frames(cls, frames_dir: str, scale: tuple[int, int] | None):
        key = (frames_dir, scale)
        if key not in cls._frames_cache:
            base = Path(frames_dir)
            frames = []
            # якщо у тебе 1..16
            for i in range(1, 17):
                img = pg.image.load(str(base / f"{i}.png"))
                if scale:
                    img = pg.transform.scale(img, scale)
                frames.append(img)
            cls._frames_cache[key] = frames
        return cls._frames_cache[key]

    def update(self) -> None:
        self.index += 1
        if self.index >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[self.index]
