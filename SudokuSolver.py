import numpy as np
from random import randint

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
    if i_row < 0 or i_row > 8:
        return False
    if i_collum < 0 or i_collum > 8:
        return False
    if number < 1 or number > 9:
        return False
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
    if not empty:
        return True  
    row, collum = empty

    for number in range(1,10):
        if is_valid(grid, row, collum, number):
            grid[row][collum] = number
            
            if solve_sudoku(grid):
                return True
            grid[row][collum] = 0

    return False

def permutate_rows(grid, row1, row2):
    for collum in range(9):
        temp = grid[row1][collum]
        grid[row1][collum] = grid[row2][collum]
        grid[row2][collum] = temp

def permutate_collums(grid, col1, col2):
    for row in range(9):
        temp = grid[row][col1]
        grid[row][col1] = grid[row][col2]
        grid[row][col2] = temp

def create_sudoku(empty_percentage):
    # Grants the empty space percantege is valid
    if empty_percentage < 0 or empty_percentage > 1:
        return None
    # Calculate the needed empty spaces
    empty_cells = int(81 * empty_percentage)

    # Start the sudoku grid with zeros
    grid = np.zeros((9, 9), dtype=int)
    while True:
        # Initialize 30 random numbers at the grid
        for x in range(30):
            rand_i = randint(0, 8)
            rand_j = randint(0, 8)
            rand_n = randint(1, 9)
            if grid[rand_i][rand_j] != 0:
                if is_valid(grid, rand_i, rand_j, rand_n):
                    grid[rand_i][rand_j] = rand_n
                    if not solve_sudoku:
                        grid[rand_i][rand_j] = 0
        # Check if the result is a solvable grid
        # if true, solves it and end the loop
        if solve_sudoku(grid):
            break
    
    # Do some permutations to randomize the grid a little more
    for collum in range(0,3,3):
        permutate_collums(grid, collum, collum + 2)
        permutate_collums(grid, collum + 1, collum + 2)
    for row in range(0,3,3):
        permutate_rows(grid, row, row + 2)
        permutate_rows(grid, row + 1, row + 2)

    # Remove random cells to match the empty_percentage
    while empty_cells:
        rand_i = randint(0, 8)
        rand_j = randint(0, 8)
        if grid[rand_i][rand_j] != 0:
            grid[rand_i][rand_j] = 0
            empty_cells -= 1    
    return grid

# Usage example
def main():
    sudoku_grid = create_sudoku(0.8)
    print(sudoku_grid)

    solve_sudoku(sudoku_grid)
    print(sudoku_grid)

main()