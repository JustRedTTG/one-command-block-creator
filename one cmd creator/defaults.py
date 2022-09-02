functions = {
    'default-start':"""@{id:"minecraft:falling_block",BlockState:{Name:"minecraft:activator_rail"},Time:1}\n""",
    'new-start':"""?summon minecraft:falling_block ~ ~2 ~ {Time:1,BlockState:{Name:"minecraft:activator_rail"},Passengers:[{id:"command_block_minecart", Command:"summon falling_block ~ ~2 ~ {Time:1, BlockState:{Name:\\"redstone_block\\"}}",CustomName:"\\"m\\""},{id:"command_block_minecart", Command:"summon falling_block ~ ~3 ~ {Time:1, BlockState:{Name:\\"activator_rail\\"}}",CustomName:"\\"m\\""},{id:"command_block_minecart", Command:"summon command_block_minecart ~ ~4 ~ {Command:\\"tp @e[type=command_block_minecart,distance=..2] ~ ~ ~\\",CustomName:\\"\\\\\\"m\\\\\\"\\"}",CustomName:"\\"m\\""},{id:"command_block_minecart", Command:"summon command_block_minecart ~ ~4 ~ {Command:\\"kill @e[type=command_block_minecart,distance=..2,name=m]\\",CustomName:\\"\\\\\\"m\\\\\\"\\"}",CustomName:"\\"m\\""},{id:"command_block_minecart", Command:"setblock ~ ~ ~ air",CustomName:"\\"m\\""},""",
    'default-end':"""setblock ~ ~1 ~ minecraft:chain_command_block[facing=up]{auto:1,Command:"fill ~ ~ ~ ~ ~-2 ~ air"}
setblock ~ ~ ~ minecraft:command_block[facing=up]{auto:1,Command:"kill @e[type=minecraft:command_block_minecart,distance=..2]"}\n""",
    'default-fullend':"""setblock ~ ~1 ~ minecraft:chain_command_block[facing=up]{auto:1,Command:"fill ~ ~ ~ ~ ~-3 ~ air"}
setblock ~ ~ ~ minecraft:command_block[facing=up]{auto:1,Command:"kill @e[type=minecraft:command_block_minecart,distance=..2]"}\n"""
}
