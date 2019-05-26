import pygame as pg
import datetime
import json
import cv2
import numpy as np
import requests
import time
# import eventlet
import threading
from checkers.Field import Field
from checkers.Field import Player
import checkers.configs.config_checkers_window as ccw
import checkers.configs.config_colors as ccc
import checkers.configs.config_buttons as cb
from checkers.button import Button
from checkers.detector import start
from checkers.move_validation import MoveValidation
import checkers.utils as utils


class CheckersWindow:
    """
    Class that analyzes state on board, shows it and save data of game if user wants that
    Using frames from camera(in our project we use streaming phone camera via wifi)
    analyze them(finds chessboard with pawns) then checks if move was legal and if it was
    it shows it.
    There is also possibility to save the game to file
    """

    def __init__(self):
        self._url = "http://192.168.1.66:8080/shot.jpg"

        self._player = Player.WHITE
        self._camera = None
        self._state = ccw.BEGIN_STATE
        self._move_validation = MoveValidation()
        self._game = [self._state]

        self._screen = pg.display.set_mode(ccw.SIZE, pg.FULLSCREEN)
        self.changing_name = False
        self.name_to_set = ccw.NO_NAME
        self._done = False
        self._save = False
        self._reset = False
        self._all_sprites = pg.sprite.Group()

        self._black_field = ccc.BLACK
        self._white_field = ccc.WHITE
        self._white_pawn = ccc.WHITE
        self._black_pawn = ccc.BLACK
        self._clock = pg.time.Clock()

        self._dt = self._clock.tick(30) / 1000
        self._frame = cv2.imread('chessboardClean.png')
        self._frame = cv2.resize(self._frame, (500, 500))
        self._img = self._frame.copy()
        self._img_print = self._img.copy()

        pg.display.set_caption("checkers")
        self.init_textures()

        self.change_name_field = Button(ccw.SELECT_NAME_OFFSET_X,
                                        ccw.SELECT_NAME_OFFSET_Y,
                                        ccw.SELECT_NAME_WIDTH, ccw.SELECT_NAME_HEIGHT, self.change_name, ccw.FONT,
                                        self.name_to_set, (255, 0, 0))
        self.save_game_button = Button(ccw.SAVE_GAME_OFFSET_X,
                                        ccw.SAVE_GAME_OFFSET_Y,
                                        ccw.SAVE_GAME_WIDTH, ccw.SAVE_GAME_HEIGHT, self.save_game, ccw.FONT,
                                        "Save Game", (255, 0, 0))
        self.set_status = Button(ccw.SET_STATE_OFFSET_X,
                                        ccw.SET_STATE_OFFSET_Y,
                                        ccw.SET_STATE_WIDTH, ccw.SET_STATE_HEIGHT, self.reset_state, ccw.FONT,
                                        "Reset", (255, 0, 0))
        self._all_sprites.add(self.change_name_field, self.save_game_button, self.set_status)

    def run(self):
        """
        Main loop
        returns: True
        """
        while not self._done:
            self._dt = self._clock.tick(30) / 1000
            self.handle_events()
            self.draw()
            self.get_camera_frame()

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
                        self.changing_name = False
                        self.name_to_set = ccw.NO_NAME
                    else:
                        self._done = True
                if self.changing_name:
                    if event.key == pg.K_RETURN:
                        self.changing_name = False
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
        using requests gets current frame from this._url
        to host we use "ip webcam"
        returns: True
        """
        try:
            img_resp = requests.get(self._url, verify=False, timeout=0.1)
            img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
            self._frame = cv2.imdecode(img_arr, -1)
        except Exception as e:
            # self._frame = cv2.imread('chessboardClean.png')
            # self._frame = cv2.resize(self._frame, (500, 500))
            # self._img = self._frame.copy()
            print(e)

    def run_logic(self):
        """
        Checking if move was correct and saving state of the game
        returns: True
        """
        while not self._done:
            temp_old_state = self._state.copy()
            temp_old_img = self._img.copy()
            self._img, self._state = start(self._frame, self._state, n=10)
            if self._reset:
                self._game = self._state.copy()
                self._reset = False
            else:
                self._move_validation.compare_boards(temp_old_state, self._state)
                temp_result, self._player = self._move_validation.validate_move(self._player)
                print(self._player)
                if not temp_result:
                    print('Error!: ', self._move_validation.ErrorMessage)
                    self._state = temp_old_state.copy()
                    self._img_print = temp_old_img.copy()
                else:
                    # self._img = cv2.flip(self._img, 1)
                    print('Success!: ', self._move_validation.SuccessMessage)
                    self._img_print = self._img.copy()

                    if "No differences" not in self._move_validation.SuccessMessage:
                        self._save = True

        if self._save:
            self._game.append(self._state)
            self._save = False

        self._clock.tick(60)
        #while not self._done:

    def save_game(self):
        """
        Saves actual game to file with name: game_<date>
        date has format Year-month-day_Hour-Min-Sec
        returns: True
        """
        print("Zapisalem")
        game = utils.enum_to_int_game(self._game)
        if self.name_to_set is not ccw.NO_NAME:
            file_name = 'games_archive/{}'.format(self.name_to_set)
        else:
            file_name = 'games_archive/game_{}'.format(datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
        with open(file_name, 'w') as outfile:
            json.dump(game, outfile)

    def reset_state(self):
        """
        Set actual state as the right state
        returns: True
        """
        self._reset = True
        print("Zresetowalem")

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
                if field == Field.BLACK:
                    self._screen.blit(self._black_field, [ccw.RECT_OFFSET_X + (ccw.RECT_SIZE * f_counter),
                                                          ccw.RECT_OFFSET_Y + r_counter * ccw.RECT_SIZE,
                                                          ccw.RECT_SIZE, ccw.RECT_SIZE])
                elif field == Field.WHITE:
                    self._screen.blit(self._white_field, [ccw.RECT_OFFSET_X + (ccw.RECT_SIZE * f_counter),
                                                          ccw.RECT_OFFSET_Y + r_counter * ccw.RECT_SIZE,
                                                          ccw.RECT_SIZE, ccw.RECT_SIZE])
                elif field == Field.BLACK_FIELD_BLUE_PAWN:
                    self._screen.blit(self._black_field, [ccw.RECT_OFFSET_X + (ccw.RECT_SIZE * f_counter),
                                                          ccw.RECT_OFFSET_Y + r_counter * ccw.RECT_SIZE,
                                                          ccw.RECT_SIZE, ccw.RECT_SIZE])

                    pg.draw.ellipse(self._screen, ccc.BLUE, [ccw.PAWN_OFFSET_X + (ccw.RECT_SIZE * f_counter),
                                                              ccw.PAWN_OFFSET_Y + r_counter * ccw.RECT_SIZE,
                                                              ccw.PAWN_SIZE, ccw.PAWN_SIZE])
                elif field == Field.BLACK_FIELD_RED_PAWN:
                    self._screen.blit(self._black_field, [ccw.RECT_OFFSET_X + (ccw.RECT_SIZE * f_counter),
                                                          ccw.RECT_OFFSET_Y + r_counter * ccw.RECT_SIZE,
                                                          ccw.RECT_SIZE, ccw.RECT_SIZE])

                    pg.draw.ellipse(self._screen, ccc.RED, [ccw.PAWN_OFFSET_X + (ccw.RECT_SIZE * f_counter),
                                                              ccw.PAWN_OFFSET_Y + r_counter * ccw.RECT_SIZE,
                                                              ccw.PAWN_SIZE, ccw.PAWN_SIZE])
                elif field == Field.BLACK_FIELD_BLUE_KING:
                    self._screen.blit(self._black_field, [ccw.RECT_OFFSET_X + (ccw.RECT_SIZE * f_counter),
                                                          ccw.RECT_OFFSET_Y + r_counter * ccw.RECT_SIZE,
                                                          ccw.RECT_SIZE, ccw.RECT_SIZE])

                    pg.draw.ellipse(self._screen, ccc.YELLOW, [ccw.PAWN_OFFSET_X + (ccw.RECT_SIZE * f_counter),
                                                              ccw.PAWN_OFFSET_Y + r_counter * ccw.RECT_SIZE,
                                                              ccw.PAWN_SIZE, ccw.PAWN_SIZE])
                elif field == Field.BLACK_FIELD_RED_KING:
                    self._screen.blit(self._black_field, [ccw.RECT_OFFSET_X + (ccw.RECT_SIZE * f_counter),
                                                          ccw.RECT_OFFSET_Y + r_counter * ccw.RECT_SIZE,
                                                          ccw.RECT_SIZE, ccw.RECT_SIZE])

                    pg.draw.ellipse(self._screen, ccc.GRAY, [ccw.PAWN_OFFSET_X + (ccw.RECT_SIZE * f_counter),
                                                              ccw.PAWN_OFFSET_Y + r_counter * ccw.RECT_SIZE,
                                                              ccw.PAWN_SIZE, ccw.PAWN_SIZE])

                f_counter = f_counter + 1
            r_counter = r_counter + 1

        # --- drawing frame on the window
        # img = np.rot90(self._img_print)
        img = cv2.flip(self._img_print, 1)
        img = np.rot90(img)
        #img = self._img
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
        t1 = threading.Thread(target=self.run_logic)
        t1.start()
        self.run()

