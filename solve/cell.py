import string


class Cell:
    """
    This class represents a cell in the sudoku board.
    """
    def __init__(self, name, is_given, value, puzzle_size):

        self.name = name
        self.is_given = is_given
        self.value = value
        self.neighbors = list()
        self.possible_values = set()
        self.puzzle_size = puzzle_size
        self.is_assigned = False
        if is_given:
            self.is_assigned = True
            self.possible_values.add(value)
        else:
            self.possible_values.update(range(1, self.puzzle_size**2 + 1))

    def set_neighbors(self, board, squares):
        """
        Creates the list of neighbors of the cell.
        """
        rows = string.ascii_uppercase[:self.puzzle_size ** 2]

        # sets neighbors from same row
        for letter in rows:
            if letter != self.name[0]:
                neighbor = letter + self.name[1:]
                self.neighbors.append(board[neighbor])

        # sets neighbors from same column
        for num in range(1, self.puzzle_size**2 + 1):
            if str(num) != self.name[1:]:
                neighbor = self.name[0] + str(num)
                self.neighbors.append(board[neighbor])

        # sets neighbors from same square
        for square in squares:
            if self.name in square:
                for cell_name in square:
                    if cell_name != self.name:
                        self.neighbors.append(board[cell_name])

    def set_value(self, num):
        """
        assigns a value to the cell.
        """
        self.value = num
