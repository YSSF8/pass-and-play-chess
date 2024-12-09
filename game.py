import pygame
import sys
import copy

pygame.init()

# Screen dimensions and constants
WIDTH, HEIGHT = 640, 640
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Pass-and-Play Chess')

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_BROWN = (222, 184, 135)
DARK_BROWN = (139, 69, 19)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 102)
RED = (255, 0, 0)

# Fonts
FONT = pygame.font.SysFont('arial', 48)
LARGE_FONT = pygame.font.SysFont('arial', 72)

# Piece representations
PIECE_LETTERS = {
    ('white', 'king'): 'K',
    ('white', 'queen'): 'Q',
    ('white', 'rook'): 'R',
    ('white', 'bishop'): 'B',
    ('white', 'knight'): 'N',
    ('white', 'pawn'): 'P',
    ('black', 'king'): 'K',
    ('black', 'queen'): 'Q',
    ('black', 'rook'): 'R',
    ('black', 'bishop'): 'B',
    ('black', 'knight'): 'N',
    ('black', 'pawn'): 'P',
}

class Piece:
    def __init__(self, color, kind):
        self.color = color  # 'white' or 'black'
        self.kind = kind    # 'pawn', 'rook', 'knight', 'bishop', 'queen', 'king'

def create_board():
    board = [[None for _ in range(COLS)] for _ in range(ROWS)]

    # Place black pieces
    board[0][0] = Piece('black', 'rook')
    board[0][1] = Piece('black', 'knight')
    board[0][2] = Piece('black', 'bishop')
    board[0][3] = Piece('black', 'queen')
    board[0][4] = Piece('black', 'king')
    board[0][5] = Piece('black', 'bishop')
    board[0][6] = Piece('black', 'knight')
    board[0][7] = Piece('black', 'rook')
    for i in range(COLS):
        board[1][i] = Piece('black', 'pawn')

    # Place white pieces
    board[7][0] = Piece('white', 'rook')
    board[7][1] = Piece('white', 'knight')
    board[7][2] = Piece('white', 'bishop')
    board[7][3] = Piece('white', 'queen')
    board[7][4] = Piece('white', 'king')
    board[7][5] = Piece('white', 'bishop')
    board[7][6] = Piece('white', 'knight')
    board[7][7] = Piece('white', 'rook')
    for i in range(COLS):
        board[6][i] = Piece('white', 'pawn')

    return board

def draw_board(screen, selected_square=None, valid_moves=None, last_move=None):
    for row in range(ROWS):
        for col in range(COLS):
            # Determine the square color
            if (row + col) % 2 == 0:
                color = LIGHT_BROWN
            else:
                color = DARK_BROWN

            # Highlight squares involved in the last move
            if last_move and (row, col) in last_move:
                color = YELLOW

            rect = pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            pygame.draw.rect(screen, color, rect)

    if valid_moves:
        # Highlight valid moves in green
        for move in valid_moves:
            row, col = move
            rect = pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            pygame.draw.rect(screen, GREEN, rect, 3)

    if selected_square:
        row, col = selected_square
        rect = pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
        pygame.draw.rect(screen, BLUE, rect, 3)

def render_text_with_outline(text, font, text_color, outline_color):
    base = font.render(text, True, text_color)
    # Create a new Surface with transparent background
    size = (base.get_width() + 2, base.get_height() + 2)
    img = pygame.Surface(size, pygame.SRCALPHA)

    # Render outline by blitting the text shifted in 8 directions
    for dx, dy in [(-1,0), (1,0), (0,-1), (0,1), (-1,-1), (-1,1), (1,-1), (1,1)]:
        img.blit(font.render(text, True, outline_color), (dx + 1, dy + 1))
    # Blit the main text
    img.blit(base, (1,1))

    return img

