import os
import sys

from Machine import Machine, MachineError
import Define
import Operators

machine = Machine()
machine.addOperator( Define.DefineOperator() )
machine.addOperator( Define.VariableOperator() )

for i in Operators.__dict__:
    if i[0] != '_':
        op = Operators.__dict__[i]
        machine.addOperator( op() )

if len(sys.argv) >= 2:
    print('loading file "'+sys.argv[1]+'"')
    inputFile = open(sys.argv[1],'r');

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
                print( machine.parse(text[index:i+1]))
                index = i+1
    if openCount != 0:
        error('The number of opening and closing brackets '+
        'do not matching the arguments to processing file')
else:
    print('Starting REPL.')
    print('Type "stop" or "exit" to end')
    text = ''
    while True:
        text = raw_input('>>> ')
        text = text.strip().replace(' ','')
        if text == 'stop' or text == 'exit':
            break
        try:
            print(machine.parse(text))
        except MachineError as exc:
            print(machine.errorMessage)
            for i in range(len(machine.stack)-1,-1,-1):
                frame = machine.stack[i]
                print('  '+str(frame))
            machine.clearError()

