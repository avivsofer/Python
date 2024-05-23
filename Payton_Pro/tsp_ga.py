import random
import math

class Point:
    def __init__(self) -> None:
        self.x = random.randint(-100,100)
        self.y = random.randint(-100,100)
        
def dist(p1,p2):
    return (math.sqrt((p1.x-p2.x)**2 + (p1.y-p2.y)**2))

def fitness(points):
    sum=0
    for i in range(1,len(points)):
        sum+=dist(points[i-1],points[i])
    return sum

def initPop(points): # creates a population of 200 routes
    pop = []
    for i in range (150):
        ps = points.copy()
        random.shuffle(ps)
        pop.append(ps)
    return pop

def crossover (pointsA, pointsB):
    midA = len(pointsA) //2
    midB = len(pointsB) //2
    la = []
    for i in range(midA):
        la.append(pointsA[i])
    for i in range(midB+1, len(pointsB)):
        la.append(pointsB[i])
    la = set(la)
    la = list(la)

    lb = []
    for i in range(midB):
        lb.append(pointsB[i])
    for i in range(midA+1, len(pointsA)):
        lb.append(pointsA[i])
    lb = set(lb)
    lb = list(lb)

    return la, lb

def mutate(org_points, points):
    l = points.copy()
    if (0 < len(points)):
        i = random.choice(points)
        j = random.choice(org_points)
        while j in points:
            j = random.choice(org_points)
        l.remove(i)
        l.append(j)
    return l

def ga(points, generations, muProb):
    pop = initPop(points)
    pop.sort(key = fitness)
    best = pop[0]

    for i in range(generations):
        pop = pop[:len(pop)//2]
        children = []
        for j in range(1, len(pop), 2):
            c1,c2 = crossover(pop[j-1], pop[j])
            if (random.random() < muProb):
                c1 = mutate(points, c1)
            if (random.random() < muProb):
                c2 = mutate(points, c2)
            children.append(c1)
            children.append(c2)
        pop.extend(children)
        pop.sort(key = fitness)
        if (fitness(pop[0]) < fitness(best)):
            best = pop[0]
    return best


def solve(points):
    return ga(points, 5000, 0.08)














