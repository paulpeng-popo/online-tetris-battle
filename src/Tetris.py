import pygame
from os import walk
from tools.GameGUI import A_Button
from tools.GameGUI import IMG_Button
from tools.GameGUI import DropDown
from tools.GameGUI import Single
from tools.GameGUI import Multiple

pygame.init()
pygame.mixer.init()
pygame.font.init()

window_figures = { "window_size": (900, 800) }

startBGM = { "path": "musics/vocaloid.mp3", "volume": 0.7 }
gameBGM = {}

titlePNG = { "path": "images/title.png", "size": (600, 800) }
soundPNG = { "path": "images/sound.png", "size": (100, 100) }
mutePNG = { "path": "images/mute.png", "size": (100, 100) }


def change_music(win):

    run = True
    
    musics_data = []
    for (dirpath, dirnames, filenames) in walk("./musics"):
    
        try: filenames.remove("descend.mp3")
        except: pass
        
        musics_data.extend(filenames)
        break
        
    for song in musics_data:
        gameBGM[song[:-4]] = { "path": "./musics/"+song, "volume": 0.7 }

    def back_to_home(args):
        nonlocal run
        run = False

    title = pygame.image.load(titlePNG["path"])
    title = pygame.transform.scale(title, titlePNG["size"])
    title_rect = title.get_rect()

    canvas = pygame.Surface(win.get_size())
    canvas = canvas.convert()

    back = A_Button(canvas, "Return", back_to_home, 650, 600, 200, 80)
    musics_list = DropDown(
        "vocaloid", list(gameBGM.keys()),
        650, 100, 200, 80
    )

    while run:

        canvas.blit(title, title_rect)
        win.blit(canvas, (0,0))

        event_list = pygame.event.get()
        for event in event_list:
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                back.on_click(event, win)

        back.update(pygame.event.get())
        selected_option = musics_list.update(event_list)
        
        if selected_option >= 0:
        
            musics_list.main = musics_list.options[selected_option]
            pygame.mixer.music.stop()
            pygame.mixer.music.load(gameBGM[musics_list.main]["path"])
            pygame.mixer.music.set_volume(gameBGM[musics_list.main]["volume"])
            pygame.mixer.music.play(-1)

        canvas.fill((128,128,128))
        musics_list.draw(canvas)
        back.draw_button()
        pygame.display.flip()


def main_menu(win):

    run = True
    clock = pygame.time.Clock()

    title = pygame.image.load(titlePNG["path"])
    title = pygame.transform.scale(title, titlePNG["size"])
    title_rect = title.get_rect()

    sound = pygame.image.load(soundPNG["path"])
    sound = pygame.transform.scale(sound, soundPNG["size"])

    mute = pygame.image.load(mutePNG["path"])
    mute = pygame.transform.scale(mute, mutePNG["size"])

    canvas = pygame.Surface(win.get_size())
    canvas = canvas.convert()

    def quit_game(args):
        nonlocal run
        run = False

    single = A_Button(canvas, "Practice", Single, 650, 150, 200, 80)
    online = A_Button(canvas, "Online", Multiple, 650, 250, 200, 80)
    quit = A_Button(canvas, "Quit", quit_game, 650, 350, 200, 80)
    music = A_Button(canvas, "Edit Music", change_music, 650, 450, 200, 80)
    
    buttons = [ single, online, quit, music ]

    ibutton = IMG_Button(sound, mute, (700, 650))

    while run:

        canvas.fill((128,128,128))
        canvas.blit(title, title_rect)
        canvas.blit(ibutton.image, ibutton.rect)

        for button in buttons:
            button.draw_button()

        win.blit(canvas, (0, 0))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                ibutton.on_click(event)
                for button in buttons:
                    button.on_click(event, win)

        for button in buttons:
            button.update(pygame.event.get())
            
        pygame.display.update()
        clock.tick(30)

    pygame.display.quit()


def tetris():

    win = pygame.display.set_mode(window_figures["window_size"])

    programIcon = pygame.image.load(titlePNG["path"])
    pygame.display.set_icon(programIcon)
    pygame.display.set_caption("Tetris Battle")

    pygame.mixer.music.load(startBGM["path"])
    pygame.mixer.music.set_volume(startBGM["volume"])
    pygame.mixer.music.play(-1)

    main_menu(win)


if __name__=='__main__':
    tetris()

