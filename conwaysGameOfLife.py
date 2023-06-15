# Python program to implement Conway's Game of Life
#
# Cells living in a grid.
#
# Cells follow the following rules:
# 1.    Any live cell with < 2 neighbors dies
# 2.    Any live cell with 2 or 3 neighbors lives in the next generation
# 3.    Any live cell with > 3 neighbors dies
# 4.    Any ded cell with 3 neighbors becomes a live cell
#

import time

def create_grid(rows, columns):
    return [[0 for i in range(columns)] for j in range(rows)]

"""
Function to create the next generation of the board.

Parameters:
grid: List containing the grid
rows: Number of rows in the grid
columns: Number of columns in the grid

Returns: The new grid as a List.
"""
def next_generation(grid, rows, columns) -> list:
    # Initialise empty board
    future = create_grid(rows, columns)
    
    # Loop through each cell on the board
    for row in range(rows):
        for column in range(columns):
            # Determine number of alive neighbors
            numberOfNeighbors = get_number_of_alive_neighbors(row, column, grid, rows, columns)
            
            if (grid[row][column] == 1):
                # Check if cell is alive
                if (numberOfNeighbors < 2 or numberOfNeighbors > 3):
                    # Kill if neighbors < 2 or > 3
                    future[row][column] = 0
                else:
                    # Cell remains alive
                    future[row][column] = 1
            else:
                # Check if cell is dead
                if (numberOfNeighbors == 3):
                    # Make dead cell alive
                    future[row][column] = 1
                else:
                    # Cell remains dead
                    future[row][column] = 0
    
    # Return new generation
    return future


"""
Determines the number of neighbors alive for a specific cell.

Parameters:
row: the row the cell is on
column: the column the cell is on
grid: the List containing the grid
rows: the number of rows in the grid
columns: the number of columns in the grid

Returns: The number of alive cells.
"""
def get_number_of_alive_neighbors(row, column, grid, rows, columns) -> int:
    aliveNeighbors = 0
    for i in range(-1, 2):  # -1, 0, 1
        for j in range(-1, 2):  # -1; 0; 1
            if (((row + i) >= 0 and (row + i) < columns) and 
                ((column + j) >= 0 and (column + j) < rows)):
                # The index is within the bounds of the grid.
                aliveNeighbors += grid[row + i][column +j]
                
    # Remove the current cell from the count
    aliveNeighbors -= grid[row][column]
    
    return aliveNeighbors

"""
Steps the board and returns the new board

Parameters:
grid: list containing the current state of the board
rows: the number of rows in the board
columns: the number of columns in the board
"""
def step_board(grid, rows, columns) -> list:
    
        for i in range(rows):
            for j in range(columns):
                
                if (grid[i][j] == 0):
                    print(".", end="")
                else:
                    print("#", end="")
                
            print()
        print()
        
        return next_generation(grid, rows, columns)

def main():
    # Initialise board
    rows, columns = 10, 10
    
    # initialise grid
    initialGrid = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
                   [0, 0, 1, 1, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
                   [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    
    grid = initialGrid
    
    while (True):
        grid = step_board(grid, rows, columns)
        time.sleep(1)

if __name__ == "__main__":
    main()