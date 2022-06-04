from MainGame import *
import pygame
import random

pygame.init()
pygame.mixer.init()
pygame.font.init()

# s_width = 900
# s_height = 800
# play_width = 300  # meaning 300 // 10 = 30 width per block
# play_height = 600  # meaning 600 // 20 = 30 height per block
# block_size = 30
#
# top_left_x = (s_width - play_width) // 2
# top_left_y = (s_height - play_height) // 2


def main(win):

    tutorial(win)

    last_score = max_score()
    locked_positions = {}
    grid = create_grid(locked_positions)
    shapes_box = [I, Z, S, J, L, T, Q]
    down_sound = pygame.mixer.Sound("music/descend.mp3")

    run = True
    pause = False
    change_piece = False
    current_piece = get_shape(shapes_box)
    next_pieces = [
        get_shape(shapes_box),
        get_shape(shapes_box),
        get_shape(shapes_box),
        get_shape(shapes_box),
        get_shape(shapes_box)
    ]
    hold_piece = get_shape(shapes_box, "empty")
    temp_piece = get_shape(shapes_box, "empty")
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 1
    sep_time = 800
    score = 0
    keys_buffer = [0, 0, 0, 0]
    project_pos = {}
    replace_lock = False
    replace_color = (0, 0, 0)
    pause_time = 0
    start_ticks = pygame.time.get_ticks()

    combo = 0
    spin_count = 0
    isTSpin = False
    mini_TSpin = False
    tetris = False
    back_to_back = False
    arrive = False

    while run:

        if len(shapes_box) <= 0:
            shapes_box = [I, Z, S, J, L, T, Q]

        seconds = (pygame.time.get_ticks()-start_ticks)/1000
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        clock.tick()

        if fall_time/sep_time > fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not(valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        shape_pos = convert_shape_format(current_piece)
        project_pos = get_project(grid, shape_pos)

        if any(pos in project_pos for pos in shape_pos):
            arrive = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    current_piece.rotation += 1
                    if arrive and current_piece.shape == T:
                        spin_count += 1
                    if not(valid_space(current_piece, grid, True)):
                        current_piece.rotation -= 1
                        if arrive and current_piece.shape == T:
                            spin_count -= 1
                elif event.key == pygame.K_z:
                    if arrive and current_piece.shape == T:
                        spin_count = 1
                    current_piece.rotation -= 1
                    if not(valid_space(current_piece, grid, True)):
                        current_piece.rotation += 1
                        if arrive and current_piece.shape == T:
                            spin_count = 0
                elif event.key == pygame.K_SPACE:
                    if down_sound:
                        pygame.mixer.Sound.play(down_sound)
                    shape_pos = project_pos
                    change_piece = True
                elif event.key == pygame.K_m:
                    if down_sound:
                        down_sound = None
                    else:
                        down_sound = pygame.mixer.Sound("music/descend.mp3")
                elif event.key == pygame.K_c:
                    if replace_lock: pass
                    else:
                        temp_piece.replace(current_piece)
                        current_piece.replace(hold_piece)
                        hold_piece.replace(temp_piece)
                        if current_piece.color == (0, 0, 0):
                            current_piece = next_pieces.pop(0)
                            next_pieces.append(get_shape(shapes_box))
                        replace_lock = True
                        replace_color = hold_piece.color
                        hold_piece.color = (131, 139, 139)

                elif event.key == pygame.K_ESCAPE:
                    run = False
                elif event.key == pygame.K_p:
                    pause_time = pygame.time.get_ticks()
                    pause = not pause

                    surf = pygame.Surface(win.get_size())
                    surf.set_alpha(128)
                    surf.fill((255, 105, 180))
                    win.blit(surf, (0,0))

                    font_path = pygame.font.match_font("times")
                    font = pygame.font.Font(font_path, 80, bold=True)
                    label = font.render("Pause", 1, (255,255,255))

                    win.blit(label, (top_left_x + play_width/2 - (label.get_width()/2),
                                         top_left_y + play_height/2 - (label.get_height()/2)))
                    pygame.display.update()

        while pause:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                    pause = not pause
                    start_ticks += (pygame.time.get_ticks() - pause_time)

        keys_pressed = pygame.key.get_pressed()

        if keys_pressed[pygame.K_LEFT] and keys_buffer[0] >= 15:
            keys_buffer = [0, 0, 0, 0]
            current_piece.x -= 1
            if not(valid_space(current_piece, grid)):
                current_piece.x += 1
        else: keys_buffer[0] += 1

        if keys_pressed[pygame.K_RIGHT] and keys_buffer[1] >= 15:
            keys_buffer = [0, 0, 0, 0]
            current_piece.x += 1
            if not(valid_space(current_piece, grid)):
                current_piece.x -= 1
        else: keys_buffer[1] += 1

        if keys_pressed[pygame.K_DOWN] and keys_buffer[2] >= 15:
            keys_buffer = [0, 0, 0, 0]
            current_piece.y += 1
            if not(valid_space(current_piece, grid)):
                current_piece.y -= 1
        else: keys_buffer[2] += 1

        for i in range(len(project_pos)):
            x, y = project_pos[i]
            if y > -1:
                grid[y][x] = (238, 229, 222)

        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_piece.color

        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            current_piece = next_pieces.pop(0)
            next_pieces.append(get_shape(shapes_box))
            eli_rows = clear_rows(grid, locked_positions)

            if spin_count and eli_rows: isTSpin = True
            if spin_count == 1 and eli_rows: mini_TSpin = True

            # print("spin count", spin_count)
            # print("isTSpin", isTSpin)
            # print("mini_TSpin", mini_TSpin)

            if len(locked_positions) == 0: score += 10
            tetris = eli_rows == 4

            result = cal_score(isTSpin, eli_rows, combo, back_to_back, mini_TSpin)
            score += result[0]
            back_to_back = result[1]

        timeup = draw_window(win, grid,
                            tetris, combo, mini_TSpin, isTSpin, back_to_back,
                            score, last_score, 181-seconds)
        draw_next_shape(next_pieces, win)
        draw_hold_shape(hold_piece, win)
        pygame.display.update()

        if change_piece:

            change_piece = False
            replace_lock = False
            hold_piece.color = replace_color
            if eli_rows > 0: combo += 1
            else: combo = 0

            spin_count = 0
            isTSpin = False
            mini_TSpin = False
            arrive = False

            fall_speed *= 0.995

        if check_lost(locked_positions) or timeup:
            draw_text_middle(win, "Gme Over", 80, (255,255,255), score)
            pygame.display.update()
            pygame.time.delay(2000)

            run = False
            update_score(score)


def cal_score(isTSpin, rows, combo, b2b, mini):

    general = 0

    if mini: general += 1
    elif isTSpin and rows >= 1: general += (rows << 1)
    elif rows > 1: general += (1 << (rows-2))

    if b2b and (isTSpin or rows == 4):
        if mini: general += 1
        else: general *= 1.5
    elif isTSpin or rows == 4:
        b2b = True
    elif rows > 0:
        b2b = False

    if combo >= 7: bouns = 4
    else: bouns = (combo-1)//2+1

    if general > 0:
        add_scores = general + bouns
    else:
        add_scores = 0

    return (add_scores, b2b)


def tutorial(win):

    run = True

    arrow = pygame.image.load("images/key_arrow.png")
    arrow = pygame.transform.scale(arrow, (450, 300))
    arrow_rect = arrow.get_rect()

    keyp = pygame.image.load("images/key_p.png")
    keyp = pygame.transform.scale(keyp, (150, 150))
    keyp_rect = keyp.get_rect()

    keyz = pygame.image.load("images/key_z.png")
    keyz = pygame.transform.scale(keyz, (150, 150))
    keyz_rect = keyz.get_rect()

    keym = pygame.image.load("images/key_m.png")
    keym = pygame.transform.scale(keym, (150, 150))
    keym_rect = keym.get_rect()

    keyc = pygame.image.load("images/key_c.png")
    keyc = pygame.transform.scale(keyc, (150, 150))
    keyc_rect = keyc.get_rect()

    space = pygame.image.load("images/space_bar.png")
    space = pygame.transform.scale(space, (450, 150))
    space_rect = space.get_rect()

    canvas = pygame.Surface(win.get_size())
    canvas = canvas.convert()

    arrow_rect.topleft = (100, 100)
    keyp_rect.topleft = (650, 80)
    keyz_rect.topleft = (650, 250)
    keyc_rect.topleft = (650, 420)
    keym_rect.topleft = (650, 590)
    space_rect.topleft = (100, 500)

    start_ticks = pygame.time.get_ticks()

    while run:

        seconds = (pygame.time.get_ticks()-start_ticks)/1000

        event_list = pygame.event.get()
        for event in event_list:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                run = False

        if seconds >= 5: run = False

        canvas.blit(arrow, arrow_rect)
        canvas.blit(keyp, keyp_rect)
        canvas.blit(keyz, keyz_rect)
        canvas.blit(keyc, keyc_rect)
        canvas.blit(keym, keym_rect)
        canvas.blit(space, space_rect)
        win.blit(canvas, (0,0))
        canvas.fill((128, 128, 128))
        pygame.display.flip()


def change_music(win):

    run = True
    music_data = ["Vocaloid.mp3", "Rise.mp3", "Polonaise.mp3", "Ashes.mp3"]

    def back_to(args):
        nonlocal run
        run = False

    title = pygame.image.load("images/title.png")
    title = pygame.transform.scale(title, (600, 800))
    title_rect = title.get_rect()

    canvas = pygame.Surface(win.get_size())
    canvas = canvas.convert()

    back = A_Button(canvas, "Return", back_to, 650, 600, 200, 80)
    music_list = DropDown(
        "Vocaloid", ["Vocaloid", "Rise", "Polonaise", "Ashes"],
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
        selected_option = music_list.update(event_list)
        if selected_option >= 0:
            music_list.main = music_list.options[selected_option]
            pygame.mixer.music.stop()
            pygame.mixer.music.load("music/"+music_data[selected_option])
            pygame.mixer.music.set_volume(0.7)
            pygame.mixer.music.play(-1)

        canvas.fill((128,128,128))
        music_list.draw(canvas)
        back.draw_button()
        pygame.display.flip()


class A_Button():

    def __init__(self, screen, text, callback, x=0, y=0, w=200, h=80):
        self.canvas = screen
        self.text = text
        self.button = {}
        self.callback = callback
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.create_button()
        self.draw_button()

    def draw_button(self):
        if self.button == {}:
            print("You should create button first!")
            return
        pygame.draw.rect(self.canvas, self.button['color'], self.button['rect'])
        self.canvas.blit(self.button['text'], self.button['text rect'])
        pygame.display.update()

    def create_button(self):
        font_path = pygame.font.match_font("times")
        font = pygame.font.Font(font_path, 40)
        text_surf = font.render(self.text, True, (0, 0, 0))
        button_rect = pygame.Rect(self.x, self.y, self.w, self.h)
        text_rect = text_surf.get_rect(center=button_rect.center)
        self.button = {
            'rect': button_rect,
            'text': text_surf,
            'text rect': text_rect,
            'color': (238, 221, 130),
            'callback': self.callback,
        }

    def on_click(self, event, args):
        if event.button == 1:
            if self.button['rect'].collidepoint(event.pos):
                self.callback(args)

    def update(self, event_list):
        mpos = pygame.mouse.get_pos()
        self.active = self.button['rect'].collidepoint(mpos)

        if self.active: self.button['color'] = (255, 215, 0)
        else: self.button['color'] = (238, 221, 130)


class IMG_Button:
    def __init__(self, image, click_image, position):
        self.image = image
        self.rect = self.image.get_rect(topleft=position)
        self.click_image = click_image
        self.position = position
        self.type = True

    def on_click(self, event):
        if event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.change_type()

    def change_type(self):
        self.temp = self.image
        self.image = self.click_image
        self.click_image = self.temp
        self.rect = self.image.get_rect(topleft=self.position)
        self.type = not self.type

        if self.type: pygame.mixer.music.unpause()
        else: pygame.mixer.music.pause()


class DropDown():

    def __init__(self, main, options, x=0, y=0, w=200, h=80):
        font_path = pygame.font.match_font("times")
        self.font = pygame.font.Font(font_path, 40)

        self.color_menu = [ (238, 221, 130), (255, 215, 0) ]
        self.color_option = [ (255, 100, 100), (255, 150, 150) ]
        self.rect = pygame.Rect(x, y, w, h)
        self.main = main
        self.options = options
        self.draw_menu = False
        self.menu_active = False
        self.active_option = -1

    def draw(self, surf):
        pygame.draw.rect(surf, self.color_menu[self.menu_active], self.rect, 0)
        msg = self.font.render(self.main, 1, (0, 0, 0))
        surf.blit(msg, msg.get_rect(center = self.rect.center))

        if self.draw_menu:
            for i, text in enumerate(self.options):
                rect = self.rect.copy()
                rect.y += (i+1) * self.rect.height
                pygame.draw.rect(surf, self.color_option[1 if i == self.active_option else 0], rect, 0)
                msg = self.font.render(text, 1, (0, 0, 0))
                surf.blit(msg, msg.get_rect(center = rect.center))

    def update(self, event_list):
        mpos = pygame.mouse.get_pos()
        self.menu_active = self.rect.collidepoint(mpos)

        self.active_option = -1
        for i in range(len(self.options)):
            rect = self.rect.copy()
            rect.y += (i+1) * self.rect.height
            if rect.collidepoint(mpos):
                self.active_option = i
                break

        if not self.menu_active and self.active_option == -1:
            self.draw_menu = False

        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.menu_active:
                    self.draw_menu = not self.draw_menu
                elif self.draw_menu and self.active_option >= 0:
                    self.draw_menu = False
                    return self.active_option
        return -1


def main_menu(win):

    clock = pygame.time.Clock()
    run = True

    title = pygame.image.load("images/title.png")
    title = pygame.transform.scale(title, (600, 800))
    title_rect = title.get_rect()

    sound = pygame.image.load("images/sound.png")
    sound = pygame.transform.scale(sound, (100, 100))

    mute = pygame.image.load("images/mute.png")
    mute = pygame.transform.scale(mute, (100, 100))

    canvas = pygame.Surface(win.get_size())
    canvas = canvas.convert()

    def quit_game(args):
        nonlocal run
        run = False

    def music_state(args):
        nonlocal run
        run = False

    single = A_Button(canvas, "Practice", main, 650, 150, 200, 80)
    online = A_Button(canvas, "Online", quit_game, 650, 250, 200, 80)
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


win = pygame.display.set_mode((s_width, s_height))

programIcon = pygame.image.load("images/title.png")
pygame.display.set_icon(programIcon)
pygame.display.set_caption("Online Tetris Battle")

pygame.mixer.music.load("music/vocaloid.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

main_menu(win)
