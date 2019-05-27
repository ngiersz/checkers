import pygame as pg
import checkers.configs.config_settings as ccs
import checkers.configs.config_colors as ccc
import checkers.configs.config_buttons as cb

from checkers.button import Button


class SettingsWindow:
    """
    """

    def __init__(self):

        self._screen = pg.display.set_mode(ccs.SETTING_SIZE, pg.FULLSCREEN)
        self.changing_camera_url = False
        self._url = ccs.URL
        self._port = ccs.PORT
        self._ip = ccs.IP

        self.changing_ip = False
        self.changing_port = False
        self._clock = pg.time.Clock()
        self._done = False
        self._dt = self._clock.tick(30) / 1000
        self._all_sprites = pg.sprite.Group()

        pg.display.set_caption("settings")

        self.camera_url = Button(
            ccs.SETTING_SIZE[0] / 2 - ccs.NORMAL_RECT*10 / 2,  ccs.SETTING_SIZE[1]/3,
            ccs.NORMAL_RECT*10, ccs.NORMAL_RECT, self.change_url,
            cb.FONT, self._url, (255, 255, 255))
        self.change_camera_ip = Button(
            ccs.SETTING_SIZE[0] / 2 - ccs.NORMAL_RECT*4 / 2,  ccs.SETTING_SIZE[1]/3+ccs.NORMAL_RECT*2,
            ccs.NORMAL_RECT*4, ccs.NORMAL_RECT, self.change_ip,
            cb.FONT, self._ip, (255, 255, 255))
        self.change_camera_port = Button(
            ccs.SETTING_SIZE[0] / 2 - ccs.NORMAL_RECT,  ccs.SETTING_SIZE[1]/3+ccs.NORMAL_RECT*4,
            ccs.NORMAL_RECT*2, ccs.NORMAL_RECT, self.change_port,
            cb.FONT, self._port, (255, 255, 255))
        self._all_sprites.add(self.camera_url, self.change_camera_ip, self.change_camera_port)

    def run(self):
        """
        Main loop
        returns: True
        """
        while not self._done:
            self._dt = self._clock.tick(30) / 1000
            self.handle_events()
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
                    if self.changing_ip:
                        self.changing_ip = False
                        self._ip = ccs.IP
                    if self.changing_port:
                        self.changing_port = False
                        self._port = ccs.PORT
                    else:
                        self._done = True
                if self.changing_ip:
                    if event.key == pg.K_RETURN:
                        self.changing_ip = False
                    elif event.key == pg.K_BACKSPACE:
                        self._ip = self._ip[:-1]
                    else:
                        self._url += event.unicode
                        print(self._ip)
                    self.change_camera_ip.set_text(self._ip)
                    self.change_url()
                if self.changing_port:
                    if event.key == pg.K_RETURN:
                        self.changing_port = False
                    elif event.key == pg.K_BACKSPACE:
                        self._port = self._ip[:-1]
                    else:
                        self._port += event.unicode
                        print(self._port)
                    self.change_camera_port.set_text(self._port)
                    self.change_url()

            elif event.type == pg.QUIT:
                self._done = True
            for button in self._all_sprites:
                button.handle_event(event, False)

    def draw(self):
        """
        Function with main loop for window with checkers board and view
        from the camera
        returns: True
        """

        self._screen.fill(ccc.BEIGE)

        self._all_sprites.draw(self._screen)

        # --- Drawing code should go here

        pg.display.flip()
        pg.display.update()

        # --- Limit to 60 frames per second
        self._clock.tick(60)

        # Close the window and quit.
    def change_url(self):
        self._url = 'http://'+self._ip+':'+self._port+'/shot.jpg'
        self.camera_url.set_text(self._url)


    def change_ip(self):
        print("loog hello")
        if self.changing_ip:
            self.changing_ip = False
            print("loog FALSE")
        else:
            self.changing_ip = True
            print("loog TRUE")
            self._ip = ""

    def change_port(self):
        print("loog hello")
        if self.changing_port:
            self.changing_port = False
            print("loog FALSE")
        else:
            self.changing_port = True
            print("loog TRUE")
            self._port = ""

    def udpate_url(self):
        self.changing_port = True




    def main(self):
        self.run()

