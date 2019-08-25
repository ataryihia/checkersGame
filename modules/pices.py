import pygame

class Piece(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        # Call the parent class (Sprite) constructor
        super(Piece,self).__init__()
        self.color = color
        self.glow = 0

        # position on board matrix
        self.x = width
        self.y = height

        # allows for transparency
        self.image = pygame.Surface((123, 123), pygame.SRCALPHA, 32)
        self.image.convert_alpha()

        # position on screen surface
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = width * 60, height * 60

    def update_pygame(self):
        self.image = pygame.Surface((123, 123), pygame.SRCALPHA, 32)
        self.image.convert_alpha()
        self.image.blit(self.sprite, (0, 0))

    def change_place(self, x,y):
        self.x = x
        self.y = y
        # position on screen surface
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x * 60, y * 60


class Pawn(Piece):

    def __init__(self, color, x, y):
        super(Pawn,self).__init__(color, x, y)
        self.symbol = 'P'

        # load the corresponding sprite image and draw on own surface.
        # similar process for the other pieces
        self.sprite = pygame.image.load("assets/{}pawn.png".format(self.color))
        self.image.blit(self.sprite, (0, 0))

    def set_glowing(self):

        if self.glow == 0:
            self.glow = 1
            self.sprite = pygame.image.load("assets/{}pawnglow.png".format(self.color))
        else:
            self.glow = 0
            self.sprite = pygame.image.load("assets/{}pawn.png".format(self.color))

        self.update_pygame()

    #   return  0 if not legal move return None
    #           1 if regular move return the move piece
    #           2 if eat move return the eaten piece
    def gen_legal_moves(self, board , new_x , new_y, second_move):
        #   case of white color turn
        if board[new_x][new_y] is not None:
            return None
        if self.color == 'w' or self.color =='g':
            if self.y <= new_y:
                return None
            #   standard move
            if new_y+1 == self.y and (new_x + 1 == self.x or new_x - 1 == self.x) and board[new_x][new_y] is None:
                return self
            #   'left eating'
            if (new_y + 2 == self.y and new_x + 2 == self.x and board[new_x][new_y] is None and
                    board[new_x+1][new_y+1] is not None and board[new_x+1][new_y+1].color == 'b'):
                return board[new_x+1][new_y+1]
            #   'right eating'
            if (new_y + 2 == self.y and new_x - 2 == self.x and board[new_x][new_y] is None and
                    board[new_x-1][new_y+1] is not None and board[new_x-1][new_y+1].color == 'b'):
                return board[new_x-1][new_y+1]

        elif self.color == 'b' or self.color =='g':
            if self.y >= new_y:
                return None

            #   standard move
            if new_y - 1 == self.y and (new_x + 1 == self.x or new_x - 1 == self.x) and board[new_x][new_y] is None:
                return self
            #   'right eating'
            if (new_y - 2 == self.y and new_x + 2 == self.x and board[new_x][new_y] is None and
                    board[new_x + 1][new_y - 1] is not None and board[new_x + 1][new_y - 1].color == 'w'):
                return board[new_x + 1][new_y - 1]
            #   'left eating'
            if (new_y - 2 == self.y and new_x - 2 == self.x and board[new_x][new_y] is None and
                    board[new_x - 1][new_y - 1] is not None and board[new_x - 1][new_y - 1].color == 'w'):
                return board[new_x - 1][new_y - 1]

        return None

    def gen_sec_moves(self, board, new_x, new_y, second_move):

        if board[new_x][new_y] is not None:
            return None

        #   'left eating'
        if (new_y + 2 == self.y and new_x + 2 == self.x and board[new_x][new_y] is None and
                board[new_x+1][new_y+1] is not None and board[new_x+1][new_y+1].color != self.color):
            return board[new_x+1][new_y+1]
        #   'right eating'
        if (new_y + 2 == self.y and new_x - 2 == self.x and board[new_x][new_y] is None and
                board[new_x-1][new_y+1] is not None and board[new_x-1][new_y+1].color != self.color):
            return board[new_x-1][new_y+1]

        #   'right eating'
        if (new_y - 2 == self.y and new_x + 2 == self.x and board[new_x][new_y] is None and
                board[new_x + 1][new_y - 1] is not None and board[new_x + 1][new_y - 1].color != self.color):
            return board[new_x + 1][new_y - 1]
        #   'left eating'
        if (new_y - 2 == self.y and new_x - 2 == self.x and board[new_x][new_y] is None and
                board[new_x - 1][new_y - 1] is not None and board[new_x - 1][new_y - 1].color != self.color):
            return board[new_x - 1][new_y - 1]

        return None


class King(Piece):

    def __init__(self, color, x, y):
        super(King,self).__init__(color, x, y)
        self.symbol = 'K'
        self.glow = 1
        # load the corresponding sprite image and draw on own surface.
        # similar process for the other pieces
        self.sprite = pygame.image.load("assets/{}king.png".format(self.color))
        self.image.blit(self.sprite, (0, 0))

    def gen_legal_moves(self, board, new_x, new_y, second_move):
        gg = 5

        if board[new_x][new_y] is not None:
            return None

        if abs(self.x-new_x) != abs(self.y-new_y):
            return None

        else:

            if self.x < new_x:
                return check_if_king_can_eat(self, board, new_x, new_y, self.x, self.y)
            else:
                return check_if_king_can_eat(self, board, self.x, self.y, new_x, new_y)

        return None

    def gen_sec_moves(self, board, new_x, new_y, second_move):
        tmp = self.gen_legal_moves(board, new_x, new_y, second_move)
        return tmp

        if tmp is None:
            return None
        if tmp.x == self.x and tmp.y == self.y:
            return self
        else:
            return None

    def set_glowing(self):

        if self.glow == 0:
            self.glow = 1
            self.sprite = pygame.image.load("assets/{}kingglow.png".format(self.color))
        else:
            self.glow = 0
            self.sprite = pygame.image.load("assets/{}king.png".format(self.color))

        self.update_pygame()


def get_ans_check_eat(self, count_pieces, my_piece_in_way, ans_eat):

    if count_pieces == 0:
        return self
    elif count_pieces == 1:
        return ans_eat
    return None


def check_if_king_can_eat(self, board, big_x1, y1, small_x, y2):

    # count if there are pieces
    # with same color on the way
    my_piece_in_way = 0

    # if there was eating
    count_pieces = 0

    #   if the way is complete
    way_flag = False
    # if there was eating get the eaten piece
    ans_eat = None
    # check left Up
    if y1 > y2:
        for i in range(1, 7, 1):
            if small_x+i < 8 and y2+i < 8:

                if small_x+i == big_x1 and y2+i == y1:
                    way_flag = True
                if board[small_x + i][y2 + i] is not None and not way_flag:
                    if board[small_x + i][y2 - i] != self and board[small_x + i][y2 + i].color == self.color:
                        my_piece_in_way = 1
                    else:
                        count_pieces += 1
                        ans_eat = board[small_x + i][y2 + i]

            if way_flag:
                return get_ans_check_eat(self, count_pieces, my_piece_in_way, ans_eat)
    # check left down
    else:

        for i in range(1, 7, 1):

            if small_x + i < 8 and y2 - i > -1:

                if small_x + i == big_x1 and y2 - i == y1:
                    way_flag = True
                if board[small_x + i][y2 - i] is not None and not way_flag:
                    if board[small_x + i][y2 - i] != self and board[small_x + i][y2 - i].color == self.color:
                        my_piece_in_way = 1
                    else:
                        count_pieces += 1
                        ans_eat = board[small_x + i][y2 - i]

            if way_flag:
                return get_ans_check_eat(self, count_pieces, my_piece_in_way, ans_eat)