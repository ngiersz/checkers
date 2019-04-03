import os
import pygame
import checkers.configs.config_colors as ccc
from checkers.checker_window import CheckersWindow
import checkers.configs.config_menu as ccm
from checkers.utils import text_format


class MenuWindow:

    def __init__(self):
        pygame.init()
        os.environ['SDL_VIDEO_CENTERED'] = '1'  # Center the Game Application
        self._screen = pygame.display.set_mode(ccm.MENU_SIZE, pygame.FULLSCREEN)  # Game Resolution
        self._clock = pygame.time.Clock()  # Game Frame rate

    def main_menu(self):
        menu = True
        selected = "start"

        while menu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        selected = "start"
                    elif event.key == pygame.K_DOWN:
                        selected = "quit"
                    if event.key == pygame.K_RETURN:
                        if selected == "start":
                            print("Start")
                            CheckersWindow().main()
                        if selected == "quit":
                            pygame.quit()
                            quit()

            # Main Menu UI
            self._screen.fill(ccc.BLUE)

            title = text_format("Checkers", ccm.FONT, ccm.TITLE_FONT, ccc.YELLOW)
            if selected == "start":
                text_start = text_format("START", ccm.FONT, ccm.OPTION_FONT, ccc.WHITE)
            else:
                text_start = text_format("START", ccm.FONT, ccm.SELECTED_FONT, ccc.BLACK)
            if selected == "quit":
                text_quit = text_format("QUIT", ccm.FONT, ccm.OPTION_FONT, ccc.WHITE)
            else:
                text_quit = text_format("QUIT", ccm.FONT, ccm.SELECTED_FONT, ccc.BLACK)

            title_rect = title.get_rect()
            start_rect = text_start.get_rect()
            quit_rect = text_quit.get_rect()

            # Main Menu Text
            self._screen.blit(title, (ccm.MENU_SIZE[0] / 2 - (title_rect[2] / 2), ccm.MENU_SIZE[1] / 3))
            self._screen.blit(text_start, (ccm.MENU_SIZE[0] / 2 - (start_rect[2] / 2), ccm.MENU_SIZE[1] / 3 + 200))
            self._screen.blit(text_quit, (ccm.MENU_SIZE[0] / 2 - (quit_rect[2] / 2), ccm.MENU_SIZE[1] / 3 + 350))
            pygame.display.update()
            self._clock.tick(ccm.FPS)
            pygame.display.set_caption("Checkers Main Menu")


