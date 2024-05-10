from abc import ABC
from numpy import double
from abc import ABC,abstractmethod
from collections import deque
import re

class Expression(ABC): 
    @abstractmethod
    def calc(self) -> double: 
        pass

class Num(Expression): 
    def __init__(self, value): 
        self.value = value  

    def calc(self) -> double: 
        return double(self.value) 

class BinExp(Expression): 
    def __init__(self, left, right):
        self.left = left
        self.right = right

class Plus(BinExp):
    def calc(self) -> double:
        return self.left.calc() + self.right.calc()

class Minus(BinExp):
    def calc(self) -> double:
        return self.left.calc() - self.right.calc()

class Mul(BinExp):
    def calc(self) -> double:
        return self.left.calc() * self.right.calc()

class Div(BinExp):
    def calc(self) -> double:
        return self.left.calc() / self.right.calc()

def isNumber(n) -> bool:    
    if ('0' <= n <= '99'):
       return True
    else:
        return False
    
def parser(expression: str):
    queue = deque() 
    stack = deque()


    priority = {
        '+': 0,
        '-': 0,
        '*': 1,
        '/': 1
    }

    expression = expression.replace("(-", "(0-")
    split = re.findall(r'[()+\-*/]|(?:\d+\.\d+|\d+)', expression)
    
    for i in split:
        if (isNumber(i)):
            queue.append(float(i))

        elif (i == '('):
            stack.append(i)

        elif ( i == ')' and 1 < len(queue)):
            while (stack and stack[-1] != '('):
                right = Num(queue[-1])
                left = Num(queue[-2])
                queue.pop()
                queue.pop()
            
                if (stack[-1] == '/'):
                    queue.append(Div(left, right).calc())

                elif (stack[-1] == '*'):
                    queue.append(Mul(left, right).calc())

                elif (stack[-1] == '+'):
                    queue.append(Plus(left, right).calc())

                elif (stack[-1] == '-'):
                    queue.append(Minus(left, right).calc())
                stack.pop()
                
            if(stack and stack[-1] == '('):
                stack.pop()
        
        else:
            while ((stack) and (stack[-1] != '(' ) and (not isNumber(i)) and (priority[i] <= priority[stack[-1]])):
                right = Num(queue[-1])
                left = Num(queue[-2])
                queue.pop()
                queue.pop()
            
                if (stack[-1] == '/'):
                    queue.append(Div(left, right).calc())

                elif (stack[-1] == '*'):
                    queue.append(Mul(left, right).calc())

                elif (stack[-1] == '+'):
                    queue.append(Plus(left, right).calc())

                elif (stack[-1] == '-'):
                    queue.append(Minus(left, right).calc())
                stack.pop()
                
            stack.append(i)

    while (stack and 1 < len(queue)):
        right = Num(queue[-1])
        left = Num(queue[-2])
        queue.pop()
        queue.pop()
    
        if (stack[-1] == '/'):
            queue.append(Div(left, right).calc())

        elif (stack[-1] == '*'):
            queue.append(Mul(left, right).calc())

        elif (stack[-1] == '+'):
            queue.append(Plus(left, right).calc())

        elif (stack[-1] == '-'):
            queue.append(Minus(left, right).calc())
        stack.pop()

    return queue[0]