import copy
import random
import math

def printSudoku(board):
    N = len(board)
    n = int(math.sqrt(Individual.size)) 

    for i in range(N):
        if i % n == 0 and i != 0:
            print("----------------------------") 
        row= ""
        for j in range(N):
            if j % n == 0 and j != 0:
                row += "| "
            val = board[i][j]
            row += (str(val) if val != 0 else ".") + " "
        print(row)
    print()

class Individual:
    size=0
    bestFitness=0
    initialPositions =[]
    def __init__(self,initialBoard):
        newBoard = copy.deepcopy(initialBoard)
        for row in range(Individual.size):
            missing = [n for n in range(1,Individual.size+1) if n not in newBoard[row]]            
            random.shuffle(missing)
            for col in range(Individual.size):
                if newBoard[row][col] == 0:
                    newBoard[row][col]=missing.pop()
        self.board=newBoard
        self.calculateFitness()

    def calculateFitness(self):
        N = Individual.size
        boxSize = int(math.sqrt(N))
        conflicts = 0

        for col in range(N):
            vals = [self.board[row][col] for row in range(N)]
            conflicts += (len(vals) - len(set(vals)))

        for boxRow in range(0, N, boxSize):
            for boxCol in range(0, N, boxSize):
                vals = []
                for r in range(boxSize):
                    for c in range(boxSize):
                        vals.append(self.board[boxRow+r][boxCol+c])
                conflicts += (len(vals) - len(set(vals))) 

        self.fitness = -conflicts 

def selection(population: list[Individual],k:int):
    k = min(len(population),k)
    participants = random.sample(population,k)
    return max(participants,key=lambda x:x.fitness)

def crossoverByRow(parent1,parent2,child1,child2):
    cut = random.randint(0,Individual.size-1)

    child1.board=copy.deepcopy(parent1.board[:cut]+parent2.board[cut:])
    child2.board=copy.deepcopy(parent2.board[:cut]+parent1.board[cut:])

def crossoverByColumn(parent1,parent2,child1,child2):
    cut = random.randint(0,Individual.size-1)
    newBoard1 =[ [] for _ in range(Individual.size)]
    newBoard2 =[ [] for _ in range(Individual.size)]

    for row in range(Individual.size):
        for column in range(Individual.size):
            if column< cut:
                newBoard1[row].append(parent1.board[row][column])
                newBoard2[row].append(parent2.board[row][column])
            else:
                newBoard1[row].append(parent2.board[row][column])
                newBoard2[row].append(parent1.board[row][column])
    child1.board=newBoard1
    child2.board=newBoard2


def mutation(child:Individual,p:float,initialBoard):
    if(random.random() > p):
         return
    
    if random.random() <0.5:
        for row in range(Individual.size):
            mutable = [i for i in range(Individual.size) if initialBoard[row][i]==0 ]

            if(len(mutable)>=2):
                a,b=random.sample(mutable,2)
                child.board[row][a],child.board[row][b]=child.board[row][b],child.board[row][a]

    else:
        for col in range(Individual.size):
            mutable = [i for i in range(Individual.size) if initialBoard[i][col] == 0]
            if(len(mutable)>=2):
                a,b=random.sample(mutable,2)
                child.board[a][col],child.board[b][col]=child.board[b][col],child.board[a][col]

def ga(initialBoard,populationSize,numGenerations,tournamentSize,mutationProbability,elitismSize):

    population = [Individual(initialBoard) for _ in range(populationSize)]
    newPopulation = [Individual(initialBoard) for _ in range(populationSize)]

    bestResult =[]
    if elitismSize %2 != populationSize %2:
        elitismSize+=1

    for it in range(numGenerations):

        population.sort(key=lambda x:x.fitness,reverse=True)
        bestResult=population[0]

        if(bestResult.fitness == Individual.bestFitness):
            break

        print(f"Best Fitness:{population[0].fitness}; Fifth:{population[4].fitness}; Worst Fitness:{population[-1].fitness}; Generation: {it}; mutProb:{mutationProbability + it/numGenerations}", end="\r")
        
        newPopulation[:elitismSize] = population[:elitismSize]

        for i in range(elitismSize,populationSize,2):
            parent1 = selection(population,tournamentSize)

            tmp,parent1.fitness = parent1.fitness, float('-inf')

            parent2= selection(population,tournamentSize)

            parent1.fitness=tmp
            if(random.random() < 0.5):
                crossoverByRow(parent1,parent2,newPopulation[i],newPopulation[i+1])
            else:
                crossoverByColumn(parent1,parent2,newPopulation[i],newPopulation[i+1])

            mutation(newPopulation[i],mutationProbability,initialBoard)
            mutation(newPopulation[i+1],mutationProbability ,initialBoard)

            newPopulation[i].calculateFitness()
            newPopulation[i+1].calculateFitness()

        population=copy.deepcopy(newPopulation)

        bestResult=population[0]


    return bestResult


enigmatikaExtreme = [
    [0,7,0, 0,1,0, 0,0,0],
    [0,8,0, 0,0,2, 0,0,0],
    [0,9,0, 0,0,8, 0,1,5],

    [0,0,0, 0,5,6, 7,0,0],
    [6,0,0, 8,0,3, 0,0,4],
    [0,0,1, 9,4,0, 0,0,0],

    [9,2,0, 3,0,0, 0,4,0],
    [0,0,0, 4,0,0, 0,3,0],
    [0,0,0, 0,8,0, 0,5,0]
]

evilSudoku = [
    [5,3,0, 0,7,0, 0,0,0],
    [6,0,0, 1,9,5, 0,0,0],
    [0,9,8, 0,0,0, 0,6,0],

    [8,0,0, 0,6,0, 0,0,3],
    [4,0,0, 8,0,3, 0,0,1],
    [7,0,0, 0,2,0, 0,0,6],

    [0,6,0, 0,0,0, 2,8,0],
    [0,0,0, 4,1,9, 0,0,5],
    [0,0,0, 0,8,0, 0,7,9]
]
easySudoku = [
    [0,0,3, 0,2,0, 6,0,0],
    [9,0,0, 3,0,5, 0,0,1],
    [0,0,1, 8,0,6, 4,0,0],

    [0,0,8, 1,0,2, 9,0,0],
    [7,0,0, 0,0,0, 0,0,8],
    [0,0,6, 7,0,8, 2,0,0],

    [0,0,2, 6,0,9, 5,0,0],
    [8,0,0, 2,0,3, 0,0,9],
    [0,0,5, 0,1,0, 3,0,0]
]
solvedSudoku = [
    [5,0,4, 6,0,8, 9,0,2],
    [6,7,2, 1,9,5, 3,4,8],
    [1,9,8, 3,4,2, 5,6,7],

    [8,5,9, 7,6,1, 4,2,3],
    [4,2,6, 8,0,3, 7,9,1],
    [7,1,3, 9,2,4, 8,5,6],

    [9,0,1, 5,3,7, 2,8,4],
    [2,8,7, 4,1,9, 6,3,5],
    [3,4,5, 2,8,6, 1,0,9]
]


sudoku2x2 = [
    [1, 0, 0, 4],
    [0, 0, 2, 0],
    [0, 3, 0, 0],
    [2, 0, 0, 1]
]

Individual.size=9

printSudoku(easySudoku)
result = ga(easySudoku,populationSize=5000,numGenerations=1000,tournamentSize=6,mutationProbability=0.3,elitismSize=50)

print('\n\n')
print('Best: '+str(result.fitness))
printSudoku(result.board)