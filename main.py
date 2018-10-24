import sys,os
import pygame as pg
import interface

W = 30
H = 30

class Control(object):
    def __init__(self):
        self.Screen = pg.display.get_surface()
        self.done = False
        self.Clock = pg.time.Clock()
        self.fps = 120
        self.State = interface.Interface()
    def event_loop(self):
        for event in pg.event.get():
            self.keys = pg.key.get_pressed()
            if event.type == pg.QUIT or self.keys[pg.K_ESCAPE]:
                self.done = True
            if self.State.mode != "RUN":
                self.State.get_event(event)
    def game_loop(self):
        while not self.done:
            self.event_loop()
            self.State.update(self.Screen)
            self.Clock.tick_busy_loop(self.fps)
            pg.display.flip()

###
def main():
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pg.init()
    pg.display.set_caption("A* GUI")
    pg.display.set_mode((W*20,H*20))
    RunIt = Control()
    RunIt.game_loop()
    pg.quit();sys.exit()

####
if __name__ == "__main__":
    main()

