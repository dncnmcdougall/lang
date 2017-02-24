from types import *

class MachineError(Exception):
    def __init__(self):
        self.message = 'The machine encountered a problem'


class Machine:
    def __init__(self):
        self.operators = {}
        self.stack = []
        self.errorMessage = ""

    def clearError(self):
        self.errorMessage = ""
        self.stack = []

    def addOperator(self, processor):
        try:
            if type( processor.symbol ) is not StringType:
                raise AttributeError('symbol not defined')
            if type( processor.minArgs ) is not IntType:
                raise AttributeError('minArgs not defined')
            if type( processor.maxArgs ) is not IntType:
                raise AttributeError('maxArgs not defined')
            if type( processor.process ) is not MethodType:
                raise AttributeError('process not defined')
            if type( processor.description ) is not StringType:
                raise AttributeError('description not defined')
            if processor.minArgs < 0:
                raise AttributeError('minArgs < 0')
            if processor.maxArgs >=0 and processor.minArgs > processor.maxArgs:
                raise AttributeError('minArgs > maxArgs')
        except AttributeError as err:
            self.error("The operator is malformed: "+err.message+"\n received: "+str(processor.__dict__))
        self.operators[ processor.symbol ] = processor

    def describeOperator(self, operator):
        if operator in self.operators:
            print( self.operators[operator].description )
        else:
            self.error('operator "'+operator+'" not defined ')

    def error(self, message):
        self.errorMessage = 'error: '+str(message)
        raise MachineError()

    def parse(self, text):
        self.stack.append( text )
        parts = text.split('(',1);
        operator = parts[0]
        if operator not in self.operators:
            try:
                value = float(operator)
                self.stack.pop()
                return value
            except Exception as e:
                self.error('operator "'+operator+'" not found: '+str(e))
        if len(parts) != 2:
            self.error('expected ( to follow operator')
        if parts[1][-1] != ')':
            self.error('unclosed parentheses: '+parts[1])


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
            self.error('The number of opening and closing brackets '+
            'do not matching the arguments to processing "'+operator+'"')
        parts += [args[index:]]
        if len(parts) == 1:
            if len(parts[0]) == 0:
                parts = []

        processor = self.operators[operator]
        numArgs = len(parts)

        if numArgs < processor.minArgs:
            self.error('"'+operator+'" takes at least '+
                    str(processor.minArgs)+
                    ' arguments but found '+str(numArgs))
        elif processor.maxArgs >=0 and numArgs > processor.maxArgs:
            self.error('"'+operator+'" takes at most '+
                    str(processor.maxArgs)+
                    ' arguments but found '+str(numArgs))
        result = processor.process(parts, self)

        self.stack.pop()
        return result


