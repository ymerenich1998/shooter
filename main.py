from pygame import *
from random import randint

init()
# Initialize the game window
class GameSprite(sprite.Sprite):
  def __init__(self, player_image, player_x, player_y, player_speed, player_width=65, player_height=65):
    super().__init__()
    self.image = transform.scale(image.load(player_image), (player_width, player_height))    
    self.speed = player_speed
    self.rect = self.image.get_rect()
    self.rect.x = player_x
    self.rect.y = player_y 
  def reset(self):
    win.blit(self.image, (self.rect.x, self.rect.y))

# Class Player
class Player(GameSprite):
  def update(self):
    keys = key.get_pressed()
    if keys[K_LEFT] and self.rect.x > 5:
      self.rect.x -= self.speed
    if keys[K_RIGHT] and self.rect.x < win_width - 80:
      self.rect.x += self.speed
  
  def fire(self):
    bullet = Bullet("bullet.png", self.rect.centerx, self.rect.top, 10, 15, 20)
    bullets.add(bullet)
    

# Class Enemy
class Enemy(GameSprite):
  def update(self):
    global lost
    self.rect.y += self.speed
    if self.rect.y > win_height:
      self.rect.y = 0
      self.rect.x = randint(80, win_width - 80)
      lost += 1

# Class Bullet
class Bullet(GameSprite):
  def update(self):
    self.rect.y -= self.speed
    if self.rect.y < 0:
      self.kill()
  
win_width = 700
win_height = 500
win =  display.set_mode((win_width, win_height))
display.set_caption("Space Shooter")
bg = transform.scale(image.load("galaxy.jpg"), (win_width, win_height))

clock = time.Clock()

mixer.init()
mixer.music.load("space.ogg")
mixer.music.set_volume(0.1)
mixer.music.play(-1)

fire_sound = mixer.Sound("fire.ogg")
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
    global finished, player, lost, enemies, score, bullets, ammo, life    
    finished = False
    lost = 0
    score = 0
    ammo = 10
    life = 3
    win.fill((0, 0, 0))
    player = Player("rocket.png", 300, 400, 5, 80, 80)
    player.reset()
    enemies = sprite.Group()
    bullets = sprite.Group()
    for _ in range(5):
        enemy = Enemy("ufo.png", randint(80, win_width - 80), randint(-100, -40), randint(1, 3), 80, 40)
        enemies.add(enemy)
    print("Game restarted")


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
        if ammo > 0:
          player.fire()
          ammo -= 1
          fire_sound.play()
        
  if not finished:
    win.blit(bg, (0, 0))

    # Display score and lost count
    text_score = stat_font.render(f"Score: {score}", True, (255, 255, 255))
    text_lost = stat_font.render(f"Lost: {lost}", True, (255, 255, 255))
    text_life = life_font.render(f"{life}", True, (123, 225, 100))
    win.blit(text_score, (10, 10))
    win.blit(text_lost, (10, 50))
    win.blit(text_life, (650, 10))

    if life <= 0:
      finished = True
      win.blit(lose_text, (win_width // 2 - lose_text.get_width() // 2, win_height // 2 - lose_text.get_height() // 2))
    
    if lost >= 10:
      finished = True
      win.blit(lose_text, (win_width // 2 - lose_text.get_width() // 2, win_height // 2 - lose_text.get_height() // 2))

    if score >= 30:
      finished = True
      win.blit(win_text, (win_width // 2 - win_text.get_width() // 2, win_height // 2 - win_text.get_height() // 2))
   
    # Update and draw player and enemies
    player.update()
    enemies.update()
    bullets.update()

    player.reset()
    enemies.draw(win)
    bullets.draw(win)

    collides = sprite.groupcollide(enemies, bullets, True, True)
    for _ in collides:
      score += 1
      if ammo < max_ammo:
        chance = randint(0, 1)
        if chance == 1:
          ammo += 1
      enemy = Enemy("ufo.png", randint(80, win_width - 80), randint(-100, -40), randint(1, 3), 80, 40)
      enemies.add(enemy)
    
    for enemy in enemies:
      if sprite.collide_rect(player, enemy):
        life -= 1
        enemy.kill()
        new_enemy = Enemy("ufo.png", randint(80, win_width - 80), randint(-100, -40), randint(1, 3), 80, 40)
        enemies.add(new_enemy)
        player.rect.x = 300
        player.rect.y = 400
   
    if ammo > 0:
      ammo_text = stat_font.render(f"Ammo: {ammo}", True, (255, 255, 0))
      win.blit(ammo_text, (10, 90))
    else:
      ammo_text = stat_font.render("Out of Ammo!", True, (255, 0, 0))
      win.blit(ammo_text, (10, 90))

    if time.get_ticks() % 150 == 0 and ammo < max_ammo:
      ammo += 1

  display.update()
  clock.tick(60)
  
