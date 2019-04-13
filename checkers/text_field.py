import pygame as pg
import checkers.configs.config_buttons as cb


class TextField(pg.sprite.Sprite):
    """
    Class that defines TextField
    TextField is a sprite subclass, you can update and  draw
    all sprites by calling 'group.update()' 'group.draw(screen)'
    """
    def __init__(self, x, y, width, height, text='',
                 font=cb.FONT, text_color=(0, 0, 0),
                 image_normal=cb.IMAGE_NORMAL):
        super().__init__()
        self.img_back = image_normal
        self.width = width
        self.height = height
        # Scale the images to the desired size (doesn't modify the originals).
        self.image_normal = pg.transform.scale(self.img_back, (self.width,  self.height))

        self.image = self.image_normal  # The currently active image.
        self.rect = self.image.get_rect(topleft=(x, y))
        # To center the text rect.
        self.image_center = self.image.get_rect().center
        self.text_color = text_color
        self.font = font
        self.text_surf = self.font.render(text, True, self.text_color)
        self.set_text(text)

        # This function will be called when the button gets pressed.

    def set_text(self, text):
        self.image_normal = pg.transform.scale(self.img_back, (self.width,  self.height))
        self.image = self.image_normal  # The currently active image.
        self.image_center = self.image.get_rect().center
        self.text_surf = self.font.render(text, True, self.text_color)
        text_rect = self.text_surf.get_rect(center=self.image_center)
        self.image_normal.blit(self.text_surf, text_rect)

    def handle_event(self, event, is_active):
        is_active = False






