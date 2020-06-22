import random
import pygame
import math
import sys
import numpy as np

BLUE = (0, 0, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

ROW_COUNT = 6
COLUMN_COUNT = 7

EVEN = 0
ODD = 1

# turns
PLAYER = 0
AI = 1

# Agent actions
PLAYER_PIECE = 1
AI_PIECE = 2


def create_Board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board


# Print_Board
# Flips the printed to better reflect an actual Connect4 board.
def print_Board(board):
    print(np.flip(board, 0))


# drop_piece function
# Drops piece in requested column
def drop_piece(board, row, column, player):
    board[row][column] = player


# valid_move
# Checks to see if the move requested is valid. Will return false if the player tries a number
# Greater than 6 or less than 0.
def valid_move(board, column):
    # Checks to see if the top row of that column hasn't been filled. True if empty, false if filled.
    # If this statement is true, then we are free to drop a piece
    return board[ROW_COUNT - 1][column] == 0


# getNextRow
def getNextRow(board, column):
    for row in range(ROW_COUNT):
        if board[row][column] == 0:
            return row


def get_valid_spot(board):
    valid_spot = []
    for column in range(COLUMN_COUNT):
        if valid_move(board, column):
            valid_spot.append(column)
    return valid_spot


# Evaluate Window function
def evaluate_window(window, piece):
    score = 0
    opp_piece = PLAYER_PIECE
    if piece == PLAYER_PIECE:
        opp_piece = AI_PIECE

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(0) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(0) == 2:
        score += 2

    if window.count(opp_piece) == 3 and window.count(0) == 1:
        score -= 4

    return score


# Winner function
# Checks to see if a Connect 4 has been found.
# Does not currently check for diagonal moves
# But functionality will be similar to vertical and horizontal checking
def Winner(board, player):
    # Check Horizontal Moves
    for column in range(COLUMN_COUNT - 3):
        for row in range(ROW_COUNT):
            if board[row][column] == player and board[row][column + 1] == player and board[row][column + 2] == player and board[row][column + 3] == player:
                return True
    # Check Vertical Moves
    for column in range(COLUMN_COUNT):
        for row in range(ROW_COUNT - 3):
            if board[row][column] == player and board[row + 1][column] == player and board[row + 2][column] == player and board[row + 3][column] == player:
                return True
    # check diagonal moves (up right)
    for column in range(COLUMN_COUNT - 3):
        for row in range(ROW_COUNT - 3):
            if board[row][column] == player and board[row + 1][column + 1] == player and board[row + 2][column + 2] == player and board[row + 3][column + 3] == player:
                return True
    # check diagonal moves (down left)
    for column in range(COLUMN_COUNT-3):
        for row in range(3, ROW_COUNT):
            if board[row][column] == player and board[row - 1][column + 1] == player and board[row - 2][column + 2] == player and board[row - 3][column + 3] == player:
                return True


# score move
# Scores move based tactical advantage
# For example, center moves are better because there's more options.
def score_move(board, piece):
    score = 0

    # Score center
    center_array = [int(i) for i in list(board[:, COLUMN_COUNT//2])]
    center_count = center_array.count(piece)
    score += center_count * 3

    # Score Horiztonal
    for row in range(ROW_COUNT):
        row_array = [int(i) for i in list(board[row, :])]
        for column in range(COLUMN_COUNT - 3):
            window = row_array[column:column + 4]
            score += evaluate_window(window, piece)
    # Score Vertical
    for column in range(COLUMN_COUNT):
        column_array = [int(i) for i in list(board[:, column])]
        for row in range(ROW_COUNT - 3):
            window = column_array[row:row + 4]
            score += evaluate_window(window, piece)
    # Score Diagonal (up right)
    for row in range(ROW_COUNT - 3):
        for column in range(COLUMN_COUNT - 3):
            window = [board[row + i][column + i] for i in range(4)]
            score += evaluate_window(window, piece)
    # Score Diagonal (down right)
    for row in range(ROW_COUNT - 3):
        for column in range(COLUMN_COUNT - 3):
            window = [board[row + 3 - i][column - i] for i in range(4)]
            score += evaluate_window(window, piece)
    return score


def node(board):
    return Winner(board, PLAYER_PIECE) or Winner(board, AI_PIECE) or len(get_valid_spot(board)) == 0


# optimal move function
# Returns the best column for the AI to make the move
# Bases its decision off the score in score_move
# Agent should prioritize
def optimal_move(board, piece):
    valid_spot = get_valid_spot(board)
    best_score = 1000
    best_column = random.choice(valid_spot)
    for column in valid_spot:
        row = getNextRow(board, column)
        temp_board = board.copy()
        drop_piece(temp_board, row, column, piece)
        score = score_move(temp_board, piece)
        if score > best_score:
            best_score = score
            best_column = column
    return best_column


# AI Agents
# Random Agent
# Randomly places a move with no thought put into it
# NOTE:Not finished, obviously. Decided for this version to just implement the Random Agent
# In main and finish the AI part later this week.
def Random(board, player):
    while True:
        i = random.randint(0, 6)
        return valid_move(board, i)


# MiniMax function
# Based on Pseudocode from Wikipedia
# maxPlayer will return False if we're looking at the player's moves and true when looking at the AI's.
def miniMax(board, depth, maxPlayer):
    valid_spot = get_valid_spot(board)
    is_node = node(board)
    # Left node
    if depth == 0 or is_node:
        if is_node:
            if Winner(board, AI_PIECE):
                return (None, 100000000000)
            elif Winner(board, PLAYER_PIECE):
                return (None, -100000000000)
            # No more moves to make
            # Game is over
            else:
                return (None, 0)
        # depth is zero
        else:
            return (None, score_move(board, AI_PIECE))
    if maxPlayer:
        value = -math.inf
        best_column = random.choice(valid_spot)
        for column in valid_spot:
            row = getNextRow(board, column)
            temp_board = board.copy()
            drop_piece(temp_board, row, column, AI_PIECE)
            score = miniMax(temp_board, depth - 1, False)[1]
            if score > value:
                value = score
                best_column = column
        return best_column, value
    else:  # Mini
        value = math.inf
        best_column = random.choice(valid_spot)
        for column in valid_spot:
            row = getNextRow(board, column)
            temp_board = board.copy()
            drop_piece(temp_board, row, column, PLAYER_PIECE)
            score = miniMax(temp_board, depth - 1, True)[1]
            if score < value:
                value = score
                best_column = column

        return best_column, value


def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (
                int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == PLAYER_PIECE:
                pygame.draw.circle(screen, RED, (
                    int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
            elif board[r][c] == AI_PIECE:
                pygame.draw.circle(screen, YELLOW, (
                    int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
    pygame.display.update()


board = create_Board()
print_Board(board)
game_over = False
turn = 0

pygame.init()

SQUARESIZE = 100
RADIUS = int(SQUARESIZE / 2 - 5)
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT + 1) * SQUARESIZE

myfont = pygame.font.SysFont("monospace", 75)

size = (width, height)

screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

# While game_over is false
# If game_over becomes true, the loop ends
while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
            posx = event.pos[0]
            if turn == PLAYER_PIECE:
                pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE / 2)), RADIUS)
        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
            # Player 1
            if turn == PLAYER:
                posx = event.pos[0]
                column = int(math.floor(posx / SQUARESIZE))
                if (valid_move(board, column)):
                    row = getNextRow(board, column)
                    drop_piece(board, row, column, PLAYER_PIECE)
                    if (Winner(board, PLAYER_PIECE)):
                        message = myfont.render("Humans win!", 1, RED)
                        screen.blit(message, (40, 10))
                        game_over = True
                        print_Board(board)
                        draw_board(board)
                        pygame.time.wait(5000)
                    # When turn is odd, it's player 2's turn. When zero, it's player 1's
                    turn += 1
                    turn = turn % 2
                    print_Board(board)
                    draw_board(board)
            # else:
            #     posx = event.pos[0]
            #     column = int(math.floor(posx/SQUARESIZE))
            #
            #     if valid_move(board, column):
            #         row = getNextRow(board, column)
            #         drop_piece(board, row, column, AI_PIECE)
            #         if(Winner(board, PLAYER_PIECE)):
            #             message = myfront.render("Robots win and killed us all!", 1, YELLOW)
            #             screen.blit(message,(40,10))
            #             game_over = True
            #         turn +=1
            #         turn = turn%2
            #         print_Board(board)
            #         draw_board(board)

    if turn == AI:
        # Need two variables here in order to unpack the tuple. Otherwie you will get some nasty errors
        # In regards to indices
        column, minimax_score = miniMax(board, 3, True)
        # column = optimal_move(board, AI_PIECE)
        if valid_move(board, column):
            row = getNextRow(board, column)
            drop_piece(board, row, column, AI_PIECE)

            if Winner(board, AI_PIECE):
                label = myfont.render("Robots won!", 1, YELLOW)
                screen.blit(label, (40, 10))
                game_over = True
                print_Board(board)
                draw_board(board)
                pygame.time.wait(5000)
            print_Board(board)
            draw_board(board)

            turn += 1
            turn = turn % 2

    # if turn == AI:

    # Asks for player 1 input
    # if turn == 0:
    #     column = int(input("Player 1, make your move. (0-6):"))
    #     if valid_move(board, column):
    #         row = getNextRow(board, column)
    #         drop_piece(board, row, column, 1)
    #
    #         if Winner(board, 1):
    #             print("Player 1 Wins!")
    #             game_over = True
    #
    #
    # #Asks for Player 2 input
    # else:
    #     #column = int(input("Player 2, make your move. (0-6):"))
    #     #Implements a random agent. Will just place random moves.
    #     i = random.randint(0,6)
    #     if valid_move(board, i):
    #         row = getNextRow(board, i)
    #         drop_piece(board, row, i, 2)
    #
    #         if Winner(board, 2):
    #             print("Player 2 Wins!")
    #             game_over = True