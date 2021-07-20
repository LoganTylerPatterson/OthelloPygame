import sys
import pygame
from pygame.locals import *
import random


class Othello:

    def __init__(self):
        pygame.init()
        self.c_white = (255, 255, 255)
        self.c_black = (0, 0, 0)
        self.c_blue = (0, 0, 255)
        self.c_red = (255, 0, 0)

        self.screen = pygame.display.set_mode((1200, 1200))
        pygame.display.set_caption("Othello")

        self.width = 8
        self.height = 8
        self.board = [[" "] * 8, [" "] * 8, [" "] * 8, [" "]
                      * 8, [" "] * 8, [" "] * 8, [" "] * 8, [" "] * 8]
        self.player_score = 0
        self.computer_score = 0

        self.board[3][3] = "player"
        self.board[3][4] = "computer"
        self.board[4][3] = "computer"
        self.board[4][4] = "player"

    def run_game(self):
        self.draw_initial_board()
        self.turn = "player"

        """Start the main loop for the game."""
        while True:
            # Watch for mouse events
            if self.turn == "player":
               if self.check_for_events():
                   self.get_player_move()
                   self.check_win()
                   self.turn = "computer"
            elif self.turn == "computer":
                self.get_computer_move()
                self.check_win()
                self.turn = "player"
        
            pygame.display.flip()

    def get_player_score(self, board, tile):
        score = 0
        for row in range(self.height):
            for col in range(self.width):
                if board[row][col] == tile:
                    score = score + 1
        return score

    def get_computer_move(self):
        valid_moves = self.get_valid_moves(self.board, "computer")
        random.shuffle(valid_moves)

        #Going for the corner is the best option
        for x, y in valid_moves:
            if self.is_on_corner(x, y):
                return [x, y]

        #Get the highest scoring move
        best_score = -1
        bestx = 0
        besty = 0
        for x, y in valid_moves:
            board_copy = self.get_board_copy(self.board)
            self.make_move(board_copy, "computer", x, y)
            score = self.get_player_score(board_copy, "computer")
            print(">>get_computer_move: Score is ")
            print(score)
            if score > best_score:
                best_score = score
                bestx = x
                besty = y
        
        #Get all the tiles to flip from this move
        tiles_to_flip = self.is_valid_move(self.board, "computer", y + 1 ,x + 1)
        for tile in tiles_to_flip:
            x_to_change = x
            y_to_change = y
            self.board[x][y] = "computer"
            self.draw_square(y + 1, x + 1, self.c_red)
        #Update the current tile
        self.board[bestx][besty] = "computer"
        self.draw_square(besty + 1, bestx + 1, self.c_red)
        
    def get_board_copy(self, board):
        board_copy = [[" "] * 8,[" "] * 8,[" "] * 8,[" "] * 8,[" "] * 8,[" "] * 8,[" "] * 8,[" "] * 8]

        for x in range(self.width):
            for y in range(self.height):
                board_copy[x][y] = self.board[x][y]
        return board_copy

    def make_move(self, board, tile, x, y):
        tiles_to_change = self.is_valid_move(board, tile, x + 1, y + 1)

        if tiles_to_change == False:
            return False
        
        board[x][y] = tile
        for x, y in tiles_to_change:
            board[x][y] = tile
        return True

    def is_on_corner(self, x, y):
        return (x == 0 or x == self.width - 1 and y == 0 or y == self.height - 1)

    def check_win(self):
        player_can_move = self.get_valid_moves(self.board, "player")
        computer_can_move = self.get_valid_moves(self.board, "computer")
        if player_can_move == [] or computer_can_move == []:
            return True

    def check_for_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                return True

    def get_player_move(self):
        x, y = pygame.mouse.get_pos()
        row, column = self.player_click(x, y)
        valid_moves = self.is_valid_move(self.board, "player", row, column)
        if valid_moves != False:
            for tile in valid_moves:
                x, y = tile
                self.draw_square(x + 1, y + 1, self.c_blue)
                self.board[x][y] = 'player'

            self.draw_square(row, column, self.c_blue)
            self.board[row-1][column-1] = "player"

    def get_random_starter(self):
        turn = random.randint(0, 1)
        if turn == 1:
            return "player"
        elif turn == 0:
            return "computer"

    def get_valid_moves(self, board, tile):
        valid_moves = []
        for row in range(self.width):
            for col in range(self.height):
                if self.is_valid_move(board, tile, row + 1, col + 1):
                    valid_moves.append([row, col])
        return valid_moves
    
    def is_on_board(self, row, col):
        #Works as expected
        return row > 0 and row <= self.width and col > 0 and col <= self.height

    def is_valid_move(self, board, tile, row_start, col_start):
        #This is working
        if board[row_start-1][col_start-1] != " " or not self.is_on_board(row_start, col_start):
            return False

        if tile == "player":
            other_tile = "computer"
        else:
            other_tile = "player"

        tiles_to_flip = []
        for x_dir, y_dir in [[0, 1], [1,1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
            col, row = row_start, col_start
            col += x_dir
            row += y_dir
            while self.is_on_board(col, row) and board[col - 1][row - 1] == other_tile:
                col += x_dir
                row += y_dir
                if self.is_on_board(col, row) and board[col - 1][row - 1] == tile:
                    while True:
                        col -= x_dir
                        row -= y_dir
                        if col == row_start and row == col_start:
                            break
                        tiles_to_flip.append([col-1,row-1])

        if len(tiles_to_flip) == 0:
            return False
        return tiles_to_flip

    def player_click(self, x, y):
        unit = 1200 / 8
        column = 1
        row = 1
        for i in range(self.width + 1):
            if x < unit * i:
                column = i
                break
        for i in range(self.height + 1):
            if y < unit * i:
                row = i
                break
        return [row, column]

    def draw_initial_board(self):
        self.screen.fill(self.c_white)
        line_width = 150
        # Draw game grid
        for i in range(self.width):
            pygame.draw.line(self.screen, self.c_black,
                             (i * 150, 0), (i * 150, 1200), 2)
            pygame.draw.line(self.screen, self.c_black,
                             (0, i * 150), (1200, i * 150), 2)

        # Draw initial squares
        self.draw_square(4, 4, self.c_blue)
        self.draw_square(5, 4, self.c_red)
        self.draw_square(4, 5, self.c_red)
        self.draw_square(5, 5, self.c_blue)

        pygame.display.flip()

    def draw_square(self, row, col, color):
        y = (row - 1) * 150 + 3
        x = (col - 1) * 150 + 3
        pygame.draw.rect(self.screen, color, (x, y, 146, 146))

    def update_board(self):
        for col in range(self.height):
            for row in range(self.width):
                square = self.board[col][row]
                if square == "player":
                    self.draw_square(col, row, self.c_blue)
                elif square == "computer":
                    self.draw_square(col, row, self.c_red)

    def get_score(self):
        for row in range(self.height):
            for col in range(self.width):
                square = self.board[row][col]
                if square == "player":
                    self.player_score += 1
                elif square == "computer":
                    self.computer_score += 1


if __name__ == '__main__':
    othello = Othello()
    othello.run_game()
