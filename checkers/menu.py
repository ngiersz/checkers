import os
import pygame as pg
import cv2
pg.init()

import checkers.configs.config_colors as ccc
import checkers.configs.config_menu as ccm
from checkers.checker_window import CheckersWindow
from checkers.archive_window import ArchiveWindow
from checkers.button import Button
from checkers.settings_window import SettingsWindow
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
        self._screen_background = ccc.BEIGE

        self.button_normal = ccc.BEIGE
        self.button_hover = ccc.BEIGE
        self.button_down = ccc.BEIGE

        self.init_textures()

        self.start_button = Button(
            ccm.MENU_SIZE[0] / 2 - ccm.NORMAL_RECT,  ccm.MENU_SIZE[1]/3,
            ccm.NORMAL_RECT*2, ccm.NORMAL_RECT, self.checker_window,
            cb.FONT, 'Checkers', (255, 255, 255), self.button_normal, self.button_hover,self.button_down)
        # If you don't pass images, the default images will be used.
        self.archive_button = Button(
            ccm.MENU_SIZE[0] / 2 - ccm.NORMAL_RECT,  ccm.MENU_SIZE[1]/3 + ccm.NORMAL_RECT*2,
            ccm.NORMAL_RECT*2, ccm.NORMAL_RECT, self.archive_window,
            cb.FONT, 'Archive', (255, 255, 255),
            self.button_normal, self.button_hover, self.button_down
        )
        self.settings_button = Button(
            ccm.MENU_SIZE[0] / 2 - ccm.NORMAL_RECT, ccm.MENU_SIZE[1]/3 + ccm.NORMAL_RECT*4,
            ccm.NORMAL_RECT*2, ccm.NORMAL_RECT, self.settings_window,
            cb.FONT, 'Settings', (255, 255, 255), self.button_normal, self.button_hover,self.button_down)
        self.quit_button = Button(
            ccm.MENU_SIZE[0] / 2 - ccm.NORMAL_RECT, ccm.MENU_SIZE[1] / 3 + ccm.NORMAL_RECT*6,
            ccm.NORMAL_RECT * 2, ccm.NORMAL_RECT, self.quit_game,
            cb.FONT, 'Quit', (255, 255, 255), self.button_normal, self.button_hover,self.button_down)

        # Add the button sprites to the sprite group.
        self._all_sprites.add(self.start_button, self.archive_button, self.settings_button, self.quit_button)
        self._to_select_buttons = [self.start_button, self.archive_button, self.settings_button, self.quit_button]
        self._selectedIT = 0
        self._selected = self._to_select_buttons[0]

    def run(self):
        while not self._done:
            self._dt = self._clock.tick(30) / 1000
            self.handle_events()
            self.run_logic()
            self.draw()

    def draw(self):
        # self._screen.fill(self._screen_color)
        self._screen.blit(self._screen_background, [0, 0, ccm.MENU_SIZE[0], ccm.MENU_SIZE[1]])
        self._all_sprites.draw(self._screen)
        pg.display.update()

    def run_logic(self):
        self._all_sprites.update(self._dt)

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self._done = True
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self._done = True
                    print("esc")
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

    def settings_window(self):
        SettingsWindow().main()
        print("Settings")

    def archive_window(self):
        ArchiveWindow().main()
        print("archive")

    def quit_game(self):
        self._done = True

    def init_textures(self):
        self._screen_background = pg.surfarray.make_surface(ccm.BACKGROUND)
        self.button_normal = pg.surfarray.make_surface(ccm.BUTTON)
        self.button_hover = pg.surfarray.make_surface(ccm.BUTTON2)
        self.button_down = pg.surfarray.make_surface(ccm.BUTTON3)




