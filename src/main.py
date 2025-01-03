import pygame
from pygame import mixer
import tkinter
import os
from sys import exit
import ctypes
import pywinauto
import pyautogui

class Button():
    def __init__(self, name, x, y):
        self.name = name
        self.img = pygame.image.load('img_files/ui_button.png')
        self.x = x
        self.y = y
        self.font = pygame.font.SysFont('cambria', 50)
        self.rect = self.img.get_rect(center=(self.x, self.y))
        self.txt = self.font.render(self.name, True, 'gray')
        self.txt_rect = self.txt.get_rect(center=(self.x, self.y))
    
    def update(self, screen):
        screen.blit(self.img, self.rect)
        screen.blit(self.txt, self.txt_rect)

    def check_for_input(self, pos):
        if pos[0] in range(self.rect.left, self.rect.right) and pos[1] in range(self.rect.top, self.rect.bottom):
            return 1
        
    def change_color(self, pos):
        if pos[0] in range(self.rect.left, self.rect.right) and pos[1] in range(self.rect.top, self.rect.bottom):
            self.txt = self.font.render(self.name, True, 'white')
            self.img = pygame.image.load('img_files/ui_button_selected.png')
        else:
            self.txt = self.font.render(self.name, True, 'gray')
            self.img = pygame.image.load('img_files/ui_button.png')

class Cycle():
    def __init__(self, x, y, list, idx=0):
        self.img = pygame.image.load('img_files/ui_options.png')
        self.x = x
        self.y = y
        self.list = list
        self.idx = idx
        self.name = self.list[self.idx]
        self.font = pygame.font.SysFont('cambria', 50)
        self.rect = self.img.get_rect(center=(self.x, self.y))
        self.txt = self.font.render(self.name, True, 'gray')
        self.txt_rect = self.txt.get_rect(center=(self.x, self.y))
    
    def update(self, screen):
        screen.blit(self.img, self.rect)
        screen.blit(self.txt, self.txt_rect)

    def check_for_input(self, pos):
        if pos[0] in range(self.rect.left, self.rect.left+56) and pos[1] in range(self.rect.top, self.rect.bottom):
            return 1
        elif pos[0] in range(self.rect.right-56, self.rect.right) and pos[1] in range(self.rect.top, self.rect.bottom):
            return 2
        else:
            return 0
        
    def change_color(self, pos):
        if pos[0] in range(self.rect.left, self.rect.left+56) and pos[1] in range(self.rect.top, self.rect.bottom):
            self.img = pygame.image.load('img_files/ui_options_left.png')
        elif pos[0] in range(self.rect.right-56, self.rect.right) and pos[1] in range(self.rect.top, self.rect.bottom):
            self.img = pygame.image.load('img_files/ui_options_right.png')
        else:
            self.img = pygame.image.load('img_files/ui_options.png')
        self.txt = self.font.render(self.name, True, 'gray')

    def change_idx(self, dir):
        if dir == 0:
            if self.idx - 1 > -1:
                self.idx -= 1
            else: 
                self.idx = len(self.list)-1
            self.name = self.list[self.idx]
        if dir == 1:
            if self.idx + 1 > len(self.list)-1:
                self.idx = 0
            else:
                self.idx += 1
            self.name = self.list[self.idx]

class Protag():
    def __init__(self, name="protag", dir=1):
        self.name = name # name of the character protrayed in the sprite, displayed above dialogue box
        self.dir = dir # determines whether sprite faces left or right, 1 = right, 0 = left

    def draw(self, screen, skin, hair, race):
        """
        Draws character sprite on screen. 

        :param screen: The 'screen' surface that other surfaces are blitted onto. 
        :type screen: Surface

        :return: None. 
        :rtype: None. 
        """
        surf = pygame.image.load(f"img_files/spr_protag_bottom_{skin}.png") # bottom
        if race == 'cat':
            surf.blit(pygame.image.load(f"img_files/spr_protag_tail_{hair}.png"), (0,0)) # tail
        surf.blit(pygame.image.load(f"img_files/spr_protag_top_{skin}.png"), (0,0)) # top
        surf.blit(pygame.image.load(f"img_files/spr_protag_head_{race}_{skin}.png"), (0,0)) # head
        if race == 'cat':
            surf.blit(pygame.image.load(f"img_files/spr_protag_ear_{hair}.png"), (0,0)) # cat ear recolor
        surf.blit(pygame.image.load(f"img_files/spr_clothing_bottom_1_1.png"), (0,0))
        surf.blit(pygame.image.load(f"img_files/spr_clothing_top_1_1.png"), (0,0))
        if self.dir == 0: # direction
            surf = pygame.transform.flip(surf, 1, 0)
        surf = pygame.transform.scale_by(surf, .6)
        screen.blit(surf, (0,0))

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

