from node import Node
import copy as cp
import random

class Genome:
    """
    Represents a genome with a specific target fitness goal and a list of numerical values. 
    The genome is structured as a binary expression tree and evaluated based on its 
    closeness to the target goal using mathematical operations.

    Attributes:
        goal (int): The target value that the genome attempts to approximate.
        numbers (list): A list of integers used as leaf nodes in the gene's binary tree structure.
        chance (float): The probability of mutation occurring in the gene structure.
        gene (Node): The root of the binary tree representing the genome's expression.
        
    Methods:
        getFitness(): Calculates the fitness of the genome based on its approximation to the target goal.
        isValid(): Validates if the genome's expression is integer-valued and uses only the specified numbers.
        mutate(): Applies a random mutation to the genome, potentially altering nodes and operations in the expression tree.

    Private methods:
        __makeGene(): Constructs the initial binary expression tree with random operations and operands.
        __mutateNode(): Internal helper for `mutate()` that performs single-node mutations within the tree, 
                        altering operands or operators.
        __str__(): Returns a string representation of the genome's expression.
        __lt__(other): Defines comparison based on genome fitness and expression value. 
    """
    def __init__(self, goal: int, numbers: list, chance: float = 0.05):
        """
        Initializes a Genome instance with a target goal, list of numbers, and a mutation chance.
        
        Args:
            goal (int): The target integer value for the fitness function.
            numbers (list): A list of integers used in constructing the binary tree.
            chance (float, optional): The probability of mutation in the genome; default is 0.05.
        
        Raises:
            AttributeError: If the `numbers` list is empty.
        """
        if len(numbers) == 0:
            raise AttributeError("List needs to have at least one number!")
        
        self.goal = goal
        self.numbers = numbers
        self.chance = chance
        self.gene = self.__makeGene()

    # __makeGene : O(...)
    # __generate : O(...)
    # getFitness : O(n)
    # isValid : O(n)
    # mutate() : O(n log n)  
    # _mutateNode() : O(n log n)
    
    def __makeGene(self) -> 'Node':
        if len(self.numbers) == 1:
            return Node(self.numbers[0])

        numOfOperands = random.randint(2, len(self.numbers)-1)
        chosenOperands = random.sample(self.numbers, k = numOfOperands)
        
        return self.__generate(chosenOperands)

    def __generate(self, givenList: list) -> 'Node':
        if len(givenList) == 1:
            return Node(givenList[0])

        op = random.choice(['+', '-', '*']) #['+', '-', '*', '/'] 
        index = random.randint(1, len(givenList) - 1) 
        left = self.__generate(givenList[:index]) 
        right = self.__generate(givenList[index:]) 
        return Node(left, op, right)
        
    def getFitness(self):
        if not self.isValid():
            return 0
        return 100 * (1 - abs(self.goal - self.gene.value) / (abs(self.goal) + 1))

    def isValid(self):
        if not self.gene.value.is_integer() or self.gene.size > 2*len(self.numbers)-1:
            return False
            
        try:
            nums = self.numbers.copy()
            for n in self.gene.getLeaves():
                nums.remove(n)
            return True
        except (ValueError):
            return False
    
    def mutate(self):
        if random.random() < self.chance and self.gene.size > 1:
            nums = random.sample(self.numbers, k = 2)
            nodeIn = self.__generate(nums)
        
            num = random.randint(2, self.gene.size)
            self.gene.subTree(num, nodeIn)
    
        self.__mutateNode()

    def __mutateNode(self) -> None:
        if self.gene.size < 2:
            return
        
        for i in range(1, self.gene.size):
            if random.random() < self.chance:
                tree = self.gene.subTree(i)
                if tree.size == 1:
                    operands = self.numbers.copy()
                    operands.remove(tree.value)
                    if operands: #list needs to have at leas one number
                        tree.setOperand(random.choice(operands))
                else:
                    operations = ['+', '-', '*'] #['+', '-', '*', '/']
                    operations.remove(tree.getOperation())
                    tree.setOperation(random.choice(operations))
                break
    
    def __str__(self):
        return str(self.gene)

    def __lt__(self, other):
        return self.getFitness() < other.getFitness()
        
