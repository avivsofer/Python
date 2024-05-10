from numpy import double
from abc import ABC,abstractmethod

class Expression(ABC): #יורש מABC מתודה אבסטרקטית
  @abstractmethod
  def calc(self) -> double: #שיטה הכרחית למימוש אצל היושים
    pass


class Num(Expression): #ירושה מהמחלקה Expression
    def __init__(self, value): #בנאי
        self.value = value  #הפרמטר של האובייקט שווה למה שהבנאי קיבל

    def calc(self) -> double: #פנוקציית calc מחזירה ערך double
        return double(self.value) #ב מחזירה ערך מספרי מהפרמטר לפונקציה

class BinExp(Expression): #מייצגת ביטוי בינארי
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

def shunting_yard(expression: str) -> str:
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
    output = []
    stack = []
    number_buffer = ""

    for token in expression:
        if token.isdigit() or token == '.':
            number_buffer += token
        else:
            if number_buffer:
                output.append(number_buffer)
                number_buffer = ""
            if token in precedence:
                while (stack and precedence.get(stack[-1], 0) >= precedence[token]):
                    output.append(stack.pop())
                stack.append(token)
            elif token == '(':
                stack.append(token)
            elif token == ')':
                while stack and stack[-1] != '(':
                    output.append(stack.pop())
                stack.pop()

    if number_buffer:
        output.append(number_buffer)

    while stack:
        output.append(stack.pop())

    return ''.join(output)

def parser(expression: str) -> double:
    postfix_expression = shunting_yard(expression)
    stack = []

    for token in postfix_expression:
        if token.replace('.', '', 1).isdigit(): 
            stack.append(float(token))
        elif token in {'+', '-', '*', '/'}:
            right = stack.pop()
            left = stack.pop()
            if token == '+':
                stack.append(left + right)
            elif token == '-':
                stack.append(left - right)
            elif token == '*':
                stack.append(left * right)
            elif token == '/':
                stack.append(left / right)

    return stack[-1]




