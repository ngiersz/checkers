import pygame as pg
import os
import json
import checkers.configs.config_settings as ccs
import checkers.configs.config_colors as ccc
import checkers.configs.config_buttons as cb
from checkers.text_field import TextField

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

        self.button_normal = ccc.BEIGE
        self.button_hover = ccc.BEIGE
        self.button_down = ccc.BEIGE
        self._screen_background = ccc.BEIGE

        pg.display.set_caption("settings")

        self.init_textures()
        self.load_settings()

        self.camera_url = TextField(ccs.SETTING_SIZE[0] / 2 - ccs.NORMAL_RECT*10 / 2,  ccs.SETTING_SIZE[1]/3,
                                    ccs.NORMAL_RECT * 10, ccs.NORMAL_RECT, self._url, cb.FONT,  (255, 255, 255),
                                    self.button_normal)
        self.change_camera_ip = Button(
            ccs.SETTING_SIZE[0] / 2 - ccs.NORMAL_RECT*4 / 2,  ccs.SETTING_SIZE[1]/3+ccs.NORMAL_RECT*2,
            ccs.NORMAL_RECT*4, ccs.NORMAL_RECT, self.change_ip,
            cb.FONT, self._ip, (255, 255, 255), self.button_normal, self.button_hover, self.button_down)
        self.change_camera_port = Button(
            ccs.SETTING_SIZE[0] / 2 - ccs.NORMAL_RECT,  ccs.SETTING_SIZE[1]/3+ccs.NORMAL_RECT*4,
            ccs.NORMAL_RECT*2, ccs.NORMAL_RECT, self.change_port,
            cb.FONT, self._port, (255, 255, 255), self.button_normal, self.button_hover,self.button_down)
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
                        print(self.changing_ip)
                    elif event.key == pg.K_BACKSPACE:
                        self._ip = self._ip[:-1]
                    else:
                        self._ip += event.unicode
                        print(self._ip)
                    self.change_camera_ip.set_text(self._ip)
                    self.change_url()
                if self.changing_port:
                    if event.key == pg.K_RETURN:
                        self.changing_port = False
                        print(self.changing_port)
                    elif event.key == pg.K_BACKSPACE:
                        self._port = self._port[:-1]
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

        self._screen.blit(self._screen_background, [0, 0, ccs.SETTING_SIZE[0], ccs.SETTING_SIZE[1]])

        # self._screen.fill(ccc.BEIGE)

        self._all_sprites.draw(self._screen)

        # --- Drawing code should go here

        pg.display.flip()
        pg.display.update()

        # --- Limit to 60 frames per second
        self._clock.tick(60)

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
            self.changing_port = False
            print("loog TRUE")
            self._ip = ""

    def change_port(self):
        print("loog hello")
        if self.changing_port:
            self.changing_port = False
            print("loog FALSE")
        else:
            self.changing_port = True
            self.changing_ip = False
            print("loog TRUE")
            self._port = ""

    def load_settings(self):
        try:
            with open("configs/url.txt", "r") as json_file:
                json_data = json.load(json_file)
                self._url = json_data["url"]
                self._ip = json_data["ip"]
                self._port = json_data["port"]
        except Exception as e:
            print(e)

    def save_settings(self):
        try:
            with open("configs/url.txt", "w") as json_file:
                data = {"url": self._url, "ip": self._ip, "port": self._port}
                json.dump(data, json_file)

        except Exception as e:
            print(e)

    def init_textures(self):
        self._screen_background = pg.surfarray.make_surface(ccs.BACKGROUND)
        self.button_normal = pg.surfarray.make_surface(ccs.BUTTON)
        self.button_hover = pg.surfarray.make_surface(ccs.BUTTON2)
        self.button_down = pg.surfarray.make_surface(ccs.BUTTON3)

    def main(self):
        self.run()
        self.save_settings()
