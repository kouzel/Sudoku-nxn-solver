import math
import time

def isValid(board, row, col, num):
    N = len(board)
    boxSize = int(math.sqrt(N))

    if num in board[row]:
        return False

    if num in [board[r][col] for r in range(N)]:
        return False

    startRow = (row // boxSize) * boxSize
    startCol = (col // boxSize) * boxSize
    for r in range(startRow, startRow + boxSize):
        for c in range(startCol, startCol + boxSize):
            if board[r][c] == num:
                return False

    return True


def backtrackingAlgorithm(board):
    N = len(board)
    for row in range(N):
        for col in range(N):
            if board[row][col] == 0:
                for num in range(1, N + 1):
                    if isValid(board, row, col, num):
                        board[row][col] = num
                        if backtrackingAlgorithm(board):
                            return True
                        board[row][col] = 0
                return False
    return True


def printSudoku(board, N):
    N = len(board)
    n = int(math.sqrt(N))

    for i in range(N):
        if i % n == 0 and i != 0:
            print("----------------------------")
        row = ""
        for j in range(N):
            if j % n == 0 and j != 0:
                row += "| "
            val = board[i][j]
            row += (str(val) if val != 0 else ".") + " "
        print(row)
    print()


puzzle = [
    [8, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 3, 6, 0, 0, 0, 0, 0],
    [0, 7, 0, 0, 9, 0, 2, 0, 0],
    [0, 5, 0, 0, 0, 7, 0, 0, 0],
    [0, 0, 0, 0, 4, 5, 7, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 3, 0],
    [0, 0, 1, 0, 0, 0, 0, 6, 8],
    [0, 0, 8, 5, 0, 0, 0, 1, 0],
    [0, 9, 0, 0, 0, 0, 4, 0, 0],
]

start = time.perf_counter()
N = 9
printSudoku(puzzle, N)
backtrackingAlgorithm(puzzle)
end= time.perf_counter()
print()
printSudoku(puzzle, N)
print(str(end-start))