def draw_pieces(screen, board):
    for row in range(ROWS):
        for col in range(COLS):
            piece = board[row][col]
            if piece is not None:
                piece_text = PIECE_LETTERS[(piece.color, piece.kind)]
                text_color = BLACK if piece.color == 'black' else WHITE
                outline_color = WHITE if piece.color == 'black' else BLACK
                text_surface = render_text_with_outline(piece_text, FONT, text_color, outline_color)
                text_rect = text_surface.get_rect(center=(
                    col * SQUARE_SIZE + SQUARE_SIZE // 2,
                    row * SQUARE_SIZE + SQUARE_SIZE // 2))
                screen.blit(text_surface, text_rect)

def is_valid_move(board, piece, start_pos, end_pos, turn):
    # First, check if the basic movement rules allow the move
    if not basic_move_rules(board, piece, start_pos, end_pos):
        return False

    # Create a deep copy of the board and make the move to test for check
    board_copy = copy.deepcopy(board)
    board_copy[end_pos[0]][end_pos[1]] = piece
    board_copy[start_pos[0]][start_pos[1]] = None

    if is_in_check(board_copy, turn):
        # Move would leave the king in check
        return False

    return True

def basic_move_rules(board, piece, start_pos, end_pos):
    start_row, start_col = start_pos
    end_row, end_col = end_pos
    delta_row = end_row - start_row
    delta_col = end_col - start_col

    if end_row < 0 or end_row >= ROWS or end_col < 0 or end_col >= COLS:
        # Move is off the board
        return False

    if board[end_row][end_col] and board[end_row][end_col].color == piece.color:
        # Cannot capture own piece
        return False

    if piece.kind == 'pawn':
        direction = -1 if piece.color == 'white' else 1
        start_row_pawn = 6 if piece.color == 'white' else 1

        if delta_col == 0:
            # Moving forward
            if delta_row == direction:
                if board[end_row][end_col] is None:
                    return True
            elif delta_row == 2 * direction and start_row == start_row_pawn:
                # First move, can move two squares
                intermediate_row = start_row + direction
                if board[end_row][end_col] is None and board[intermediate_row][end_col] is None:
                    return True
        elif abs(delta_col) == 1 and delta_row == direction:
            # Capturing
            if board[end_row][end_col] is not None and board[end_row][end_col].color != piece.color:
                return True
        return False

    elif piece.kind == 'rook':
        if delta_row == 0 or delta_col == 0:
            # Check if path is clear
            step_row = 0 if delta_row == 0 else int(delta_row / abs(delta_row))
            step_col = 0 if delta_col == 0 else int(delta_col / abs(delta_col))
            current_row, current_col = start_row + step_row, start_col + step_col
            while (current_row, current_col) != (end_row, end_col):
                if board[current_row][current_col] is not None:
                    return False
                current_row += step_row
                current_col += step_col
            return True
        return False

    elif piece.kind == 'bishop':
        if abs(delta_row) == abs(delta_col):
            # Check if path is clear
            step_row = int(delta_row / abs(delta_row))
            step_col = int(delta_col / abs(delta_col))
            current_row, current_col = start_row + step_row, start_col + step_col
            while (current_row, current_col) != (end_row, end_col):
                if board[current_row][current_col] is not None:
                    return False
                current_row += step_row
                current_col += step_col
            return True
        return False

    elif piece.kind == 'queen':
        if delta_row == 0 or delta_col == 0 or abs(delta_row) == abs(delta_col):
            # Combine rook and bishop movements
            if delta_row == 0:
                step_row = 0
            else:
                step_row = int(delta_row / abs(delta_row))
            if delta_col == 0:
                step_col = 0
            else:
                step_col = int(delta_col / abs(delta_col))
            current_row, current_col = start_row + step_row, start_col + step_col
            while (current_row, current_col) != (end_row, end_col):
                if board[current_row][current_col] is not None:
                    return False
                current_row += step_row
                current_col += step_col
            return True
        return False

    elif piece.kind == 'king':
        if abs(delta_row) <= 1 and abs(delta_col) <= 1:
            return True
        return False

    elif piece.kind == 'knight':
        if (abs(delta_row), abs(delta_col)) in [(1, 2), (2, 1)]:
            return True
        return False

    return False

def get_all_valid_moves(board, color):
    all_moves = []
    for row in range(ROWS):
        for col in range(COLS):
            piece = board[row][col]
            if piece and piece.color == color:
                moves = get_valid_moves(board, piece, (row, col), color)
                if moves:
                    all_moves.extend(moves)
    return all_moves

def get_valid_moves(board, piece, position, turn):
    valid_moves = []
    for row in range(ROWS):
        for col in range(COLS):
            if is_valid_move(board, piece, position, (row, col), turn):
                valid_moves.append((row, col))
    return valid_moves

def find_king(board, color):
    for row in range(ROWS):
        for col in range(COLS):
            piece = board[row][col]
            if piece and piece.color == color and piece.kind == 'king':
                return (row, col)
    return None

def is_in_check(board, color):
    king_pos = find_king(board, color)
    if not king_pos:
        # King is not on the board (this should not happen)
        return True

    for row in range(ROWS):
        for col in range(COLS):
            piece = board[row][col]
            if piece and piece.color != color:
                if basic_move_rules(board, piece, (row, col), king_pos):
                    return True
    return False

def is_checkmate(board, color):
    if not is_in_check(board, color):
        return False
    # Check if any move can get the king out of check
    for row in range(ROWS):
        for col in range(COLS):
            piece = board[row][col]
            if piece and piece.color == color:
                moves = get_valid_moves(board, piece, (row, col), color)
                if moves:
                    return False  # There is at least one move to get out of check
    return True  # No moves can get the king out of check

def display_winner(screen, winner_color):
    screen.fill(BLACK)
    # Display winner message
    winner_text = f"{winner_color.capitalize()} Wins!"
    text_surface = LARGE_FONT.render(winner_text, True, WHITE)
    text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    screen.blit(text_surface, text_rect)

    # Display replay button
    button_text = "Replay"
    button_surface = FONT.render(button_text, True, BLACK)
    button_rect = button_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
    button_background = pygame.Rect(button_rect.left - 10, button_rect.top - 10,
                                    button_rect.width + 20, button_rect.height + 20)
    pygame.draw.rect(screen, WHITE, button_background)
    screen.blit(button_surface, button_rect)

    pygame.display.flip()

    # Wait for user to click replay
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if button_background.collidepoint(pos):
                    waiting = False  # Exit the loop to restart the game

def main():
    while True:
        board = create_board()
        selected_piece = None
        valid_moves = None
        running = True
        turn = 'white'  # White moves first
        game_over = False
        last_move = None  # Stores the last move squares as a tuple ((from_row, from_col), (to_row, to_col))

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                    pos = pygame.mouse.get_pos()
                    col = pos[0] // SQUARE_SIZE
                    row = pos[1] // SQUARE_SIZE

                    if selected_piece:
                        # Move the selected piece
                        old_row, old_col = selected_piece
                        piece = board[old_row][old_col]
                        if piece and piece.color == turn:
                            if (row, col) in valid_moves:
                                board[row][col] = piece
                                board[old_row][old_col] = None
                                last_move = ((old_row, old_col), (row, col))  # Update last move
                                selected_piece = None
                                valid_moves = None

                                # Check for pawn promotion (simplified to always promote to queen)
                                if piece.kind == 'pawn':
                                    if (piece.color == 'white' and row == 0) or (piece.color == 'black' and row == 7):
                                        piece.kind = 'queen'

                                # Change turn
                                turn = 'black' if turn == 'white' else 'white'

                                # Check if the other player is in checkmate
                                if is_checkmate(board, turn):
                                    game_over = True
                                    display_winner(SCREEN, 'white' if turn == 'black' else 'black')
                                    break  # Exit the event loop

                            else:
                                # Invalid move or clicked elsewhere
                                selected_piece = None
                                valid_moves = None
                        else:
                            selected_piece = None
                            valid_moves = None
                    else:
                        if board[row][col] and board[row][col].color == turn:
                            selected_piece = (row, col)
                            piece = board[row][col]
                            valid_moves = get_valid_moves(board, piece, (row, col), turn)

                            if not valid_moves:
                                # No valid moves for this piece
                                selected_piece = None
                                valid_moves = None
                        else:
                            selected_piece = None
                            valid_moves = None

            if not game_over:
                # Highlight last move squares in yellow
                last_move_squares = None
                if last_move:
                    last_move_squares = last_move

                draw_board(SCREEN, selected_square=selected_piece, valid_moves=valid_moves, last_move=last_move_squares)
                draw_pieces(SCREEN, board)
                pygame.display.flip()
            else:
                # Game is over, wait for replay
                break  # Exit the game loop to start a new game

if __name__ == "__main__":
    main()
