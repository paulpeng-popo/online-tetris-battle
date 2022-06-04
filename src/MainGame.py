import pygame
import random

pygame.init()
pygame.mixer.init()
pygame.font.init()

s_width = 900
s_height = 800
play_width = 300  # meaning 300 // 10 = 30 width per block
play_height = 600  # meaning 600 // 20 = 30 height per block
block_size = 30

top_left_x = (s_width - play_width) // 2
top_left_y = (s_height - play_height) // 2


S = [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

Q = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

N = [['.....',
      '.....',
      '.....',
      '.....',
      '.....']]

shapes = [I, Z, S, J, L, T, Q]
shape_colors = [
    (0, 191, 255), # LightSkyBlue
    (255, 48, 48), # Firebrick1
    (0, 255, 127), # SpringGreen1
    (0, 0, 255), # Blue
    (255, 140, 0), # DarkOrange
    (160, 32, 240), # Purple
    (255, 215, 0) # Gold
]


class Piece(object):
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape # one of 2d list from I, Z, S, J, L, T, Q
        if shape != N: self.color = shape_colors[shapes.index(shape)]
        else: self.color = (0, 0, 0)
        self.rotation = 0

    def replace(self, shape_piece):
        self.x = 5
        self.y = 0
        self.shape = shape_piece.shape
        self.color = shape_piece.color
        self.rotation = shape_piece.rotation

def create_grid(locked_pos={}):

    # create 10x20 grid field with (r,g,b) blocks
    grid = [[(0,0,0) for _ in range(10)] for _ in range(20)]

    for i in range(len(grid)): # 20
        for j in range(len(grid[i])): # 10
            if (j, i) in locked_pos: # location(j, i) < left -- right > has occupied
                c = locked_pos[(j, i)] # get location color
                grid[i][j] = c # set location color in grid field
    return grid


def convert_shape_format(shape):
    positions = []

    # get block shape list and decide rotation form
    format = shape.shape[shape.rotation % len(shape.shape)]

    # convert 0 into (x, y) and append into positions = []
    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((shape.x + j, shape.y + i))

    # reset location to center and move up to hide blocks
    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)

    return positions


def valid_space(shape, grid, spin=False):
    accepted_pos = [[(j, i) for j in range(10) if grid[i][j] == (0,0,0)] for i in range(20)]
    accepted_pos = [j for sub in accepted_pos for j in sub]

    if spin and shape.y > -1:
        test_pos = [(0,0), (1,0), (-1,0), (2, 0), (-2, 0), (1,1), (-1,1), (1, 2), (-1, 2)]
        reset_pos = [(0,0), (-1,0), (1,0), (-2, 0), (2, 0), (-1,-1), (1,-1), (-1, -2), (1, -2)]

        for test_i in range(len(test_pos)):
            shape.x += test_pos[test_i][0]
            shape.y += test_pos[test_i][1]
            formatted = convert_shape_format(shape)

            if all(pos in accepted_pos for pos in formatted):
                return True

            shape.x += reset_pos[test_i][0]
            shape.y += reset_pos[test_i][1]

        return False
    else:
        formatted = convert_shape_format(shape)
        for pos in formatted:
            if pos not in accepted_pos:
                if pos[1] > -1 or pos[0] < 0 or pos[0] > 9:
                    return False
        return True


def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True

    return False


def get_shape(shapes_box, args=""):

    if args == "empty":
        return Piece(5, 0, N)

    shape = random.choice(shapes_box)
    shapes_box.remove(shape)

    # start point at (5, 0)
    return Piece(5, 0, shape)


def draw_text_middle(surface, text, size, color, score=-1):

    if text != "Game Over": pass
    else: surface.fill((255, 105, 180))

    font_path = pygame.font.match_font("times")
    font = pygame.font.Font(font_path, size, bold=True)
    label = font.render(text, 1, color)

    surface.blit(label, (top_left_x + play_width/2 - (label.get_width()/2),
                         top_left_y + play_height/2 - (label.get_height()/2) - 50))

    if score == -1: pass
    else:
        label = font.render("Lines sent: "+str(score), 1, color)

        surface.blit(label, (top_left_x + play_width/2 - (label.get_width()/2),
                             top_left_y + play_height/2 - (label.get_height()/2) + 50))


def draw_grid(surface, grid):
    sx = top_left_x
    sy = top_left_y

    for i in range(len(grid)):
        pygame.draw.line(surface, (119, 136, 153), (sx, sy+i*block_size), (sx+play_width, sy+i*block_size))
        for j in range(len(grid[i])):
            pygame.draw.line(surface, (119, 136, 153), (sx+j*block_size, sy),(sx+j*block_size, sy+play_height))


def clear_rows(grid, locked):

    inc = 0 # num of eliminated rows
    ind_list = []  # the eliminated rows

    for i in range(len(grid)-1, -1, -1):
        row = grid[i]
        if (0,0,0) not in row:
            inc += 1
            ind_list.append(i)
            for j in range(len(row)):
                try:
                    del locked[(j,i)]
                except:
                    continue

    if inc > 0:

        bias = 0
        temp = inc
        while temp > 0:
            gap = ind_list[bias]-ind_list[-1]+1-temp
            if gap == 0: break
            bias += 1
            temp -= 1

        ind_count = [bias, temp]
        # [0, 1], [0, 2], [0, 3], [0, 4], [1, 1], [1, 2], [2, 1]

        sorted_locked = sorted(list(locked), key=lambda x: x[1])

        if ind_count[0] == 0:
            for key in sorted_locked[::-1]:
                x, y = key
                if y < ind_list[-1]:
                    newKey = (x, y + ind_count[1])
                    locked[newKey] = locked.pop(key)
        else:
            for key in sorted_locked[::-1]:
                x, y = key
                if y < ind_list[0] and y > ind_list[-1]:
                    newKey = (x, y + ind_count[0])
                    locked[newKey] = locked.pop(key)
                elif y < ind_list[-1]:
                    newKey = (x, y + ind_count[0] + ind_count[1])
                    locked[newKey] = locked.pop(key)

    return inc


