import msvcrt
import pygame
from pygame.locals import *
import cv2
import numpy as np
import sys
import checkers.checkers_detector as c_d

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BROWN = (66, 38, 17)
BEIGE = (255, 255, 180)

SIZE = (1920, 1080)
# SIZE = (500, 400)
RECT_SIZE = SIZE[0]/20
CHECKER_SIZE = SIZE[0]/30

RECT_OFFSET_X = SIZE[0]/2
RECT_OFFSET_Y = SIZE[0]/30

CAMERA_H = int(SIZE[1]/2)
CAMERA_W = int(SIZE[0]/2.5)

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
        screen = pygame.display.set_mode(SIZE, pygame.FULLSCREEN)
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

                if event.type == pygame.KEYUP:
                    done = True

                elif event.type == pygame.QUIT:
                    done = True
            # --- camera
            ret, frame = camera.read()
            frame = cv2.resize(frame, (CAMERA_W, CAMERA_H))
            frame = cv2.cvtColor(frame, 3)
            #frame = np.rot90(frame)
            #frame = pygame.surfarray.make_surface(frame)

            # --- Game logic should go here

            # Calling for chessboard info

            img = c_d.findCheesboard(frame)
            # Checking if the move was valid

            # --- Screen-clearing code goes here

            # Here, we clear the screen to white. Don't put other drawing commands
            # above this, or they will be erased with this command.

            # If you want a background image, replace this clear with blit'ing the
            # background image.

            screen.fill(BEIGE)

            # Drawing chessboard
            p = 0

            for i in tab:
                r = 0
                for j in i:
                    if j == 0:
                        # pygame.Surface.blit(black_img, screen, [RECT_OFFSET_X + (RECT_SIZE * r), RECT_OFFSET_Y + p * RECT_SIZE, RECT_SIZE, RECT_SIZE])
                        pygame.draw.rect(screen, BROWN, [RECT_OFFSET_X + (RECT_SIZE * r), RECT_OFFSET_Y + p * RECT_SIZE, RECT_SIZE, RECT_SIZE])
                    elif j == 1:
                        # pygame.Surface.blit(white_img, screen, [RECT_OFFSET_X + (RECT_SIZE * r), RECT_OFFSET_Y + p * RECT_SIZE, RECT_SIZE, RECT_SIZE])
                        pygame.draw.rect(screen, WHITE, [RECT_OFFSET_X + (RECT_SIZE * r), RECT_OFFSET_Y + p * RECT_SIZE, RECT_SIZE, RECT_SIZE])
                    elif j == 2:
                        pygame.draw.rect(screen, BROWN, [RECT_OFFSET_X + (RECT_SIZE * r), RECT_OFFSET_Y + p * RECT_SIZE, RECT_SIZE, RECT_SIZE])
                        pygame.draw.ellipse(screen, WHITE, [CHECKER_OFFSET_X + (RECT_SIZE * r), CHECKER_OFFSET_Y + p * RECT_SIZE, CHECKER_SIZE, CHECKER_SIZE])
                    elif j == 3:
                        pygame.draw.rect(screen,BROWN , [RECT_OFFSET_X + (RECT_SIZE * r), RECT_OFFSET_Y + p * RECT_SIZE, RECT_SIZE, RECT_SIZE])
                        pygame.draw.ellipse(screen, BLACK, [CHECKER_OFFSET_X + (RECT_SIZE * r), CHECKER_OFFSET_Y + p * RECT_SIZE, CHECKER_SIZE, CHECKER_SIZE])
                    r = r+1
                p = p+1
            img = np.rot90(img)
            img = pygame.surfarray.make_surface(img)
            screen.blit(img, (SIZE[0]/30, SIZE[1]/30))
            pygame.display.update()
            # --- Drawing code should go here

            # --- Go ahead and update the screen with what we've drawn.
            pygame.display.flip()

            # --- Limit to 60 frames per second
            clock.tick(60)

        # Close the window and quit.
        pygame.quit()


if __name__ == '__main__':
    Window.draw_window()
