import os, compiler, pyperclip, time
from datetime import datetime
from colorama import Fore
from defaults import functions

project = input("Project name: ")
file = compiler.find_project(project)
project = project.split('.')[-1]

if not os.path.exists(file):
    if input(f"Make a new project called {project} - Y/N : ").lower() != 'y':
        exit()
    if not os.path.exists(os.path.dirname(file)):
        os.makedirs(os.path.dirname(file))
    with open(file, 'w') as f:
        f.write(f"""$default-start
^ Project name: {project}

$default-end""")

print(f'Project "{project}" located at "{file}"\n')

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
    mount, issues, compiler_type = compiler.mount(string, project, 'MAIN')
    with open(file.replace(project+'.txt', f'{project}_compiled.txt'), 'w', encoding='utf-8') as f:
        f.write(mount)
    compile, issues = compiler.compile(mount, issues, compiler_type)
    pyperclip.copy(compile)
    print(f"       Finished Compiling! Your command is now in your clipboard.")
    print(f"       finished at:         [{datetime.now().strftime('%H:%M:%S')}]")
    print(f"       total time to compile: [{time.time()-before:.02f}]")
    if len(issues)>0:
        print("Issues: "+Fore.RED)
    for issue in issues:
        print(issue)
    print(Fore.RESET)
