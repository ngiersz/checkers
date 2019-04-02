import pygame
import cv2
import numpy as np
import checkers.checkers_detector as c_d
import checkers.configs.config_checkers_window as ccw
import checkers.configs.config_colors as ccc


class CheckersWindow:

    def __init__(self):
        #pygame.init()
        self._camera = cv2.VideoCapture(0)
        self._tab = [[3, 1, 3, 1, 3, 1, 3, 1],
                     [1, 3, 1, 3, 1, 3, 1, 3],
                     [3, 1, 3, 1, 3, 1, 3, 1],
                     [1, 0, 1, 0, 1, 0, 1, 0],
                     [0, 1, 0, 1, 0, 1, 0, 1],
                     [1, 2, 1, 2, 1, 2, 1, 2],
                     [2, 1, 2, 1, 2, 1, 2, 1],
                     [1, 2, 1, 2, 1, 2, 1, 2]]
        self._screen = pygame.display.set_mode(ccw.SIZE, pygame.FULLSCREEN)
        self._done = False
        pygame.display.set_caption("checkers")

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
            img = c_d.find_chessboard(frame)

            # Checking if the move was valid

            # --- Screen-clearing code goes here
            self._screen.fill(ccc.BEIGE)

            # Drawing chessboard
            r_counter = 0
            for row in self._tab:
                f_counter = 0
                for field in row:
                    if field == 0:
                        pygame.draw.rect(self._screen, ccc.BROWN, [ccw.RECT_OFFSET_X + (ccw.RECT_SIZE * f_counter),
                                                                   ccw.RECT_OFFSET_Y + r_counter * ccw.RECT_SIZE,
                                                                   ccw.RECT_SIZE, ccw.RECT_SIZE])
                    elif field == 1:
                        pygame.draw.rect(self._screen, ccc.WHITE, [ccw.RECT_OFFSET_X + (ccw.RECT_SIZE * f_counter),
                                                                   ccw.RECT_OFFSET_Y + r_counter * ccw.RECT_SIZE,
                                                                   ccw.RECT_SIZE, ccw.RECT_SIZE])
                    elif field == 2:
                        pygame.draw.rect(self._screen, ccc.BROWN, [ccw.RECT_OFFSET_X + (ccw.RECT_SIZE * f_counter),
                                                                   ccw.RECT_OFFSET_Y + r_counter * ccw.RECT_SIZE,
                                                                   ccw.RECT_SIZE, ccw.RECT_SIZE])

                        pygame.draw.ellipse(self._screen, ccc.WHITE, [ccw.CHECKER_OFFSET_X + (ccw.RECT_SIZE * f_counter),
                                                                      ccw.CHECKER_OFFSET_Y + r_counter * ccw.RECT_SIZE,
                                                                      ccw.CHECKER_SIZE, ccw.CHECKER_SIZE])
                    elif field == 3:
                        pygame.draw.rect(self._screen, ccc.BROWN, [ccw.RECT_OFFSET_X + (ccw.RECT_SIZE * f_counter),
                                                                   ccw.RECT_OFFSET_Y + r_counter * ccw.RECT_SIZE,
                                                                   ccw.RECT_SIZE, ccw.RECT_SIZE])

                        pygame.draw.ellipse(self._screen, ccc.BLACK, [ccw.CHECKER_OFFSET_X + (ccw.RECT_SIZE * f_counter),
                                                                      ccw.CHECKER_OFFSET_Y + r_counter * ccw.RECT_SIZE,
                                                                      ccw.CHECKER_SIZE, ccw.CHECKER_SIZE])
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
        #pygame.quit()

    def main(self):
        self.draw_window()
