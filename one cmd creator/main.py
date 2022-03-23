import os, compiler, pyperclip
from colorama import Fore

project = input("Project name: ")
if not os.path.exists(os.path.join('commands', project)):
    os.makedirs(os.path.join('commands', project))
file = os.path.join('commands', project, project+'.txt')

if not os.path.exists(file):
    with open(file, 'w') as f:
        f.write(f"""$default-start
^Project name: {project}

$default-end""")
os.system("cls")
print('')
last = 0
while True:
    while last == os.stat(file).st_mtime:
        pass
    last = os.stat(file).st_mtime
    with open(file, 'r') as f:
        string = f.read()
    mount, issues = compiler.mount(string)
    with open(file.replace(project+'.txt', f'{project}_compiled.txt'), 'w') as f:
        f.write(mount)
    compile, issues = compiler.compile(mount, issues)
    pyperclip.copy(compile)
    print("Finished Compiling - copied to clipboard")
    if len(issues)>0:
        print("Issues: "+Fore.RED)
    for issue in issues:
        print(issue)
    print(Fore.RESET)
