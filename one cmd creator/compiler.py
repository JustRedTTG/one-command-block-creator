import os
from defaults import functions

def mount(string:str):
    # Functions
    final = ''
    issues = []
    lineI = 1
    lines = string.splitlines()
    while lineI <= len(lines):
        line = lines[lineI-1]
        if line.startswith('>$'):
            name = line[2:len(line)]
            function = ''
            lineI += 1
            while True:
                try:
                    line = lines[lineI-1]
                except:
                    issues.append(f'[mount:{lineI}] - Expected function to end.')
                if line.startswith('<'):
                    break
                function += line + '\n'
                lineI += 1
            functions[name] = function
        elif line.startswith('$<'):
            name = line[2:len(line)]
            file = os.path.join('commands', name, name+'.txt')
            with open(file, 'r') as f:
                string = f.read()
            mount(string)
        elif line.startswith('$'):
            try:
                function_name = line[1:len(line)].split(' ')[0]
                function = functions[function_name]
                i = 0
                variables = line[1:len(line)].split(' ')
                while i < len(variables):
                    function = function.replace(f'%{i}%', variables[i])
                    i += 1
                final += function
            except KeyError:
                function_name = line[1:len(line)].split(' ')[0]
                final += f'^Unknown function "{function_name}"'
                issues.append(f'[mount:{lineI}] - Unknown function "{function_name}"')
        else:
            final += line + '\n'
        lineI += 1
    lineI = 1
    lines = final.splitlines()
    final = ''
    while lineI <= len(lines):
        line = lines[lineI - 1]
        squig = '#$'
        if len(line.split(squig))>1 and int(len(line.split(squig))/2) != len(line.split(squig))/2:
            dips = line.split(squig)
            index = 0
            while index < len(dips)-1:
                mathO = dips[index+1]
                index += 2
                try:
                    result = eval(mathO)
                except:
                    issues.append(f'[mount:{lineI}] - Cannot eval {mathO}')
                    result = 0
                line = line.replace(f'{squig}{mathO}{squig}', str(result))
            final += line + '\n'
        elif len(line.split(squig))>1 and int(len(line.split(squig))/2) == len(line.split(squig))/2:
            issues.append(f'[mount:{lineI}] - Missing closing {squig}')
        else:
            final += line + '\n'
        lineI += 1
    return final, issues

def compile(string:str, issues):
    final = 'summon minecraft:falling_block ~ ~1 ~ {Time:1,BlockState:{Name:"minecraft:redstone_block"},Passengers:['

    for line in string.splitlines():
        if line == '' or line.startswith('^'):
            continue
        if line.startswith('@'):
            final += '{id:"minecraft:falling_block",BlockState:{Name:"'+line[1:len(line)]+'"},Time:1}'
        else:
            final += '{id:"minecraft:command_block_minecart",Command:"'+line.replace('"','\\"')+'"}'
        final += ','
    final += ']}'
    return final, issues
