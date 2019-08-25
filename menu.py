import pygame
from game import play


pygame.init()


def set_display(x, y):
    pygame.display.set_caption('my game')
    display = pygame.display.set_mode((x, y))
    image = pygame.image.load("assets/menu.jpg")
    display.blit(image, (0, 0))
    pygame.display.update()
    return display
    # draw the sprites onto the screen


display_surface = set_display(640, 480)
done = False

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    pygame.display.flip()

# The menu with start and resum
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                # start button
                if 219 < x < 422 and 194 < y < 223:
                    play(False)
                # resume button
                elif 183 < x < 458 and 262 < y < 292:
                    play(True)
            if event.type == pygame.QUIT:
                # deactivates the pygame library
                pygame.quit()
                # quit the program.
                quit()
