import copy
from block import *
from cursor import *


class Blueprint:
    def __init__(self, block, size):
        self.blueprint = [[[block for col in range(size)]
                           for row in range(size)] for z in range(size)]
        self.size = size

    def __getCommand_setblock(self, x, y, z, block):
        replaceStr = ["bottom", "top", "scursor.block.namede",
                      "front", "base", "(off)", "(on)", "[je only]", "side"]
        name = block.name
        for i in replaceStr:
            name = name.replace("_"+i, "")
        if "block_of" in block.name:
            name = name.replace("block_of_", "")+"_block"

        if x == 0:
            x = ""
        if y == 0:
            y = ""
        if z == 0:
            z = ""
        return "setblock ~{} ~{} ~{} {}:{}\n".format(x, y, z, block.namespace, name)

    def build(self):
        f = open("C:/Users/jjoon/AppData/Roaming/.minecraft/saves/function/datapacks/ejun/data/ejun/functions/blueprint.mcfunction", 'w')

        for y in range(len(self.blueprint)):
            for x in range(len(self.blueprint[y])):
                for z in range(len(self.blueprint[y][x])):
                    if self.blueprint[y][x][z].number > 1:
                        for i in range(1, self.blueprint[y][x][z].number):
                            if(len(self.blueprint) == i):
                                self.blueprint.append([[Block("", 0) for col in range(
                                    len(self.blueprint[y][x]))] for row in range(len(self.blueprint[y]))])
                            elif(len(self.blueprint[y+i]) == 0):
                                self.blueprint[y+i] = [[Block("", 0) for col in range(
                                    len(self.blueprint[y][x]))] for row in range(len(self.blueprint[y]))]
                            if (self.blueprint[y+i][x][z].number == 0):
                                self.blueprint[y + i][x][z] = copy.deepcopy(
                                    self.blueprint[y][x][z])
                                self.blueprint[y+i][x][z].number = 1
                        self.blueprint[y][x][z].number = 1

        for y in range(len(self.blueprint)):
            for x in range(len(self.blueprint[y])):
                for z in range(len(self.blueprint[y][x])):
                    if(self.blueprint[y][x][z].number):
                        f.write(self.__getCommand_setblock(
                            x=x, y=y, z=z, block=self.blueprint[y][x][z]))
        f.close()
