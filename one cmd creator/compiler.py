import os
functions = {}
mounts = {}

def variable_split(data):
    variable = ''
    variables = []
    string = False
    i = 0
    while i<len(data):
        if data[i] == '"':
            string = not string
        elif data[i] == ' ' and not string:
            variables.append(variable)
            variable = ''
        else:
            variable += data[i]
        i += 1
    variables.append(variable)
    return variables
    

def mount(string:str, filename='unknown', origin='', quiet = False):
    if not quiet:
        print(f"Mount {filename}{' <<< ' if origin else ''}{origin}")
    # Functions
    final = ''
    issues = []
    lineI = 1
    changes = False
    lines = string.splitlines()
    while lineI <= len(lines):
        line = lines[lineI-1]
        if line.startswith('>$'):
            name = line[2:len(line)]
            if name in list(functions): 
                while True:
                    line = lines[lineI-1]
                    if line.startswith('<'):
                        break
                    lineI += 1
                
            function = ''
            lineI += 1
            while not name in list(functions):
                try:
                    line = lines[lineI-1]
                except:
                    issues.append(f'[{origin}{" | " if origin else ""}mount:{lineI}:{filename}] - Expected function to end.')
                if line.startswith('<'):
                    break
                function += line + '\n'
                lineI += 1
            if not name in list(functions):
                functions[name] = function
                changes = True
        elif line.startswith('$<'):
            name = line[2:len(line)]
            file = os.path.join('commands', name, name+'.txt')
            with open(file, 'r') as f:
                string = f.read()
            m, iss = mount(string, name, f'{filename} | $<{name}')
            issues += iss
        elif line.startswith('$'):
            try:
                function_name = line[1:len(line)].split(' ')[0]
                function = functions[function_name]
                i = 0
                variables = variable_split(line[1:len(line)])
                while i < len(variables):
                    function = function.replace(f'%{i}%', variables[i])
                    i += 1
                function, iss = mount(function, '$'+function_name, f'"{filename}"', True)
                issues += iss
                mounts[function_name] = function
                changes = True
                final += function
            except KeyError:
                function_name = line[1:len(line)].split(' ')[0]
                final += f'^Unknown function "{function_name}"'
                issues.append(f'[{origin}{" | " if origin else ""}mount:{lineI}:{filename}] - Unknown function "{function_name}"')
        else:
            final += line + '\n'
        lineI += 1
    lineI = 1
    lines = final.splitlines()
    final = ''
    while lineI <= len(lines):
        line = lines[lineI - 1]
        squig = '#$'
        squig2 = '//'
        if len(line.split(squig))>1 and int(len(line.split(squig))/2) != len(line.split(squig))/2:
            dips = line.split(squig)
            index = 0
            while index < len(dips)-1:
                mathO = dips[index+1]
                index += 2
                try:
                    result = eval(mathO)
                except:
                    issues.append(f'[{origin}{" | " if origin else ""}mount:{lineI}:{filename}] - Cannot eval {mathO}')
                    result = 0
                line = line.replace(f'{squig}{mathO}{squig}', str(result))
            final += line + '\n'
        elif len(line.split(squig))>1 and int(len(line.split(squig))/2) == len(line.split(squig))/2:
            issues.append(f'[{origin}{" | " if origin else ""}mount:{lineI}:{filename}] - Missing closing {squig}')
        elif len(line.split(squig2))>1 and int(len(line.split(squig2))/2) != len(line.split(squig2))/2:
            dips = line.split(squig2)
            index = 0
            while index < len(dips)-1:
                string = dips[index+1]
                index += 2
                try:
                    result = string.replace('"', '\\"')
                except:
                    issues.append(f'[{origin}{" | " if origin else ""}mount:{lineI}:{filename}] - Cannot fix "{string}"')
                    result = 0
                line = line.replace(f'{squig2}{string}{squig2}', result)
            final += line + '\n'
        elif len(line.split(squig2))>1 and int(len(line.split(squig2))/2) == len(line.split(squig2))/2:
            issues.append(f'[{origin}{" | " if origin else ""}mount:{lineI}:{filename}] - Missing closing {squig2}')
        else:
            final += line + '\n'
        lineI += 1
    if changes or origin == 'MAIN':
        if not quiet:
            print(f'       {filename}\n')
    return final, issues

def compile(string:str, issues):
    print("Compiling command...")
    starter = 'summon minecraft:falling_block ~ ~1 ~ {Time:1,BlockState:{Name:"minecraft:redstone_block"},Passengers:['
    final = ''

    for line in string.splitlines():
        if line == '' or line.startswith('^'):
            continue
        if line.startswith('@'):
            final += line[1:len(line)]
        if line.startswith('?'):
            starter = line[1:len(line)]
        else:
            final += '{id:"minecraft:command_block_minecart",Command:"'+line.replace('"','\\"')+'"}'
            final += ','
    final += ']}'
    return starter+final, issues
