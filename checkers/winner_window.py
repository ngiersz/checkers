import checkers.configs.config_colors as ccc
import checkers.configs.config_checkers_window as ccw
import pygame as pg


class WinnerWindow():

    def __init__(self, winner):
        self._clock = pg.time.Clock()
        self._done = False
        self._screen = pg.display.set_mode(ccw.SIZE, pg.FULLSCREEN)
        self._all_sprites = pg.sprite.Group()

    def run(self):
        """
        Main loop
        returns: True
        """
        while not self._done:
            self._dt = self._clock.tick(30) / 1000
            self.handle_events()
            self.draw()

    def draw(self):
        """
        Function with main loop for window with checkers board and view
        from the camera
        returns: True
        """

        self._screen.fill(ccc.BEIGE)

        self._all_sprites.draw(self._screen)

        # --- Limit to 60 frames per second
        self._clock.tick(60)

        # Close the window and quit.

    def handle_events(self):
        """
        Deals with events:
            ESC = exit
        returns: True
        """
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                self._done = True
                # if event.key == pg.K_ESCAPE:
                #     if self.changing_name:
                #         self.changing_name = False
                #         self.name_to_set = ccw.NO_NAME
                #     else:
                #         self._done = True

            elif event.type == pg.QUIT:
                self._done = True
            # for button in self._all_sprites:
            #     button.handle_event(event, False)