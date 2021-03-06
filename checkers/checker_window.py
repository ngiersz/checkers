import pygame as pg
import datetime
import json
import cv2
import numpy as np
import requests
import threading
from checkers.fields import Field
from checkers.fields import Player
import checkers.configs.config_checkers_window as ccw
import checkers.configs.config_colors as ccc
from checkers.button import Button
from checkers.detector import detect
from checkers.move_validation import MoveValidation
import checkers.utils as utils
from checkers.text_field import TextField
from checkers.winner_window import WinnerWindow
import time

class CheckersWindow:
    """
    Class that analyzes state on board, shows it and save data of game if user wants that
    Using frames from camera(in our project we use streaming phone camera via wifi)
    analyze them(finds chessboard with pawns) then checks if move was legal and if it was
    it shows it.
    There is also possibility to save the game to file
    """

    def __init__(self):
        self.load_url()
        # self._url = "http://192.168.43.1:8080/shot.jpg"

        self._player = Player.WHITE
        self._camera = None
        self._state = ccw.BEGIN_STATE
        self._move_validation = MoveValidation()
        self._game = []
        self._game.append(self._state)
        self._move_made = False

        self._screen = pg.display.set_mode(ccw.SIZE, pg.FULLSCREEN)
        self.changing_name = False
        self.name_to_set = ccw.NO_NAME
        self._done = False
        self._save = False
        self._reset = False
        self._all_sprites = pg.sprite.Group()

        self._black_field = ccc.BLACK
        self._white_field = ccc.WHITE
        self._blue_pawn = ccc.BLUE
        self._red_pawn = ccc.RED
        self._blue_queen = ccc.BLUE
        self._red_queen = ccc.RED
        self._background = ccc.BEIGE
        self._camera_window = ccc.BEIGE
        self._bottom_bar = ccc.BEIGE
        self._board_background = ccc.BEIGE

        self.button_normal = ccw.IMAGE_NORMAL
        self.button_hover = ccw.IMAGE_HOVER
        self.button_down = ccw.IMAGE_DOWN

        self.button_text_normal = ccw.IMAGE_TEXT_NORMAL
        self.button_text_hover = ccw.IMAGE_TEXT_HOVER
        self.button_text_down = ccw.IMAGE_TEXT_DOWN

        self._clock = pg.time.Clock()

        self._dt = self._clock.tick(30) / 1000
        self._frame = cv2.imread('chessboardClean.png')
        self._frame = cv2.resize(self._frame, (500, 500))
        self._img = self._frame.copy()
        self._img_print = self._img.copy()

        self._error_message = None
        self._error_counter = 0

        pg.display.set_caption("checkers")
        self.init_textures()

        self.change_name_field = Button(ccw.SELECT_NAME_OFFSET_X,
                                        ccw.SELECT_NAME_OFFSET_Y,
                                        ccw.SELECT_NAME_WIDTH, ccw.SELECT_NAME_HEIGHT, self.change_name, ccw.FONT,
                                        self.name_to_set, (255, 255, 255), self.button_normal, self.button_hover,self.button_down)
        self.save_game_button = Button(ccw.SAVE_GAME_OFFSET_X,
                                        ccw.SAVE_GAME_OFFSET_Y,
                                        ccw.SAVE_GAME_WIDTH, ccw.SAVE_GAME_HEIGHT, self.save_game, ccw.FONT,
                                        "Save Game", (255, 255, 255), self.button_normal, self.button_hover,self.button_down)
        self.set_status = Button(ccw.SET_STATE_OFFSET_X,
                                        ccw.SET_STATE_OFFSET_Y,
                                        ccw.SET_STATE_WIDTH, ccw.SET_STATE_HEIGHT, self.reset_state, ccw.FONT,
                                        "Reset", (255, 255, 255), self.button_normal, self.button_hover,self.button_down)
        self.move_comunicate = TextField(ccw.MOVE_COMMUNICATE_OFFSET_X,
                                         ccw.MOVE_COMMUNICATE_OFFSET_Y,
                                         ccw.MOVE_COMMUNICATE_WIDTH,
                                         ccw.MOVE_COMMUNICATE_HEIGHT,
                                         'Turn: Blue pawns',  ccw.FONT, (255, 255, 255), self.button_text_normal)
        self._all_sprites.add(self.change_name_field, self.save_game_button, self.set_status, self.move_comunicate)

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
            self._error_message = "NO CONNECTION"
            self.move_comunicate.set_text(self._error_message)
            print(e)

    def run_logic(self):
        """
        Checking if move was correct and saving state of the game
        returns: True
        """
        while not self._done:
            temp_old_state = self._state.copy()
            temp_old_img = self._img.copy()
            self._img, self._state = detect(self._frame, self._state)
            self.winner = None

            if self._reset:
                self._game = []
                self._game.append(self._state.copy())
                self._reset = False
                self._move_made = False
                self.move_comunicate.set_text('Turn: Blue pawns')
            else:
                self._move_validation.compare_boards(temp_old_state, self._state)
                temp_result, self._player = self._move_validation.validate_move(self._player)
                print(self._player)

                if not temp_result:
                    print('Error!: ', self._move_validation.ErrorMessage)
                    self._state = temp_old_state.copy()
                    self._img_print = temp_old_img.copy()

                    if self._error_message == self._move_validation.ErrorMessage:
                        self._error_counter += 1
                    else:
                        self._error_message = self._move_validation.ErrorMessage
                        self._error_counter = 0

                    if self._error_counter > 10:
                        self.move_comunicate.set_text(self._move_validation.ErrorMessage)
                        self._error_counter = 0
                        self._error_message = None

                else:
                    # self._img = cv2.flip(self._img, 1)
                    if (self._move_made is False) and (self._move_validation.SuccessMessage is 'No differences'):
                        self.move_comunicate.set_text('Turn: Blue pawns')
                    if (self._move_made is False) and (self._move_validation.SuccessMessage != 'No differences'
                                                       and self._move_validation.SuccessMessage != ''):
                        self._move_made = True
                    print('Success!: ', self._move_validation.SuccessMessage)
                    self.move_comunicate.set_text('')
                    self._img_print = self._img.copy()
                    piece_count = self._move_validation.count_pieces()

                    if "No differences" not in self._move_validation.SuccessMessage:
                        self._save = True

                    if piece_count.Current_black == 0:
                        self.winner = "BLUE"
                    elif piece_count.Current_white == 0:
                        self.winner = "RED"

                    if self.winner != None and self._move_made == True:
                        self.move_comunicate.set_text('We have a winner! Player: ' + str(self.winner))
                        time.sleep(3)
                        # self._done = True
                        # self.run_winner_window(self.winner)
                    #     run winner window

                if not self._move_made:
                    self.move_comunicate.set_text('Turn: Blue pawns')

            if self._save:
                self._game.append(self._state)
                self._save = False

        self._clock.tick(60)

    def save_game(self):
        """
        Saves actual game to file with name: game_<date>
        date has format Year-month-day_Hour-Min-Sec
        returns: True
        """
        print("Zapisalem")
        print(self._game)
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

        # self._screen.fill(ccc.BEIGE)
        self._screen.blit(self._background, [0, 0, ccw.SIZE[0], ccw.SIZE[1]])
        self._screen.blit(self._board_background, [ccw.RECT_OFFSET_X - ccw.RECT_SIZE/2,
                                                   ccw.RECT_OFFSET_Y - ccw.RECT_SIZE/2, ccw.BOARD_SIZE, ccw.BOARD_SIZE])
        self._screen.blit(self._camera_window, (ccw.CAMERA_OFFSET_X-20, ccw.CAMERA_OFFSET_Y-20))

        self._screen.blit(self._bottom_bar, (0, ccw.SIZE[1]-ccw.BAR_SIZE_Y))

        # Drawing chessboard
        r_counter = 0
        for row in self._state:
            f_counter = 0
            for field in row:
                if field == Field.BLACK:
                    self._screen.blit(self._black_field, [ccw.RECT_OFFSET_X + int(ccw.RECT_SIZE*1.0) * f_counter,
                                                          ccw.RECT_OFFSET_Y + r_counter*ccw.RECT_SIZE,
                                                          ccw.RECT_SIZE, int(ccw.RECT_SIZE*1.0)])
                elif field == Field.WHITE:
                    self._screen.blit(self._white_field, [ccw.RECT_OFFSET_X + int(ccw.RECT_SIZE*1.0) * f_counter,
                                                          ccw.RECT_OFFSET_Y + r_counter*ccw.RECT_SIZE,
                                                          ccw.RECT_SIZE, int(ccw.RECT_SIZE*1.0)])
                elif field == Field.BLACK_FIELD_BLUE_PAWN:
                    self._screen.blit(self._blue_pawn, [ccw.RECT_OFFSET_X + int(ccw.RECT_SIZE*1.0) * f_counter,
                                                        ccw.RECT_OFFSET_Y + r_counter*ccw.RECT_SIZE,
                                                        ccw.RECT_SIZE, int(ccw.RECT_SIZE*1.0)])

                elif field == Field.BLACK_FIELD_RED_PAWN:
                    self._screen.blit(self._red_pawn, [ccw.RECT_OFFSET_X + int(ccw.RECT_SIZE*1.0) * f_counter,
                                                       ccw.RECT_OFFSET_Y + r_counter*ccw.RECT_SIZE,
                                                       ccw.RECT_SIZE, int(ccw.RECT_SIZE*1.0)])

                elif field == Field.BLACK_FIELD_BLUE_QUEEN:
                    self._screen.blit(self._blue_queen, [ccw.RECT_OFFSET_X + int(ccw.RECT_SIZE*1.0) * f_counter,
                                                         ccw.RECT_OFFSET_Y + r_counter*ccw.RECT_SIZE,
                                                         ccw.RECT_SIZE, int(ccw.RECT_SIZE*1.0)])

                elif field == Field.BLACK_FIELD_RED_QUEEN:
                    self._screen.blit(self._red_queen, [ccw.RECT_OFFSET_X + int(ccw.RECT_SIZE*1.0) * f_counter,
                                                        ccw.RECT_OFFSET_Y + r_counter*ccw.RECT_SIZE,
                                                        ccw.RECT_SIZE, int(ccw.RECT_SIZE*1.0)])

                f_counter = f_counter + 1
            r_counter = r_counter + 1

        # --- drawing frame on the window
        # img = np.rot90(self._img_print)
        img = cv2.flip(self._img_print, 1)
        img = np.rot90(img)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (500, 500))
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
        self._black_field = cv2.resize(ccw.BLACK_FIELD, (ccw.RECT_SIZE, int(ccw.RECT_SIZE*1.0)))
        self._black_field = cv2.rotate(self._black_field, 0)
        self._black_field = pg.surfarray.make_surface(self._black_field)
        self._white_field = cv2.resize(ccw.WHITE_FIELD, (ccw.RECT_SIZE, int(ccw.RECT_SIZE*1.0)))
        self._white_field = cv2.rotate(self._white_field, 0)
        self._white_field = pg.surfarray.make_surface(self._white_field)
        self._blue_pawn = cv2.resize(ccw.BLUE_PAWN, (ccw.RECT_SIZE, int(ccw.RECT_SIZE*1.0)))
        self._blue_pawn = cv2.rotate(self._blue_pawn, 0)
        self._blue_pawn = pg.surfarray.make_surface(self._blue_pawn)
        self._blue_queen = cv2.resize(ccw.BLUE_QUEEN, (ccw.RECT_SIZE, int(ccw.RECT_SIZE*1.0)))
        self._blue_queen = cv2.rotate(self._blue_queen, 0)
        self._blue_queen = pg.surfarray.make_surface(self._blue_queen)
        self._red_pawn = cv2.resize(ccw.RED_PAWN, (ccw.RECT_SIZE, int(ccw.RECT_SIZE*1.0)))
        self._red_pawn = cv2.rotate(self._red_pawn, 0)
        self._red_pawn = pg.surfarray.make_surface(self._red_pawn)
        self._red_queen = cv2.resize(ccw.RED_QUEEN, (ccw.RECT_SIZE, int(ccw.RECT_SIZE*1.0)))
        self._red_queen = cv2.rotate(self._red_queen, 0)
        self._red_queen = pg.surfarray.make_surface(self._red_queen)
        self._background = cv2.resize(ccw.BACKGROUND, ccw.SIZE)
        self._background = cv2.rotate(self._background, 2)
        self._background = pg.surfarray.make_surface(self._background)
        self._camera_window = cv2.resize(ccw.WINDOW_CAMERA, (540, 540))
        self._camera_window = cv2.rotate(self._camera_window, 2)
        self._camera_window = pg.surfarray.make_surface(self._camera_window)
        self._bottom_bar = cv2.resize(ccw.WINDOW_CAMERA, (ccw.SIZE[0], ccw.BAR_SIZE_Y))
        self._bottom_bar = cv2.rotate(self._bottom_bar, 2)
        self._bottom_bar = pg.surfarray.make_surface(self._bottom_bar)
        self._board_background = cv2.resize(ccw.WINDOW_CAMERA, (ccw.BOARD_SIZE, ccw.BOARD_SIZE))
        self._board_background = cv2.rotate(self._board_background, 2)
        self._board_background = pg.surfarray.make_surface(self._board_background)


    def load_url(self):
        try:
            with open("configs/url.txt", "r") as json_file:
                json_data = json.load(json_file)
                self._url = json_data["url"]
        except Exception as e:
            print(e)

    def run_winner_window(self, winner):
        WinnerWindow(winner).run()

    def main(self):
        t1 = threading.Thread(target=self.run_logic)
        t1.start()
        self.run()

