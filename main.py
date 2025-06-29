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
    pass

# Class Enemy
class Enemy(GameSprite):
  def update(self):
    global lost
    self.rect.y += self.speed
    if self.rect.y > win_height:
      self.rect.y = 0
      self.rect.x = randint(80, win_width - 80)
      lost += 1
  
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

font.init()
stat_font = font.SysFont("Arial", 24)

run = True
finished = False

def start_game():
    global finished, player, lost, enemies, score
    finished = False
    lost = 0
    score = 0
    win.fill((0, 0, 0))
    player = Player("rocket.png", 300, 400, 5, 80, 80)
    player.reset()
    enemies = sprite.Group()
    for _ in range(5):
        enemy = Enemy("ufo.png", randint(80, win_width - 80), randint(-100, -40), randint(1, 5), 80, 40)
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
  
  if not finished:
    win.blit(bg, (0, 0))

    # Display score and lost count
    text_score = stat_font.render(f"Score: {score}", True, (255, 255, 255))
    text_lost = stat_font.render(f"Lost: {lost}", True, (255, 255, 255))
    win.blit(text_score, (10, 10))
    win.blit(text_lost, (10, 50))
    # Update and draw player and enemies
    player.update()
    enemies.update()

    player.reset()
    enemies.draw(win)


  display.update()
  clock.tick(60)
  
