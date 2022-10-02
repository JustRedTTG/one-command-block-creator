import os.path, json
import tkinter as tk
from tkinter import filedialog
from litemapy import Schematic

root = tk.Tk()
root.withdraw()
file = filedialog.askopenfilename()
schem = Schematic.load(file)
reg = list(schem.regions.values())[0]
final=f"""$default-start
fill ~1 ~1 ~1 ~{reg.xrange().stop+1} ~{reg.yrange().stop+1} ~{reg.zrange().stop+1} air
"""
parts = 0
path = file.split('/')
path.reverse()
name = path[0].split('.')[0]
if not os.path.exists(f'../commands/scem_{name}'):
    os.makedirs(f'../commands/scem_{name}')

for x in reg.xrange():
    for z in reg.zrange():
        for y in reg.yrange():
            b = reg.getblock(x, y, z)
            if b.blockid == 'minecraft:air':
                continue
            sq = '{}'
            p = json.loads(str(b).replace(b.blockid,''))
            squareItems = ''
            squiggleItems = ''
            for item in list(p):
                squareItems+=f'{item}={p[item]},'
            s = f"setblock ~{x+1} ~{y+1} ~{z+1} {b.blockid}[{squareItems}]{sq[0]}{squiggleItems}{sq[1]}\n"
            if len(s)+len(final)<10000:
                final += s
                parts += 1
            else:
                final += "$default-end"
                with open(f'../commands/scem_{name}/scem_{name}.txt', 'w') as f:
                    f.write(final)
                final = "$default-start\n"
                print(f"Packed {parts} blocks")
                input("Press enter to get next part... ")
                parts = 0