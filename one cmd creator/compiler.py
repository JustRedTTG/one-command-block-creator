from defaults import functions

def mount(string:str):
    # Functions
    final = ''
    issues = []
    lineI = 1
    for line in string.splitlines():
        if line.startswith('$'):
            try:
                final += functions[line[1:len(line)].replace(' ', '')]
            except:
                final += f'^Unknown function "{line[1:len(line)].replace(" ", "")}"'
                issues.append(f'[mount:{lineI}] - Unknown function "{line[1:len(line)].replace(" ", "")}"')
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