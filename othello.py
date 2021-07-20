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

    """Main game loop to wrange all this sheet"""
    def run_game(self):
        self.draw_initial_board()
        self.turn = "player"

        """Start the main loop for the game."""
        while True:
            #Watch for mouse events
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

    """Given a board and a player, it will iterate through the board and return the score of said board"""
    def get_player_score(self, board, tile):
        print(">>Get player score")
        score = 0
        for row in range(self.height):
            for col in range(self.width):
                if board[row][col] == tile:
                    score = score + 1
        return score

    """This method will iterate through the valid moves, determine which gives the highest value, and returns a tuple of the x and y coordinates"""
    def get_computer_move(self):
        print(">>Get Computer Move")
        bestx = -1
        besty = -1
        valid_moves = self.get_valid_moves(self.board, "computer")
        random.shuffle(valid_moves)

        #Going for the corner is the best option
        for x, y in valid_moves:
            if self.is_on_corner(x, y):
                return [x, y]

        #Get the highest scoring move
        best_score = -1

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
        return [bestx, besty]

    """Gives us a copy of the board so the computer can do some nice testing"""
    def get_board_copy(self, board):
        print(">>Get Board Copy")

        board_copy = [[" "] * 8,[" "] * 8,[" "] * 8,[" "] * 8,[" "] * 8,[" "] * 8,[" "] * 8,[" "] * 8]

        for x in range(self.width):
            for y in range(self.height):
                board_copy[x][y] = board[x][y]
        return board_copy

    """Takes a board, player, x and y and updates that tile along with all the tiles that should be flipped """
    def make_move(self, board, tile, x, y):
        print(">>Make Move")

        tiles_to_change = self.is_valid_move(board, tile, x, y)

        if tiles_to_change == False:
            return False

        board[x][y] = tile
        for x, y in tiles_to_change:
            board[x][y] = tile
        return True

    """Pretty simple"""
    def is_on_corner(self, x, y):
        print(">>Is On Corner")

        return (x == 0 or x == self.width - 1 and y == 0 or y == self.height - 1)

    """If neither the player nor the computer can move, game is over; returns True if play continues"""
    def check_win(self):
        print(">>Check Win")

        player_can_move = self.get_valid_moves(self.board, "player")
        computer_can_move = self.get_valid_moves(self.board, "computer")
        if player_can_move == [] or computer_can_move == []:
            return True

    """Looks for any player events, returns true if so"""
    def check_for_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                return True

    """Get the position of the mouse, get the row and column of the click. Get the tiles to flip if the move is valid, flip them and draw the associated squares """
    def get_player_move(self):
        x, y = pygame.mouse.get_pos()
        row, column = self.player_click(x, y)
        tiles_to_flip = self.is_valid_move(self.board, "player", row, column)
        if tiles_to_flip != False:
            for tile in tiles_to_flip:
                x, y = tile
                self.draw_square(x, y, self.c_blue)
                self.board[x][y] = 'player'

            self.draw_square(row, column, self.c_blue)
            self.board[row][column] = "player"

    """Not too hard to decipher"""
    def get_random_starter(self):
        print(">>Get Random Starter")

        turn = random.randint(0, 1)
        if turn == 1:
            return "player"
        elif turn == 0:
            return "computer"

    """Iterates through the board, checks each to see if it is a valid move, returns a list of valid moves"""
    def get_valid_moves(self, board, tile):
        print(">>Get Valid Moves")

        valid_moves = []
        for row in range(self.width):
            for col in range(self.height):
                if self.is_valid_move(board, tile, row, col):
                    valid_moves.append([row, col])
        return valid_moves

    """returns True/False depending on whether the row and column are inside/outside the board"""
    def is_on_board(self, row, col):
        return row >= 0 and row <= self.width - 1 and col >= 0 and col <= self.height - 1

    """This method returns False if the move is not valid and a list of the tiles that need to be flipped if it is valid"""
    def is_valid_move(self, board, tile, row_start, col_start):
        #This is working
        if board[row_start][col_start] != " " or not self.is_on_board(row_start, col_start):
            return False

        if tile == "player":
            other_tile = "computer"
        else:
            other_tile = "player"

        tiles_to_flip = []
        for x_dir, y_dir in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
            row, col = row_start, col_start
            row += y_dir
            col += x_dir
            while self.is_on_board(col, row) and board[row][col] == other_tile:
                col += x_dir
                row += y_dir
                if self.is_on_board(col, row) and board[row][col] == tile:
                    while True:
                        col -= x_dir
                        row -= y_dir
                        if col == col_start and row == row_start:
                            break
                        tiles_to_flip.append([row, col])

        if len(tiles_to_flip) == 0:
            return False
        return tiles_to_flip

    """Takes in the mouse x and y position, and divides by a squares len/width to determine which row/column the click occured in"""
    def player_click(self, x, y):
        unit = 1200 / 8
        column = 1
        row = 1
        for i in range(self.width):
            if x < unit * i:
                column = i - 1
                break
        for i in range(self.height):
            if y < unit * i:
                row = i - 1
                break
        return [row, column]

    """Draws the grid lines with 4 initial squares filled in in the center of the grid"""
    def draw_initial_board(self):
        print(">>Draw Initial Board")
        self.screen.fill(self.c_white)
        line_width = 150
        # Draw game grid
        for i in range(self.width):
            pygame.draw.line(self.screen, self.c_black,
                             (i * 150, 0), (i * 150, 1200), 2)
            pygame.draw.line(self.screen, self.c_black,
                             (0, i * 150), (1200, i * 150), 2)

        # Draw initial squares
        self.draw_square(3, 3, self.c_blue)
        self.draw_square(4, 3, self.c_red)
        self.draw_square(3, 4, self.c_red)
        self.draw_square(4, 4, self.c_blue)

        pygame.display.flip()

    """Draws a square at the given position on the board"""
    def draw_square(self, row, col, color):
        print(">>Draw Square")
        y = (row) * 150 + 3
        x = (col) * 150 + 3
        pygame.draw.rect(self.screen, color, (x, y, 146, 146))

    """After a element has been updated in self.board, this method will redraw the entire grid -> flip() will need to be called"""
    def update_board(self):
        print(">>Update Board")
        for col in range(self.height):
            for row in range(self.width):
                square = self.board[col][row]
                if square == "player":
                    self.draw_square(col, row, self.c_blue)
                elif square == "computer":
                    self.draw_square(col, row, self.c_red)

    """Iterates through the board and updates the players score by one each time their name is found"""
    def get_score(self):
        print(">>Get Score")
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
