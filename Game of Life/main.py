import pygame  # 2.0.1
import copy
import math
import numpy as np

"""
left click to select squares
right click to unselect squares
press the scroll button to start the animation

The process takes place on a finite world. 
The window wraps around from left to right and from top to bottom

"""


class game_of_life():
    def __init__(self):
        ################################################################################
        # CHANGE THESE PARAMETERS
        self.WIDTH = 1200
        self.HEIGHT = 600

        self.CELL_HEIGHT = 10
        self.CELL_WIDTH = 10

        ################################################################################

        self.N_ROWS = int(self.HEIGHT/self.CELL_HEIGHT)
        self.N_COLS = int(self.WIDTH/self.CELL_WIDTH)

        pygame.init()

        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.GRID = [
            [False for j in range(int(self.WIDTH/self.CELL_WIDTH))] for i in range(int(self.HEIGHT/self.CELL_HEIGHT))
        ]

        self.run = True
        self.clock = pygame.time.Clock()
        self.start = False
        self.initial = True

    def update(self):
        self.screen.fill((0, 0, 0))

        for i in range(len(self.GRID)):
            for j in range(len(self.GRID[i])):
                if self.GRID[i][j] is True:

                    pygame.draw.rect(
                        self.screen, (255, 255, 255), (j*self.CELL_WIDTH, i*self.CELL_HEIGHT, self.CELL_WIDTH, self.CELL_HEIGHT))

    def get_neighbour(self, array, m, n):
        indices = np.array([[-1 + m, n + -1], [m, n + -1], [-1 + m, n], [1 + m, n + 1],
                            [m, n + 1], [1 + m, n], [1 + m, n + -1], [-1 + m, n + 1]])

        for x in indices:
            if x[0] < 0:
                x[0] += self.N_ROWS
            elif x[0] == self.N_ROWS:
                x[0] -= self.N_ROWS

            if x[1] < 0:
                x[1] += self.N_COLS
            elif x[1] == self.N_COLS:
                x[1] -= self.N_COLS 

        count = 0

        for x in indices:
            if array[x[0]][x[1]] is True:
                count += 1
        return count

    def next_generation(self):
        self.last_gen = copy.deepcopy(self.GRID)

        for i in range(self.N_ROWS):
            for j in range(self.N_COLS):

                cnt = self.get_neighbour(self.last_gen, i, j)

                if self.last_gen[i][j] is False:
                    if cnt == 3:
                        self.GRID[i][j] = True
                    else:
                        self.GRID[i][j] = False
                    continue

                else:
                    if cnt == 3 or cnt == 2:
                        self.GRID[i][j] = True
                    else:
                        self.GRID[i][j] = False

    def user_initial(self):
        if self.initial:
            if pygame.mouse.get_pressed()[0]:
                x, y = pygame.mouse.get_pos()
                self.GRID[math.floor(y/self.CELL_HEIGHT)
                          ][math.floor(x/self.CELL_WIDTH)] = True

            if pygame.mouse.get_pressed()[2]:
                x, y = pygame.mouse.get_pos()
                self.GRID[math.floor(y/self.CELL_HEIGHT)
                          ][math.floor(x/self.CELL_WIDTH)] = False

            if pygame.mouse.get_pressed()[1]:
                self.initial = False
                self.start = True
            self.clock.tick(60)

    def start_game(self):
        while self.run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
            self.update()
            if self.start:
                self.next_generation()
                self.clock.tick(240)
            self.user_initial()
            pygame.display.update()


game = game_of_life()
game.start_game()
