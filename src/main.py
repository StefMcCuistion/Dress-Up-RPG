import pygame
from pygame import mixer
import tkinter
import os
from sys import exit
import ctypes
import pywinauto

class Button():
    def __init__(self, name, img, x, y, font):
        self.name = name
        self.img = img
        self.x = x
        self.y = y
        self.font = font
        self.rect = self.img.get_rect(center=(self.x, self.y))
        self.txt = font.render(self.name, True, 'light gray')
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
        else:
            self.txt = font.render(self.name, True, 'light gray')

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

def main_menu(res):
    screen = pygame.display.set_mode(res, pygame.FULLSCREEN)
    pygame.display.set_caption('Dress Up RPG')
    activate_window("Dress Up RPG")
    clock = pygame.time.Clock()
    font_main = pygame.font.SysFont('cambria', 50)

    bg_img = pygame.image.load(f"img_files/ui_main_menu.png")
    bg_scaled = pygame.transform.scale(bg_img, res)
    screen.fill('blue')
    screen.blit(bg_scaled, (0,0))

    button_surf = pygame.image.load('img_files/ui_button.png')
    button = Button('CLOSE', button_surf, 100, 100, font_main)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button.check_for_input(pygame.mouse.get_pos()):
                    pygame.quit()
                    exit()
        button.update(screen)
        button.change_color(pygame.mouse.get_pos(), font_main)
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

    main_menu(res)

if __name__ == "__main__":
    main()