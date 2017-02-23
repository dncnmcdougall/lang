import os
import sys

import Operators

global operators 
operators = {}

class Expression:
    numberOfArguments = 0
    def __init__(self, text):
        self.text = text
    def process(self ):
        global operators
        parts = self.text.split('(',1);
        operator = parts[0]
        if operator not in operators:
            try:
                return float(operator)
            except Exception as e:
                error('operator "'+operator+'" not found: '+str(e))
        if len(parts) != 2:
            error('expected ( to follow operator')
        if parts[1][-1] != ')':
            error('unclosed parentheses: '+parts[1])

        args = parts[1][:-1]
        openCount=0
        index = 0
        parts = []
        for i in range(0,len(args)):
            if args[i] == '(':
                openCount += 1
            elif args[i] == ')':
                openCount -= 1
            elif openCount == 0 and args[i] == ',':
                parts += [args[index:i]]
                index = i+1
        if openCount != 0:
            error('The number of opening and closing brackets '+
            'do not matching the arguments to processing "'+operator+'"')
        parts += [args[index:]]

        cls = operators[operator]
        if len(parts) != cls.numberOfArguments:
            error('"'+operator+'" takes '+
                    str(cls.numberOfArguments)+
                    ' arguments but found '+str(len(parts)))
        args = []
        if cls.symbol == Define.symbol:
            args += [parts[0]]
            args += [Expression(parts[1])]
            args += [parts[2]]
        elif cls.userDeined:
            args = parts
        else:
            for part in parts:
                args += [Expression(part)]
        result = cls.process(args)
        return result

class UserDefinedOperator:
    userDeined = True
    def __init__(self, symbol, numberOfArguments, expression):
        self.symbol = symbol
        self.numberOfArguments = numberOfArguments
        self.expression = expression
    def process(self, values):
        text = ''
        openIndex = 0
        closeIndex = -1
        openCount = 0
        for i in range(0,len(self.expression)):
            if self.expression[i] == '{':
                openCount += 1
                if openCount == 1:
                    openIndex = i
            elif self.expression[i] == '}':
                openCount -= 1
                if openCount == 0:
                    text += self.expression[closeIndex+1:openIndex]
                    closeIndex = i
                    inxText = self.expression[openIndex+1:closeIndex]
                    exp = Expression(inxText)
                    val = exp.process();
                    text += values[int(exp.process())]
        if openCount != 0:
            error('The number of opening and closing brackets '+
            'do not matching the arguments to processing "'+self.symbol+'"')
        text += self.expression[closeIndex+1:]
        exp = Expression(text)
        return exp.process()

class Define:
    symbol='def'
    numberOfArguments = 3
    def process(self,values):
        global operators
        symbol = values[0]
        numberOfArguments = values[1].process()
        expression = values[2]
        operators[symbol] = UserDefinedOperator(symbol, numberOfArguments, expression)
        return 0


for i in Operators.__dict__:
    if i[0] != '_':
        cls = Operators.__dict__[i]
        operators[cls.symbol] = cls()

operators[Define.symbol] = Define()

def error(message):
    print('error: '+str(message))
    # raise 'Cats'
    exit(1)

inputFile = open('input.lang','r');

text = '';

for line in inputFile:
    text += line.strip()

text = text.replace(' ','')
text = text.replace('\t','')

openCount = 0
index = 0
for i in range(0,len(text)):
    if text[i] == '(':
        openCount += 1
    elif text[i] == ')':
        openCount -= 1
        if openCount == 0:
            print( Expression(text[index:i+1]).process())
            index = i+1
if openCount != 0:
    error('The number of opening and closing brackets '+
    'do not matching the arguments to processing file')

