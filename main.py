from pygame import *

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

run = True
finished = False

def start_game():
    global finished, player
    finished = False
    win.fill((0, 0, 0))
    player = Player("rocket.png", 300, 400, 5, 80, 80)
    player.reset()
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
    player.update()
    player.reset()


  display.update()
  clock.tick(60)
  
