import pygame
from pygame import mixer
import tkinter
import os
from sys import exit
import ctypes
import pywinauto
import pyautogui

class Button():
    def __init__(self, name, img, x, y, font):
        self.name = name
        self.img = img
        self.x = x
        self.y = y
        self.font = font
        self.rect = self.img.get_rect(center=(self.x, self.y))
        self.txt = font.render(self.name, True, 'gray')
        self.txt_rect = self.txt.get_rect(center=(self.x, self.y))
    
    def update(self, screen):
        screen.blit(self.img, self.rect)
        screen.blit(self.txt, self.txt_rect)

    def check_for_input(self, pos):
        if pos[0] in range(self.rect.left, self.rect.right) and pos[1] in range(self.rect.top, self.rect.bottom):
            return 1
        
    def change_color(self, pos, font):
        if pos[0] in range(self.rect.left, self.rect.right) and pos[1] in range(self.rect.top, self.rect.bottom):
            self.txt = font.render(self.name, True, 'white')
            self.img = pygame.image.load('img_files/ui_button_selected.png')
        else:
            self.txt = font.render(self.name, True, 'gray')
            self.img = pygame.image.load('img_files/ui_button.png')


def activate_window(title):
    app = pywinauto.Application().connect(title_re=title)
    app.top_window().set_focus()

def get_display_size():
    root = tkinter.Tk()
    root.update_idletasks()
    root.attributes('-fullscreen', True)
    root.state('iconic')
    height = root.winfo_screenheight()
    width = root.winfo_screenwidth()
    root.destroy()
    return width, height

def main_menu(res, screen):
    clock = pygame.time.Clock()
    font_main = pygame.font.SysFont('cambria', 50)

    cursor_img = pygame.image.load('img_files/ui_cursor.png')
    cursor = pygame.cursors.Cursor((0,0), cursor_img)
    pygame.mouse.set_cursor(cursor)

    mixer.music.load("music/claire_de_lune.mp3")
    mixer.music.play(-1)

    bg_img = pygame.image.load(f"img_files/ui_main_menu.png")
    bg_scaled = pygame.transform.scale(bg_img, res)
    screen.blit(bg_scaled, (0,0))

    button_surf = pygame.image.load('img_files/ui_button.png')
    button_start = Button('START', button_surf, res[0]/2, res[1]*.45, font_main)
    button_settings = Button('SETTINGS', button_surf, res[0]/2, res[1]*.65, font_main)
    button_close = Button('CLOSE', button_surf, res[0]/2, res[1]*.85, font_main)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_close.check_for_input(pygame.mouse.get_pos()):
                    pygame.quit()
                    exit()
                if button_settings.check_for_input(pygame.mouse.get_pos()):
                    mixer.music.stop()
                    settings_menu(res, screen)
        button_start.update(screen)
        button_settings.update(screen)
        button_close.update(screen)
        button_start.change_color(pygame.mouse.get_pos(), font_main)
        button_settings.change_color(pygame.mouse.get_pos(), font_main)
        button_close.change_color(pygame.mouse.get_pos(), font_main)
        pygame.display.update()
        clock.tick(60)

def settings_menu(res, screen):
    screen.fill('black')
    clock = pygame.time.Clock()
    font_main = pygame.font.SysFont('cambria', 50)

    button_surf = pygame.image.load('img_files/ui_button.png')
    button_return = Button('RETURN', button_surf, res[0]/2, res[1]*.85, font_main)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_return:
                    main_menu(res, screen)
        button_return.update(screen)
        button_return.change_color(pygame.mouse.get_pos(), font_main)
        pygame.display.update()
        clock.tick(60)

def main():
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.init()
    pygame.font.init()
    ctypes.windll.user32.SetProcessDPIAware()


    x, y = get_display_size()
    res = (x, y)
    print(f"Resolution = {res}!")

    pygame.mouse.set_visible(True)

    screen = pygame.display.set_mode(res, pygame.FULLSCREEN)
    pygame.display.set_caption('Dress Up RPG')
    activate_window("Dress Up RPG")

    pyautogui.moveTo((res[0]/2, res[1]/2))

    main_menu(res, screen)

if __name__ == "__main__":
    main()