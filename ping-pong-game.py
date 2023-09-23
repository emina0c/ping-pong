from pygame import *

color = (200,255,255)
win_width = 600
win_height = 500
window = display.set_mode((win_width,win_height))
window.fill(color)

clock = time.Clock()
FPS = 60
game = True

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

    display.update()
    clock.tick(FPS)