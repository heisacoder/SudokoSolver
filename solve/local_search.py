import numpy as np
import random
import itertools
MAX_RESTARTS = 1000


class Counter:
    def __init__(self):
        self.nodes = 0


class LocalSearch:
    """
    This class is responsible for running the local search algorithms. The board is represented
    by a matrix this time.
    """
    def __init__(self, size, given_cells):
        self.size = size
        self.given_cell_indices = dict()
        self.non_given_indices = dict()
        self.board = self.initialize_numpy_board(given_cells)
        print("Initial board:")
        print(self.board)
        self.init_board = self.board.copy()
        self.restarts = 0
        self.board = self.fill_board(self.board)

    def initialize_numpy_board(self, given_cells):
        np_board = np.zeros((self.size**2, self.size**2))
        for cell_name in given_cells:
            y = ord(cell_name[0]) - 65
            x = int(cell_name[1:]) - 1
            np_board[y][x] = given_cells[cell_name]
            if y not in self.given_cell_indices:
                self.given_cell_indices[y] = np.array([], dtype=np.int8)
            self.given_cell_indices[y] = np.append(self.given_cell_indices[y], x)
        return np_board

    def fill_board(self, board):
        """
        randomly fills each row with all the numbers 1-9. This makes sure there are no
        collisions in rows and all requires numbers appear in the board.
        """
        for i in range(self.size**2):
            possible_vals = np.arange(1, 1 + self.size**2)
            given_indices = self.given_cell_indices[i]
            given_values = board[i][given_indices]
            possible_vals = np.delete(possible_vals, given_values - 1)
            random.shuffle(possible_vals)
            left_indices = np.delete(np.arange(self.size**2), given_indices)
            board[i][left_indices] = possible_vals
        return board

    def collision_with_given(self, board):
        """
        This is a heuristic which checks collisions only with the given numbers.
        """
        collision_counter = 0
        for given_cell_row in self.given_cell_indices:
            for given_cell_column in self.given_cell_indices[given_cell_row]:
                cur_column = board[:, given_cell_column]
                if len(np.where(cur_column == board[given_cell_row, given_cell_column])[0]) > 1:  # if appears in the column more than once
                    collision_counter += 1
                square_row = given_cell_row - (given_cell_row % self.size)
                square_column = given_cell_column - (given_cell_column % self.size)
                cur_square = board[square_row:square_row + self.size, square_column: square_column + self.size]
                if len(np.where(cur_square == board[given_cell_row, given_cell_column])[0]) > 1:
                    collision_counter += 1

        return collision_counter

    def random_restart(self):
        """
        This function sends to the function "climb_random_restart" which is responsible for finding the solution.
        If a solution is not found within the max number of restarts, then we give up.
        Otherwise, it prints the solution and the number of steps required.
        """
        counter = Counter()
        while self.count_collisions(self.board) != 0:
            if self.restarts == MAX_RESTARTS:
                print("Couldn't solve in reasonable time... :('")
                break
            self.board = self.climb_random_restart(counter)
        print("Solved:")
        print(self.board)
        print("Num of steps: ", counter.nodes)


    def beam_search(self):
        """
        This function sens to the "climb_beam_search" which is responsible for finding the
        solution. When a solution is found, it prints it and also the numbers of steps required.
        :return:
        """
        counter = Counter()
        beam = self.create_initials()
        board = self.board
        while self.count_collisions(board) != 0:
            if self.restarts == MAX_RESTARTS:
                print("Couldn't solve in reasonable time... :('")
                break
            board = self.climb_beam_search(counter, beam)
        print("Solved:")
        print(board)
        print("num of steps: ", counter.nodes)


    def count_collisions(self, board):
        #checking collisions in rows
        errors = 0
        rows, cols = self.size**2, self.size**2

        #checking collisions in columns
        for j in range(cols):
            cur_col = board[:, j]
            # cur_col = cur_col[np.where(cur_col != 0)]  # deleting zeros
            cur_col_err = cur_col.shape[0] - np.unique(cur_col).shape[0]
            errors += cur_col_err

        #checking collisions in squares
        for s1 in range(0, rows, self.size):
            for s2 in range(0, cols, self.size):
                cur_square = board[s1:s1 + self.size, s2: s2 + self.size]
                cur_square = cur_square[np.where(cur_square != 0)[0], np.where(cur_square != 0)[1]]
                cur_square_err = cur_square.shape[0] - np.unique(cur_square).shape[0]
                errors += cur_square_err
        return errors

    @staticmethod
    def flip_coin(p):
        r = random.random()
        return r < p

    def climb_beam_search(self, counter, beam):
        """
        runs one iteration in which it tries to improve each of the 7 states in the beam.
        For each of them it decides to use the best successor with 0.75 chance and otherwise
        chooses a random successor.
        :return: A solution if found.
        """
        counter.nodes += 1

        for k, curr_neighbor in enumerate(beam):

            cur_successor = curr_neighbor
            min_collisions = self.count_collisions(curr_neighbor)
            for i in range(self.size**2):
                left_indices = np.delete(np.arange(self.size**2), self.given_cell_indices[i])
                for idx1, idx2 in itertools.combinations(left_indices, 2):
                    new_board = curr_neighbor.copy()
                    new_board[i][idx1], new_board[i][idx2] = curr_neighbor[i][idx2], curr_neighbor[i][idx1]
                    cur_collisions = self.count_collisions(new_board)
                    if cur_collisions < min_collisions:
                        min_collisions = cur_collisions
                        cur_successor = new_board
            if min_collisions == 0:
                return cur_successor
            if self.flip_coin(0.75):
                beam[k] = cur_successor
            else:
                row = np.random.randint(0, self.size ** 2 - 1)
                left_indices = np.delete(np.arange(self.size ** 2), self.given_cell_indices[row])
                idx1, idx2 = np.random.choice(left_indices, size=2)
                while idx1 == idx2:
                    idx1, idx2 = np.random.choice(left_indices, size=2)
                curr_neighbor[row][idx1], curr_neighbor[row][idx2] = curr_neighbor[row][idx2], curr_neighbor[row][idx1]

        print("Collisions: ", [self.count_collisions(neighb) for neighb in beam])

        return self.board

    def climb_random_restart(self, counter):
        """
        Does one iteration of hill climbing, finding a better successor each time. If stuck
        in local minimum, restarts the board.
        :param counter: counts the number of steps done.
        :return: the successor.
        """
        counter.nodes += 1
        cur_successor = self.board
        min_given_collision = self.collision_with_given(self.board)
        min_collisions = self.count_collisions(self.board) + min_given_collision
        orig_collisions = min_collisions
        for i in range(self.size ** 2):
            left_indices = np.delete(np.arange(self.size ** 2), self.given_cell_indices[i])
            for idx1, idx2 in itertools.combinations(left_indices, 2):
                new_board = self.board.copy()
                new_board[i][idx1], new_board[i][idx2] = self.board[i][idx2], self.board[i][idx1]
                cur_given_collision = self.collision_with_given(new_board)
                cur_collisions = self.count_collisions(new_board) + cur_given_collision
                if cur_collisions < min_collisions:
                    min_collisions = cur_collisions
                    cur_successor = new_board

        print("Collisions: ", min_collisions)
        if orig_collisions == min_collisions:
            self.restarts += 1
            return self.fill_board(self.init_board)
        return cur_successor

    def create_initials(self):
        """
        Creates the beam, i.e 7 random successors of the initial state.
        """

        beam = []
        beam2 = []
        board = self.board
        for i in range(self.size ** 2):
            left_indices = np.delete(np.arange(self.size ** 2),
                                     self.given_cell_indices[i])
            for idx1, idx2 in itertools.combinations(left_indices, 2):
                new_board = self.board.copy()
                new_board[i][idx1], new_board[i][idx2] = board[i][idx2], board[i][idx1]

                beam.append(new_board)
        indices = []
        for i in range(7):
            curr_index = random.randint(0, len(beam)-1)
            while curr_index in indices:
                curr_index = random.randint(0, len(beam)-1)
            indices.append(curr_index)
            beam2.append(beam[curr_index])

        return beam2
