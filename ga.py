import copy
import random
import math
import time

from utils import printSudoku, easySudoku, evilSudoku, sudoku2x2,enigmatikaExtreme

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
        # for row in range(N):
        #     vals= [self.board[row][col] for col in range(N)]
        #     conflicts+= (len(vals) - len(set(vals)))

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
def crossoverByBlock(parent1, parent2, child1, child2):
    N = Individual.size
    boxSize = int(math.sqrt(N))

    # napravimo prazne table za decu
    newBoard1 = [[0]*N for _ in range(N)]
    newBoard2 = [[0]*N for _ in range(N)]

    # biramo mesto preseka po blokovima
    cutRow = random.randint(0, boxSize-1)   # koji blok po redovima
    cutCol = random.randint(0, boxSize-1)   # koji blok po kolonama

    for br in range(boxSize):
        for bc in range(boxSize):
            for r in range(boxSize):
                for c in range(boxSize):
                    row = br*boxSize + r
                    col = bc*boxSize + c

                    # ako je blok presek – dete1 dobija iz parent1, dete2 iz parent2
                    if br < cutRow or (br == cutRow and bc <= cutCol):
                        newBoard1[row][col] = parent1.board[row][col]
                        newBoard2[row][col] = parent2.board[row][col]
                    else:
                        newBoard1[row][col] = parent2.board[row][col]
                        newBoard2[row][col] = parent1.board[row][col]

    child1.board = newBoard1
    child2.board = newBoard2


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

        print(f"Best Fitness:{population[0].fitness}; Fifth:{population[4].fitness}; Worst Fitness:{population[-1].fitness}; Generation: {it}; mutProb:{mutationProbability}", end="\r")
        
        newPopulation[:elitismSize] = population[:elitismSize]

        for i in range(elitismSize,populationSize,2):
            parent1 = selection(population,tournamentSize)

            tmp,parent1.fitness = parent1.fitness, float('-inf')

            parent2= selection(population,tournamentSize)

            parent1.fitness=tmp
            randCrossover=random.random()
            if(randCrossover<0.33):
                crossoverByBlock(parent1,parent2,newPopulation[i],newPopulation[i+1])
            elif randCrossover>0.66:
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


sudokuToSolve = enigmatikaExtreme

Individual.size=len(sudokuToSolve)

start = time.perf_counter()
random.seed(3)

printSudoku(easySudoku)
result = ga(easySudoku,populationSize=2000,numGenerations=10000,tournamentSize=5,mutationProbability=0.6,elitismSize=50)
end = time.perf_counter()

print('\n\n')
print('Best: '+str(result.fitness))
printSudoku(result.board)
print(str(end-start))