import pygame
from pygame.locals import *
import cv2
import numpy as np
import sys

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BROWN = (66, 38, 17)
BEIGE = (255, 255, 180)

SIZE = (700, 500)
RECT_SIZE = 50
CHECKER_SIZE = 40

RECT_OFFSET_X = SIZE[1]/2
RECT_OFFSET_Y = 40

CHECKER_OFFSET_X = RECT_OFFSET_X + (RECT_SIZE - CHECKER_SIZE) / 2
CHECKER_OFFSET_Y = RECT_OFFSET_Y + (RECT_SIZE - CHECKER_SIZE) / 2


class Window:



    @staticmethod
    def draw_window():
        """
        Main function that draws window and calls for other functions
        """
        pygame.init()

        camera = cv2.VideoCapture(0)
        pygame.init()
        pygame.display.set_caption("OpenCV camera stream on Pygame")

        # Set the width and height of the screen [width, height]
        screen = pygame.display.set_mode(SIZE)

        pygame.display.set_caption("checkers")

        # Loop until the user clicks the close button.
        done = False
        tab = [[3, 1, 3, 1, 3, 1, 3, 1],
               [1, 3, 1, 3, 1, 3, 1, 3],
               [3, 1, 3, 1, 3, 1, 3, 1],
               [1, 0, 1, 0, 1, 0, 1, 0],
               [0, 1, 0, 1, 0, 1, 0, 1],
               [1, 2, 1, 2, 1, 2, 1, 2],
               [2, 1, 2, 1, 2, 1, 2, 1],
               [1, 2, 1, 2, 1, 2, 1, 2]]
        # Used to manage how fast the screen updates
        clock = pygame.time.Clock()
        
        # -------- Main Program Loop -----------
        while not done:

            # --- Main event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True

            # --- Game logic should go here

            # Calling for chessboard info

            # Checking if the move was valid

            # --- Screen-clearing code goes here

            # Here, we clear the screen to white. Don't put other drawing commands
            # above this, or they will be erased with this command.

            # If you want a background image, replace this clear with blit'ing the
            # background image.
            screen.fill(BEIGE)

            ret, frame = camera.read()
            frame = cv2.resize(frame, (200, 160))
            frame = cv2.cvtColor(frame, 3)
            frame = np.rot90(frame)
            frame = pygame.surfarray.make_surface(frame)

            # Drawing chessboard
            p = 0
            for i in tab:
                r = 0
                for j in i:
                    if j == 0:
                        #pygame.Surface.blit(black_img, screen, [RECT_OFFSET_X + (RECT_SIZE * r), RECT_OFFSET_Y + p * RECT_SIZE, RECT_SIZE, RECT_SIZE])
                        pygame.draw.rect(screen, BROWN, [RECT_OFFSET_X + (RECT_SIZE * r), RECT_OFFSET_Y + p * RECT_SIZE, RECT_SIZE, RECT_SIZE])
                    elif j == 1:
                        #pygame.Surface.blit(white_img, screen, [RECT_OFFSET_X + (RECT_SIZE * r), RECT_OFFSET_Y + p * RECT_SIZE, RECT_SIZE, RECT_SIZE])
                        pygame.draw.rect(screen, WHITE, [RECT_OFFSET_X + (RECT_SIZE * r), RECT_OFFSET_Y + p * RECT_SIZE, RECT_SIZE, RECT_SIZE])
                    elif j == 2:
                        pygame.draw.rect(screen, BROWN, [RECT_OFFSET_X + (RECT_SIZE * r), RECT_OFFSET_Y + p * RECT_SIZE, RECT_SIZE, RECT_SIZE])
                        pygame.draw.ellipse(screen, WHITE, [CHECKER_OFFSET_X + (RECT_SIZE * r), CHECKER_OFFSET_Y + p * RECT_SIZE, CHECKER_SIZE, CHECKER_SIZE])
                    elif j == 3:
                        pygame.draw.rect(screen,BROWN , [RECT_OFFSET_X + (RECT_SIZE * r), RECT_OFFSET_Y + p * RECT_SIZE, RECT_SIZE, RECT_SIZE])
                        pygame.draw.ellipse(screen, BLACK, [CHECKER_OFFSET_X + (RECT_SIZE * r), CHECKER_OFFSET_Y + p * RECT_SIZE, CHECKER_SIZE, CHECKER_SIZE])
                    r = r+1
                p = p+1

            screen.blit(frame, (20, 20))
            pygame.display.update()
            # --- Drawing code should go here

            # --- Go ahead and update the screen with what we've drawn.
            pygame.display.flip()

            # --- Limit to 60 frames per second
            clock.tick(30)

        # Close the window and quit.
        pygame.quit()


if __name__ == '__main__':
    Window.draw_window()
