import sys
import pygame


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
        self.board = [[None] * 8, [None] * 8, [None] * 8, [None] * 8,[None] * 8, [None] * 8, [None] * 8, [None] * 8]
        self.player_score = 0
        self.computer_score = 0

        self.board[3][3] = "player"
        self.board[3][4] = "computer"
        self.board[4][3] = "computer"
        self.board[4][4] = "player"

    def run_game(self):
        self.draw_initial_board()
        
        """Start the main loop for the game."""

        while True:
            #Watch for mouse events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            
            pygame.display.flip()

    def draw_initial_board(self):
        self.screen.fill(self.c_white)
        line_width = 150
        #Draw game grid
        for i in range(self.width):
            pygame.draw.line(self.screen, self.c_black, (i * 150, 0), (i * 150, 1200), 2)
            pygame.draw.line(self.screen, self.c_black, (0, i * 150), (1200, i * 150), 2)

        #Draw initial squares
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
        for row in range(self.height):
            for col in range(self.width):
                square = self.board[row][col]
                if square == "player":
                    self.draw_square(row, col, self.c_blue)
                elif square == "computer":
                    self.draw_square(row, col, self.c_red)

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