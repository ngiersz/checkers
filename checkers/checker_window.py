import pygame
import pygame.gfxdraw
import cv2
import numpy as np
import checkers.checkers_detector as c_d
import checkers.configs.config_checkers_window as ccw
import checkers.configs.config_colors as ccc


class CheckersWindow:

    def __init__(self):
        self._camera = cv2.VideoCapture(0)
        self._tab = [[0, 1, 0, 1, 0, 1, 0, 1],
                     [1, 0, 1, 0, 1, 0, 1, 0],
                     [0, 1, 0, 1, 0, 1, 0, 1],
                     [1, 0, 1, 0, 1, 0, 1, 0],
                     [0, 1, 0, 1, 0, 1, 0, 1],
                     [1, 0, 1, 0, 1, 0, 1, 0],
                     [0, 1, 0, 1, 0, 1, 0, 1],
                     [1, 0, 1, 0, 1, 0, 1, 0]]
        self._screen = pygame.display.set_mode(ccw.SIZE, pygame.FULLSCREEN)
        self._done = False
        pygame.display.set_caption("checkers")
        self._black_field = ccc.BLACK
        self._white_field = ccc.WHITE
        self._white_pawn = ccc.WHITE
        self._black_pawn = ccc.BLACK

        self.init_textures()




    def draw_window(self):
        """
        Function with main loop for window with checkers board and view
        from the camera
        returns: True
        """

        # Used to manage how fast the screen updates
        clock = pygame.time.Clock()

        # -------- Main Program Loop -----------
        while not self._done:
            # --- Main event loop
            for event in pygame.event.get():

                if event.type == pygame.KEYDOWN:
                    self._done = True

                elif event.type == pygame.QUIT:
                    self._done = True

            # --- reading frame from camera
            ret, frame = self._camera.read()
            frame = cv2.resize(frame, (ccw.CAMERA_W, ccw.CAMERA_H))
            frame = cv2.cvtColor(frame, 3)

            # --- Game logic should go here

            # Calling for chessboard info
            img = c_d.find_chessboard(cv2.flip(frame,1))

            # Checking if the move was valid

            # --- Screen-clearing code goes here
            self._screen.fill(ccc.BEIGE)

            # Drawing chessboard
            r_counter = 0
            for row in self._tab:
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

                        # self._screen.blit(self._white_pawn, [ccw.RECT_OFFSET_X + (ccw.RECT_SIZE * f_counter),
                        #                                       ccw.RECT_OFFSET_Y + r_counter * ccw.RECT_SIZE,
                        #                                       ccw.RECT_SIZE, ccw.RECT_SIZE])

                        pygame.draw.ellipse(self._screen, ccc.WHITE, [ccw.PAWN_OFFSET_X + (ccw.RECT_SIZE * f_counter),
                                                                      ccw.PAWN_OFFSET_Y + r_counter * ccw.RECT_SIZE,
                                                                      ccw.PAWN_SIZE, ccw.PAWN_SIZE])
                    elif field == 3:
                        self._screen.blit(self._black_field, [ccw.RECT_OFFSET_X + (ccw.RECT_SIZE * f_counter),
                                                              ccw.RECT_OFFSET_Y + r_counter * ccw.RECT_SIZE,
                                                              ccw.RECT_SIZE, ccw.RECT_SIZE])

                        pygame.draw.ellipse(self._screen, ccc.BLACK, [ccw.PAWN_OFFSET_X + (ccw.RECT_SIZE * f_counter),
                                                                      ccw.PAWN_OFFSET_Y + r_counter * ccw.RECT_SIZE,
                                                                      ccw.PAWN_SIZE, ccw.PAWN_SIZE])
                    f_counter = f_counter+1
                r_counter = r_counter+1

            # --- drawing frame on the window
            img = np.rot90(img)
            img = pygame.surfarray.make_surface(img)
            self._screen.blit(img, (ccw.CAMERA_OFFSET_X, ccw.CAMERA_OFFSET_Y))

            # --- Drawing code should go here

            pygame.display.flip()
            pygame.display.update()

            # --- Limit to 60 frames per second
            clock.tick(60)

        # Close the window and quit.

    def init_textures(self):
        self._black_field = cv2.resize(ccw.BLACK_FIELD, (ccw.RECT_SIZE, ccw.RECT_SIZE))
        self._black_field = pygame.surfarray.make_surface(self._black_field)
        self._white_field = cv2.resize(ccw.WHITE_FIELD, (ccw.RECT_SIZE, ccw.RECT_SIZE))
        self._white_field = pygame.surfarray.make_surface(self._white_field)
        self._white_pawn = cv2.resize(ccw.WHITE_PAWN, (ccw.RECT_SIZE, ccw.RECT_SIZE))
        self._white_pawn = pygame.surfarray.make_surface(self._white_pawn)
        self._black_pawn = cv2.resize(ccw.BLACK_PAWN, (ccw.RECT_SIZE, ccw.RECT_SIZE))
        self._black_pawn = pygame.surfarray.make_surface(self._black_pawn)


    def main(self):
        self.draw_window()
