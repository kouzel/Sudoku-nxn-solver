import copy
import random
import math
import time

from utils import (
    printSudoku,
    easySudoku,
    evilSudoku,
    sudoku2x2,
    enigmatikaExtreme,
    worldsMostDificult,
)
from simulatedAnneling import (
    simulatedAnnealingImprove
)


class Individual:
    size = 0
    bestFitness = 0
    initialPositions = []

    def __init__(self, initialBoard):
        N = Individual.size
        boxSize = int(math.sqrt(N))
        newBoard = copy.deepcopy(initialBoard)

        for boxRow in range(0, N, boxSize):
            for boxCol in range(0, N, boxSize):

                fixed_nums = set()
                for r in range(boxSize):
                    for c in range(boxSize):
                        if newBoard[boxRow + r][boxCol + c] != 0:
                            fixed_nums.add(newBoard[boxRow + r][boxCol + c])

                missing = [n for n in range(1, N + 1) if n not in fixed_nums]
                random.shuffle(missing)

                for r in range(boxSize):
                    for c in range(boxSize):
                        if newBoard[boxRow + r][boxCol + c] == 0:
                            newBoard[boxRow + r][boxCol + c] = missing.pop()

        self.board = newBoard
        self.calculateFitness()

    def calculateFitness(self):
        N = Individual.size
        conflicts = 0
        for row in range(N):
            vals = [self.board[row][col] for col in range(N)]
            conflicts += len(vals) - len(set(vals))

        for col in range(N):
            vals = [self.board[row][col] for row in range(N)]
            conflicts += len(vals) - len(set(vals))
        
        for row in range(N):
            for col in range(N):
                val = self.board[row][col]
                if val == 0:
                    continue

                rowVals = [self.board[row][c] for c in range(N)]
                rowConflict = rowVals.count(val) > 1

                colVals = [self.board[r][col] for r in range(N)]
                colConflict = colVals.count(val) > 1

                if rowConflict and colConflict:
                    conflicts += 1

        self.fitness = -conflicts


def selection(population: list[Individual], k: int):
    k = min(len(population), k)
    participants = random.sample(population, k)
    return max(participants, key=lambda x: x.fitness)


def crossoverByCell(parent1, parent2, child1, child2):
    cut = random.randint(0, Individual.size * Individual.size - 1)
    newBoard1 = [[] for _ in range(Individual.size)]
    newBoard2 = [[] for _ in range(Individual.size)]

    for row in range(Individual.size):
        for column in range(Individual.size):
            if row * Individual.size + column < cut:
                newBoard1[row].append(parent1.board[row][column])
                newBoard2[row].append(parent2.board[row][column])
            else:
                newBoard1[row].append(parent2.board[row][column])
                newBoard2[row].append(parent1.board[row][column])
    child1.board = newBoard1
    child2.board = newBoard2


def crossoverByRow(parent1, parent2, child1, child2):
    cut = random.randint(0, Individual.size - 1)

    child1.board = copy.deepcopy(parent1.board[:cut] + parent2.board[cut:])
    child2.board = copy.deepcopy(parent2.board[:cut] + parent1.board[cut:])


def crossoverByColumn(parent1, parent2, child1, child2):
    cut = random.randint(0, Individual.size - 1)
    newBoard1 = [[] for _ in range(Individual.size)]
    newBoard2 = [[] for _ in range(Individual.size)]

    for row in range(Individual.size):
        for column in range(Individual.size):
            if column < cut:
                newBoard1[row].append(parent1.board[row][column])
                newBoard2[row].append(parent2.board[row][column])
            else:
                newBoard1[row].append(parent2.board[row][column])
                newBoard2[row].append(parent1.board[row][column])
    child1.board = newBoard1
    child2.board = newBoard2


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


