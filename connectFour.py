import random
import pygame
import math
import sys
import numpy as np

ROW_COUNT = 6
COLUMN_COUNT = 7
EVEN = 0
ODD = 1

BLUE = (0,0,255)
BLACK = (0, 0, 0)
RED = (255,0,0)
YELLOW = (255,255,0)



def create_Board():
    board = np.zeros((ROW_COUNT,COLUMN_COUNT))
    return board

#Print_Board
#Flips the printed to better reflect an actual Connect4 board.
def print_Board(board):
    print(np.flip(board, 0))

#drop_piece function
#Drops piece in requested column
def drop_piece(board, row, column, player):
    board[row][column] = player

#valid_move
#Checks to see if the move requested is valid. Will return false if the player tries a number
#Greater than 6 or less than 0.
def valid_move(board, column):
    #Checks to see if the top row of that column hasn't been filled. True if empty, false if filled.
    #If this statement is true, then we are free to drop a piece
    return board[ROW_COUNT-1][column] == 0

#getNextRow
def getNextRow(board, column):
    for row in range(ROW_COUNT):
        if board[row][column] == 0:
            return row
#Winner function
#Checks to see if a Connect 4 has been found.
#Does not currently check for diagonal moves
#But functionality will be similar to vertical and horizontal checking
def Winner(board, player):
    #Check Horizontal Moves
    for column in range(COLUMN_COUNT-3):
        for row in range(ROW_COUNT):
            if board[row][column] == player and board[row][column+1] == player and board[row][column+2] == player and board[row][column+3] == player:
                return True
    #Check Vertical Moves
    for column in range(COLUMN_COUNT):
        for row in range(ROW_COUNT-3):
            if board[row][column] == player and board[row+1][column] == player and board[row+2][column] == player and board[row+3][column] == player:
                return True
    #check positive diagonals
    for column in range(COLUMN_COUNT-3):
        for row in range(3,ROW_COUNT):
            if board[row][column] == player and board[row-1][column+1] == player and board[row-2][column+2] == player and board[row-3][column+3] == player:
                return True
#AI Agents
#Random Agent
#Randomly places a move with no thought put into it
#NOTE:Not finished, obviously. Decided for this version to just implement the Random Agent
#In main and finish the AI part later this week.
def Random(board, player):
    while True:
        i = random.randint(0,6)
        return valid_move(board, i)


def draw_board(board):
    for column in range (COLUMN_COUNT):
        for row in range (ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (column*SQUARESIZE, row*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int(column*SQUARESIZE+SQUARESIZE/2), int(row*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
    for column in range (COLUMN_COUNT):
        for row in range (ROW_COUNT):
            if  board[row][column] == 1:
                pygame.draw.circle(screen, RED, (int(column*SQUARESIZE+SQUARESIZE/2), height -int(row*SQUARESIZE+SQUARESIZE/2)), RADIUS)
            elif board[row][column] == 2:
                pygame.draw.circle(screen, YELLOW, (int(column*SQUARESIZE+SQUARESIZE/2), height -int(row*SQUARESIZE+SQUARESIZE/2)), RADIUS)
    pygame.display.update()
turn = 0
pygame.init()
game_over = False
board = create_Board()
print_Board(board)
SQUARESIZE = 100


width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1)* SQUARESIZE
RADIUS = int(SQUARESIZE/2 - 5)

size = (width, height)
screen= pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

font = pygame.font.SysFont("monospace", 75)



#While game_over is false
#If game_over becomes true, the loop ends
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
            posx = event.pos[0]
            if turn == 0:
                pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)
            else:
                pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE/2)), RADIUS)
            pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            #Asks for player 1 input
            if turn == 0:
                posx = event.pos[0]
                column = int(math.floor(posx/SQUARESIZE))
                if valid_move(board, column):
                    row = getNextRow(board, column)
                    drop_piece(board, row, column, 1)

                    if Winner(board, 1):
                        label = font.render("Player 1 wins!", 1, RED)
                        screen.blit(label, (40, 10))
                        game_over = True


            # #Asks for Player 2 input
            else:
                #Implements a random agent. Will just place random moves.
                posx = event.pos[0]
                column = int(math.floor(posx/SQUARESIZE))
                #column = int(input("Player 2, make your move. (0-6):"))
                # i = random.randint(0,6)
                if valid_move(board, column):
                    row = getNextRow(board, column)
                    drop_piece(board, row, column, 2)

                    if Winner(board, 2):
                        label = font.render("Player 2 wins!", 1, YELLOW)
                        screen.blit(label, (40, 10))
                        game_over = True

            print_Board(board)
            draw_board(board)

            #When turn is odd, it's player 2's turn. When zero, it's player 1's
            turn +=1
            turn = turn%2

            if game_over:
                pygame.time.wait(2000)
