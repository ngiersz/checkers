import pygame as pg
import datetime
import json
import cv2
import numpy as np
import checkers.checkers_detector as c_d
import checkers.configs.config_checkers_window as ccw
import checkers.configs.config_colors as ccc
import checkers.configs.config_buttons as cb
from checkers.button import Button


class CheckersWindow:
    """
    Class that analyzes state on board, shows it and save data of game if user wants that
    Using frames from camera(in our project we use streaming phone camera via wifi)
    analyze them(finds chessboard with pawns) then checks if move was legal and if it was
    it shows it.
    There is also possibility to save the game to file
    """

    def __init__(self):
        self._camera = cv2.VideoCapture(0)

        self._state = [[0, 1, 0, 1, 0, 1, 0, 1],
                       [1, 0, 1, 0, 1, 0, 1, 0],
                       [0, 1, 0, 1, 0, 1, 0, 1],
                       [1, 0, 1, 0, 1, 0, 1, 0],
                       [0, 1, 0, 1, 0, 1, 0, 1],
                       [1, 0, 1, 0, 1, 0, 1, 0],
                       [0, 1, 0, 1, 0, 1, 0, 1],
                       [1, 0, 1, 0, 1, 0, 1, 0]]

        self._game = [self._state]

        self._screen = pg.display.set_mode(ccw.SIZE, pg.FULLSCREEN)
        self.changing_name = False
        self.name_to_set = ccw.NO_NAME
        self._done = False
        self._save = False
        self._all_sprites = pg.sprite.Group()

        self._black_field = ccc.BLACK
        self._white_field = ccc.WHITE
        self._white_pawn = ccc.WHITE
        self._black_pawn = ccc.BLACK
        self._clock = pg.time.Clock()

        self._dt = self._clock.tick(30) / 1000
        self._frame = cv2.imread('images/chessboard.png')
        self._img = self._frame

        pg.display.set_caption("checkers")
        self.init_textures()

        self.change_name_field = Button(ccw.SELECT_NAME_OFFSET_X,
                                        ccw.SELECT_NAME_OFFSET_Y,
                                        ccw.SELECT_NAME_WIDTH, ccw.SELECT_NAME_HEIGHT, self.change_name, ccw.FONT,
                                        self.name_to_set, (255, 0, 0))
        self._all_sprites.add(self.change_name_field)

    def run(self):
        """
        Main loop
        returns: True
        """
        while not self._done:
            self._dt = self._clock.tick(30) / 1000
            self.handle_events()
            self.get_camera_frame()
            self.run_logic()
            self.draw()

    def handle_events(self):
        """
        Deals with events:
            ESC = exit
        returns: True
        """
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    if self.changing_name:
                        self.name_to_set = ccw.NO_NAME
                    else:
                        self._done = True
                if self.changing_name:
                    if event.key == pg.K_RETURN:
                        self.changing_name = False
                        print("loog FALSE")
                    elif event.key == pg.K_BACKSPACE:
                        self.name_to_set = self.name_to_set[:-1]
                    else:
                        self.name_to_set += event.unicode
                        print(self.name_to_set)
                    self.change_name_field.set_text(self.name_to_set)

            elif event.type == pg.QUIT:
                self._done = True
            for button in self._all_sprites:
                button.handle_event(event, False)

    def get_camera_frame(self):
        """
        updates _frame from phone camera
        #TODO describes how to connect camera with app
        returns: True
        """
        # ret, self._frame = self._camera.read()
        self._frame = cv2.resize(self._frame, (ccw.CAMERA_W, ccw.CAMERA_H))
        self._frame = cv2.cvtColor(self._frame, 3)

    def run_logic(self):
        """
        Checking if move was correct and saving state of the game
        returns: True
        """

        self._img = c_d.find_chessboard(cv2.flip(self._frame, 1))
        if self._save:
            self._game.append(self._state)

        self._clock.tick(60)

    def save_game(self):
        """
        Saves actual game to file with name: game_<date>
        date has format Year-month-day_Hour-Min-Sec
        returns: True
        """

        file_name = 'game_{}'.format(datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
        with open(file_name, 'w') as outfile:
            json.dump(self._game, outfile)

    def draw(self):
        """
        Function with main loop for window with checkers board and view
        from the camera
        returns: True
        """

        self._screen.fill(ccc.BEIGE)

        # Drawing chessboard
        r_counter = 0
        for row in self._state:
            f_counter = 0
            for field in row:
                if field == 0:
                    self._screen.blit(self._black_field, [ccw.RECT_OFFSET_X + (ccw.RECT_SIZE * f_counter),
                                                          ccw.RECT_OFFSET_Y + r_counter * ccw.RECT_SIZE,
                                                          ccw.RECT_SIZE, ccw.RECT_SIZE])
                elif field == 1:
                    self._screen.blit(self._white_field, [ccw.RECT_OFFSET_X + (ccw.RECT_SIZE * f_counter),
                                                          ccw.RECT_OFFSET_Y + r_counter * ccw.RECT_SIZE,
                                                          ccw.RECT_SIZE, ccw.RECT_SIZE])
                elif field == 2:
                    self._screen.blit(self._black_field, [ccw.RECT_OFFSET_X + (ccw.RECT_SIZE * f_counter),
                                                          ccw.RECT_OFFSET_Y + r_counter * ccw.RECT_SIZE,
                                                          ccw.RECT_SIZE, ccw.RECT_SIZE])

                    pg.draw.ellipse(self._screen, ccc.WHITE, [ccw.PAWN_OFFSET_X + (ccw.RECT_SIZE * f_counter),
                                                              ccw.PAWN_OFFSET_Y + r_counter * ccw.RECT_SIZE,
                                                              ccw.PAWN_SIZE, ccw.PAWN_SIZE])
                elif field == 3:
                    self._screen.blit(self._black_field, [ccw.RECT_OFFSET_X + (ccw.RECT_SIZE * f_counter),
                                                          ccw.RECT_OFFSET_Y + r_counter * ccw.RECT_SIZE,
                                                          ccw.RECT_SIZE, ccw.RECT_SIZE])

                    pg.draw.ellipse(self._screen, ccc.BLACK, [ccw.PAWN_OFFSET_X + (ccw.RECT_SIZE * f_counter),
                                                              ccw.PAWN_OFFSET_Y + r_counter * ccw.RECT_SIZE,
                                                              ccw.PAWN_SIZE, ccw.PAWN_SIZE])
                f_counter = f_counter + 1
            r_counter = r_counter + 1

        # --- drawing frame on the window
        img = np.rot90(self._img)
        img = pg.surfarray.make_surface(img)
        self._screen.blit(img, (ccw.CAMERA_OFFSET_X, ccw.CAMERA_OFFSET_Y))

        self._all_sprites.draw(self._screen)

        # --- Drawing code should go here

        pg.display.flip()
        pg.display.update()

        # --- Limit to 60 frames per second
        self._clock.tick(60)

        # Close the window and quit.
    def change_name(self):
        print("loog hello")
        if self.changing_name:
            self.changing_name = False
            print("loog FALSE")
        else:
            self.changing_name = True
            print("loog TRUE")
            self.name_to_set = ""

    def init_textures(self):
        self._black_field = cv2.resize(ccw.BLACK_FIELD, (ccw.RECT_SIZE, ccw.RECT_SIZE))
        self._black_field = pg.surfarray.make_surface(self._black_field)
        self._white_field = cv2.resize(ccw.WHITE_FIELD, (ccw.RECT_SIZE, ccw.RECT_SIZE))
        self._white_field = pg.surfarray.make_surface(self._white_field)
        self._white_pawn = cv2.resize(ccw.WHITE_PAWN, (ccw.RECT_SIZE, ccw.RECT_SIZE))
        self._white_pawn = pg.surfarray.make_surface(self._white_pawn)
        self._black_pawn = cv2.resize(ccw.BLACK_PAWN, (ccw.RECT_SIZE, ccw.RECT_SIZE))
        self._black_pawn = pg.surfarray.make_surface(self._black_pawn)

    def main(self):
        self.run()
