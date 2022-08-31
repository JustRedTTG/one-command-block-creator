import os, compiler, pyperclip, time
from datetime import datetime
from colorama import Fore
from defaults import functions

project = input("Project name: ")
if not os.path.exists(os.path.join('commands', project)):
    os.makedirs(os.path.join('commands', project))
file = os.path.join('commands', project, project+'.txt')

if not os.path.exists(file):
    if input(f"Make a new project called {project} - Y/N : ").lower() != 'y':
        exit()
    with open(file, 'w') as f:
        f.write(f"""$default-start
^ Project name: {project}

$default-end""")

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')
    
last = 0
while True:
    try:
        while last == os.stat(file).st_mtime:
            pass
    except KeyboardInterrupt:
        exit()
    clear()
    last = os.stat(file).st_mtime
    with open(file, 'r') as f:
        string = f.read()
    
    compiler.functions = functions.copy()
    compiler.mounts = functions.copy()
     
    before = time.time()
    mount, issues = compiler.mount(string, project, 'MAIN')
    with open(file.replace(project+'.txt', f'{project}_compiled.txt'), 'w') as f:
        f.write(mount)
    compile, issues = compiler.compile(mount, issues)
    pyperclip.copy(compile)
    print(f"       Finished Compiling! Your command is now in your clipboard.")
    print(f"       finished at:         [{datetime.now().strftime('%H:%M:%S')}]")
    print(f"       total time to compile: [{time.time()-before:.02f}]")
    if len(issues)>0:
        print("Issues: "+Fore.RED)
    for issue in issues:
        print(issue)
    print(Fore.RESET)
