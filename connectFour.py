import random
import pygame
import math
import sys
import numpy as np

ROW_COUNT = 6
COLUMN_COUNT = 7
EVEN = 0
ODD = 1




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

#AI Agents
#Random Agent
#Randomly places a move with no thought put into it
#NOTE:Not finished, obviously. Decided for this version to just implement the Random Agent
#In main and finish the AI part later this week.
def Random(board, player):
    while True:
        i = random.randint(0,6)
        return valid_move(board, i)




board = create_Board()
print_Board(board)
game_over = False
turn = 0


#While game_over is false
#If game_over becomes true, the loop ends
while not game_over:
    #Asks for player 1 input
    if turn == 0:
        column = int(input("Player 1, make your move. (0-6):"))
        if valid_move(board, column):
            row = getNextRow(board, column)
            drop_piece(board, row, column, 1)

            if Winner(board, 1):
                print("Player 1 Wins!")
                game_over = True


    #Asks for Player 2 input
    else:
        #column = int(input("Player 2, make your move. (0-6):"))
        #Implements a random agent. Will just place random moves.
        i = random.randint(0,6)
        if valid_move(board, i):
            row = getNextRow(board, i)
            drop_piece(board, row, i, 2)

            if Winner(board, 2):
                print("Player 2 Wins!")
                game_over = True

    print_Board(board)

    #When turn is odd, it's player 2's turn. When zero, it's player 1's
    turn +=1
    turn = turn%2
