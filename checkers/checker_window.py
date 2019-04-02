import pygame
import cv2
import numpy as np
import checkers.checkers_detector as c_d


class CheckersWindow:
    # -- colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    BROWN = (66, 38, 17)
    BEIGE = (255, 255, 180)
    # -- sizes
    SIZE = (1920, 1080)
    RECT_SIZE = SIZE[0] / 20
    CHECKER_SIZE = SIZE[0] / 30
    CAMERA_H = int(SIZE[1] / 2)
    CAMERA_W = int(SIZE[0] / 2.5)
    # -- offsets
    RECT_OFFSET_X = SIZE[0] / 2
    RECT_OFFSET_Y = SIZE[0] / 30
    CHECKER_OFFSET_X = RECT_OFFSET_X + (RECT_SIZE - CHECKER_SIZE) / 2
    CHECKER_OFFSET_Y = RECT_OFFSET_Y + (RECT_SIZE - CHECKER_SIZE) / 2

    def __init__(self):
        pygame.init()
        self.camera = cv2.VideoCapture(0)
        self.tab = [[3, 1, 3, 1, 3, 1, 3, 1],
                    [1, 3, 1, 3, 1, 3, 1, 3],
                    [3, 1, 3, 1, 3, 1, 3, 1],
                    [1, 0, 1, 0, 1, 0, 1, 0],
                    [0, 1, 0, 1, 0, 1, 0, 1],
                    [1, 2, 1, 2, 1, 2, 1, 2],
                    [2, 1, 2, 1, 2, 1, 2, 1],
                    [1, 2, 1, 2, 1, 2, 1, 2]]

    def draw_window(self):
        """
        Function with main loop for window with checkers board and view
        from the camera
        returns:
        """
        pygame.display.set_caption("OpenCV camera stream on Pygame")

        # Set the width and height of the screen [width, height]
        screen = pygame.display.set_mode(self.SIZE, pygame.FULLSCREEN)
        pygame.display.set_caption("checkers")

        # Loop until the user clicks the close button.
        done = False

        # Used to manage how fast the screen updates
        clock = pygame.time.Clock()

        # -------- Main Program Loop -----------
        while not done:
            # --- Main event loop
            for event in pygame.event.get():

                if event.type == pygame.KEYUP:
                    done = True

                elif event.type == pygame.QUIT:
                    done = True

            # --- reading frame from camera
            ret, frame = self.camera.read()
            frame = cv2.resize(frame, (self.CAMERA_W, self.CAMERA_H))
            frame = cv2.cvtColor(frame, 3)

            # --- Game logic should go here

            # Calling for chessboard info
            img = c_d.find_chessboard(frame)

            # Checking if the move was valid

            # --- Screen-clearing code goes here
            screen.fill(self.BEIGE)

            # Drawing chessboard
            r_counter = 0
            for row in self.tab:
                f_counter = 0
                for field in row:
                    if field == 0:
                        pygame.draw.rect(screen, self.BROWN, [self.RECT_OFFSET_X + (self.RECT_SIZE * f_counter),
                                                              self.RECT_OFFSET_Y + r_counter * self.RECT_SIZE,
                                                              self.RECT_SIZE, self.RECT_SIZE])
                    elif field == 1:
                        pygame.draw.rect(screen, self.WHITE, [self.RECT_OFFSET_X + (self.RECT_SIZE * f_counter),
                                                              self.RECT_OFFSET_Y + r_counter * self.RECT_SIZE,
                                                              self.RECT_SIZE, self.RECT_SIZE])
                    elif field == 2:
                        pygame.draw.rect(screen, self.BROWN, [self.RECT_OFFSET_X + (self.RECT_SIZE * f_counter),
                                                              self.RECT_OFFSET_Y + r_counter * self.RECT_SIZE,
                                                              self.RECT_SIZE, self.RECT_SIZE])

                        pygame.draw.ellipse(screen, self.WHITE, [self.CHECKER_OFFSET_X + (self.RECT_SIZE * f_counter),
                                                                 self.CHECKER_OFFSET_Y + r_counter * self.RECT_SIZE,
                                                                 self.CHECKER_SIZE, self.CHECKER_SIZE])
                    elif field == 3:
                        pygame.draw.rect(screen, self.BROWN, [self.RECT_OFFSET_X + (self.RECT_SIZE * f_counter),
                                                              self.RECT_OFFSET_Y + r_counter * self.RECT_SIZE,
                                                              self.RECT_SIZE, self.RECT_SIZE])

                        pygame.draw.ellipse(screen, self.BLACK, [self.CHECKER_OFFSET_X + (self.RECT_SIZE * f_counter),
                                                                 self.CHECKER_OFFSET_Y + r_counter * self.RECT_SIZE,
                                                                 self.CHECKER_SIZE, self.CHECKER_SIZE])
                    f_counter = f_counter+1
                r_counter = r_counter+1

            # --- drawing frame on the window
            img = np.rot90(img)
            img = pygame.surfarray.make_surface(img)
            screen.blit(img, (self.SIZE[0]/30, self.SIZE[1]/30))

            # --- Drawing code should go here

            pygame.display.flip()
            pygame.display.update()

            # --- Limit to 60 frames per second
            clock.tick(60)

        # Close the window and quit.
        pygame.quit()

    def main(self):
        self.draw_window()
