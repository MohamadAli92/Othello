import pygame
import sys

# Initialize Pygame
pygame.init()
pygame.mixer.init()  # Initialize the mixer module for playing sounds

# Load music and set it to play
pygame.mixer.music.load("music.mp3")
pygame.mixer.music.play(-1)  # Play the music indefinitely

# Set up the game window
BOARD_SIZE = 8
SQUARE_SIZE = 60
WINDOW_SIZE = BOARD_SIZE * SQUARE_SIZE
PANEL_HEIGHT = 100
WINDOW_TOTAL_SIZE = WINDOW_SIZE + PANEL_HEIGHT
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 128, 0)
BUTTON_HOVER_COLOR = (150, 150, 150)  # Lighter gray for button hover

# Define new color scheme
BACKGROUND_COLOR = (0x1E, 0x1E, 0x1E)  # Dark Grey background
BOARD_COLOR = (0x4A, 0x4A, 0x4A)  # Dark Grey for the board
VALID_MOVE_COLOR = (0x5C, 0xF4, 0x7F)  # Soft green for valid moves
BUTTON_COLOR = (0x2D, 0xD6, 0xF5)  # Soft Blue for buttons
BUTTON_HOVER_COLOR = (0x1F, 0x9D, 0xF4)  # Hover effect for the button
TEXT_COLOR = (0x00, 0x00, 0x00)  # Light Text Color
TITLE_COLOR = (0x00, 0x00, 0x00)  # Warm orange for titles

# Set up the display
window = pygame.display.set_mode((WINDOW_SIZE, WINDOW_TOTAL_SIZE))
pygame.display.set_caption("Othello")

# Load custom font
font = pygame.font.Font("OpenSans-Regular.ttf", 28)
small_font = pygame.font.Font("OpenSans-Regular.ttf", 18)

# Load custom images
background_image = pygame.image.load('bg.jpg')  # Place your background image here
# difficulty = "easy"

# Define selected_mode globally at the beginning of the script
selected_mode = None  # This will be set to 'two_player', 'ai', or 'settings' depending on user choice
sound_on = True


