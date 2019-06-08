import pygame as pg
import os
import cv2
import glob
import json
import checkers.configs.config_archive_window as caw
import checkers.configs.config_colors as ccc
import checkers.utils as utils
from checkers.Field import Field
from checkers.text_field import TextField
from checkers.button import Button


class ArchiveWindow:
    """
    Class that lets user re watch his game play
    """

    def __init__(self):
        self._files = []
        self._game = []
        self._state = [[0, 1, 0, 1, 0, 1, 0, 1],
                       [1, 0, 1, 0, 1, 0, 1, 0],
                       [0, 1, 0, 1, 0, 1, 0, 1],
                       [1, 0, 1, 0, 1, 0, 1, 0],
                       [0, 1, 0, 1, 0, 1, 0, 1],
                       [1, 0, 1, 0, 1, 0, 1, 0],
                       [0, 1, 0, 1, 0, 1, 0, 1],
                       [1, 0, 1, 0, 1, 0, 1, 0]]

        self.no_games_saved = caw.NO_GAMES
        self._done = False
        self._clock = pg.time.Clock()
        self._dt = self._clock.tick(30) / 1000
        self._all_sprites = pg.sprite.Group()

        self.moves_counter = 0
        self.moves_number = 0
        self.games_counter = 0
        self.games_number = 0

        self._screen = pg.display.set_mode(caw.SIZE, pg.FULLSCREEN)

        self._black_field = ccc.BLACK
        self._white_field = ccc.WHITE
        self._white_pawn = ccc.WHITE
        self._black_pawn = ccc.BLACK

        self._blue_pawn = ccc.BLUE
        self._red_pawn = ccc.RED
        self._blue_queen = ccc.BLUE
        self._red_queen = ccc.RED

        self._background = ccc.BEIGE
        self._board_background = ccc.BEIGE
        self._bottom_bar = ccc.BEIGE
        self._side_bar = ccc.BEIGE

        self.button_normal = ccc.BEIGE
        self.button_hover = ccc.BEIGE
        self.button_down = ccc.BEIGE

        self._clock = pg.time.Clock()
        self.init_textures()

        self.selected_game_info = TextField(caw.SELECT_GAME_OFFSET_X_T, caw.SELECT_GAME_OFFSET_Y,
                                            caw.SELECT_GAME_WIDTH_TEXT, caw.SELECT_GAME_HEIGHT_TEXT, self.no_games_saved,
                                            caw.FONT_TEXT, (0, 0, 255), self.button_normal)

        self.selected_game_up = Button(caw.SELECT_GAME_OFFSET_X_B,(caw.SELECT_GAME_OFFSET_Y-2*caw.SELECT_GAME_HEIGHT_B),
                                       caw.SELECT_GAME_WIDTH_B, caw.SELECT_GAME_HEIGHT_B, self.game_up, caw.FONT, "NEXT",
                                       (255, 0, 0), self.button_normal, self.button_hover,self.button_down)

        self.selected_game_down = Button(caw.SELECT_GAME_OFFSET_X_B, (caw.SELECT_GAME_OFFSET_Y+2*caw.SELECT_GAME_HEIGHT_B),
                                         caw.SELECT_GAME_WIDTH_B, caw.SELECT_GAME_HEIGHT_B, self.game_down, caw.FONT,
                                         "PREVIOUS", (255, 0, 0), self.button_normal, self.button_hover, self.button_down)

        self.selected_move_info = TextField(caw.SELECT_MOVE_OFFSET_X, caw.SELECT_MOVE_OFFSET_Y,
                                            caw.SELECT_MOVE_WIDTH, caw.SELECT_MOVE_HEIGHT, "MOVE X", caw.FONT_TEXT,
                                            (0, 0, 255), self.button_normal)

        self.selected_move_left = Button(caw.SELECT_MOVE_OFFSET_X - 2 * caw.SELECT_MOVE_WIDTH,
                                         caw.SELECT_MOVE_OFFSET_Y,
                                         caw.SELECT_MOVE_WIDTH, caw.SELECT_MOVE_HEIGHT, self.move_left, caw.FONT,
                                         "LEFT", (255, 0, 0), self.button_normal, self.button_hover,self.button_down)

        self.selected_move_right = Button(caw.SELECT_MOVE_OFFSET_X + 2 * caw.SELECT_MOVE_WIDTH,
                                          caw.SELECT_MOVE_OFFSET_Y,
                                          caw.SELECT_MOVE_WIDTH, caw.SELECT_MOVE_HEIGHT, self.move_right, caw.FONT,
                                          "RIGHT", (255, 0, 0), self.button_normal, self.button_hover,self.button_down)

        self._all_sprites.add(self.selected_game_info, self.selected_game_up, self.selected_game_down,
                              self.selected_move_info, self.selected_move_right, self.selected_move_left)
        self.load_file_names()

    def run(self):
        """
        Main loop
        returns: True
        """
        while not self._done:
            self._dt = self._clock.tick(30) / 1000
            self.handle_events()
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
                    self._done = True
                    print("esc")
            elif event.type == pg.QUIT:
                self._done = True

            for button in self._all_sprites:
                button.handle_event(event, False)

    def run_logic(self):
        """
        Checking if move was correct and saving state of the game
        returns: True
        """

        self._clock.tick(60)

    def draw(self):
        """
        Function with main loop for window with checkers board and view
        from the camera
        returns: True
        """

        # self._screen.fill(ccc.BEIGE)
        self._screen.blit(self._background, [0, 0, caw.SIZE[0], caw.SIZE[1]])
        self._screen.blit(self._board_background, [caw.RECT_OFFSET_X - caw.RECT_SIZE/2,
                                                   caw.RECT_OFFSET_Y - caw.RECT_SIZE/2, caw.BOARD_SIZE, caw.BOARD_SIZE])
        self._screen.blit(self._side_bar, (caw.SELECT_GAME_OFFSET_X_T-20, caw.SELECT_GAME_OFFSET_Y-2*caw.SELECT_GAME_HEIGHT_B - 20))

        self._screen.blit(self._bottom_bar, (caw.SELECT_MOVE_OFFSET_X - 2 * caw.SELECT_MOVE_WIDTH - 20, caw.SELECT_MOVE_OFFSET_Y - 20))
        # Drawing chessboard
        r_counter = 0
        for row in self._state:
            f_counter = 0
            for field in row:
                if field == Field.BLACK:
                    self._screen.blit(self._black_field, [caw.RECT_OFFSET_X + int(caw.RECT_SIZE*1.0) * f_counter,
                                                          caw.RECT_OFFSET_Y + r_counter*caw.RECT_SIZE,
                                                          caw.RECT_SIZE, int(caw.RECT_SIZE*1.0)])
                elif field == Field.WHITE:
                    self._screen.blit(self._white_field, [caw.RECT_OFFSET_X + int(caw.RECT_SIZE*1.0) * f_counter,
                                                          caw.RECT_OFFSET_Y + r_counter*caw.RECT_SIZE,
                                                          caw.RECT_SIZE, int(caw.RECT_SIZE*1.0)])
                elif field == Field.BLACK_FIELD_BLUE_PAWN:
                    self._screen.blit(self._blue_pawn, [caw.RECT_OFFSET_X + int(caw.RECT_SIZE*1.0) * f_counter,
                                                        caw.RECT_OFFSET_Y + r_counter*caw.RECT_SIZE,
                                                        caw.RECT_SIZE, int(caw.RECT_SIZE*1.0)])

                elif field == Field.BLACK_FIELD_RED_PAWN:
                    self._screen.blit(self._red_pawn, [caw.RECT_OFFSET_X + int(caw.RECT_SIZE*1.0) * f_counter,
                                                       caw.RECT_OFFSET_Y + r_counter*caw.RECT_SIZE,
                                                       caw.RECT_SIZE, int(caw.RECT_SIZE*1.0)])

                elif field == Field.BLACK_FIELD_BLUE_QUEEN:
                    self._screen.blit(self._blue_queen, [caw.RECT_OFFSET_X + int(caw.RECT_SIZE*1.0) * f_counter,
                                                         caw.RECT_OFFSET_Y + r_counter*caw.RECT_SIZE,
                                                         caw.RECT_SIZE, int(caw.RECT_SIZE*1.0)])

                elif field == Field.BLACK_FIELD_RED_QUEEN:
                    self._screen.blit(self._red_queen, [caw.RECT_OFFSET_X + int(caw.RECT_SIZE*1.0) * f_counter,
                                                        caw.RECT_OFFSET_Y + r_counter*caw.RECT_SIZE,
                                                        caw.RECT_SIZE, int(caw.RECT_SIZE*1.0)])
                f_counter = f_counter + 1
            r_counter = r_counter + 1

        self._all_sprites.draw(self._screen)

        pg.display.flip()
        pg.display.update()

        # --- Limit to 60 frames per second
        self._clock.tick(60)

        # Close the window and quit.

    def load_file_names(self):
        self._files = []
        for file in glob.glob("games_archive/*"):
            self._files.append(file)
        if len(self._files) == 0:
            self._files.append(self.no_games_saved)
        else:
            self.games_number = len(self._files)
            self.games_counter = 0
            self.load_game(self._files[self.games_counter])
            self.change_state()

    def load_game(self, file_name):
        with open(file_name) as infile:
            j_tab2 = json.load(infile)
        self.selected_game_info.set_text(os.path.basename(file_name))
        j_tab2_dump = json.dumps(j_tab2)
        game = json.loads(j_tab2_dump)
        self._game = utils.int_to_enum_game(game)
        self.moves_number = len(self._game)

    def change_state(self):
        self.selected_move_info.set_text("{} of {}".format(self.moves_counter+1, self.moves_number))
        self._state = self._game[self.moves_counter]

    def game_up(self):
        if self._files[0] != self.no_games_saved:
            if self.games_number != 1:
                if self.games_counter == 0:
                    self.games_counter = self.games_number - 1
                else:
                    self.games_counter -= 1
                self.load_game(self._files[self.games_counter])
                self.moves_counter = 0
                self.change_state()
        print("game up")
        print(self.games_counter)

    def game_down(self):
        if self._files[0] != self.no_games_saved:
            if self.games_number != 1:
                if self.games_counter == (self.games_number - 1):
                    self.games_counter = 0
                else:
                    self.games_counter += 1
                self.load_game(self._files[self.games_counter])
                self.moves_counter = 0
                self.change_state()
        print("game down")
        print(self.games_counter)

    def move_left(self):
        if self._files[0] != self.no_games_saved:
            if self.moves_number != 0:
                if self.moves_counter == 0:
                    self.moves_counter = self.moves_number - 1
                else:
                    self.moves_counter -= 1
                self.change_state()
        print("move left")
        print(self.moves_counter)

    def move_right(self):
        if self._files[0] != self.no_games_saved:
            if self.moves_number != 0:
                if self.moves_counter == (self.moves_number - 1):
                    self.moves_counter = 0
                else:
                    self.moves_counter += 1
                self.change_state()
        print("move right")
        print(self.moves_counter)

    def init_textures(self):
        self._black_field = cv2.resize(caw.BLACK_FIELD, (caw.RECT_SIZE, caw.RECT_SIZE))
        self._black_field = pg.surfarray.make_surface(self._black_field)
        self._white_field = cv2.resize(caw.WHITE_FIELD, (caw.RECT_SIZE, caw.RECT_SIZE))
        self._white_field = pg.surfarray.make_surface(self._white_field)
        self._blue_pawn = cv2.resize(caw.BLUE_PAWN, (caw.RECT_SIZE, int(caw.RECT_SIZE * 1.0)))
        self._blue_pawn = cv2.rotate(self._blue_pawn, 0)
        self._blue_pawn = pg.surfarray.make_surface(self._blue_pawn)
        self._blue_queen = cv2.resize(caw.BLUE_QUEEN, (caw.RECT_SIZE, int(caw.RECT_SIZE * 1.0)))
        self._blue_queen = cv2.rotate(self._blue_queen, 0)
        self._blue_queen = pg.surfarray.make_surface(self._blue_queen)
        self._red_pawn = cv2.resize(caw.RED_PAWN, (caw.RECT_SIZE, int(caw.RECT_SIZE * 1.0)))
        self._red_pawn = cv2.rotate(self._red_pawn, 0)
        self._red_pawn = pg.surfarray.make_surface(self._red_pawn)
        self._red_queen = cv2.resize(caw.RED_QUEEN, (caw.RECT_SIZE, int(caw.RECT_SIZE * 1.0)))
        self._red_queen = cv2.rotate(self._red_queen, 0)
        self._red_queen = pg.surfarray.make_surface(self._red_queen)
        self._background = cv2.resize(caw.BACKGROUND, caw.SIZE)
        self._background = cv2.rotate(self._background, 2)
        self._background = pg.surfarray.make_surface(self._background)
        self._board_background = cv2.resize(caw.WINDOW_BACKGROUND, (caw.BOARD_SIZE, caw.BOARD_SIZE))
        self._board_background = cv2.rotate(self._board_background, 2)
        self._board_background = pg.surfarray.make_surface(self._board_background)
        self._bottom_bar = cv2.resize(caw.WINDOW_BACKGROUND, (caw.SELECT_MOVE_WIDTH * 5 + 40, caw.SELECT_MOVE_HEIGHT + 40))
        self._bottom_bar = cv2.rotate(self._bottom_bar, 2)
        self._bottom_bar = pg.surfarray.make_surface(self._bottom_bar)
        self._side_bar = cv2.resize(caw.WINDOW_BACKGROUND, (caw.SELECT_GAME_WIDTH_TEXT + 40, 5 * caw.SELECT_GAME_HEIGHT_B + 40))
        self._side_bar = cv2.rotate(self._side_bar, 2)
        self._side_bar = pg.surfarray.make_surface(self._side_bar)
        self.button_normal = pg.surfarray.make_surface(caw.BUTTON)
        self.button_hover = pg.surfarray.make_surface(caw.BUTTON2)
        self.button_down = pg.surfarray.make_surface(caw.BUTTON3)

    def main(self):
        self.run()
