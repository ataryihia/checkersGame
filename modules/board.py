import numpy as np

from modules.pices import *

class Board:

    def __init__(self, arr=None):
        self.array = [
            [None for x in range(8)],
            [None for x in range(8)],
            [None for x in range(8)],
            [None for x in range(8)],
            [None for x in range(8)],
            [None for x in range(8)],
            [None for x in range(8)],
            [None for x in range(8)]

        ]
        if arr is None:

            for i in range(0, 8, 2):
                self.array[i][0] = Pawn('b', i, 0)
            for i in range(1, 8, 2):
                self.array[i][1] = Pawn('b', i, 1)
            for i in range(0, 8, 2):
                self.array[i][2] = Pawn('b', i, 2)

            for i in range(1, 8, 2):
                self.array[i][5] = Pawn('w', i, 5)
            for i in range(0, 8, 2):
                self.array[i][6] = Pawn('w', i, 6)
            for i in range(1, 8, 2):
                self.array[i][7] = Pawn('w', i, 7)

        else:
            for x in range(0, 8):
                for y in range(0, 8):
                    if arr[x][y] == 1:
                        self.array[x][y] = Pawn('w', x, y)
                    elif arr[x][y] == 2:
                        self.array[x][y] = King('w', x, y)
                    elif arr[x][y] == -1:
                        self.array[x][y] = Pawn('b', x, y)
                    elif arr[x][y] == -2:
                        self.array[x][y] = King('b', x, y)

    def remove_piece(self, piece):
        self.array[piece.x][piece.y] = None

    def move_piece(self, piece, new_x, new_y):
        #   change piece data
        self.array[piece.x][piece.y] = None
        piece.change_place(new_x, new_y)
        self.array[new_x][new_y] = piece

    def make_new_king(self, piece, glow):
        self.array[piece.x][piece.y] = King(piece.color, piece.x, piece.y)
        if glow:
            self.array[piece.x][piece.y].set_glowing()

        del piece

    # if white win return w
    # if black win return b
    # if no one win yet return n
    def check_if_game_end(self):
        white = 0
        black = 0
        for (x, y), value in np.ndenumerate(self.array):
            #  for cell in self.array.flatten():
            if white > 0 and black > 0:
                return 'n'
            if self.array[x][y] is not None:
                if self.array[x][y].color == 'w':
                    white += 1
                else:
                    black += 1
        if white == 0:
            return 'b'
        elif black == 0:
            return 'w'
        return 'n'



