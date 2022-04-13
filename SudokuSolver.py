import numpy as np

# Check if it's possible to put number at that row
def check_row(grid, i_row, i_collum, number):
    for collum in range(9):
        if number == grid[i_row][collum] and collum != i_collum:
                return False
    return True

# Check if it's possible to put number at that collum
def check_collum(grid, i_row, i_collum, number):
    for row in range(9):
        if number == grid[row][i_collum] and row != i_row:
                return False
    return True

# Check if it's possible to put number at that cell
def check_cell(grid, i_row, i_collum, number):
    for row in range((i_row // 3) * 3, ((i_row // 3) * 3) + 3):
        for collum in range((i_collum // 3) * 3, ((i_collum // 3) * 3) + 3):
            if number == grid[row][collum] and (row != i_row or collum != i_collum):
                return False
    return True

# Define if it's valid to put number at position i_rox x i_collum in the grid
def is_valid(grid, i_row, i_collum, number):
    return(
        check_row(grid, i_row, i_collum, number)
        and check_collum(grid, i_row, i_collum, number)
        and check_cell(grid, i_row, i_collum, number)
        )

# Returns the first empty position at the grid
def find_empty(grid):
    for row in range(9):
        for collum in range(9):
            if grid[row][collum] == 0:
                return (row, collum)
    return None

# Receive an 9x9 numpy array (sudoku grid) and solve it 
def solve_sudoku(grid):
    empty = find_empty(grid)
    if empty == None:
        return True    
    row, collum = empty 

    for number in range(1,10):
        if is_valid(grid, row, collum, number):
            grid[row][collum] = number
            
            if solve_sudoku(grid):
                return True
            grid[row][collum] = 0

# Usage example
def main():
    sudoku_grid = [
        5, 3, 0,  0, 7, 0,  0, 0, 0,
        6, 0, 0,  1, 9, 5,  0, 0, 0,
        0, 9, 8,  0, 0, 0,  0, 6, 0,
        
        8, 0, 0,  0, 6, 0,  0, 0, 3,
        4, 0, 0,  8, 0, 3,  0, 0, 1,
        7, 0, 0,  0, 2, 0,  0, 0, 6,
        
        0, 6, 0,  0, 0, 0,  2, 8, 0,
        0, 0, 0,  4, 1, 9,  0, 0, 5,
        0, 0, 0,  0, 8, 0,  0, 7, 9
    ]

    sudoku_grid = np.reshape(sudoku_grid, (9, 9))
    solve_sudoku(sudoku_grid)

    print(sudoku_grid)

main()