
class UserDefinedOperator:
    def __init__(self, symbol, minArgs, maxArgs, expression, description):
        self.symbol = symbol
        self.minArgs = minArgs
        self.maxArgs = maxArgs
        self.expression = expression
        self.description = description
    def process(self, values, machine):
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
                    val = machine.parse(inxText)
                    text += values[int(val)]
        if openCount != 0:
            error('The number of opening and closing brackets '+
            'do not matching the arguments to processing "'+self.symbol+'"')
        text += self.expression[closeIndex+1:]
        val = machine.parse( text )
        return val

class DefineOperator:
    symbol='def'
    minArgs = 3
    maxArgs = 5
    description = """defines a new operator 
    This has three forms: 
        def( symbol, numArgs, code) 
            returns 0 and uses a default description
        def(symbol, numArgs, code, expression)
            returns the evaluated expression and uses a default description
        def(symbol, numArgs, code, description, expression)
            returns the evaluated expression and uses a the given description
    code is text that defines the operation of this definition.
    It is the same as normal code except that {i} will be replaced by the ith parameter 
    parsed into the operator. 
    The text inside {} is evaluated to give the number. 
    Note that {}s cannot be nested and the evaluation must resolve to a whole number.
    """
    def process(self, values, machine):
        numArgs = len(values)
        symbol = values[0]
        minArgs = int(machine.parse(values[1]))
        maxArgs = minArgs
        expression = values[2]

        if numArgs == 5:
            description = values[3]
        elif numArgs <= 4:
            description = 'User operator: "'+symbol+'" taking ['+str(minArgs)+', '+str(maxArgs)+'] arguments'

        machine.addOperator( UserDefinedOperator(
            symbol, minArgs, maxArgs, expression, description) )

        if numArgs == 5:
            return machine.parse(values[4])
        elif numArgs == 4:
            return machine.parse(values[3])
        else:
            return 0.0

class VariableOperator:
    symbol='var'
    minArgs = 2
    maxArgs = 4
    description = """This defines a variable.
    This has three forms:
        var(name, expression)
            defines a variable with name and sets its value to the result of expression.
            uses a default description
            returns the value of the variable
        var(name, varExp, nextExp)
            defines a variable with name and sets its value to the result of varExp.
            uses a default description
            returns the result of nextExp.
        var(name, varExp, description, nextExp)
            defines a variable with name and sets its value to the result of varExp.
            uses the given description
            returns the result of nextExp.
    This is an alias for
    def(name, 0, varExp, description, nextExp)
    with the difference that varExp is evaluated now when using var,
    and at execution time when using def.
    """
    def process(self, values, machine):
        name = str(values[0])
        value = machine.parse( values[1] )
        machine.addOperator( UserDefinedOperator(
            name, 0, 0, str(value), "Variable "+name) )
        if len(values) == 3:
            return machine.parse( values[2] )
        else:
            return value


            
