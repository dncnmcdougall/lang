
class PlusOperator:
    symbol = '+'
    minArgs = 2
    maxArgs = -1
    description = "{0}+{1}+{2}...+{n}"
    def process(self, values, machine):
        value = machine.parse(values[0])
        for i in range(1,len(values)):
            value += machine.parse(values[i])
        return value

class SubtractOperator:
    symbol = '-'
    minArgs = 2
    maxArgs = -1
    description = "{0}-{1}-{2}...-{n}"
    def process(self, values, machine):
        value = machine.parse(values[0])
        for i in range(1,len(values)):
            value -= machine.parse(values[i])
        return value

class MultiplyOperator:
    symbol = '*'
    minArgs = 2
    maxArgs = -1
    description = "{0}*{1}*{2}...*{n}"
    def process(self, values, machine):
        value = machine.parse(values[0])
        for i in range(1,len(values)):
            value *= machine.parse(values[i])
        return value

class DivideOperator:
    symbol = '/'
    minArgs = 2
    maxArgs = 2
    description = "{0}/{1}"
    def process(self, values, machine):
        return machine.parse(values[0]) / machine.parse(values[1])

class LessThan:
    symbol = "<"
    minArgs = 4
    maxArgs = 4
    description = "if {0} < {1} then {2} else {3}"
    def process(self, values, machine):
        if machine.parse(values[0]) < machine.parse(values[1]):
            return machine.parse( values[2] )
        else:
            return machine.parse( values[3] )

class If:
    symbol='if'
    minArgs = 3
    maxArgs = 3
    description = "if {0} si not zero then {1} else {2}"
    def process(self, values, machine):
        if machine.parse( values[0] ):
            return machine.parse( values[1] )
        else:
            return machine.parse( values[2] )

class Print:
    symbol='print'
    minArgs = 1
    maxArgs = 1
    description = "prints 'print: {0}' and returns {0}"
    def process(self, values, machine):
        val = machine.parse( values[0] )
        print('print: ' +str(val))
        return val

class Describe:
    symbol='desc'
    minArgs = 1
    maxArgs = 2
    description = """Prints the description of an operator. 
    This has two forms:
        desc(operator)
            describes operator and returns 0.0.
        desc(operatr, expression)
            describes operator and then returns the result of expression."
    """
    def process(self, values, machine):
        machine.describeOperator( values[0] )
        if len(values) == 2:
            return machine.parse( values[1] )
        else:
            return 0.0

