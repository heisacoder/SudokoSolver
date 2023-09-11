import utility
import cell as c
import heuristics as h
import GUI
import string


class Counter:
    def __init__(self):
        self.backtracks = 0

class CSP:
    def __init__(self, size, given_cells):
        """
        Initiates the current problem to work on.
        """
        self.ROWS = string.ascii_uppercase[:size ** 2]
        self.COLS = [str(i) for i in range(1, size ** 2)]
        self.size = size
        self.given_cells = given_cells
        self.board = self.create_board()
        self.squares = [utility.cross(i, j) for i in [self.ROWS[i:i + size] for i in range(0, len(self.ROWS), size)]
                        for j in [self.COLS[i:i + size] for i in range(0, len(self.COLS), size)]]
        self.attach_neighbors()
        self.update_neighbor_values_by_given()
        print("Initial board:")
        GUI.print_sudoku(self.board, self.size)

    def create_square_neighbors(self):
        squares = []
        for letters in [self.ROWS[i:i + self.size] for i in range(0, self.size**2, self.size)]:
            for nums in range(1, self.size**2, self.size):
                square = []
                for num in range(nums, nums + self.size):
                    for letter in letters:
                        square.append(letter + str(num))
                squares.append(square)
        return squares

    def create_cell_names(self):
        names = []
        for letter in self.ROWS:
            for num in range(1, self.size**2 + 1):
                names.append(letter + str(num))
        return names

    def create_board(self):
        """
        creates the board itself which is represented as a dictionary. The keys are the cell
        names and the values are the matching cell objects.
        """
        board = dict()
        cell_names = self.create_cell_names()

        for cell_name in cell_names:
            if cell_name in self.given_cells:
                is_given = True
                value = self.given_cells[cell_name]
            else:
                is_given = False
                value = 0
            new_cell = c.Cell(cell_name, is_given, value, self.size)
            board[cell_name] = new_cell
        return board

    def attach_neighbors(self):
        for cell in self.board.values():
            cell.set_neighbors(self.board, self.squares)

    def update_neighbor_values_by_given(self):
        for cell in self.board.values():
            if cell.is_given:
                for neighbor in cell.neighbors:
                    neighbor.possible_values = neighbor.possible_values.difference(cell.possible_values)

    def save_current(self):
        """
        Saves the information of the cells for the ability to restore later in case of failure.
        """
        current_dict = dict()
        for cell_name, cell in self.board.items():
            current_dict[cell_name] = (cell.possible_values, cell.is_assigned, cell.value)
        return current_dict

    def restore(self, count, curr_dict):
        """
        Used when we encounter a failure in the backtracking algorithm for restoring the old
        information from the previous iteration.
        """
        count.backtracks += 1
        for cell_name in self.board:
            self.board[cell_name].possible_values = curr_dict[cell_name][0]
            self.board[cell_name].is_assigned = curr_dict[cell_name][1]
            self.board[cell_name].value = curr_dict[cell_name][2]


    def recursive_backtracking(self, count, strategy1, strategy2, order_function, value_function):
        """
        The main function that searches for the solution. In case there is a variable with
        no remaining values, backtracks and continue.
        :param count: a counter object that counts the number of recursive calls made
        :param strategy1: strategy to detect early failure.
        :param strategy2: same but could be a defaultive function that always returns true.
        :param order_function: a function that chooses the next variable to assign to.
        :param value_function: a function that chooses the value to assign.
        :return: true if puzzle was solved, false otherwise
        """
        if self.check_if_solved():
            return True
        backtrack_dict = self.save_current()
        cur_cell = order_function(self.board)
        for num in value_function(cur_cell):
            if strategy1(cur_cell, num) and strategy2(cur_cell, num):
                cur_cell.set_value(num)
                cur_cell.is_assigned = True
                worked = self.recursive_backtracking(count, strategy1, strategy2, order_function, value_function)
                if worked:
                    return True
                else:
                    self.restore(count, backtrack_dict)
            else:
                self.restore(count, backtrack_dict)
        return False

    def check_if_solved(self):
        """
        check if the puzzle is all solved
        :return:
        """
        for cell in self.board.values():
            if not cell.value:
                return False
        return True

    def solve(self, order, value, strategy1, strategy2=h.default_strategy):
        counter = Counter()

        self.recursive_backtracking(counter, strategy1, strategy2, order, value)
        if not self.check_if_solved():
            print("Puzzle could not be solved!")
        else:
            print("Solved:")
            GUI.print_sudoku(self.board, self.size)
            print("Num of backtracks: ", counter.backtracks)
