import pygame as pg
import os
import cv2
import glob
import json
import checkers.configs.config_archive_window as caw
import checkers.configs.config_colors as ccc

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

        self._clock = pg.time.Clock()
        self.init_textures()

        self.selected_game_info = TextField(caw.SELECT_GAME_OFFSET_X_T, caw.SELECT_GAME_OFFSET_Y,
                                            caw.SELECT_GAME_WIDTH_TEXT, caw.SELECT_GAME_HEIGHT_TEXT, self.no_games_saved,
                                            caw.FONT_TEXT, (0, 0, 255))

        self.selected_game_up = Button(caw.SELECT_GAME_OFFSET_X_B,(caw.SELECT_GAME_OFFSET_Y-2*caw.SELECT_GAME_HEIGHT_B),
                                       caw.SELECT_GAME_WIDTH_B, caw.SELECT_GAME_HEIGHT_B, self.game_up, caw.FONT, "UP",
                                       (255, 0, 0))

        self.selected_game_down = Button(caw.SELECT_GAME_OFFSET_X_B, (caw.SELECT_GAME_OFFSET_Y+2*caw.SELECT_GAME_HEIGHT_B),
                                         caw.SELECT_GAME_WIDTH_B, caw.SELECT_GAME_HEIGHT_B, self.game_down, caw.FONT,
                                         "DOWN", (255, 0, 0))

        self.selected_move_info = TextField(caw.SELECT_MOVE_OFFSET_X, caw.SELECT_MOVE_OFFSET_Y,
                                            caw.SELECT_MOVE_WIDTH, caw.SELECT_MOVE_HEIGHT, "MOVE X", caw.FONT_TEXT,
                                            (0, 0, 255))

        self.selected_move_left = Button(caw.SELECT_MOVE_OFFSET_X - 2 * caw.SELECT_MOVE_WIDTH,
                                         caw.SELECT_MOVE_OFFSET_Y,
                                         caw.SELECT_MOVE_WIDTH, caw.SELECT_MOVE_HEIGHT, self.move_left, caw.FONT,
                                         "LEFT", (255, 0, 0))

        self.selected_move_right = Button(caw.SELECT_MOVE_OFFSET_X + 2 * caw.SELECT_MOVE_WIDTH,
                                          caw.SELECT_MOVE_OFFSET_Y,
                                          caw.SELECT_MOVE_WIDTH, caw.SELECT_MOVE_HEIGHT, self.move_right, caw.FONT,
                                          "RIGHT", (255, 0, 0))

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

        self._screen.fill(ccc.BEIGE)

        # Drawing chessboard
        r_counter = 0
        for row in self._state:
            f_counter = 0
            for field in row:
                if field == 0:
                    self._screen.blit(self._black_field, [caw.RECT_OFFSET_X + (caw.RECT_SIZE * f_counter),
                                                          caw.RECT_OFFSET_Y + r_counter * caw.RECT_SIZE,
                                                          caw.RECT_SIZE, caw.RECT_SIZE])
                elif field == 1:
                    self._screen.blit(self._white_field, [caw.RECT_OFFSET_X + (caw.RECT_SIZE * f_counter),
                                                          caw.RECT_OFFSET_Y + r_counter * caw.RECT_SIZE,
                                                          caw.RECT_SIZE, caw.RECT_SIZE])
                elif field == 2:
                    self._screen.blit(self._black_field, [caw.RECT_OFFSET_X + (caw.RECT_SIZE * f_counter),
                                                          caw.RECT_OFFSET_Y + r_counter * caw.RECT_SIZE,
                                                          caw.RECT_SIZE, caw.RECT_SIZE])

                    pg.draw.ellipse(self._screen, ccc.WHITE, [caw.PAWN_OFFSET_X + (caw.RECT_SIZE * f_counter),
                                                              caw.PAWN_OFFSET_Y + r_counter * caw.RECT_SIZE,
                                                              caw.PAWN_SIZE, caw.PAWN_SIZE])
                elif field == 3:
                    self._screen.blit(self._black_field, [caw.RECT_OFFSET_X + (caw.RECT_SIZE * f_counter),
                                                          caw.RECT_OFFSET_Y + r_counter * caw.RECT_SIZE,
                                                          caw.RECT_SIZE, caw.RECT_SIZE])

                    pg.draw.ellipse(self._screen, ccc.BLACK, [caw.PAWN_OFFSET_X + (caw.RECT_SIZE * f_counter),
                                                              caw.PAWN_OFFSET_Y + r_counter * caw.RECT_SIZE,
                                                              caw.PAWN_SIZE, caw.PAWN_SIZE])
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
        for file in glob.glob("games_archive/game*"):
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
        self._game = json.loads(j_tab2_dump)
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
        self._white_pawn = cv2.resize(caw.WHITE_PAWN, (caw.RECT_SIZE, caw.RECT_SIZE))
        self._white_pawn = pg.surfarray.make_surface(self._white_pawn)
        self._black_pawn = cv2.resize(caw.BLACK_PAWN, (caw.RECT_SIZE, caw.RECT_SIZE))
        self._black_pawn = pg.surfarray.make_surface(self._black_pawn)

    def main(self):
        self.run()
