import pygame.ftfont
from checkers.Field import Field


def text_format(message, text_font, text_size, text_color):
    new_font = pygame.font.Font(text_font, text_size)
    new_text = new_font.render(message, 0, text_color)
    return new_text


def enum_to_int_game(game):
    int_game = []
    temp_states = []
    for state in game:
        temp_rows = []
        for row in state:
            temp_fields = []
            for field in row:
                temp_fields.append(field.value)

            temp_rows.append(temp_fields)
        temp_states.append(temp_rows)
    int_game = temp_states
    return int_game

def int_to_enum_game(game):
    enum_game = []
    temp_states = []
    for state in game:
        temp_rows = []
        for row in state:
            temp_fields = []
            for field in row:
                temp_fields.append(Field(field))
            temp_rows.append(temp_fields)
        temp_states.append(temp_rows)
    enum_game = temp_states
    return enum_game

