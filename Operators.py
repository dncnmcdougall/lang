
class PlusOperator:
    userDeined = False
    symbol = '+'
    numberOfArguments = 2
    def process(self, values):
        return values[0].process() + values[1].process()

class SubtractOperator:
    userDeined = False
    symbol = '-'
    numberOfArguments = 2
    def process(self, values):
        return values[0].process() - values[1].process()

class MultiplyOperator:
    userDeined = False
    symbol = '*'
    numberOfArguments = 2
    def process(self, values):
        return values[0].process()*values[1].process()

class DivideOperator:
    userDeined = False
    symbol = '/'
    numberOfArguments = 2
    def process(self, values):
        return values[0].process()/values[1].process()

class LessThan:
    userDeined = False
    symbol = "<"
    numberOfArguments = 4
    def process(self, values):
        if values[0].process() < values[1].process():
            return values[2].process()
        else:
            return values[3].process()

class If:
    userDeined = False
    symbol='if'
    numberOfArguments = 3
    def process(self, values):
        if values[0].process():
            return values[1].process()
        else:
            return values[2].process()

class Print:
    userDeined = False
    symbol='print'
    numberOfArguments = 1
    def process(self, values):
        val = values[0].process()
        print('print: ' +str(val))
        return val

