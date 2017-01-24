import sys

class PyTetris:
    """
    Create my own tetris game using Python
    """
    def __init__(self, difficulty, size = None):
        self.__difficulty__ = difficulty
        self.__shapes__ = None
        self.__position__ = None
        self.__score__ = 0
        self.__block__ = "O "
        if not size:
            size = [10,22]
            # Default Size [10, 22]
        self.__screen__ =  [[self.__block__ for _ in range(size[0]+2)]] + \
                            [[self.__block__] +["  " for _ in range(size[0])] + [self.__block__]
                                         for _ in range(size[1])] + \
                                [[self.__block__ for _ in range(size[0]+2)]]
        self.__stacks__ = None
        self.__tetris__ = {"J_d":[5,10]}
        self.__allshapes__ = {"J_d":[[0,1],[1,-1],[1,-2]], \
                              "J_l":[[0,-1],[0,-2],[1,-1]], \
                              "J_u":[[0,-1],[1,1],[1,2]], \
                              "J_r":[[0,1],[0,2],[1,1]] \
                              }

    def PlotPiece(self, type, position):
        ploted = [position[:]]
        for i in range(1,3):
            ploted[i][self.__allshapes__[type][0]] += self.__allshapes__[type][1]
        return ploted

    def PrintScreen(self, direction = None, rotation = None, removal = None):
        screen = self.__screen__[:]
        # for block in self.__tetris__:
        #     screen[block[1]][block[0]] = self.__block__
        screen = "".join(["".join(x)+"\n" for x in screen])
        if (direction, rotation, removal).count(None) == 3:
            # sys.stdout.write("="*(self.__size__[0]+2)+"\n")
            # sys.stdout.write(("|"+" "*self.__size__[0]+"|\n")*(self.__size__[1]))
            # sys.stdout.write("="*(self.__size__[0]+2)+"\n")
            # sys.stdout.flush()
            print(screen)
        pass
    
    def Rotate(self, shape, direction):
        pass
    
    def Move(self, shape, direction):
        pass
    
    def Remove(self, rows):
        pass
    
    def GenerateBlocks(self):
        pass
    
    def AddScore(self, score):
        pass
    
    def GameOver(self):
        pass

if __name__ == "__main__":
    testPy = PyTetris(3)
    control = "start"
    while control != "Q":
        if control == "flush":
            sys.stdout.flush()
        else:
            testPy.PrintScreen()
        control = input("Input Control: ")
    