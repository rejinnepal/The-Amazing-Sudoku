'''
This is the main module of the Game. It contains the main functions. The functions written in this module check whether a unique number is present in each row, column, and small-sized bix or not. This module also checks if the Game is conitinuing or should be stopped. In this module, the sudoku board from a webiste is imported as well.
'''
import pygame as pg
import sys, requests
from bs4 import BeautifulSoup
from Control_Room import COLOUR_WHITE, COLOUR_BLACK, COLOUR_PINK, COLOUR_PURPLE, COLOUR_CYAN, COLOUR_YELLOW, COLOUR_DARKRED, COLOUR_PURPLEBLUE, FIXED_COLOUR, INCORRECT_COLOUR, WIDTH, HEIGHT, LOCATION, SIZE, L_SIZE
from Tester import TO_CHECK_WITH
from Buttons import Tab

class Game:
    # This function initiates the Game.
    def __init__(self):
        pg.init()
        self.bird_chirps = pg.mixer.Sound('bird_chirps.wav')
        self.evil_sound = pg.mixer.Sound('evil_sound.wav')
        self.rainfall = pg.mixer.Sound('rainfall.wav')
        self.river_flow = pg.mixer.Sound('river_flow.wav')
        self.window = pg.display.set_mode((WIDTH, HEIGHT))
        self.running = True
        self.grid = TO_CHECK_WITH
        self.selected = None
        self.mouse_position = None
        self.state = "playing"
        self.finished = False
        self.cellChanged = False
        self.button_player = []
        self.fixed_cells = []
        self.invalid_cells = []
        self.font = pg.font.SysFont("calibri", SIZE // 2)
        self.grid = []
        self.puzzle_game("4")
        self.load()

    # This function checks if the Game should be continued or not.
    def run(self):
        while self.running:
            if self.state == "playing":
                self.playing_events()
                self.playing_update()
                self.playing_draw()
        pg.quit()
        sys.exit()


# This is the state of the playing function.

    def playing_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False

            # The user can click in a desired box.
            if event.type == pg.MOUSEBUTTONDOWN:
                selected = self.mouse_on_box()
                if selected:
                    self.selected = selected
                else:
                    self.selected = None
                    for button in self.button_player:
                        if button.highlighted:
                            button.click()

            # The user can type a number in the desired box
            if event.type == pg.KEYDOWN:
                if self.selected != None and self.selected not in self.fixed_cells:
                    if self.isint(event.unicode):
                        # The cell (box) is changed here
                        self.grid[self.selected[1]][self.selected[0]] = int(
                            event.unicode)
                        self.cellChanged = True

    # This function updates the Game every time.
    def playing_update(self):
        self.mouse_position = pg.mouse.get_pos()
        for button in self.button_player:
            button.update(self.mouse_position)

        if self.cellChanged:
            self.invalid_cells = []
            if self.boxes_are_fixed():
                # It checks whether the board is complete or not
                self.cells_checker()
                if len(self.invalid_cells) == 0:
                    self.finished = True

    def playing_draw(self):
        self.window.fill(COLOUR_WHITE)

        for button in self.button_player:
            button.draw(self.window)

        if self.selected:
            self.make_selection(self.window, self.selected)

        self.colour_fixed_boxes(self.window, self.fixed_cells)
        self.colour_invalid_boxes(self.window, self.invalid_cells)

        self.import_number(self.window)

        self.make_grid(self.window)
        pg.display.update()
        self.cellChanged = False

    # This function checks if the cells (boxes) are filled or not.
    def boxes_are_fixed(self):
        for row in self.grid:
            for number in row:
                if number == 0:
                    return False
        return True

    # This function runs the checking process in each row, each column, and each medium-sized boxes at once.
    def cells_checker(self):
        self.row_checker()
        self.column_checker()
        self.small_box_checker()

    # This function checks the number in each medium-sized box to make sure that no number repeats in the medium-sized boxes.
    def small_box_checker(self):
        for row in range(3):
            for col in range(3):
                varieties = [1, 2, 3, 4, 5, 6, 7, 8, 9]

                for c in range(3):
                    for d in range(3):
                        row_index = row * 3 + c
                        col_index = col * 3 + d
                        if self.grid[col_index][row_index] in varieties:
                            varieties.remove(self.grid[col_index][row_index])
                        else:
                            if [row_index, col_index] not in self.fixed_cells and [
                                    row_index, col_index
                            ] not in self.invalid_cells:
                                self.invalid_cells.append([row_index, col_index])
                            if [row_index, col_index] in self.fixed_cells:
                                for row2 in range(3):
                                    for col2 in range(3):
                                        row2_index = row * 3 + row2
                                        col2_index = col * 3 + col2
                                        if self.grid[col2_index][
                                                row2_index] == self.grid[
                                                    col_index][row_index] and [
                                                        row2_index, col2_index
                                                    ] not in self.fixed_cells:
                                            self.invalid_cells.append(
                                                [row2_index, col2_index])

    # This function checks every element in the rows to make sure than no number repeats in the rows.
    def row_checker(self):
        for col_index, row in enumerate(self.grid):
            varieties = [1, 2, 3, 4, 5, 6, 7, 8, 9]
            for row_index in range(9):
                if self.grid[col_index][row_index] in varieties:
                    varieties.remove(self.grid[col_index][row_index])
                else:
                    if [row_index, col_index] not in self.fixed_cells and [
                            row_index, col_index
                    ] not in self.invalid_cells:
                        self.invalid_cells.append([row_index, col_index])
                    if [row_index, col_index] in self.fixed_cells:
                        for t in range(9):
                            if self.grid[col_index][t] == self.grid[col_index][
                                    row_index] and [t, col_index
                                                  ] not in self.fixed_cells:
                                self.invalid_cells.append([t, col_index])

    # This function checks each element in the columns to make sure that no number repeats in the columns.
    def column_checker(self):
        for row_index in range(9):
            varieties = [1, 2, 3, 4, 5, 6, 7, 8, 9]
            for col_index, row in enumerate(self.grid):
                if self.grid[col_index][row_index] in varieties:
                    varieties.remove(self.grid[col_index][row_index])
                else:
                    if [row_index, col_index] not in self.fixed_cells and [
                            row_index, col_index
                    ] not in self.invalid_cells:
                        self.invalid_cells.append([row_index, col_index])
                    if [row_index, col_index] in self.fixed_cells:
                        for t, row in enumerate(self.grid):
                            if self.grid[t][row_index] == self.grid[col_index][
                                    row_index] and [row_index, t
                                                  ] not in self.fixed_cells:
                                self.invalid_cells.append([row_index, t])

    # This function imports the sudoku board (with fixed numbers) from the given website
    def puzzle_game(self, difficulty_level):
        html_doc = requests.get("https://nine.websudoku.com/?level={}".format(
            difficulty_level)).content
        soup = BeautifulSoup(html_doc, "html.parser")
        ids = [
            'f00', 'f01', 'f02', 'f03', 'f04', 'f05', 'f06', 'f07', 'f08',
            'f10', 'f11', 'f12', 'f13', 'f14', 'f15', 'f16', 'f17', 'f18',
            'f20', 'f21', 'f22', 'f23', 'f24', 'f25', 'f26', 'f27', 'f28',
            'f30', 'f31', 'f32', 'f33', 'f34', 'f35', 'f36', 'f37', 'f38',
            'f40', 'f41', 'f42', 'f43', 'f44', 'f45', 'f46', 'f47', 'f48',
            'f50', 'f51', 'f52', 'f53', 'f54', 'f55', 'f56', 'f57', 'f58',
            'f60', 'f61', 'f62', 'f63', 'f64', 'f65', 'f66', 'f67', 'f68',
            'f70', 'f71', 'f72', 'f73', 'f74', 'f75', 'f76', 'f77', 'f78',
            'f80', 'f81', 'f82', 'f83', 'f84', 'f85', 'f86', 'f87', 'f88'
        ]

        data = []
        for iid in ids:
            data.append(soup.find('input', id=iid))
        board = [[0 for x in range(9)] for x in range(9)]
        for i, box in enumerate(data):
            try:
                board[i // 9][i % 9] = int(box['value'])
            except:
                pass
        self.grid = board
        self.load()

    # This function plays the sound according to the user's choice.
    def rainfall_effect(self):
        self.rainfall.play(-1)

    def bird_chirps_effect(self):
        self.bird_chirps.play(-1)

    def river_flow_effect(self):
        self.river_flow.play(-1)

    def evil_sound_effect(self):
        self.evil_sound.play(-1)

    # This function fills the colour in the incorrect boxes.
    def colour_invalid_boxes(self, window, invalid):
        for box in invalid:
            pg.draw.rect(window, INCORRECT_COLOUR,
                         (box[0] * SIZE + LOCATION[0],
                          box[1] * SIZE + LOCATION[1], SIZE, SIZE))

    # This function fills the colour in the fixed boxes.
    def colour_fixed_boxes(self, window, fixed):
        for cell in fixed:
            pg.draw.rect(window, FIXED_COLOUR,
                         (cell[0] * SIZE + LOCATION[0],
                          cell[1] * SIZE + LOCATION[1], SIZE, SIZE))

    # This function drwas the numbers.
    def import_number(self, window):
        for index_b, row in enumerate(self.grid):
            for index_a, num in enumerate(row):
                if num != 0:
                    pos = [(index_a * SIZE) + LOCATION[0],
                           (index_b * SIZE) + LOCATION[1]]
                    self.from_text_to_screen(window, str(num), pos)

    #
    def make_selection(self, window, position):
        pg.draw.rect(window, COLOUR_PINK,
                     ((position[0] * SIZE) + LOCATION[0],
                      (position[1] * SIZE) + LOCATION[1], SIZE, SIZE))

    # This function makes the grid lines of the board including the bold lines of the middlesized squares.
    def make_grid(self, window):
        pg.draw.rect(window, COLOUR_BLACK,
                     (LOCATION[0], LOCATION[1], WIDTH - 150, HEIGHT - 150), 2)
        for x in range(9):
            pg.draw.line(window, COLOUR_BLACK,
                         (LOCATION[0] + (x * SIZE), LOCATION[1]),
                         (LOCATION[0] + (x * SIZE), LOCATION[1] + 450),
                         2 if x % 3 == 0 else 1)
            pg.draw.line(window, COLOUR_BLACK,
                         (LOCATION[0], LOCATION[1] + (x * SIZE)),
                         (LOCATION[0] + 450, LOCATION[1] + +(x * SIZE)),
                         2 if x % 3 == 0 else 1)

    # This function checks if the mouse pointer in the small boxes or not.
    def mouse_on_box(self):
        if self.mouse_position[0] < LOCATION[0] or self.mouse_position[
                1] < LOCATION[1]:
            return False
        if self.mouse_position[0] > LOCATION[
                0] + L_SIZE or self.mouse_position[1] > LOCATION[1] + L_SIZE:
            return False
        return ((self.mouse_position[0] - LOCATION[0]) // 50,
                (self.mouse_position[1] - LOCATION[1]) // 50)

    # These function helps to customizes the colours, size and the text written on the difficulty tabs.
    def button_loader(self):
        self.button_player.append(
            Tab(40,
                40,
                200,
                30,
                function=self.cells_checker,
                colour=COLOUR_PURPLE,
                text="Check My Game"))
        self.button_player.append(
            Tab(250,
                40,
                120,
                30,
                colour=COLOUR_CYAN,
                function=self.puzzle_game,
                params="1",
                text="EASY"))
        self.button_player.append(
            Tab(380,
                40,
                100,
                30,
                colour=COLOUR_YELLOW,
                function=self.puzzle_game,
                params="2",
                text="MEDIUM"))
        self.button_player.append(
            Tab(490,
                40,
                100,
                30,
                colour=COLOUR_DARKRED,
                function=self.puzzle_game,
                params="4",
                text="EVIL"))
        self.button_player.append(
            Tab(40,
                80,
                160,
                30,
                colour=COLOUR_PURPLEBLUE,
                text="Choose a music :: "))
        self.button_player.append(
            Tab(205,
                80,
                70,
                30,
                colour=COLOUR_PURPLEBLUE,
                function=self.rainfall_effect,
                text="Rainfall"))
        self.button_player.append(
            Tab(280,
                80,
                100,
                30,
                colour=COLOUR_PURPLEBLUE,
                function=self.bird_chirps_effect,
                text="Bird Chirps"))
        self.button_player.append(
            Tab(385,
                80,
                100,
                30,
                colour=COLOUR_PURPLEBLUE,
                function=self.river_flow_effect,
                text="Water Flow"))
        self.button_player.append(
            Tab(490,
                80,
                100,
                30,
                colour=COLOUR_PURPLEBLUE,
                function=self.evil_sound_effect,
                text="Evil Sound"))

    def from_text_to_screen(self, window, text, position):
        font = self.font.render(text, False, COLOUR_BLACK)
        width = font.get_width()
        height = font.get_height()
        position[0] = position[0] + (50 - width) // 2
        position[1] = position[1] + (50 - height) // 2
        window.blit(font, position)

    # It loads the boxes.
    def load(self):
        self.button_player = []
        self.button_loader()
        self.fixed_cells = []
        self.invalid_cells = []
        self.finished = False

        # It sets the fixed boxes from original board imported.
        for index_b, row in enumerate(self.grid):
            for index_a, num in enumerate(row):
                if num != 0:
                    self.fixed_cells.append([index_a, index_b])

    # This function checks whether the entered value in the square box is integer or not. It is because only the integer value from 0 to 9 can be entered into the box.
    def isint(self, string):
        try:
            int(string)
            return True
        except:
            return False
