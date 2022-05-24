# compiles code into C++
import template as T
from Lexer import Lexer
import os
import sys

class KPPError(Exception):
    pass


class Compiler:
    def __init__(self):
        # all reserved keywords, cannot be used as variable names
        self.keywords = ['let', 'func', 'end']

    def Compile(self, tokens, file, Compile=True, delete=True):
        code = '''
        '''
        linenum = 0

        for line, x in tokens:
            linenum += 1
            if len(line) == 0:
                continue
            # variables
            if line[0] == 'let':
                if line[2] in self.keywords:
                    raise KPPError(f'[ERR][ln: {linenum}] Cannot use reserved keyword as variable name')
                else:
                    code += line[1] + ' ' + ' '.join(line[2:]) + ';\n'


            elif line[0] == 'func':
                code += T.FUNC.format(type=line[1], nameargs=' '.join(line[2:])) + ' {\n'

            elif line[0] == 'end':
                code += '}\n'

            elif line[0] == 'if':
                code += T.IF.format(cond=line[1]) + '{\n'
            
            elif line[0] == 'elseif':
                code += T.ELSEIF.format(cond=line[1]) + '{\n'
            
            elif line[0] == 'else':
                code += T.ELSE + '{\n'
            
            elif line[0][0] == '#':
                if line[0] == '#include':
                    if line[1][0] == '{' and line[1][-1] == '}':
                        # include file
                        filename = line[1][1:-1] # get filename
                        if os.path.isfile('./'+filename): # check if file exists
                            l = Lexer() # create lexer
                            # compile file
                            self.Compile(l.Analyse(filename), filename.replace('kpp', 'hpp'), Compile=False)
                            code += '#include "{}"\n'.format(filename.replace('kpp', 'hpp')) # add include

                        else:
                            raise KPPError(f'[ERR][ln: {linenum}] Failed to resolve include "{filename}"')

                    else:
                        code += ' '.join(line) + '\n'

                else:
                    code += ' '.join(line) + '\n'

            elif line[0] == 'using':
                code += 'using namespace ' + line[1] + ';\n'
            
            elif line[0] == 'return':
                code += 'return ' + ' '.join(line[1:]) + ';\n'
            
            elif line[0] == 'for':
                code += T.FOR.format(lp=' '.join(line[1:])) + '{\n'
            
            elif line[0] == 'while':
                code += T.WHILE.format(cond=line[1]) + '{\n'
            
            elif line[0] == 'foreach':
                code += T.FOREACH.format(var=line[1], iter=line[2]) + '{\n'
            
            else:
                code += ' '.join(line) + ';\n'

        # write code to file
        with open(file, 'w') as f:
            f.write(code)

        # compile with g++
        if Compile:
            os.system(f'g++ {file} -o {file.replace(".cpp", ".exe")}')
        
        if delete:
            os.remove(file)


c = Compiler()
l = Lexer()

tokens = l.Analyse(sys.argv[1])
c.Compile(tokens, sys.argv[1].replace('kpp', 'cpp'))
