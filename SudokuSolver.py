import numpy as np
from random import randint

# Define if it's valid to put number at position i_rox x i_column in the grid
def is_valid(grid, i_row, i_column, number):
    # Check the inputs
    if i_row < 0 or i_row > 8:
        return False
    if i_column < 0 or i_column > 8:
        return False
    if number < 1 or number > 9:
        return False
    # Check row
    for column in range(9):
        if number == grid[i_row][column] and column != i_column:
                return False
    # Check column
    for row in range(9):
        if number == grid[row][i_column] and row != i_row:
                return False
    # Check cell
    for row in range((i_row // 3) * 3, ((i_row // 3) * 3) + 3):
        for column in range((i_column // 3) * 3, ((i_column // 3) * 3) + 3):
            if number == grid[row][column] and (row != i_row or column != i_column):
                return False
    return True

# Returns the first empty position at the grid
def find_empty(grid):
    for row in range(9):
        for column in range(9):
            if grid[row][column] == 0:
                return (row, column)
    return None

# Receive an 9x9 numpy array (sudoku grid) and solve it 
def solve_sudoku(grid):
    empty = find_empty(grid)
    if not empty:
        return True  
    row, column = empty

    for number in range(1,10):
        if is_valid(grid, row, column, number):
            grid[row][column] = number
            
            if solve_sudoku(grid):
                return True
            grid[row][column] = 0

    return False

# Receive a list of possible values for a certain position on the grid
# and remove those who are not possible anymore
def reduce_possibilities(grid, possible_values, i_row, i_column):
    # Check the inputs
    if i_row < 0 or i_row > 8:
        return False
    if i_column < 0 or i_column > 8:
        return False
    if len(possible_values) <= 1:
        return False
    # Remove the possible values fot that position
    # Check row
    for column in range(9):
        for value in possible_values:
            if grid[i_row][column] == value and i_column != column:
                possible_values.remove(value)
    # Check column
    for row in range(9):
        for value in possible_values:
            if grid[row][i_column] == value and i_row != row:
                possible_values.remove(value)
    # Check cell
    for row in range((i_row // 3) * 3, ((i_row // 3) * 3) + 3):
        for column in range((i_column // 3) * 3, ((i_column // 3) * 3) + 3):
            for value in possible_values:
                if grid[row][column] == value:
                    if i_row != row or i_column != column:
                        possible_values.remove(value)
    return True

# Check if the grid have any empty space yet
def solved(grid):
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0:
                return False
    return True

# This function simulates the way a human would solve a sudoku.
# It calculates the possible values and, when the 
# possibilitities is reduced to 1, it fills the grid.
# I think it does not solve every unique solution puzzle, but that's the best I've got
def unique_solution(grid):
    grid = grid.copy()
    numbers = [n for n in range(1,10)]
    # Create a list of possible values for each position the grid
    possible_values = []
    for i in range(9):
        possible_values.append([])
    for i in range(9):
        for j in range(9):
            possible_values[i].append([])
    for i in range(9):
        for j in range(9):
            possible_values[i][j] = numbers.copy()

    # Solve the grid by calculating the possible values
    # once the possible values is reduced to 1, it changes the grid
    while not solved(grid):
        before = grid.copy()
        for i in range(9):
            for j in range(9):
                reduce_possibilities(grid, possible_values[i][j], i, j)
                if len(possible_values[i][j]) == 1:
                    grid[i][j] = int(possible_values[i][j][0])
        # If there's no difference between the grid before the loop, means that
        # the algorithm cannot solve the grid because it have multiple solutions
        if before.all() == grid.all():
            return False

    return True

def permutate_rows(grid, row1, row2):
    for column in range(9):
        temp = grid[row1][column]
        grid[row1][column] = grid[row2][column]
        grid[row2][column] = temp

def permutate_columns(grid, col1, col2):
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
    for column in range(0,3,3):
        permutate_columns(grid, column, column + 2)
        permutate_columns(grid, column + 1, column + 2)
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

# Returns a solvable value at that position
def hint(grid, pos):
    grid = grid.copy()
    for number in range(1,10):
        if is_valid(grid, pos[0], pos[1], number):
            grid[pos[0]][pos[1]] = number
            if solve_sudoku(grid.copy()):
                return number
            grid[pos[0]][pos[1]] = 0
    return 0

# Usage example
def main():
    sudoku_grid = create_sudoku(0.8)
    print(sudoku_grid)

    solve_sudoku(sudoku_grid)
    print(sudoku_grid)

main()