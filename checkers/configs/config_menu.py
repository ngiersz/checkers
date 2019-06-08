"""
CONFIG
Default Menu settings
"""
import cv2
MENU_SIZE = (1920, 1080)  # size of menu (w, h)
FONT = "Retro.ttf"
FPS = 30
TITLE_FONT = int(MENU_SIZE[0]/10)
OPTION_FONT = int(MENU_SIZE[0]/25)
SELECTED_FONT = int(MENU_SIZE[0]/35)
NORMAL_RECT = int(MENU_SIZE[0]/25)
SELECTED_RECT = int(MENU_SIZE[0]/35)
BACKGROUND = cv2.flip(cv2.rotate(cv2.resize(cv2.cvtColor(cv2.imread("images/menu_background.jpg"), 3), MENU_SIZE),2),0)
BUTTON = cv2.rotate(cv2.cvtColor(cv2.imread("images/button_menu.jpg"), 3), 2)
BUTTON2 = cv2.rotate(cv2.cvtColor(cv2.imread("images/button_menu2.jpg"), 3), 2)
BUTTON3 = cv2.rotate(cv2.cvtColor(cv2.imread("images/button_menu3.jpg"), 3), 2)
