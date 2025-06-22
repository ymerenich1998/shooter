from pygame import *

init()
win_width = 700
win_height = 500
win =  display.set_mode((win_width, win_height))
display.set_caption("Space Shooter")
bg = transform.scale(image.load("galaxy.jpg"), (win_width, win_height))
win.blit(bg, (0, 0))

clock = time.Clock()

mixer.init()
mixer.music.load("space.ogg")
mixer.music.set_volume(0.1)
mixer.music.play(-1)

run = True

while run:
  display.update()
  clock.tick(60)
  for e in event.get():
    if e.type == QUIT:
      run = False
    if e.type == KEYDOWN:
      if e.key == K_ESCAPE:
        run = False
  
