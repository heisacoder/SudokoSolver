

def print_sudoku(board, n):
    rows = []

    if n == 3:
        rows = ["A", "B", "C", "D", "E", "F", "G", "H", "I"]
    if n == 4:
        rows = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P"]

    for i, row in enumerate(rows):
        for col in range(1, n**2+1):
            print(str(board[row + str(col)].value), end="  ")
            if col % n == 0 and col != n**2:
                print("|", end=" ")
        if (i + 1) % n == 0 and i != n**2 - 1:
            if n == 3:
                line = "----------"*n
            if n == 4:
                line = "---------------"*n
            print("\n"+line)
        else:
            print()
    print("\n")