# Define the board
def init_board():
    global board, player
    board = [[' ' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    board[3][3], board[4][4] = 'W', 'W'
    board[3][4], board[4][3] = 'B', 'B'
    player = 'B'


# In draw_menu function
def draw_menu():
    global selected_mode  # Ensure selected_mode is accessible

    while True:
        window.blit(background_image, (0, 0))  # Draw the background image

        title_surface = font.render("Othello Game", True, TITLE_COLOR)
        title_rect = title_surface.get_rect(center=(WINDOW_SIZE / 2, WINDOW_SIZE / 4))
        window.blit(title_surface, title_rect)

        two_player_button = pygame.Rect(WINDOW_SIZE / 2 - 100, WINDOW_SIZE / 2 - 30, 200, 60)
        ai_button = pygame.Rect(WINDOW_SIZE / 2 - 100, WINDOW_SIZE / 2 + 40, 200, 60)
        go_back_button = pygame.Rect(WINDOW_SIZE / 2 - 100, WINDOW_SIZE / 2 + 110, 200, 60)  # New go back button

        # Define button color based on hover
        mouse_pos = pygame.mouse.get_pos()
        two_player_color = BUTTON_HOVER_COLOR if two_player_button.collidepoint(mouse_pos) else BUTTON_COLOR
        ai_color = BUTTON_HOVER_COLOR if ai_button.collidepoint(mouse_pos) else BUTTON_COLOR
        go_back_color = BUTTON_HOVER_COLOR if go_back_button.collidepoint(mouse_pos) else BUTTON_COLOR

        pygame.draw.rect(window, two_player_color, two_player_button,
                         border_radius=12)  # Rounded corners for the button
        pygame.draw.rect(window, ai_color, ai_button, border_radius=12)  # Rounded corners for the button
        pygame.draw.rect(window, go_back_color, go_back_button, border_radius=12)  # Draw go back button

        two_player_text = small_font.render("Two Player Mode", True, TEXT_COLOR)
        ai_text = small_font.render("Play with AI Mode", True, TEXT_COLOR)
        go_back_text = small_font.render("Go Back", True, TEXT_COLOR)  # Go Back button text

        window.blit(two_player_text, two_player_text.get_rect(center=two_player_button.center))
        window.blit(ai_text, ai_text.get_rect(center=ai_button.center))
        window.blit(go_back_text, go_back_text.get_rect(center=go_back_button.center))  # Render go back button text

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONUP:
                if two_player_button.collidepoint(event.pos):
                    selected_mode = 'two_player'
                    start_new_game()  # Start a new game in two-player mode
                elif ai_button.collidepoint(event.pos):
                    selected_mode = 'ai'
                    start_new_game()  # Start a new game in AI mode
                elif go_back_button.collidepoint(event.pos):
                    return  # Go back to the main menu


# Draw the board
def draw_board(valid_moves, next_move_button=None):
    window.blit(background_image, (0, 0))  # Draw the background image

    for x in range(BOARD_SIZE):
        for y in range(BOARD_SIZE):
            rect = pygame.Rect(x * SQUARE_SIZE, y * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            pygame.draw.rect(window, BOARD_COLOR, rect)
            pygame.draw.rect(window, BLACK, rect, 1)  # Draw the grid lines
            if board[y][x] == 'W':
                pygame.draw.circle(window, WHITE, rect.center, SQUARE_SIZE // 2 - 4)
            elif board[y][x] == 'B':
                pygame.draw.circle(window, BLACK, rect.center, SQUARE_SIZE // 2 - 4)
            elif (y, x) in valid_moves:
                pygame.draw.circle(window, VALID_MOVE_COLOR if rect.collidepoint(
                    pygame.mouse.get_pos()) else BUTTON_HOVER_COLOR, rect.center, SQUARE_SIZE // 8)

    # Draw the panel
    pygame.draw.rect(window, WHITE, pygame.Rect(0, WINDOW_SIZE, WINDOW_SIZE, PANEL_HEIGHT))

    if not next_move_button:  # Only show the turn information if there is no next_move_button
        # Show whose turn it is
        turn_text = f"Current Turn: {'Black' if player == 'B' else 'White'}"
        turn_surface = font.render(turn_text, True, TEXT_COLOR)
        turn_rect = turn_surface.get_rect(center=(WINDOW_SIZE / 2, WINDOW_SIZE + PANEL_HEIGHT / 2))
        window.blit(turn_surface, turn_rect)

    if next_move_button:
        pygame.draw.rect(window, BUTTON_COLOR, next_move_button, border_radius=12)  # Rounded corners for the button
        button_text = small_font.render("Next Move", True, TEXT_COLOR)
        button_rect = button_text.get_rect(center=next_move_button.center)
        window.blit(button_text, button_rect)

    pygame.display.flip()


# Get the square under the mouse
def get_square_under_mouse():
    mouse_pos = pygame.mouse.get_pos()
    return mouse_pos[0] // SQUARE_SIZE, mouse_pos[1] // SQUARE_SIZE


# Check if a move is valid
def is_valid_move(board, row, col, player):
    if board[row][col] != ' ':
        return False
    opponent = 'B' if player == 'W' else 'W'
    valid = False
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
    for d in directions:
        x, y = row + d[0], col + d[1]
        while 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE and board[x][y] == opponent:
            x += d[0]
            y += d[1]
        if 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE and board[x][y] == player and (
                x - d[0] != row or y - d[1] != col):
            valid = True
    return valid


# Apply a move to the board
def apply_move(board, row, col, player):
    opponent = 'B' if player == 'W' else 'W'
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
    board[row][col] = player
    for d in directions:
        x, y = row + d[0], col + d[1]
        pieces_to_flip = []
        while 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE and board[x][y] == opponent:
            pieces_to_flip.append((x, y))
            x += d[0]
            y += d[1]
        if 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE and board[x][y] == player and (
                x - d[0] != row or y - d[1] != col):
            for flip_x, flip_y in pieces_to_flip:
                board[flip_x][flip_y] = player


# Get all valid moves for a player
def get_all_valid_moves(board, player):
    valid_moves = []
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if is_valid_move(board, row, col, player):
                valid_moves.append((row, col))
    return valid_moves


# Check if the game is over
def is_game_over(board):
    return not get_all_valid_moves(board, 'W') and not get_all_valid_moves(board, 'B')


# Count disks for each player
def count_disks(board):
    white_count = sum(row.count('W') for row in board)
    black_count = sum(row.count('B') for row in board)
    return white_count, black_count


# Display the winner at the end
def draw_button(text, center_pos, color, hover_color):
    button_text = small_font.render(text, True, TEXT_COLOR)
    button_rect = button_text.get_rect(center=center_pos)
    mouse_pos = pygame.mouse.get_pos()
    button_color = hover_color if button_rect.collidepoint(mouse_pos) else color

    pygame.draw.rect(window, button_color, button_rect.inflate(20, 20), border_radius=12)
    window.blit(button_text, button_rect)
    return button_rect

def display_winner():
    while True:
        window.blit(background_image, (0, 0))  # Draw the background image

        white_count, black_count = count_disks(board)
        winner_text = ""
        if black_count > white_count:
            winner_text = "Black Wins!"
        elif white_count > black_count:
            winner_text = "White Wins!"
        else:
            winner_text = "It's a Tie!"

        winner_surface = font.render(winner_text, True, TITLE_COLOR)
        winner_rect = winner_surface.get_rect(center=(WINDOW_SIZE / 2, WINDOW_SIZE / 2 - 50))
        window.blit(winner_surface, winner_rect)

        score_surface = small_font.render(f"Black: {black_count}  White: {white_count}", True, TEXT_COLOR)
        score_rect = score_surface.get_rect(center=(WINDOW_SIZE / 2, WINDOW_SIZE / 2 + 50))
        window.blit(score_surface, score_rect)

        button_rect = draw_button("Back to Menu", (WINDOW_SIZE / 2, WINDOW_SIZE / 2 + 175), BUTTON_COLOR, BUTTON_HOVER_COLOR)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    return  # Go back to the main menu
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Press Escape to go back to the main menu
                    return


difficulty = 'easy'  # Default to easy difficulty


# Minimax algorithm for AI mode
def minimax(board, depth, is_maximizing, alpha, beta):
    if depth == 0 or is_game_over(board):
        white_count, black_count = count_disks(board)
        return (black_count - white_count, None) if is_maximizing else (white_count - black_count, None)

    valid_moves = get_all_valid_moves(board, 'W' if is_maximizing else 'B')
    if not valid_moves:
        if is_game_over(board):
            white_count, black_count = count_disks(board)
            return (black_count - white_count, None) if is_maximizing else (white_count - black_count, None)
        return minimax(board, depth - 1, not is_maximizing, alpha, beta)

    best_move = None
    if is_maximizing:
        best_score = -float('inf')
        for move in valid_moves:
            temp_board = [row[:] for row in board]
            apply_move(temp_board, move[0], move[1], 'W')
            score, _ = minimax(temp_board, depth - 1, False, alpha, beta)
            if score > best_score:
                best_score = score
                best_move = move
            alpha = max(alpha, best_score)
            if beta <= alpha:
                break
        return best_score, best_move
    else:
        best_score = float('inf')
        for move in valid_moves:
            temp_board = [row[:] for row in board]
            apply_move(temp_board, move[0], move[1], 'B')
            score, _ = minimax(temp_board, depth - 1, True, alpha, beta)
            if score < best_score:
                best_score = score
                best_move = move
            beta = min(beta, best_score)
            if beta <= alpha:
                break
        return best_score, best_move


def draw_settings():
    global difficulty  # Ensure difficulty is accessible
    global sound_on  # Ensure sound_on is accessible

    while True:
        window.blit(background_image, (0, 0))  # Draw the background image

        # Render settings title
        settings_title_surface = font.render("Settings", True, TITLE_COLOR)
        settings_title_rect = settings_title_surface.get_rect(center=(WINDOW_SIZE / 2, WINDOW_SIZE / 4))
        window.blit(settings_title_surface, settings_title_rect)

        # Define settings buttons
        sound_button = pygame.Rect(WINDOW_SIZE / 2 - 100, WINDOW_SIZE / 2 - 30, 200, 60)
        difficulty_button = pygame.Rect(WINDOW_SIZE / 2 - 100, WINDOW_SIZE / 2 + 40, 200, 60)
        back_button = pygame.Rect(WINDOW_SIZE / 2 - 100, WINDOW_SIZE / 2 + 110, 200, 60)  # Back button

        # Set button colors based on hover state
        mouse_pos = pygame.mouse.get_pos()
        sound_color = BUTTON_HOVER_COLOR if sound_button.collidepoint(mouse_pos) else BUTTON_COLOR
        difficulty_color = BUTTON_HOVER_COLOR if difficulty_button.collidepoint(mouse_pos) else BUTTON_COLOR
        back_color = BUTTON_HOVER_COLOR if back_button.collidepoint(mouse_pos) else BUTTON_COLOR

        pygame.draw.rect(window, sound_color, sound_button, border_radius=12)
        pygame.draw.rect(window, difficulty_color, difficulty_button, border_radius=12)
        pygame.draw.rect(window, back_color, back_button, border_radius=12)

        # Render button texts
        sound_text = small_font.render(f"Sound: {'On' if sound_on else 'Off'}", True, TEXT_COLOR)
        difficulty_text = small_font.render(f"Difficulty: {difficulty.capitalize()}", True, TEXT_COLOR)
        back_text = small_font.render("Go Back", True, TEXT_COLOR)  # Updated text for the back button

        window.blit(sound_text, sound_text.get_rect(center=sound_button.center))
        window.blit(difficulty_text, difficulty_text.get_rect(center=difficulty_button.center))
        window.blit(back_text, back_text.get_rect(center=back_button.center))  # Render the back button text

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONUP:
                if sound_button.collidepoint(event.pos):
                    # Toggle the sound setting
                    sound_on = not sound_on
                    pygame.mixer.music.set_volume(1.0 if sound_on else 0.0)  # Update music volume based on sound_on
                elif difficulty_button.collidepoint(event.pos):
                    # Cycle through difficulty levels
                    if difficulty == 'easy':
                        difficulty = 'medium'
                    elif difficulty == 'medium':
                        difficulty = 'hard'
                    else:
                        difficulty = 'easy'
                elif back_button.collidepoint(event.pos):
                    return  # Exit the settings menu and return to the main menu



# Main menu
def main_menu():
    global selected_mode  # Add this line to ensure selected_mode is available

    while True:
        window.blit(background_image, (0, 0))  # Draw the background image

        # Render menu title
        title_surface = font.render("Reversi", True, TITLE_COLOR)
        title_rect = title_surface.get_rect(center=(WINDOW_SIZE / 2, WINDOW_SIZE / 4))
        window.blit(title_surface, title_rect)

        # Menu options
        new_game_button = pygame.Rect(WINDOW_SIZE / 2 - 100, WINDOW_SIZE / 2 - 30, 200, 60)
        settings_button = pygame.Rect(WINDOW_SIZE / 2 - 100, WINDOW_SIZE / 2 + 40, 200, 60)
        quit_button = pygame.Rect(WINDOW_SIZE / 2 - 100, WINDOW_SIZE / 2 + 110, 200, 60)

        # Button colors
        mouse_pos = pygame.mouse.get_pos()
        new_game_color = BUTTON_HOVER_COLOR if new_game_button.collidepoint(mouse_pos) else BUTTON_COLOR
        settings_color = BUTTON_HOVER_COLOR if settings_button.collidepoint(mouse_pos) else BUTTON_COLOR
        quit_color = BUTTON_HOVER_COLOR if quit_button.collidepoint(mouse_pos) else BUTTON_COLOR

        pygame.draw.rect(window, new_game_color, new_game_button, border_radius=12)
        pygame.draw.rect(window, settings_color, settings_button, border_radius=12)
        pygame.draw.rect(window, quit_color, quit_button, border_radius=12)

        # Render button texts
        new_game_text = small_font.render("New Game", True, TEXT_COLOR)
        settings_text = small_font.render("Settings", True, TEXT_COLOR)
        quit_text = small_font.render("Quit", True, TEXT_COLOR)

        window.blit(new_game_text, new_game_text.get_rect(center=new_game_button.center))
        window.blit(settings_text, settings_text.get_rect(center=settings_button.center))
        window.blit(quit_text, quit_text.get_rect(center=quit_button.center))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONUP:
                if new_game_button.collidepoint(event.pos):
                    draw_menu()  # Show the mode selection menu
                elif settings_button.collidepoint(event.pos):
                    draw_settings()  # Open the settings menu
                elif quit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()



# Start a new game
def start_new_game():
    global selected_mode, player, valid_moves, next_move_button

    # Initialize the board and set the starting player
    init_board()
    player = 'B'  # Black starts

    # Get valid moves for the starting player
    valid_moves = get_all_valid_moves(board, player)

    # Update next_move_button based on the selected mode
    if selected_mode == 'ai' and player == 'W':
        next_move_button = pygame.Rect(WINDOW_SIZE / 2 - 70, WINDOW_SIZE + PANEL_HEIGHT / 2, 140, 50)
    else:
        next_move_button = None

    # Draw the initial state of the board
    draw_board(valid_moves, next_move_button)

    while True:
        valid_moves = get_all_valid_moves(board, player)  # Get valid moves for the current player

        if not valid_moves:
            player = 'W' if player == 'B' else 'B'
            valid_moves = get_all_valid_moves(board, player)
            if not valid_moves:
                if is_game_over(board):
                    display_winner()
                    break
                else:
                    continue

        # Update next_move_button based on the selected mode
        if selected_mode == 'ai' and player == 'W':
            next_move_button = pygame.Rect(WINDOW_SIZE / 2 - 70, WINDOW_SIZE + PANEL_HEIGHT / 3.5, 140, 50)
        else:
            next_move_button = None

        draw_board(valid_moves, next_move_button)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONUP:
                x, y = get_square_under_mouse()
                if selected_mode == 'two_player':
                    if (y, x) in valid_moves:
                        apply_move(board, y, x, player)
                        player = 'W' if player == 'B' else 'B'
                        valid_moves = get_all_valid_moves(board, player)
                        if is_game_over(board):
                            display_winner()
                            break
                elif selected_mode == 'ai':
                    if next_move_button and next_move_button.collidepoint(event.pos) and player == 'W':
                        # AI move
                        depth = 2 if difficulty == 'easy' else 4 if difficulty == 'medium' else 6
                        score, move = minimax(board, depth, True, -float('inf'), float('inf'))
                        if move:
                            apply_move(board, move[0], move[1], player)
                            player = 'B'
                            valid_moves = get_all_valid_moves(board, player)  # Update valid moves after AI move
                            draw_board(valid_moves, next_move_button)
                            if is_game_over(board):
                                display_winner()
                                break
                    elif (y, x) in valid_moves and player == 'B':
                        apply_move(board, y, x, player)
                        player = 'W'  # Change to AI's turn
                        valid_moves = get_all_valid_moves(board, player)
                        if is_game_over(board):
                            display_winner()
                            break
                    draw_board(valid_moves, next_move_button)  # Ensure the board updates with valid moves
                elif selected_mode == 'settings':
                    pass  # No actions in the game loop during settings mode


# Start the main loop
if __name__ == "__main__":
    main_menu()  # Show the main menu when the script is run
