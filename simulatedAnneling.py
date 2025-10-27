import copy
import random
import math

def simulatedAnnealingImprove(individual, initialBoard, TStart=1.0, TEnd=0.001, cooling=0.995, maxIter=5000):
    current = individual
    best = copy.deepcopy(individual)

    N = len(current.board)
    boxSize = int(math.sqrt(N))
    fixed = [[cell != 0 for cell in row] for row in initialBoard]

    current.calculateFitness()
    best.calculateFitness()

    T = TStart
    iteration = 0

    while T > TEnd and iteration < maxIter:
        blockIndex = random.randint(0, N - 1)
        boxRowStart = (blockIndex // boxSize) * boxSize
        boxColStart = (blockIndex % boxSize) * boxSize

        mutableCells = []
        for rOffset in range(boxSize):
            for cOffset in range(boxSize):
                row = boxRowStart + rOffset
                col = boxColStart + cOffset
                if not fixed[row][col]:
                    mutableCells.append((row, col))

        if len(mutableCells) < 2:
            iteration += 1
            T *= cooling
            continue

        (r1, c1), (r2, c2) = random.sample(mutableCells, 2)
        
        oldFitness = current.fitness

        current.board[r1][c1], current.board[r2][c2] = current.board[r2][c2], current.board[r1][c1]

        current.calculateFitness()
        newFitness = current.fitness 
        
        delta = newFitness - oldFitness 

        accept = (delta > 0) or (random.random() < math.exp(delta / T))

        if accept:
            if current.fitness > best.fitness:
                best = copy.deepcopy(current)
        else:
            current.board[r1][c1], current.board[r2][c2] = current.board[r2][c2], current.board[r1][c1]            
            current.fitness = oldFitness 

        T *= cooling
        iteration += 1

    return best