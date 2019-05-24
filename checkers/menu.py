import os
import pygame as pg
pg.init()

import checkers.configs.config_colors as ccc
import checkers.configs.config_menu as ccm
from checkers.checker_window import CheckersWindow
from checkers.archive_window import ArchiveWindow
from checkers.button import Button
import checkers.configs.config_buttons as cb
from checkers.utils import text_format


class MenuWindow:

    def __init__(self):

        os.environ['SDL_VIDEO_CENTERED'] = '1'  # Center the Game Application
        self._screen = pg.display.set_mode(ccm.MENU_SIZE, pg.FULLSCREEN)  # Game Resolution
        self._clock = pg.time.Clock()  # Game Frame rate
        self._done = False
        self._all_sprites = pg.sprite.Group()
        self._dt = self._clock.tick(30) / 1000
        self._screen_color = ccc.BEIGE

        self.start_button = Button(
            ccm.MENU_SIZE[0] / 2 - ccm.NORMAL_RECT / 2,  ccm.MENU_SIZE[1]/3,
            ccm.NORMAL_RECT*2, ccm.NORMAL_RECT, self.checker_window,
            cb.FONT, 'Checkers', (255, 255, 255))
        # If you don't pass images, the default images will be used.
        self.archive_button = Button(
            ccm.MENU_SIZE[0] / 2 - ccm.NORMAL_RECT / 2,  ccm.MENU_SIZE[1]/3+ccm.NORMAL_RECT*2,
            ccm.NORMAL_RECT*2, ccm.NORMAL_RECT, self.archive_window,
            cb.FONT, 'Archive', (255, 255, 255),
            cb.IMAGE_NORMAL, cb.IMAGE_HOVER, cb.IMAGE_DOWN)
        self.quit_button = Button(
            ccm.MENU_SIZE[0] / 2 - ccm.NORMAL_RECT / 2, ccm.MENU_SIZE[1]/3+ccm.NORMAL_RECT*4,
            ccm.NORMAL_RECT*2, ccm.NORMAL_RECT, self.quit_game,
            cb.FONT, 'Quit', (255, 255, 255))

        # Add the button sprites to the sprite group.
        self._all_sprites.add(self.start_button, self.archive_button, self.quit_button)
        self._to_select_buttons = [self.start_button, self.archive_button, self.quit_button]
        self._selectedIT = 0
        self._selected = self._to_select_buttons[0]

    def run(self):
        while not self._done:
            self._dt = self._clock.tick(30) / 1000
            self.handle_events()
            self.run_logic()
            self.draw()

    def draw(self):
        self._screen.fill(self._screen_color)
        self._all_sprites.draw(self._screen)
        pg.display.update()

    def run_logic(self):
        self._all_sprites.update(self._dt)

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self._done = True
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    if self._selectedIT == 0:
                        self._selectedIT = len(self._to_select_buttons) - 1
                    else:
                        self._selectedIT -= 1
                    self._selected = self._to_select_buttons[self._selectedIT]
                elif event.key == pg.K_DOWN:
                    if self._selectedIT == len(self._to_select_buttons) - 1:
                        self._selectedIT = 0
                        self._selected = self._to_select_buttons[self._selectedIT]
                    else:
                        self._selectedIT += 1
                        self._selected = self._to_select_buttons[self._selectedIT]

            for button in self._all_sprites:
                if self._selected == button:
                    if button.handle_event(event, True):
                        self._selected = button
                        self._selectedIT = self._to_select_buttons.index(button)
                else:
                    if button.handle_event(event, False):
                        self._selected = button
                        self._selectedIT = self._to_select_buttons.index(button)

    def checker_window(self):
        CheckersWindow().main()
        print("checkers")

    def archive_window(self):
        ArchiveWindow().main()
        print("archive")

    def quit_game(self):
        self._done = True



