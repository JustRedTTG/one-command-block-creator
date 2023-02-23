import os
functions = {}
mounts = {}

def find_project(name):
    p = ['projects', *name.split('.')]
    p.append(p[-1]+'.txt')
    return os.path.join(*p)

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


def mount(string:str, filename='unknown', origin='', quiet = False, comp_type = None):
    if not quiet:
        print(f"Mount {filename}{' <<< ' if origin else ''}{origin} - {comp_type or 'mc'}")
    # Functions
    final = ''
    issues = []
    lineI = 1
    changes = False
    compiler_type = comp_type or 'mc'
    lines = string.splitlines()
    while lineI <= len(lines):
        line = lines[lineI-1]
        if line.startswith('>$'):
            name = line[2:len(line)]
            if name in list(functions):
                while lineI < len(lines)-1:
                    line = lines[lineI-1]
                    if line.startswith('>$'):
                        issues.append("Definition of function inside function")
                        break
                    if line.startswith('<'):
                        break
                    lineI += 1
                else:
                    issues.append(f'[{origin}{" | " if origin else ""}mount:{lineI}:{filename}] - Expected function to end.')


            function = ''
            lineI += 1
            while not name in list(functions):
                try:
                    line = lines[lineI-1]
                except:
                    issues.append(f'[{origin}{" | " if origin else ""}mount:{lineI}:{filename}] - Expected function to end.')
                    break
                if line.startswith('<'):
                    break
                function += line + '\n'
                lineI += 1
            if not name in list(functions):
                functions[name] = function
                changes = True
        elif line.startswith('$<'):
            name = line[2:len(line)]
            file = find_project(name)
            if not os.path.exists(file):
                m, iss = '', [f'[{origin}{" | " if origin else ""}mount:{lineI}:{filename}] - Unknown project "{name}"']
            else:
                with open(file, 'r', encoding='utf-8') as f:
                    string = f.read()
                try:
                    m, iss, compiler_type = mount(string, name, f'{filename} | $<{name}', comp_type=compiler_type)
                except RecursionError:
                    m, iss = '', [f"Recursive mounting of {filename}"]
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
                try:
                    function, iss, compiler_type = mount(function, '$'+function_name, f'"{filename}"', True, compiler_type)
                except RecursionError:
                    function, iss = '', [f"Recursive mounting of {filename}"]
                issues += iss
                mounts[function_name] = function
                changes = True
                final += function
            except KeyError:
                function_name = line[1:len(line)].split(' ')[0]
                final += f'^Unknown function "{function_name}"'
                issues.append(f'[{origin}{" | " if origin else ""}mount:{lineI}:{filename}] - Unknown function "{function_name}"')
        elif line == '\\n':
            final += '\n'
        elif not line:
            pass
        elif line.startswith('^'):
            l = line[2:15]
            if 'compiler-type' in line[2:15]:
                compiler_type = line[-2:]
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
    return final, issues, compiler_type

def compiler_mc(string:str, issues):
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
            final += '{id:"minecraft:command_block_minecart",Command:"' + line.replace('"', '\\"') + '"}'
        final += ','
        if len(final) > 32497:
            issues.append("TOO BIG")
            final = "say TOO BIG!!"
            break
    final += ']}'
    return starter + final, issues


def compiler_python(string: str, issues):
    print("Compiling command...")
    starter = '# OCBC Python compiler\n'
    final = ''

    for line in string.splitlines():
        final += line + '\r\n'
    return final, issues

def compile(string:str, issues, compiler_type="mc"):
    if compiler_type == 'mc': return compiler_mc(string, issues)
    elif compiler_type == 'py': return compiler_python(string, issues)
    elif compiler_type == 'pe': return '', [*issues, 'Compiler type not properly set']
    else: return '', [*issues, f'Compiler type "{compiler_type}" is unknown']