def draw_next_shape(shapes, surface):
    font_path = pygame.font.match_font("times")
    font = pygame.font.Font(font_path, 30)
    label = font.render("Next", 1, (255,255,255))

    sx = top_left_x + play_width + 100
    sy = top_left_y - 10

    surface.blit(label, (sx + 30, sy - 50))

    for shape in shapes:
        format = shape.shape[shape.rotation % len(shape.shape)]
        for i, line in enumerate(format):
            row = list(line)
            pygame.draw.line(surface, (119, 136, 153), (sx, sy+i*block_size), (sx+4*block_size, sy+i*block_size), 2)
            for j, column in enumerate(row):
                pygame.draw.line(surface, (119, 136, 153), (sx+j*block_size, sy),(sx+j*block_size, sy+4*block_size), 2)
                if column == "0":
                    pygame.draw.rect(surface, shape.color, (sx+j*block_size, sy+i*block_size, block_size, block_size-2), 0)
        sy += 140


def draw_hold_shape(shape, surface):
    font_path = pygame.font.match_font("times")
    font = pygame.font.Font(font_path, 30)
    label = font.render("Hold", 1, (255,255,255))

    sx = top_left_x - 200
    sy = top_left_y + 500
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        pygame.draw.line(surface, (119, 136, 153), (sx, sy+i*block_size), (sx+4*block_size, sy+i*block_size), 2)
        for j, column in enumerate(row):
            pygame.draw.line(surface, (119, 136, 153), (sx+j*block_size, sy),(sx+j*block_size, sy+4*block_size), 2)
            if column == "0":
                pygame.draw.rect(surface, shape.color, (sx+j*block_size, sy+i*block_size, block_size, block_size-2), 0)

    surface.blit(label, (sx + 30, sy - 50))


def update_score(nscore):

    score = max_score()
    with open("scores.txt", "w") as f:
        if int(score) > nscore:
            f.write(str(score))
        else:
            f.write(str(nscore))


def max_score():

    try:
        with open("scores.txt", "r") as f:
            lines = f.readlines()
            score = lines[0].strip()
        return score
    except IOError:
        return "0"


def draw_window(surface, grid, rows, combo, mini, tspin, b2b, score=0, last_score=0, seconds=120):

    surface.fill((100, 100, 100))
    font_path = pygame.font.match_font("times")
    font = pygame.font.Font(font_path, 30)

    # last score
    label = font.render("Record: " + last_score, 1, (255, 255, 255))

    sx = top_left_x // 2 - (label.get_width()/2) - 30
    sy = top_left_y // 2 + 30
    surface.blit(label, (sx, sy))

    # current score
    label = font.render("Lines sent: " + str(int(score)), 1, (255, 255, 255))

    sy += 60
    surface.blit(label, (sx, sy))

    # timer
    label = font.render("Time " + str(int(seconds//60)) + ":" + str(int(seconds%60)), 3, (255, 255, 255))
    sy += 60
    surface.blit(label, (sx, sy))

    # tetris
    if rows == 4:
        font = pygame.font.Font(font_path, 40)
        label = font.render("Tetris", 3, (255, 100, 100))
        sy += 60
        surface.blit(label, (sx, sy))

    # combo
    if combo:
        label = font.render("Combo x" + str(combo), 3, (255, 100, 100))
        sy += 60
        surface.blit(label, (sx, sy))

    # mini
    if mini:
        label = font.render("Mini T-Spin", 3, (255, 100, 100))
        sy += 60
        surface.blit(label, (sx, sy))

    # tspin
    elif tspin:
        text = ""
        if rows == 1: text = "Single"
        elif rows == 2: text = "Double"
        elif rows == 3: text = "Triple"
        label = font.render("T-Spin " + text, 3, (255, 100, 100))
        sy += 60
        surface.blit(label, (sx, sy))

    # b2b
    if b2b:
        label = font.render("Back-to-back", 3, (255, 100, 100))
        sy += 60
        surface.blit(label, (sx, sy))

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (top_left_x+j*block_size, top_left_y+i*block_size, block_size, block_size), 0)

    pygame.draw.rect(surface, (0, 255, 255), (top_left_x, top_left_y, play_width, play_height), 3)

    draw_grid(surface, grid)

    if seconds <= 10:
        draw_text_middle(surface, str(int(seconds)), 80, (255, 105, 180))
        if int(seconds) <= 0: return True

    return False


def get_project(grid, shape_pos):

    accepted_pos = [[(j, i) for j in range(10) if grid[i][j] == (0,0,0)] for i in range(20)]
    accepted_pos = [j for sub in accepted_pos for j in sub]

    assume_pos = shape_pos
    while(True):
        assume_pos = [ (pos[0], pos[1]+1) for pos in assume_pos ]
        if any(pos[1] < 0 for pos in assume_pos) or all(pos in accepted_pos for pos in assume_pos): pass
        else: break

    return [ (pos[0], pos[1]-1) for pos in assume_pos ]
