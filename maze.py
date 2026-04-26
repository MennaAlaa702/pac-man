from constants import *

maze_level_1 = [
"XXXXXXXXXXXXXXXX.XXXXXXXXXXXXXXXX",
"X..............................OX",
"X.XXX.XXX.XXXXXX.XXXXXX.XXX.XXX.X",
"X.X X.X X.X    X.X    X.X X.X X.X",
"X.XXX.X X.XXXXXX.XXXXXX.X X.XXX.X",
"X.....XXX.X....X.X....X.XXX.....X",
"XXXXX.......XX.X.X.XX.......XXXXX",
"X.....XXXXX...........XXXXX.....X",
"X.XXX.......XXXXXXXXX.......XXX.X",
"X.....XXXXX...........XXXXX.....X",
"X.XXX...O...XXXX.XXXX.......XXX.X",
"X.X X.XXXXX.X  X.X  X.XXXXX.X X.X",
"X.X X.X   X.X  X.X  X.X   X.X X.X",
"X.X X.X   X.X  X.X  X.X   X.X X.X",
"X.X X.XXXXX.X  X.X  X.XXXXX.X X.X",
"X.XXX.......XXXX.XXXX...O...XXX.X",
"X.....XXXXX...........XXXXX.....X",
"X.XXX.......XXXXXXXXX.......XXX.X",
"X.....XXXXX...........XXXXX.....X",
"XXXXX.......XX.X.X.XX.......XXXXX",
"X.....XXX.X....X.X....X.XXX.....X",
"X.XXX.X X.XXXXXX.XXXXXX.X X.XXX.X",
"X.X X.X X.X    X.X    X.X X.X X.X",
"X.XXX.XXX.XXXXXX.XXXXXX.XXX.XXX.X",
"XO..............................X",
"XXXXXXXXXXXXXXXX.XXXXXXXXXXXXXXXX"
]

def calculate_maze_data():
    walls, pellets, power = [], [], []

    for row in range(MAZE_GRID_ROWS):
        for col in range(MAZE_GRID_COLUMNS):
            c = maze_level_1[row][col]

            x = MAZE_LEVEL_START_X + CELL_SIZE * col
            y = MAZE_LEVEL_START_Y - CELL_SIZE * row

            if c == "X":
                walls.append((x, y))
            elif c == ".":
                pellets.append((x, y))
            elif c == "O":
                power.append((x, y))

    return walls, pellets, power