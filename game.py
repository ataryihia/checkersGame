import pygame
import numpy as np
from modules.pices import *
from modules.board import *
import pickle

# assigning values to X and Y variable
X = 482
Y = 482

global all_sprites_list, sprites
# update the view of the board after changes


def update(array, display_surface, image):
    all_sprites_list = pygame.sprite.Group()
    sprites = [pices for row in array for pices in row if pices]
    all_sprites_list.add(sprites)
    display_surface.blit(image, (0, 0))

    # draw the sprites onto the screen
    all_sprites_list.draw(display_surface)
    pygame.display.update()


def make_logic_board(array):
    my_array = np.empty([8, 8])

    ans = np.zeros((8, 8))
    for x in range(0, 8):
        for y in range(0, 8):
            if array[x][y] is not None:
                if array[x][y].color == 'w':
                    if array[x][y].symbol == 'P':
                        ans[x][y] = 1
                    else:
                        ans[x][y] = 2
                else:
                    if array[x][y].symbol == 'P':
                        ans[x][y] = -1
                    else:
                        ans[x][y] = -2

    return ans


def play(cont):
    pygame.init()
    pygame.font.init()
    display_surface = pygame.display.set_mode((X, Y))

    # set the pygame window name
    pygame.display.set_caption('my game')
    # create a surface object, image is drawn on it.
    image = pygame.image.load("assets/chessboard.png")
    turn = 'w'
    checked_piece = False
    second_move = False
    x1 = 0
    y1 = 0

    if cont:
        with open('game_save.pkl', 'rb') as input:
            turn = pickle.load(input)
            checked_piece = pickle.load(input)
            second_move = pickle.load(input)
            x1 = pickle.load(input)
            y1 = pickle.load(input)
            board = Board(pickle.load(input))
            if checked_piece:
                board.array[x1][y1].set_glowing()
    else:
        board = Board()

    array = board.array
    update(array, display_surface, image)
    # infinite loop
    while True:

        win_flag = board.check_if_game_end()
        if win_flag != 'n':
            if win_flag == 'w':
                print ('white win')
            else:
                print ('black win')

            quit()

        # iterate over the list of Event objects
        # that was returned by pygame.event.get() method.
        for event in pygame.event.get():
            # if event object type is QUIT
            # then quitting the pygame
            # and program both.
            if event.type == pygame.MOUSEBUTTONDOWN:
               x, y = pygame.mouse.get_pos()
               x /= 60
               y /= 60

               # check if the player choose piece
               if not checked_piece:
                   if array[x][y] is not None and array[x][y].color == turn:
                       array[x][y].set_glowing()
                       update(array, display_surface, image)
                       x1 = x
                       y1 = y
                       checked_piece = True
                       update(array, display_surface, image)
               elif array[x][y] is not None:
                   if x1 == x and y1 == y and not second_move:
                       checked_piece = False
                       array[x][y].set_glowing()
                       update(array, display_surface, image)
                   if x1 == x and y1 == y and second_move:
                       second_move = False
                       if turn == 'b':
                           turn = 'w'
                       else:
                           turn = 'b'
                       array[x][y].set_glowing()
                       checked_piece = False
                       update(array, display_surface, image)
               elif array[x][y] is None:
                   if second_move:
                       tmp = array[x1][y1].gen_sec_moves(array, x, y, second_move)
                   else:
                        tmp = array[x1][y1].gen_legal_moves(array, x, y, second_move)
                   if tmp is None:
                       gg = 5
                   else:
                       board.move_piece(array[x1][y1], x, y)
                       if tmp == array[x][y] and not second_move:
                           if turn == 'b':
                               turn = 'w'
                           else:
                               turn = 'b'
                           array[x][y].set_glowing()
                           checked_piece = False
                       else:
                           x1 = x
                           y1 = y
                           second_move = True
                           board.remove_piece(tmp)
                       if y == 0 and array[x][y].symbol == 'P' and array[x][y].color == 'w':
                           board.make_new_king(array[x][y], checked_piece)
                           array[x][y].set_glowing()
                       elif y == 7 and array[x][y].symbol == 'P' and array[x][y].color == 'b':
                           board.make_new_king(array[x][y], checked_piece)
                           array[x][y].set_glowing()
                       update(array, display_surface, image)
        # quit event
        if event.type == pygame.QUIT:

            # save the current game
            with open('game_save.pkl', 'wb') as output:
                pickle.dump(turn, output, pickle.HIGHEST_PROTOCOL)
                pickle.dump(checked_piece, output, pickle.HIGHEST_PROTOCOL)
                pickle.dump(second_move, output, pickle.HIGHEST_PROTOCOL)
                pickle.dump(x1, output, pickle.HIGHEST_PROTOCOL)
                pickle.dump(y1, output, pickle.HIGHEST_PROTOCOL)
                pickle.dump(make_logic_board(array), output, pickle.HIGHEST_PROTOCOL)

            pygame.quit()
            quit()

