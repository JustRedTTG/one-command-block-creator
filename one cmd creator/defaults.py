functions = {
    'default-start':"""@minecraft:activator_rail\n""",
    'default-end':"""setblock ~ ~1 ~ minecraft:chain_command_block[facing=up]{auto:1,Command:"fill ~ ~ ~ ~ ~-2 ~ air"}
setblock ~ ~ ~ minecraft:command_block[facing=up]{auto:1,Command:"kill @e[type=minecraft:command_block_minecart,distance=..2]"}\n"""
}