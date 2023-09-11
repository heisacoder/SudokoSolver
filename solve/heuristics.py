

def forward_checking(cell, num):
    """
    A heuristic that keeps track of remaining legal values for unassigned variables.
    :return: true if putting the given num in the given cell leaves at least one possible value for all the cell's
    neighbors, false otherwise.
    """
    cell.possible_values = {num}
    for neighbor in cell.neighbors:
        neighbor.possible_values = neighbor.possible_values.difference({num})
        if len(neighbor.possible_values) == 0:
            return False
    return True


def arc_consistency(cell, num):
    """
    A heuristic that makes sure that the assigned value is consistent with the current cell's
    neighbors. If a value is deleted from one of the neighbors we check the neighbor's neighbors
    too.
    :return: True if there is no failure, false otherwise.
    """
    cell.possible_values = {num}
    for neighbor in cell.neighbors:
        old_vals = neighbor.possible_values
        neighbor.possible_values = neighbor.possible_values.difference({num})
        if len(neighbor.possible_values) == 1 and old_vals != neighbor.possible_values:
                neighbor_val = neighbor.possible_values.pop()
                return arc_consistency(neighbor, neighbor_val)
        if len(neighbor.possible_values) == 0:
            return False
    return True


def default_strategy(cell, num):
    return True


def min_remaining_value(board):
    """
    A heuristic that chooses the variable with the minimum possible values remaining.
    :return: The cell to assign to.
    """
    chosen_var = None
    num_remaining = 10
    for cell in board.values():
        curr_len = len(cell.possible_values)
        if curr_len < num_remaining and not cell.is_given and not cell.is_assigned:
            chosen_var = cell
            num_remaining = curr_len
            if curr_len == 1:
                break
    return chosen_var


def by_order(board):
    """
    Chooses the next variable by a specific order.
    :return: the next variable
    """
    for cell_name in sorted(board):
        if not board[cell_name].is_assigned:
            return board[cell_name]


def random_value(cell):
    """
    returns a random value from the list of remaining possible values.
    """
    return list(cell.possible_values)


def least_constraining_value(cell):
    """
    A heuristic that returns a list of possible values for a given cell sorted by the possible value that deletes the
    smallest amount of values from the neighbors up to the possible value that deletes the biggest amount of values from
    neighbors.
    :param cell: the given cell.
    :return: sorted list of possible values.
    """
    deletion_num = dict()
    for possible_value in cell.possible_values:
        curr_deletion = 0
        for neighbor in cell.neighbors:
            if possible_value in neighbor.possible_values:
                curr_deletion += 1
        deletion_num[possible_value] = curr_deletion
    return sorted(deletion_num, key=deletion_num.get)
