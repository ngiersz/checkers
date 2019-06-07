import pygame as pg
import checkers.configs.config_buttons as cb


class Button(pg.sprite.Sprite):
    """
    Class that defines button and handle his actions
    Button is a sprite subclass, you can update and  draw
    all sprites by calling 'group.update()' 'group.draw(screen)'
    """
    def __init__(self, x, y, width, height, callback,
                 font=cb.FONT, text='', text_color=(0, 0, 0),
                 image_normal=cb.IMAGE_NORMAL, image_hover=cb.IMAGE_HOVER,
                 image_down=cb.IMAGE_DOWN):
        super().__init__()
        # Scale the images to the desired size (doesn't modify the originals).
        self.img_back_normal = image_normal.copy()
        self.img_back_hover = image_hover.copy()
        self.img_back_down = image_down.copy()

        self.width = width
        self.height = height
        self.font = font
        self.image_normal = pg.transform.scale(image_normal, (width, height))
        self.image_hover = pg.transform.scale(image_hover, (width, height))
        self.image_down = pg.transform.scale(image_down, (width, height))
        self.text_color = text_color

        self.image = self.image_normal  # The currently active image.
        self.rect = self.image.get_rect(topleft=(x, y))
        # To center the text rect.
        self.image_center = self.image.get_rect().center
        self.text_surf = font.render(text, True, text_color)
        self.text_rect = self.text_surf.get_rect(center=self.image_center)
        # Blit the text onto the images.
        self.images = [self.image_normal, self.image_hover, self.image_down]
        for image in self.images:
            image.blit(self.text_surf, self.text_rect)

        # This function will be called when the button gets pressed.
        self.callback = callback
        self.button_down = False

    def handle_event(self, event, is_active):
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.image = self.image_down
                self.button_down = True
        elif event.type == pg.MOUSEBUTTONUP:
            # If the rect collides with the mouse pos.
            if self.rect.collidepoint(event.pos) and self.button_down:
                self.callback()  # Call the function.
                self.image = self.image_hover
            self.button_down = False
        elif event.type == pg.MOUSEMOTION:
            collided = self.rect.collidepoint(event.pos)
            if is_active:
                self.image = self.image_hover
            elif collided and not self.button_down:
                self.image = self.image_hover
                return True
            elif not collided:
                self.image = self.image_normal
        if event.type == pg.KEYDOWN:
            if is_active:
                self.image = self.image_hover
            else:
                self.image = self.image_normal
            if event.key == pg.K_RETURN:
                if is_active:
                    self.image = self.image_down
                    self.button_down = True
        if event.type == pg.KEYUP:
            if self.button_down:
                self.callback()  # Call the function.
                self.image = self.image_hover
            self.button_down = False

    def set_text(self, text):
        self.image_normal = pg.transform.scale(self.img_back_normal, (self.width,  self.height))
        self.image_hover = pg.transform.scale(self.img_back_hover, (self.width,  self.height))
        self.image_down = pg.transform.scale(self.img_back_down, (self.width,  self.height))
        self.image = self.image_normal  # The currently active image.
        self.image_center = self.image.get_rect().center
        self.text_surf = self.font.render(text, True, self.text_color)
        text_rect = self.text_surf.get_rect(center=self.image_center)
        self.image_normal.blit(self.text_surf, text_rect)
        self.image_down.blit(self.text_surf, text_rect)
        self.image_hover.blit(self.text_surf, text_rect)




        # self.image_normal = pg.transform.scale(self.img_back_normal, (self.width,  self.height))
        # self.image = self.image_normal  # The currently active image.
        # self.image_center = self.image.get_rect().center
        # self.text_surf = self.font.render(text, True, self.text_color)
        # self.image_normal = pg.transform.scale(cb.IMAGE_NORMAL, (self.width, self.height))
        # self.image_hover = pg.transform.scale(cb.IMAGE_HOVER, (self.width, self.height))
        # self.image_down = pg.transform.scale(cb.IMAGE_DOWN, (self.width, self.height))
        # text_rect = self.text_surf.get_rect(center=self.image_center)
        # for image in self.images:
        #     image.blit(self.text_surf, text_rect)

