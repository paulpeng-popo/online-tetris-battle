from tools.GameFunctions import *
from tools.Connect import Client
import pygame

pygame.init()
pygame.mixer.init()
pygame.font.init()

arrowPNG = { "path": "images/key_arrow.png", "size": (450, 300), "left_loc": (100, 100) }
keyzPNG = { "path": "images/key_z.png", "size": (150, 150), "left_loc": (650, 80) }
keycPNG = { "path": "images/key_c.png", "size": (150, 150), "left_loc": (650, 250) }
keymPNG = { "path": "images/key_m.png", "size": (150, 150), "left_loc": (650, 420) }
keypPNG = { "path": "images/key_p.png", "size": (150, 150), "left_loc": (650, 590) }
spacebarPNG = { "path": "images/space_bar.png", "size": (450, 150), "left_loc": (100, 500) }


def tutorial(win):

    run = True

    arrow = pygame.image.load(arrowPNG["path"])
    arrow = pygame.transform.scale(arrow, arrowPNG["size"])
    arrow_rect = arrow.get_rect()
    arrow_rect.topleft = arrowPNG["left_loc"]

    keyz = pygame.image.load(keyzPNG["path"])
    keyz = pygame.transform.scale(keyz, keyzPNG["size"])
    keyz_rect = keyz.get_rect()
    keyz_rect.topleft = keyzPNG["left_loc"]

    keyc = pygame.image.load(keycPNG["path"])
    keyc = pygame.transform.scale(keyc, keycPNG["size"])
    keyc_rect = keyc.get_rect()
    keyc_rect.topleft = keycPNG["left_loc"]

    keym = pygame.image.load(keymPNG["path"])
    keym = pygame.transform.scale(keym, keymPNG["size"])
    keym_rect = keym.get_rect()
    keym_rect.topleft = keymPNG["left_loc"]

    keyp = pygame.image.load(keypPNG["path"])
    keyp = pygame.transform.scale(keyp, keypPNG["size"])
    keyp_rect = keyp.get_rect()
    keyp_rect.topleft = keypPNG["left_loc"]

    spacebar = pygame.image.load(spacebarPNG["path"])
    spacebar = pygame.transform.scale(spacebar, spacebarPNG["size"])
    spacebar_rect = spacebar.get_rect()
    spacebar_rect.topleft = spacebarPNG["left_loc"]

    canvas = pygame.Surface(win.get_size())
    canvas = canvas.convert()

    start_ticks = pygame.time.get_ticks()

    while run:

        seconds = (pygame.time.get_ticks()-start_ticks)/1000

        event_list = pygame.event.get()
        for event in event_list:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                run = False

        if seconds >= 5: run = False

        canvas.blit(arrow, arrow_rect)
        canvas.blit(keyz, keyz_rect)
        canvas.blit(keyc, keyc_rect)
        canvas.blit(keym, keym_rect)
        canvas.blit(keyp, keyp_rect)
        canvas.blit(spacebar, spacebar_rect)

        win.blit(canvas, (0,0))
        canvas.fill((128, 128, 128))
        pygame.display.flip()


def Single(win):

    tutorial(win)

    last_score = max_score()
    locked_positions = {}
    grid = create_grid(locked_positions)
    shapes_box = [I, Z, S, J, L, T, Q]
    down_sound = pygame.mixer.Sound("./musics/descend.mp3")

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
    eli_rows = 0

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
                        down_sound = pygame.mixer.Sound("./musics/descend.mp3")
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

        if keys_pressed[pygame.K_LEFT] and keys_buffer[0] >= 20:
            keys_buffer = [0, 0, 0, 0]
            current_piece.x -= 1
            if not(valid_space(current_piece, grid)):
                current_piece.x += 1
        else: keys_buffer[0] += 1

        if keys_pressed[pygame.K_RIGHT] and keys_buffer[1] >= 20:
            keys_buffer = [0, 0, 0, 0]
            current_piece.x += 1
            if not(valid_space(current_piece, grid)):
                current_piece.x -= 1
        else: keys_buffer[1] += 1

        if keys_pressed[pygame.K_DOWN] and keys_buffer[2] >= 20:
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

            result = cal_score(isTSpin, eli_rows, combo, back_to_back, mini_TSpin)
            score += result[0]
            back_to_back = result[1]

        timeup = draw_window(win, grid,
                            eli_rows, combo, mini_TSpin, isTSpin, back_to_back,
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
            draw_text_middle(win, "Game Over", 80, (255,255,255), score)
            pygame.display.update()
            pygame.time.delay(1500)

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

    return (general + bouns, b2b)


def Multiple(win):

    client = Client("popo")

    if client.active:
        select_mode(win)
        client.disconnect()


def select_mode(win):

    run = True
    clock = pygame.time.Clock()

    def back_to_home(args):
        nonlocal run
        run = False

    canvas = pygame.Surface(win.get_size())
    canvas = canvas.convert()

    create_room = A_Button(canvas, "Create New Room", back_to_home, 80, 300, 330, 200)
    join_room = A_Button(canvas, "Join A Room", back_to_home, 490, 300, 330, 200)
    back = A_Button(canvas, "Return", back_to_home, 650, 600, 200, 80)
    buttons = [ create_room, join_room, back]

    while run:

        canvas.fill((128,128,128))

        for button in buttons:
            button.draw_button()

        win.blit(canvas, (0,0))
        pygame.display.flip()

        event_list = pygame.event.get()
        for event in event_list:
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    button.on_click(event, win)

        for button in buttons:
            button.update(pygame.event.get())

        pygame.display.update()
        clock.tick(30)


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

        if event.button == 1 and self.button['rect'].collidepoint(event.pos):
            self.callback(args)

    def update(self, event_list):

        mpos = pygame.mouse.get_pos()
        self.active = self.button['rect'].collidepoint(mpos)

        if self.active: self.button['color'] = (255, 215, 0)
        else: self.button['color'] = (238, 221, 130)


class IMG_Button():

    def __init__(self, image, click_image, position):

        self.image = image
        self.rect = self.image.get_rect(topleft=position)
        self.click_image = click_image
        self.position = position
        self.type = True

    def on_click(self, event):

        if event.button == 1 and self.rect.collidepoint(event.pos):
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