def mutation(child: Individual, p: float, initialBoard):
    if random.random() > p:
        return

    N = Individual.size
    boxSize = int(math.sqrt(N))

    block_index = random.randint(0, N - 1)
    box_row_start = (block_index // boxSize) * boxSize
    box_col_start = (block_index % boxSize) * boxSize

    mutableCells = []

    for rOffset in range(boxSize):
        for cOffset in range(boxSize):
            row = box_row_start + rOffset
            col = box_col_start + cOffset

            if initialBoard[row][col] == 0:
                mutableCells.append((row, col))

    for _ in range(5): 
        if len(mutableCells) >= 2:
            (r1, c1), (r2, c2) = random.sample(mutableCells, 2)

            child.board[r1][c1], child.board[r2][c2] = (
                child.board[r2][c2],
                child.board[r1][c1],
            )


def ga(
    initialBoard,
    populationSize,
    numGenerations,
    tournamentSize,
    mutationProbability,
    elitismSize,
    restartAfterNGenerationWithoutImprovment,
):

    population = [Individual(initialBoard) for _ in range(populationSize)]
    newPopulation = [Individual(initialBoard) for _ in range(populationSize)]

    sameNumOfIterationWithoutImprovment = 0
    bestCurrentFitness = float("-inf")

    bestResult = []
    if elitismSize % 2 != populationSize % 2:
        elitismSize += 1

    for it in range(numGenerations):

        population.sort(key=lambda x: x.fitness, reverse=True)
        bestResult = population[0]
        if population[0].fitness == bestCurrentFitness:
            sameNumOfIterationWithoutImprovment += 1
        else:
            bestCurrentFitness = population[0].fitness
            sameNumOfIterationWithoutImprovment = 0
        if sameNumOfIterationWithoutImprovment == restartAfterNGenerationWithoutImprovment:
            print(f"\n\nTrying simulated annealing before restart (Gen {it})\n")
            bestBefore = population[0].fitness

            improved = simulatedAnnealingImprove(population[0], initialBoard)
            improved.calculateFitness()

            if improved.fitness > bestBefore:
                print(f"Improved fitness from {bestBefore} -> {improved.fitness} with SA!\n")
                population[0] = improved
                bestCurrentFitness = improved.fitness
                sameNumOfIterationWithoutImprovment = 0
                continue
            else:
                print(f"No improvement with SA. Restarting population at Generation {it}\n")
                printSudoku(population[0].board)
                population = population[:elitismSize] + [
                    Individual(initialBoard) for _ in range(populationSize - elitismSize)
                ]
                sameNumOfIterationWithoutImprovment = 0
                bestCurrentFitness = population[0].fitness
                continue

        if bestResult.fitness == Individual.bestFitness:
            return bestResult
        print(
            f"Best Fitness:{population[0].fitness}; 11th:{population[10].fitness}; Worst Fitness:{population[-1].fitness}; Generation: {it};",
            end="\r",
        )

        newPopulation[:elitismSize] = population[:elitismSize]

        for i in range(elitismSize, populationSize, 2):
            parent1 = selection(population, tournamentSize)

            tmp, parent1.fitness = parent1.fitness, float("-inf")

            parent2 = selection(population, tournamentSize)

            parent1.fitness = tmp

            crossoverByBlock(parent1, parent2, newPopulation[i], newPopulation[i + 1])

            customMutationProb = mutationProbability + sameNumOfIterationWithoutImprovment/restartAfterNGenerationWithoutImprovment

            mutation(newPopulation[i],customMutationProb,initialBoard)
            mutation(newPopulation[i + 1],customMutationProb,initialBoard)

            newPopulation[i].calculateFitness()
            newPopulation[i + 1].calculateFitness()

        population = copy.deepcopy(newPopulation)

        bestResult = population[0]

    return bestResult


sudokuToSolve = easySudoku

Individual.size = len(sudokuToSolve)

start = time.perf_counter()
random.seed(1)
printSudoku(sudokuToSolve)
result = ga(
    sudokuToSolve,
    populationSize=500,
    numGenerations=2000,
    tournamentSize=5,
    mutationProbability=0.2,
    elitismSize=20,
    restartAfterNGenerationWithoutImprovment=50,
)
end = time.perf_counter()

print("\n\n")
print("Best: " + str(result.fitness))
printSudoku(result.board)
print(str(end - start))
