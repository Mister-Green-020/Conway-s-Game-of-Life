import sys
import tkinter as tk
import time

from dataclasses import dataclass
from random import random
from typing import List

# Rows and columns
rows = 25
columns = 50

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

# Boards are lists containing lists containing Cells
boardtype = listtype[listtype[Cell]]

# Global variable to stop/play the simulation
stopFlag = True

"""
Creates a grid with Cells randomly set to alive or dead.

Parameters:
rows (int): the number of rows in the grid.
columns (int): the number of columns in the grid.

Returns (list): the randomly set grid as a list
"""
def create_grid(rows: int, columns: int) -> list:
    return [[Cell(round(random())) for i in range(rows)] for j in range(columns)]

"""
Randomly set Cells in the board as alive or dead to initialise board.

Parameters:
board: The board to initialise.
"""
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

"""
Draws a grid of rectangles with the specified rows and columns. Each rectangle is 20x20 pixels.
If a cell is alive, it is coloured black; otherwise it is coloured white. Only cells that have
changed states from the previous board are redrawn.

Parameters:
f (tk.Canvas): The figure window.
"""
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

"""
Determines the number of alive neighbors surrounding a given Cell.

Parameters:
board (boardtype): The board containing the cells
row (int): the row the Cell to check is on
column (int): the column the Cell to check is on

Returns (int): the number of alive neighbours
"""
def get_number_of_alive_neighbors(board: boardtype, row: int, column: int) -> int:
    aliveNeighbors = 0
    for r in range(row-1, row+2):  # -1, 0, 1
        for c in range(column-1, column+2):  # -1; 0; 1
            if ((r >= 0 and r < columns) and (c >= 0 and c < rows)):
                # The index is within the bounds of the grid.
                aliveNeighbors += board[r][c].value
                
    # Remove the current cell from the count
    aliveNeighbors -= board[row][column].value

    return aliveNeighbors

"""
Applies the rules of Conway's Game of Life to each cell on the board. Marks Cells to be
alive or dead and if their value changes.

Parameters:
board (boardtype): the board containing the Cells
"""
def check_all_cells(board: boardtype) -> None:
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
                    
"""
Updates the Cells that require their values to be changed.

Parameters:
board (boardtype): the board containign the Cells.
"""
def update_board(board: boardtype) -> None:
    for row in range(len(board)):
        for column in range(len(board[0])):
            # Check if Cell has been marked for change
            if board[row][column].change == True:
                if board[row][column].marked == True:
                    board[row][column].value = 1
                else:
                    board[row][column].value = 0
                
"""
Checks the Cells and updates the board and canvas.

Parameters:
board (boardtype): the board containing the Cells.
f (tk.Canvas): the figure window/canvas
"""
def run_and_canvas(board: boardtype, f: tk.Canvas) -> None:
    check_all_cells(board)
    update_board(board)
    update_canvas(f)

"""
Loops through the logic and updates the graphics window.
"""
def loop():
    while (not stopFlag):
        run_and_canvas(board, field)
        root.update()

"""
Function for the Pause/Play button. Sets the global stopFlag variable
"""
def pause_play():
    global stopFlag
    if (stopFlag):      # Play
        stopFlag = False
        loop()
    else:               # Pause
        stopFlag = True

"""
Function for the restart button. Re-initalises the board.
"""
def reset():
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

board = create_grid(rows, columns)

# Draw initial canvas
for i in range(len(board)):
    for j in range(len(board[0])):
        if board[i][j].value == 1:
            field.create_rectangle(i*21, j*21, i*21 + 20,j*21 + 20, fill='black')
        else:
            field.create_rectangle(i*21, j*21, i*21 + 20, j*21+20, fill='white')
    
# Loop the window
tk.mainloop()
