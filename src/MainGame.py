import pygame
import random

pygame.init()
pygame.mixer.init()
pygame.font.init()

s_width = 800
s_height = 700
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

O = [['.....',
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

shapes = [I, Z, S, J, L, T, O]
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
        self.shape = shape # one of 2d list from I, Z, S, J, L, T, O
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


def valid_space(shape, grid):
    accepted_pos = [[(j, i) for j in range(10) if grid[i][j] == (0,0,0)] for i in range(20)]
    accepted_pos = [j for sub in accepted_pos for j in sub]

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


def get_shape(args=""):

    if args == "empty":
        return Piece(5, 0, N)

    # start point at (5, 0)
    return Piece(5, 0, random.choice(shapes))


def draw_text_middle(surface, text, size, color):

    s = pygame.Surface(surface.get_size())
    s.set_alpha(128)
    s.fill((255, 105, 180))
    surface.blit(s, (0,0))

    font_path = pygame.font.match_font("dfkaisb")
    font = pygame.font.Font(font_path, size, bold=True)
    label = font.render(text, 1, color)

    surface.blit(label, (top_left_x + play_width/2 - (label.get_width()/2),
                         top_left_y + play_height/2 - (label.get_height()/2)))


def draw_grid(surface, grid):
    sx = top_left_x
    sy = top_left_y

    for i in range(len(grid)):
        pygame.draw.line(surface, (119, 136, 153), (sx, sy+i*block_size), (sx+play_width, sy+i*block_size))
        for j in range(len(grid[i])):
            pygame.draw.line(surface, (119, 136, 153), (sx+j*block_size, sy),(sx+j*block_size, sy+play_height))


def clear_rows(grid, locked):

    inc = 0 # num of eliminated rows
    for i in range(len(grid)-1, -1, -1):
        row = grid[i]
        if (0,0,0) not in row:
            inc += 1
            ind = i
            for j in range(len(row)):
                try:
                    del locked[(j,i)]
                except:
                    continue

    if inc > 0:
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind: # the bottommost eliminated row
                newKey = (x, y + inc)
                locked[newKey] = locked.pop(key) # move down row blocks to remove blank row

    return inc


def draw_next_shape(shape, surface):
    font_path = pygame.font.match_font("dfkaisb")
    font = pygame.font.Font(font_path, 30)
    label = font.render('下一個', 1, (255,255,255))

    sx = top_left_x + play_width + 50
    sy = top_left_y + 100
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        pygame.draw.line(surface, (119, 136, 153), (sx, sy+i*block_size), (sx+4*block_size, sy+i*block_size), 2)
        for j, column in enumerate(row):
            pygame.draw.line(surface, (119, 136, 153), (sx+j*block_size, sy),(sx+j*block_size, sy+4*block_size), 2)
            if column == '0':
                pygame.draw.rect(surface, shape.color, (sx+j*block_size, sy+i*block_size, block_size, block_size-2), 0)

    surface.blit(label, (sx + 10, sy - 50))


def draw_hold_shape(shape, surface):
    font_path = pygame.font.match_font("dfkaisb")
    font = pygame.font.Font(font_path, 30)
    label = font.render("替換", 1, (255,255,255))

    sx = top_left_x + play_width + 50
    sy = top_left_y + 400
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        pygame.draw.line(surface, (119, 136, 153), (sx, sy+i*block_size), (sx+4*block_size, sy+i*block_size), 2)
        for j, column in enumerate(row):
            pygame.draw.line(surface, (119, 136, 153), (sx+j*block_size, sy),(sx+j*block_size, sy+4*block_size), 2)
            if column == '0':
                pygame.draw.rect(surface, shape.color, (sx+j*block_size, sy+i*block_size, block_size, block_size-2), 0)

    surface.blit(label, (sx + 20, sy - 50))


def update_score(nscore):

    score = max_score()
    with open('scores.txt', 'w') as f:
        if int(score) > nscore:
            f.write(str(score))
        else:
            f.write(str(nscore))


def max_score():

    try:
        with open('scores.txt', 'r') as f:
            lines = f.readlines()
            score = lines[0].strip()
        return score
    except IOError:
        return "0"


def draw_window(surface, grid, score=0, last_score=0):

    surface.fill((100, 100, 100))
    font_path = pygame.font.match_font("dfkaisb")
    font = pygame.font.Font(font_path, 30)

    # last score
    label = font.render('High Score: ' + last_score, 1, (255,255,255))

    sx = top_left_x // 2 - (label.get_width()/2)
    sy = top_left_y // 2 + 30
    surface.blit(label, (sx, sy))

    # current score
    label = font.render('Score: ' + str(score), 1, (255,255,255))

    sy += 60
    surface.blit(label, (sx, sy))

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (top_left_x+j*block_size, top_left_y+i*block_size, block_size, block_size), 0)

    pygame.draw.rect(surface, (0, 255, 255), (top_left_x, top_left_y, play_width, play_height), 3)

    draw_grid(surface, grid)


def get_project(grid, shape_pos):

    accepted_pos = [[(j, i) for j in range(10) if grid[i][j] == (0,0,0)] for i in range(20)]
    accepted_pos = [j for sub in accepted_pos for j in sub]

    assume_pos = shape_pos
    while(True):
        assume_pos = [ (pos[0], pos[1]+1) for pos in assume_pos ]
        if any(pos[1] < 0 for pos in assume_pos) or all(pos in accepted_pos for pos in assume_pos): pass
        else: break

    return [ (pos[0], pos[1]-1) for pos in assume_pos ]
