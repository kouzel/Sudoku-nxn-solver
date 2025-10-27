import copy
import random
import math


from utils import (printSudoku)

def isUniqueSudoku(board):
    N = len(board)
    solutions = 0

    def isValid(board, row, col, num):
        if num in board[row]:
            return False
        for r in range(N):
            if board[r][col] == num:
                return False
        n = int(N**0.5)
        startRow = row - row % n
        startCol = col - col % n
        for r in range(startRow, startRow + n):
            for c in range(startCol, startCol + n):
                if board[r][c] == num:
                    return False
        return True

    def solve(board):
        nonlocal solutions

        if solutions >= 2:
            return

        for row in range(N):
            for col in range(N):
                if board[row][col] == 0:
                    for num in range(1, N + 1):
                        if isValid(board, row, col, num):
                            board[row][col] = num
                            solve(board)
                            board[row][col] = 0
                    return
        solutions += 1

    solve(copy.deepcopy(board))
    return solutions == 1


class Individual:
    size = 0

    def __init__(self, solvedBoard):
        self.board = copy.deepcopy(solvedBoard)  
        self.fitness = None
        self.calculateFitness(solvedBoard)

    def calculateFitness(self, solvedBoard):
        filled = sum(
            1
            for i in range(self.size)
            for j in range(self.size)
            if self.board[i][j] != 0
        )
        if not isUniqueSudoku(self.board):
            self.fitness = -1000
        else:
            self.fitness = 81 - filled


def selection(population, k):
    participants = random.sample(population, min(k, len(population)))
    return max(participants, key=lambda x: x.fitness)



def crossoverByBlock(parent1, parent2, child1, child2):
    N = Individual.size
    boxSize = int(math.sqrt(N))

    newBoard1 = copy.deepcopy(parent1.board)
    newBoard2 = copy.deepcopy(parent2.board)

    block_index = random.randint(0, N - 1)
    box_row_start = (block_index // boxSize) * boxSize
    box_col_start = (block_index % boxSize) * boxSize

    for r in range(boxSize):
        for c in range(boxSize):
            row = box_row_start + r
            col = box_col_start + c

            newBoard1[row][col], newBoard2[row][col] = (
                newBoard2[row][col],
                newBoard1[row][col],
            )

    child1.board = newBoard1
    child2.board = newBoard2



def mutation(child, mutationProb):
    if random.random() > mutationProb:
        return
    for i in range(Individual.size):
        for j in range(Individual.size):
            if child.board[i][j] != 0 and random.random() < 0.3:
                child.board[i][j] = 0


def ga(
    solvedBoard,
    populationSize,
    numGenerations,
    tournamentSize,
    mutationProbability,
    elitismSize,
):
    Individual.size = len(solvedBoard)
    population = [Individual(solvedBoard) for _ in range(populationSize)]
    newPopulation = [Individual(solvedBoard) for _ in range(populationSize)]
    bestResult = population[0]
    if elitismSize % 2 != populationSize % 2:
        elitismSize += 1

    for it in range(numGenerations):
        population.sort(key=lambda x: x.fitness, reverse=True)
        bestResult = population[0]
        print(
            f"Gen {it} Best Fitness: {bestResult.fitness} Zadati brojevi: {81 - bestResult.fitness}",
            end="\r",
        )

        if bestResult.fitness == 81:
            break

        newPopulation[:elitismSize] = population[:elitismSize]

        for i in range(elitismSize, populationSize, 2):
            parent1 = selection(population, tournamentSize)
            tmp, parent1.fitness = parent1.fitness, float("-inf")
            parent2 = selection(population, tournamentSize)
            parent1.fitness = tmp

            crossoverByBlock(parent1, parent2, newPopulation[i], newPopulation[i + 1])

            mutation(newPopulation[i], mutationProbability)
            mutation(newPopulation[i + 1], mutationProbability)
            newPopulation[i].calculateFitness(solvedBoard)
            newPopulation[i + 1].calculateFitness(solvedBoard)

        population = copy.deepcopy(newPopulation)
        bestResult = population[0]

    return bestResult


solvedSudoku = [
    [5, 3, 4, 6, 7, 8, 9, 1, 2],
    [6, 7, 2, 1, 9, 5, 3, 4, 8],
    [1, 9, 8, 3, 4, 2, 5, 6, 7],
    [8, 5, 9, 7, 6, 1, 4, 2, 3],
    [4, 2, 6, 8, 5, 3, 7, 9, 1],
    [7, 1, 3, 9, 2, 4, 8, 5, 6],
    [9, 6, 1, 5, 3, 7, 2, 8, 4],
    [2, 8, 7, 4, 1, 9, 6, 3, 5],
    [3, 4, 5, 2, 8, 6, 1, 7, 9],
]

result = ga(
    solvedSudoku,
    populationSize=10,
    numGenerations=200,
    tournamentSize=3,
    mutationProbability=0.1,
    elitismSize=2,
)
print("\n\nGenerated Sudoku with minimal clues:")
printSudoku(result.board)
