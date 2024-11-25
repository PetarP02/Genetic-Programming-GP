from genome import Genome
from node import Node
import numpy as np
import copy as cp
import random
import time

class GenProg:
    """
    Represents a genetic programming algorithm for finding an expression that approximates a target goal.

    The GenProg class uses a population of genomes, represented as binary expression trees, to evolve and find an expression
    that comes close to a specified goal. Each genome is evaluated based on its fitness relative to the target value. The
    algorithm applies selection, crossover, and mutation processes to evolve the population over a specified number of epochs.

    Attributes:
        population (list): The current population of genomes.
        bestFit (Node) : Initialy None, after calling findSolution it has gene with best solution.
        __goal (int): The target integer value that the population attempts to approximate.
        __populationSize (int): The total number of genomes in the population.
        __numbers (list): A list of integers used as operands in the genome expressions.
        __elitism (int): The number of top-performing genomes carried over to the next generation without modification.
        __mutationChance (float): The probability of mutation for each genome in the population.
        __epochs (int): The number of iterations or generations for which the algorithm runs.
        __newPopulation (list): The next generation of genomes, constructed at each epoch from the current population.
    
    Methods:
        findSolution(): Runs the genetic programming algorithm to find an expression that approximates the target goal, 
                        returns list of best values in every generation.
        crossover(genome1, genome2): Performs crossover between two genomes to produce two new offspring genomes.
        tournament(): Selects genomes from the population using a tournament selection method, returning indexes of selected genomes.
    """
    def __init__(self, goal: int, numbers: list, populationSize: int = 10, elitism: int = 0, mutationChance: float = 0.05, epochs: int = 10) -> 'GenProg':
        """
        Initializes a GenProg instance with the specified target goal, population size, mutation chance, and number of epochs.

        Args:
            goal (int): The target integer value for the fitness function, which genomes aim to approximate.
            numbers (list): A list of integers used as operands in constructing genome expressions.
            populationSize (int, optional): The size of the population of genomes; defaults to 10.
            elitism (int, optional): The number of top-performing genomes retained in each generation; defaults to 0.
            mutationChance (float, optional): The probability of mutation for each genome; defaults to 0.05.
            epochs (int, optional): The number of generations or iterations for the algorithm to run; defaults to 10.

        Raises:
            AttributeError: If `populationSize` is less than or equal to `elitism`.
        """
        
        if populationSize <= elitism:
            raise AttributeError(f"Population size : {populationSize}, it must be larger the elitism : {elitism}")
        if populationSize < 10:
            raise AttributeError(f"Population size : {populationSize}, cant be less then 10")

        self.__goal = goal
        self.__populationSize = populationSize
        self.__numbers = numbers
        self.__elitism = elitism
        self.__mutationChance = mutationChance
        self.__epochs = epochs

        self.bestFit = None
        self.population = [Genome(self.__goal, self.__numbers, self.__mutationChance) for _ in range(self.__populationSize)]
        self.__newPopulation = [Genome(self.__goal, self.__numbers, self.__mutationChance) for _ in range(self.__populationSize)]

    def findSolution(self) -> list:
        """
        Runs the genetic programming algorithm to approximate the target goal.
    
        The method evolves a population of genomes over a specified number of epochs
        using selection, crossover, and mutation. It keeps track of the best fitness
        in each generation and terminates early if a perfect solution (fitness of 100)
        is found. Elitism is applied to retain the top-performing genomes across generations.
                
        Returns:
            list: A list of the best fitness values recorded at each generation.
    
        Process:
            1. Sorts the population by fitness in descending order.
            2. Records the best fitness in the current generation.
            3. If a perfect solution is found (fitness = 100), the algorithm stops.
            4. Copies the elite genomes directly into the new population.
            5. Performs tournament selection, crossover, and mutation to fill the rest of the population.
            6. Replaces the old population with the new one and repeats the process for the specified epochs.
        """
        startintTime = time.perf_counter()
        graph = []
        
        for i in range(self.__epochs):
            if i % 100 == 0:
                print(f"{i} : {time.perf_counter() - startintTime} s")
            
            self.population.sort(reverse=True)

            graph.append(self.population[0].getFitness())

            if int(graph[-1]) == 100:
                break 
            
            self.__newPopulation[:self.__elitism] = self.population[:self.__elitism]
            
            for j in range(self.__elitism, self.__populationSize - 1, 2):
                idx1, idx2 = self.tournament()

                self.__newPopulation[j], self.__newPopulation[j+1] = self.crossover(self.population[idx1], self.population[idx2])

                self.__newPopulation[j].mutate()
                self.__newPopulation[j+1].mutate()
            
            self.population = self.__newPopulation
            
        best = max(self.population)
        self.bestFit = cp.deepcopy(best)
        print(f"elapse time : {time.perf_counter() - startintTime : .6f} s - solution: {best} - value: {best.gene.value} - fitness: {best.getFitness()}")
        return graph
    
    def crossover(self, genome1: 'Genome', genome2: 'Genome') -> list:
        """
        Performs crossover between two genomes to produce offspring.
    
        The method swaps subtrees between the two parent genomes at randomly
        selected nodes to create two new child genomes.
    
        Args:
            genome1 (Genome): The first parent genome.
            genome2 (Genome): The second parent genome.
    
        Returns:
            list: A list containing two new child genomes resulting from the crossover.
        """
        node1 = random.randint(1, genome1.gene.size)
        node2 = random.randint(1, genome2.gene.size)

        child1 = cp.deepcopy(genome1)
        child2 = cp.deepcopy(genome2)

        tree1 = child1.gene.subTree(node1)#uzmi stablo na poziciji node1
        tree2 = child2.gene.subTree(node2)
        _ = child1.gene.subTree(node1, cp.deepcopy(tree2))#zameni podstablo na poziciji node1 sa podstablom tree2
        _ = child2.gene.subTree(node2, cp.deepcopy(tree1))#uzmi stablo na poziciji node2
        
        return [child1, child2]
        
    def tournament(self) -> list:
        """
        Selects two genomes from the population using a tournament selection method.
    
        The method selects 10 random genomes from the population and then picks the
        two with the highest fitness as the winners of the tournament.
    
        Returns:
            list: A list containing the indices of the two selected genomes.
        """
        indexes = random.sample(range(len(self.population)), 10)

        maxFit = float('-inf')
        idx1 = indexes[0]
        idx2 = indexes[1]
        for i in indexes:
            if maxFit < self.population[i].getFitness():
                maxFit = self.population[i].getFitness()
                idx2 = idx1
                idx1 = i
        
        return [idx1, idx2]