def main_menu(res, screen, clock):
    mixer.music.load("music/claire_de_lune.mp3")
    mixer.music.play(-1)

    bg_img = pygame.image.load(f"img_files/ui_main_menu.png")
    bg_scaled = pygame.transform.scale(bg_img, res)
    screen.blit(bg_scaled, (0,0))

    button_start = Button('START', res[0]/2, res[1]*.45)
    button_settings = Button('SETTINGS', res[0]/2, res[1]*.65)
    button_close = Button('QUIT', res[0]/2, res[1]*.85)
    
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
                    settings_menu(res, screen, clock)
                if button_start.check_for_input(pygame.mouse.get_pos()):
                    play(res, screen, clock)
        button_start.update(screen)
        button_settings.update(screen)
        button_close.update(screen)
        button_start.change_color(pygame.mouse.get_pos())
        button_settings.change_color(pygame.mouse.get_pos())
        button_close.change_color(pygame.mouse.get_pos())
        pygame.display.update()
        clock.tick(60)

def settings_menu(res, screen, clock):
    screen.fill('gray')

    res_options = ['TEST1', 'TEST2', 'TEST3', 'TEST4', 'TEST5']

    button_return = Button('RETURN', res[0]/2, res[1]*.85)
    button_res = Cycle(res[0]/2, res[1]*.65, res_options)


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_return.check_for_input(pygame.mouse.get_pos()):
                    main_menu(res, screen, clock)
                if button_res.check_for_input(pygame.mouse.get_pos()) == 1:
                    button_res.change_idx(0)
                elif button_res.check_for_input(pygame.mouse.get_pos()) == 2:
                    button_res.change_idx(1)

        button_return.update(screen)
        button_return.change_color(pygame.mouse.get_pos())
        button_res.update(screen)
        button_res.change_color(pygame.mouse.get_pos())
        pygame.display.update()
        clock.tick(60)

def play(res, screen, clock):
    screen.fill('white')
    chara1 = Protag("Alice", 0)
    race_list = ['human', 'cat']
    hair_list = ['brown', 'black', 'blonde']
    skin_list = ['1']

    button_race = Cycle(res[0]*.8, res[1]*.2, race_list)
    button_hair = Cycle(res[0]*.8, res[1]*.25, hair_list)
    button_skin = Cycle(res[0]*.8, res[1]*.3, skin_list)
    button_return = Button('RETURN', res[0]/2, res[1]*.85)
    chara1.draw(screen, 1, 1, race_list[button_race.idx])


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_return.check_for_input(pygame.mouse.get_pos()):
                    main_menu(res, screen, clock)
                if button_race.check_for_input(pygame.mouse.get_pos()) > 0:
                    if button_race.check_for_input(pygame.mouse.get_pos()) == 1:
                        button_race.change_idx(0)
                    elif button_race.check_for_input(pygame.mouse.get_pos()) == 2:
                        button_race.change_idx(1)
                    screen.fill('white')
                if button_hair.check_for_input(pygame.mouse.get_pos()) == 1:
                    button_hair.change_idx(0)
                elif button_hair.check_for_input(pygame.mouse.get_pos()) == 2:
                    button_hair.change_idx(1)
                if button_skin.check_for_input(pygame.mouse.get_pos()) == 1:
                    button_skin.change_idx(0)
                elif button_skin.check_for_input(pygame.mouse.get_pos()) == 2:
                    button_skin.change_idx(1)
                chara1.draw(screen, skin_list[button_skin.idx], hair_list[button_hair.idx], race_list[button_race.idx])

        button_return.update(screen)
        button_return.change_color(pygame.mouse.get_pos())
        button_race.update(screen)
        button_race.change_color(pygame.mouse.get_pos())
        button_hair.update(screen)
        button_hair.change_color(pygame.mouse.get_pos())
        button_skin.update(screen)
        button_skin.change_color(pygame.mouse.get_pos())
        pygame.display.update()
        clock.tick(60)

def main():
    # initialize
    os.environ['SDL_VIDEO_CENTERED'] = '1' # centers window when not in fullscreen
    pygame.init()
    pygame.font.init()
    ctypes.windll.user32.SetProcessDPIAware() # keeps windows GUI scale settings from messing with resolution

    clock = pygame.time.Clock()

    # screen and window settings
    x, y = get_display_size()
    res = (x, y)
    print(f"Resolution = {res}!") # debug

    screen = pygame.display.set_mode(res, pygame.FULLSCREEN)
    pygame.display.set_caption('Dress Up RPG')
    activate_window("Dress Up RPG")

    # cursor settings
    cursor_img = pygame.image.load('img_files/ui_cursor.png')
    cursor = pygame.cursors.Cursor((0,0), cursor_img)
    pygame.mouse.set_cursor(cursor)
    pyautogui.moveTo((res[0]/2, res[1]/2)) # centers cursor

    main_menu(res, screen, clock)

if __name__ == "__main__":
    main()