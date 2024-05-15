from typing import Union
from abc import ABC, abstractmethod
from numpy import double
from collections import deque
import re

class Expression(ABC):
    @abstractmethod
    def calc(self):
        pass

class Num(Expression):
    def __init__(self, value):
        self.value = value

    def calc(self):
        return double(self.value)

class BinExp(Expression):
    def __init__(self, First, Latest):
        self.First = First
        self.Latest = Latest

class Plus(BinExp):
    def calc(self):
        return self.First.calc() + self.Latest.calc()

class Minus(BinExp):
    def calc(self):
        return self.First.calc() - self.Latest.calc()

class Mul(BinExp):
    def calc(self):
        return self.First.calc() * self.Latest.calc()

class Div(BinExp):
    def calc(self):
        return self.First.calc() / self.Latest.calc()

def isNumber(n) -> bool:
    if ('0' <= n <= '99'):
       return True
    return False
    
def parser(expression: str):
    priority = {'+': 0, '-': 0, '*': 1, '/': 1} # קביעת מה לפני מה
    queueNumbers = deque()
    stackSign = deque()
    
    expression = expression.replace("(-", "(0-")
    transition = re.findall(r'[()+\-*/]|(?:\d+\.\d+|\d+)', expression)
    
    for i in transition:
        if isNumber(i):
            queueNumbers.append(Num(double(i)))  # הופך את המספר לאובייקט מסוג NUM queueNumbersומכניס ל
        elif i == '(':
            stackSign.append(i)
        elif i == ')' and 1 < len(queueNumbers):
            while stackSign and stackSign[-1] != '(':
                Latest = queueNumbers.pop()
                First = queueNumbers.pop()
                sign = stackSign.pop()
                
                if sign == '/':
                    queueNumbers.append(Div(First, Latest))
                elif sign == '*':
                    queueNumbers.append(Mul(First, Latest))
                elif sign == '+':
                    queueNumbers.append(Plus(First, Latest))
                elif sign == '-':
                    queueNumbers.append(Minus(First, Latest))
            if stackSign and stackSign[-1] == '(':
                stackSign.pop()
        else:
            while not isNumber(i) and  stackSign and stackSign[-1] != '(' and priority[i] <= priority[stackSign[-1]]:
                Latest = queueNumbers.pop()
                # In the provided code, the variable `First` is being used as a placeholder to store
                # the First operand of a binary expression when parsing the input expression. It is
                # used in the context of evaluating binary expressions (such as addition, subtraction,
                # multiplication, and division) within the parser function.
                First = queueNumbers.pop()
                sign = stackSign.pop()
                
                if sign == '/':
                    queueNumbers.append(Div(First, Latest))
                elif sign == '*':
                    queueNumbers.append(Mul(First, Latest))
                elif sign == '+':
                    queueNumbers.append(Plus(First, Latest))
                elif sign == '-':
                    queueNumbers.append(Minus(First, Latest))
            stackSign.append(i)

    while stackSign and 1 < len(queueNumbers):
        Latest = queueNumbers.pop()
        First = queueNumbers.pop()
        sign = stackSign.pop()
        
        if sign == '/':
            queueNumbers.append(Div(First, Latest))
        elif sign == '*':
            queueNumbers.append(Mul(First, Latest))
        elif sign == '+':
            queueNumbers.append(Plus(First, Latest))
        elif sign == '-':
            queueNumbers.append(Minus(First, Latest))

    return queueNumbers[0].calc()  # Return the result of the calculation
