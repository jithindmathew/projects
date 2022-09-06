# Enter the board here with 0 in places of unfilled numbers
board_default = [
    # [7, 8, 0, 4, 0, 0, 1, 2, 0],
    # [6, 0, 0, 0, 7, 5, 0, 0, 9],
    # [0, 0, 0, 6, 0, 1, 0, 7, 8],
    # [0, 0, 7, 0, 4, 0, 2, 6, 0],
    # [0, 0, 1, 0, 5, 0, 9, 3, 0],
    # [9, 0, 4, 0, 6, 0, 0, 0, 5],
    # [0, 7, 0, 3, 0, 0, 0, 1, 2],
    # [1, 2, 0, 0, 0, 7, 4, 0, 0],
    # [0, 4, 9, 2, 0, 6, 0, 0, 7]

    [0, 0, 8, 1, 4, 0, 9, 0, 2],
    [0, 2, 0, 6, 7, 3, 0, 0, 0],
    [0, 6, 1, 2, 0, 0, 3, 7, 4],
    [1, 9, 0, 0, 2, 4, 0, 5, 3],
    [7, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 3, 2, 0, 0, 0, 0, 9, 0],
    [0, 0, 7, 3, 8, 0, 6, 0, 9],
    [9, 0, 0, 7, 0, 0, 5, 0, 1],
    [6, 1, 0, 0, 0, 0, 0, 2, 0]]


def printboard(bo):
    for i in range(9):
        for j in range(9):
            print(bo[i][j], end="")
            if j != 8:
                print(" ", end="")
            else:
                print("")
            if (j + 1) % 3 == 0 and j != 8:
                print("| ", end="")
        if (i + 1) % 3 == 0 and i != 8:
            print("---------------------")
    return


def isvalid(bo, num, pos):

    # checking row
    for i in range(9):
        if bo[pos[0]][i] == num and pos[1] != i:
            return False

    # checking column
    for i in range(9):
        if bo[i][pos[1]] == num and pos[0] != i:
            return False

    # checking box
    x = (pos[0] // 3) * 3
    y = (pos[1] // 3) * 3

    for i in range(x, x + 3):
        for j in range(y, y + 3):
            if bo[i][j] == num and pos[0] != i and pos[1] != j:
                return False
    return True


def find_empty(bo):
    # finding first empty position
    for i in range(9):
        for j in range(9):
            if bo[i][j] == 0:
                return (i, j)

    return None


def build():
    user_board = [
                ["*", "*", "*", "*", "*", "*", "*", "*", "*"],
                ["*", "*", "*", "*", "*", "*", "*", "*", "*"],
                ["*", "*", "*", "*", "*", "*", "*", "*", "*"],
                ["*", "*", "*", "*", "*", "*", "*", "*", "*"],
                ["*", "*", "*", "*", "*", "*", "*", "*", "*"],
                ["*", "*", "*", "*", "*", "*", "*", "*", "*"],
                ["*", "*", "*", "*", "*", "*", "*", "*", "*"],
                ["*", "*", "*", "*", "*", "*", "*", "*", "*"],
                ["*", "*", "*", "*", "*", "*", "*", "*", "*"]]

    for i in range(9):
        for j in range(9):
            printboard(user_board)
            print("                           ")

            while True:
                try:
                    a = int(input("Enter the number in position of ({}, {}) \n".format(str(i + 1),str(j + 1))))
                except ValueError:
                    print("Enter a number between 0 and 9 \n")
                    continue
                else:
                    if a > 9 or a < 0:
                        print("Enter a number between 0 and 9 \n")
                        continue
                    else:
                        break

            print("")
            user_board[i][j] = a

    return user_board


def solve(bo):
    first_empty = find_empty(bo)

    if not first_empty:
        return True

    for i in range(1, 10):
        if isvalid(bo, i, first_empty):
            bo[first_empty[0]][first_empty[1]] = i

            if solve(bo):
                return True

            bo[first_empty[0]][first_empty[1]] = 0

    return False


def ask():
    print("Do you want to enter a new sudoku or use the one in code? \n")
    print("Y -> Yes, I want to enter a new sudoku \n")
    print("N -> No, use the sudoku in the code \n")

    a = input()

    if a == "Y":
        print("Enter 0 in empty places \n ")
        return build()
    elif a == "N":
        return board_default
    else:
        print("\n")
        print("Enter 'N' or 'Y' \n")
        ask()


if __name__ == '__main__':

    board = ask()

    print("Unsolved sudoku : ")

    printboard(board)

    print("                       ")

    if solve(board):
        print("Solved sudoku : ")
        printboard(board)
    else:
        print("No Solution")
