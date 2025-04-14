import pygame
import sys

# Initialize pygame modules
pygame.init()

# ---------- Constants and Setup ----------
# Screen dimensions
WIDTH, HEIGHT = 300, 300

# Line width for the grid
LINE_WIDTH = 5

# Board setup
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = WIDTH // 3

# Symbol sizes
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 20
SPACE = SQUARE_SIZE // 4  # Margin inside each square

# Colors (RGB)
BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (66, 66, 66)

# Create the screen window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")
screen.fill(BG_COLOR)

# ---------- Game State ----------
# 3x3 board initialized with None
board = [[None]*BOARD_COLS for _ in range(BOARD_ROWS)]

# ---------- Drawing Functions ----------

def draw_lines():
    """Draws the grid lines on the board."""
    for i in range(1, 3):
        # Horizontal lines
        pygame.draw.line(screen, LINE_COLOR, (0, i * SQUARE_SIZE), (WIDTH, i * SQUARE_SIZE), LINE_WIDTH)
        # Vertical lines
        pygame.draw.line(screen, LINE_COLOR, (i * SQUARE_SIZE, 0), (i * SQUARE_SIZE, HEIGHT), LINE_WIDTH)

def draw_figures():
    """Draws Xs and Os on the board based on the game state."""
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 'O':
                # Draw a circle for 'O'
                pygame.draw.circle(screen, CIRCLE_COLOR, (col * SQUARE_SIZE + SQUARE_SIZE//2, row * SQUARE_SIZE + SQUARE_SIZE//2), CIRCLE_RADIUS, CIRCLE_WIDTH)
            elif board[row][col] == 'X':
                # Draw two diagonal lines for 'X'
                start = (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE)
                end = (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE)
                pygame.draw.line(screen, CROSS_COLOR, start, end, CROSS_WIDTH)
                pygame.draw.line(screen, CROSS_COLOR, (end[0], start[1]), (start[0], end[1]), CROSS_WIDTH)

# ---------- Game Logic ----------

def check_win(player):
    """Returns True if the specified player has won."""
    # Check rows
    for row in board:
        if all(cell == player for cell in row):
            return True
    # Check columns
    for col in range(BOARD_COLS):
        if all(board[row][col] == player for row in range(BOARD_ROWS)):
            return True
    # Check diagonals
    if all(board[i][i] == player for i in range(BOARD_ROWS)) or all(board[i][BOARD_ROWS-i-1] == player for i in range(BOARD_ROWS)):
        return True
    return False

def check_tie():
    """Returns True if the board is full and no winner."""
    return all(cell is not None for row in board for cell in row)

def restart_game():
    """Resets the game board and redraws the lines."""
    screen.fill(BG_COLOR)
    draw_lines()
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            board[row][col] = None

# ---------- Game Loop ----------
player = 'X'      # First player
game_over = False # Tracks if the game is finished

# Draw initial grid
draw_lines()

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # Exit the game
            pygame.quit()
            sys.exit()

        # Handle mouse clicks
        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mouseX = event.pos[0]  # X-coordinate
            mouseY = event.pos[1]  # Y-coordinate

            clicked_row = mouseY // SQUARE_SIZE
            clicked_col = mouseX // SQUARE_SIZE

            # If the square is empty
            if board[clicked_row][clicked_col] is None:
                board[clicked_row][clicked_col] = player

                # Check win or tie
                if check_win(player):
                    print(f"{player} wins!")
                    game_over = True
                elif check_tie():
                    print("It's a tie!")
                    game_over = True

                # Switch player
                player = 'O' if player == 'X' else 'X'

        # Handle key press to restart
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                restart_game()
                player = 'X'
                game_over = False

    # Draw the updated board
    draw_figures()
    pygame.display.update()
