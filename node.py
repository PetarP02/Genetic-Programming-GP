import copy as cp
from typing import Union

# n - number of verices
        # init : O(n)
        # setOperation : O(log n) 
        # setOperand : O(log n) 
        # __replaceNode : O(log n)
        # valueCalc : O(log n) : eval(str(self.__operand[0])) is O(N) N-number of caracters that need to be evaluated
        #                        complexity could be O(N log n) but is N is small most of times.
        # subTree : O(log n)
        # getOperation : O(1)
        # getLeaves : O(1)
        # __str__ : O(n)

class Node:
    """
    Represents a node in a binary expression tree for evaluating mathematical expressions.

    Each Node can either be a leaf (holding a single operand) or an operator with two operands.
    It supports methods for setting operations and operands, replacing nodes, retrieving leaf values,
    and calculating the value of the expression represented by the tree rooted at this node.

    Attributes:
        value (float): The calculated value of the expression rooted at this node.
        size (int): The size of the subtree, including the length of the operator and 
                    size of child nodes.
    
    Methods:
        setOperation(newOperation): Sets a new operation for the node and 
                                    recalculates its value.
        setOperand(newOperand, operandPos=0): Sets a new operand at a given position 
                                              (left or right) and recalculates.
        valueCalc(): Calculates and returns the value of the expression rooted at this node, 
                     propagating to root of this tree, handling zero division.
        subTree(pos, insertTree=None): Returns the subtree at a given position, 
                                       if insertTree is given replacing it with a new subtree 
                                       and returning that subtree.
        getLeaves(): Returns the list of leaf values in the subtree rooted at this node.
        getOperation() : Returns operation of this node.
        __replaceNode(newNode): Replaces the current node with a new node, 
                                returning the original node.

    """
    def __init__(self, first: Union['Node', int, str], operation: str = None, second: Union['Node', int, str] = None) -> 'Node':
        """
        Initializes a Node in the binary expression tree.

        If only 'first' is provided, the Node is a leaf representing a single operand (number or string).
        If both 'operation' and 'second' are provided, the Node becomes an operator node, representing 
        an expression with two operands (left and right subtrees).

        Parameters:
            first (Union[Node, int, str]): The first operand or the left subtree.
                - If 'operation' is None, this becomes a leaf node containing 'first'.
                - If 'operation' is provided, 'first' becomes the left child node.
            operation (str, optional): The operator as a string (e.g., '+', '-', '*', '/'). Defaults to None.
            second (Union[Node, int, str], optional): The second operand or the right subtree. Required if 'operation' is provided.

        Raises:
            AttributeError: If 'operation' is provided without a 'second' operand.
        """
        
        if operation is not None and second is None:
            raise AttributeError("Operation must have second operand")

        self.__parent = None
        self.__operator = None
        self.__operand = []
        self.__leaves = []
        self.size = 1
        self.value = None
        
        if operation is None:
            self.__operand.append(str(first))
            self.valueCalc()
        else:
            self.__operator = operation
            left = first if isinstance(first, Node) else Node(first)
            right = second if isinstance(second, Node) else Node(second)
            left.__parent = self
            right.__parent = self
            self.__operand = [left, right]
            self.size = len(self.__operator) + left.size + right.size
            self.valueCalc()

    def setOperation(self, newOperation: str) -> None:
        """
        Sets a new operation for the node and recalculates its value.
    
        Args:
            newOperation (str): The new operator ('+', '-', '*', or '/').
    
        Raises:
            AttributeError: If the provided operation is invalid.
        """
        if newOperation not in ['+', '-', '*', '/']:
            raise AttributeError(f"Operation {newOperation} is not accepted!");
        
        self.__operator = newOperation
        self.valueCalc()

    def setOperand(self, newOperand: Union['Node', str, int], operandPos: int = 0) -> None:
        """
        Sets a new operand for the node and recalculates its value.
    
        Args:
            newOperand (Union[Node, str, int]): The new operand or subtree.
            operandPos (int, optional): The position to update (0 for left, 1 for right). Defaults to 0.
    
        Raises:
            AttributeError: If the operand position is invalid or out of bounds.
        """
        if operandPos not in [0, 1] or (len(self.__operand) == operandPos):
            raise AttributeError(f"Operand position: {operandPos} is not valid!")
        
        newOperand = newOperand if isinstance(newOperand, Node) else Node(newOperand)
        newOperand.__parent = self
        self.__operand[operandPos] = newOperand
        self.valueCalc()
        
    def __replaceNode(self, newNode: 'Node') -> None:
        """
        Replaces the current node with a new node.
    
        Args:
            newNode (Node): The new node to replace the current node.
    
        Raises:
            AttributeError: If the provided 'newNode' is not of type 'Node'.
        """
        if not isinstance(newNode, Node):
            raise AttributeError(f"Given newNode is of type {type(newNode)}, not of type Node!")
        
        self.__operator = newNode.__operator
        self.__operand = newNode.__operand
        self.size = newNode.size
        self.value = newNode.value
        self.__leaves = newNode.__leaves
        
        for operand in self.__operand:
            if isinstance(operand, Node):
                operand.__parent = self 
        
        self.valueCalc()
    
    def valueCalc(self):
        """
        Recalculates the value of the expression represented by this node and updates the parent nodes.
    
        - Leaf nodes are evaluated directly based on their operand.
        - Internal nodes are evaluated based on their operator and the values of their children.
        - Handles division by zero by setting the value to infinity.
    
        Updates the following attributes:
            - value: The calculated value of the node.
            - __leaves: The list of leaf values in the subtree rooted at this node.
            - size: The size of the subtree.
        """
        tree = self
        while True:
            if len(tree.__operand) == 1:
                tree.value = eval(str(tree.__operand[0]))
                tree.__leaves = [tree.value]
                tree.size = 1
            else:
                try:
                    leftVal = float(tree.__operand[0].value)
                    rightVal = float(tree.__operand[1].value)
                    tree.value = eval(f"float('{leftVal}') {tree.__operator} float('{rightVal}')")
                except(ZeroDivisionError):
                    tree.value = float('inf')
                    
                tree.__leaves = tree.__operand[0].__leaves + tree.__operand[1].__leaves
                tree.size = len(tree.__operator) + tree.__operand[0].size + tree.__operand[1].size

            if tree.__parent is None:
                break
            tree = tree.__parent

    def subTree(self, pos: int, insertTree: 'Node' = None) -> 'Node':
        """
        Retrieves or replaces a subtree at a specified position in the binary tree.
    
        Args:
            pos (int): The position of the subtree (1-based index).
            insertTree (Node, optional): If provided, replaces the subtree at the position with this node.
    
        Returns:
            Node: The subtree at the specified position.
    
        Raises:
            AttributeError: If the position is out of bounds or 'insertTree' is not a valid node.
        """
        if insertTree != None and not isinstance(insertTree, Node):
            raise AttributeError(f"Given insertTree is of type {type(insertTree)}, not of type Node!")
        if pos > self.size:
            raise AttributeError(f"Goint out of bounds! Tree \"{str(self)}\" size {self.size}, trying to get subtree on node {pos}!")

        tree = self
        while pos != 1:
            if pos - tree.__operand[0].size <= 1:
                pos -= 1
                tree = tree.__operand[0]
            else:
                pos -= (tree.__operand[0].size + 1)
                tree = tree.__operand[1]
                
        if insertTree != None:
            tree.__replaceNode(insertTree)
            return tree
        return tree
        
    def getOperation(self) -> str:
        """
        Retrieves the operation of the node.
    
        Returns:
            str: The operator of the node.
    
        Raises:
            AttributeError: If the node has no operator (i.e., it is a leaf node).
        """
        if self.__operator == None:
            raise AttributeError(f"This node has no operatino!")
        return self.__operator
    
    def getLeaves(self) -> list:
        """
        Retrieves the list of leaf values in the subtree rooted at this node.
    
        Returns:
            list: A list of leaf values.
        """
        return self.__leaves

    def __str__(self) -> str:
        if self.size == 1:
            return f"{self.__operand[0]}"
        return f"({self.__operand[0]} {self.__operator} {self.__operand[1]})"

    def __lt__(self, other) -> bool:
        return self.value < other.value