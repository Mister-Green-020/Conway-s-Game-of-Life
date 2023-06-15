import sys
import tkinter as tk
import time

from dataclasses import dataclass
from random import random
from typing import List

# Rows and columns
rows = 25
columns = 50
boardDead = False

# Create list type
listtype = List

# Create class for cell
@dataclass
class Cell:
    # Alive or not
    value: int
    # Mark for life
    marked: bool = False
    # Mark to be redrawn
    change: bool = False

boardtype = listtype[listtype[Cell]]

def create_grid(rows, columns):
    return [[Cell(round(random())) for i in range(rows)] for j in range(columns)]

board = create_grid(rows, columns)

# Random board initialiser
def random_board_init(board: boardtype) -> None:
    for row in range(len(board)):
        for column in range(len(board[0])):
            alive = random()
            board[row][column].marked = False
            board[row][column].change = True
            
            if alive < 0.5:
                board[row][column].value = 0
            else:
                board[row][column].value = 1

# Update canvas
def update_canvas(f: tk.Canvas) -> None:
    for row in range(len(board)):
        for column in range(len(board[0])):
            if board[row][column].change == True:
                if board[row][column].value == 1:
                    field.create_rectangle(row*21, column*21, row*21+20, column*21+20, fill='black')
                    board[row][column].change = False
                else:
                    field.create_rectangle(row*21, column*21, row*21+20, column*21+20, fill='white')
                    board[row][column].change = False

# Get the number of neighboring alive cells
def get_number_of_alive_neighbors(board: list[list[Cell]], row: int, column: int) -> int:
    aliveNeighbors = 0
    for r in range(row-1, row+2):  # -1, 0, 1
        for c in range(column-1, column+2):  # -1; 0; 1
            if ((r >= 0 and r < columns) and (c >= 0 and c < rows)):
                # The index is within the bounds of the grid.
                aliveNeighbors += board[r][c].value
                
    # Remove the current cell from the count
    aliveNeighbors -= board[row][column].value

    return aliveNeighbors

def check_all_cells(board: list[list[Cell]]) -> None:
    for row in range(len(board)):
        for column in range(len(board[0])):
            # Determine number of alive neighbors
            numberOfNeighbors = get_number_of_alive_neighbors(board, row, column)
            
            if (board[row][column].value == 1):
                # Check if cell is alive
                if (numberOfNeighbors < 2 or numberOfNeighbors > 3):
                    # Kill if neighbors < 2 or > 3
                    board[row][column].marked = False
                    board[row][column].change = True
                else:
                    # Cell remains alive
                    board[row][column].marked = True
            else:
                # Check if cell is dead
                if (numberOfNeighbors == 3):
                    # Make dead cell alive
                    board[row][column].marked = True
                    board[row][column].change = True
                else:
                    # Cell remains dead
                    board[row][column].marked = False
                    
# Update the board
def update_board(board: list[list[Cell]]) -> None:
    global boardDead
    numAlive = 0
    for row in range(len(board)):
        for column in range(len(board[0])):
            if board[row][column].marked == True:
                board[row][column].value = 1
                numAlive += 1
            else:
                board[row][column].value = 0
                
    if (numAlive == 0):
        boardDead = True
                
# Run the simulation
def run_and_canvas(board: list[list[Cell]], f: tk.Canvas) -> None:
    check_all_cells(board)
    update_board(board)
    update_canvas(f)

# Loop the board. If the board contains no living cells, restart the board
stopFlag = True
def loop():
    global boardDead
    while (not stopFlag):
        if (not boardDead):
            run_and_canvas(board, field)
            root.update()
        else:
            boardDead = False
            random_board_init(board)
            root.update()

# Pause and play the board
def pause_play():
    global stopFlag
    if (stopFlag):      # Play
        stopFlag = False
        loop()
    else:               # Pause
        stopFlag = True

# Restart the board
def reset():
    global boardDead
    boardDead = False
    
    # Get new random board
    random_board_init(board)
    run_and_canvas(board, field)
    root.update()

# Create window
root = tk.Tk()
root.title("Conway's Game of Life")

# Create canvas
field = tk.Canvas(root, width=(22*columns), height=(22*rows))
field.pack()

# Create Pause/Play and Restart buttons
pausePlay = tk.Button(root, text="Pause/Play", command=lambda : pause_play())
pausePlay.pack()
resart = tk.Button(root, text="Restart", command=lambda : reset())
resart.pack()

# Draw initial canvas
for i in range(len(board)):
    for j in range(len(board[0])):
        if board[i][j].value == 1:
            field.create_rectangle(i*21, j*21, i*21 + 20,j*21 + 20, fill='black')
        else:
            field.create_rectangle(i*21, j*21, i*21 + 20, j*21+20, fill='white')
    
# Loop the window
tk.mainloop()