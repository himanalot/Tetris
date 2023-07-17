import pygame
import random

pygame.font.init()

# window size
WINDOW_WIDTH = 300
WINDOW_HEIGHT = 600

# board size
BOARD_WIDTH = 10
BOARD_HEIGHT = 20

# block size
BLOCK_SIZE = WINDOW_WIDTH // BOARD_WIDTH

# shapes of the tetrominoes
SHAPES = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[1, 1, 0], [0, 1, 1]],
    [[0, 1, 1], [1, 1]],
    [[1, 1, 1], [0, 1, 0]],
    [[1, 1, 0], [0, 1, 0], [0, 1, 0]],
    [[0, 1, 0], [1, 1, 1], [0, 1, 0]]
]

# colors of the tetrominoes
COLORS = [
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
    (255, 255, 0),
    (255, 0, 255),
    (0, 255, 255),
    (128, 128, 128)
]

class Tetris:
    def __init__(self, board_width=BOARD_WIDTH, board_height=BOARD_HEIGHT, block_size=BLOCK_SIZE):
        self.board_width = board_width
        self.board_height = board_height
        self.block_size = block_size
        self.board = [[0] * board_width for _ in range(board_height)]
        self.score = 0
        self.is_game_over = False
        self.current_piece = self.get_new_piece()
        self.back_to_back_tetris = False

    def get_new_piece(self):
        piece_shape = random.choice(SHAPES)
        piece_color = COLORS[SHAPES.index(piece_shape)]
        piece_position = [self.board_width // 2 - len(piece_shape[0]) // 2, 0]
        return [piece_position, piece_shape, piece_color]

    def collision_check(self, dx=0, dy=0, rotated_piece=None):
        piece_position = [self.current_piece[0][0] + dx, self.current_piece[0][1] + dy]
        if rotated_piece is None:
            rotated_piece = self.current_piece[1]
        for y, row in enumerate(rotated_piece):
            for x, block in enumerate(row):
                if block and (x + piece_position[0] < 0 or x + piece_position[0] >= self.board_width or y + piece_position[1] >= self.board_height or self.board[y + piece_position[1]][x + piece_position[0]]):
                    return True
        return False

    def rotate_piece(self):
        rotated_piece = [list(x[::-1]) for x in zip(*self.current_piece[1])]
        if not self.collision_check(rotated_piece=rotated_piece):
            self.current_piece[1] = rotated_piece

    def move_piece(self, dx, dy):
        if not self.collision_check(dx, dy):
            self.current_piece[0][0] += dx
            self.current_piece[0][1] += dy

    def drop_piece(self):
        if not self.collision_check(dy=1):
            self.current_piece[0][1] += 1
        else:
            self.lock_piece()
            cleared_lines = self.clear_lines()
            self.update_score(cleared_lines)
            if any(self.board[0]):  # check if any block has reached the top row
                self.is_game_over = True
            else:
                self.current_piece = self.get_new_piece()

    def lock_piece(self):
        for y, row in enumerate(self.current_piece[1]):
            for x, block in enumerate(row):
                if block:
                    self.board[self.current_piece[0][1] + y][self.current_piece[0][0] + x] = self.current_piece[2]

    def clear_lines(self):
        cleared_lines = [i for i, row in enumerate(self.board) if all(row)]
        if cleared_lines:
            for line in cleared_lines:
                del self.board[line]
                self.board = [[0 for _ in range(self.board_width)]] + self.board
        return len(cleared_lines)

    def update_score(self, cleared_lines):
        if cleared_lines == 1:
            self.score += 100
            self.back_to_back_tetris = False
        elif cleared_lines == 4:
            self.score += 800 if not self.back_to_back_tetris else 1200
            self.back_to_back_tetris = True
        else:
            self.back_to_back_tetris = False

    def draw_board(self, window):
        for y, row in enumerate(self.board):
            for x, block in enumerate(row):
                if block:
                    pygame.draw.rect(window, block, (x * self.block_size, y * self.block_size, self.block_size, self.block_size), 0)
        if not self.is_game_over:
            for y, row in enumerate(self.current_piece[1]):
                for x, block in enumerate(row):
                    if block:
                        pygame.draw.rect(window, self.current_piece[2], ((self.current_piece[0][0] + x) * self.block_size, (self.current_piece[0][1] + y) * self.block_size, self.block_size, self.block_size), 0)

def draw_score(window, score):
    font = pygame.font.Font(None, 36)
    text = font.render('Score: ' + str(score), 1, (255, 255, 255))
    window.blit(text, (WINDOW_WIDTH - 150, 20))

def draw_game_over(window, score):
    font = pygame.font.Font(None, 64)
    text1 = font.render('Game Over', 1, (255, 0, 0))
    text2 = font.render('Score: ' + str(score), 1, (255, 255, 255))
    window.blit(text1, (WINDOW_WIDTH // 2 - text1.get_width() // 2, WINDOW_HEIGHT // 2 - text1.get_height() // 2))
    window.blit(text2, (WINDOW_WIDTH // 2 - text2.get_width() // 2, WINDOW_HEIGHT // 2 + text1.get_height() // 2))

def main():
    pygame.init()
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pygame.time.Clock()
    game = Tetris()

    while True:
        if game.is_game_over:
            draw_game_over(window, game.score)
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        game.rotate_piece()
                    elif event.key == pygame.K_DOWN:
                        game.move_piece(0, 1)
                    elif event.key == pygame.K_LEFT:
                        game.move_piece(-1, 0)
                    elif event.key == pygame.K_RIGHT:
                        game.move_piece(1, 0)
            game.drop_piece()
            window.fill((0, 0, 0))
            game.draw_board(window)
            draw_score(window, game.score)
        pygame.display.flip()
        clock.tick(5)

if __name__ == '__main__':
    main()
