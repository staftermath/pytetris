import sys, os, copy

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
        self.__tetris__ = {"J_l":[5,10]}
        self.__allshapes__ = {"J_d":[[1,0],[0,-1],[0,-2]], \
                              "J_l":[[-1,0],[-2,0],[0,-1]], \
                              "J_u":[[-1,0],[0,1],[0,2]], \
                              "J_r":[[0,1],[1,0],[2,0]] \
                              }
        self.__rotate__ = {"J_l":[["J_d","J_u"], [[-1,1],[-1,-1]]], \
                            "J_d":[["J_r","J_l"],[[-1,-2],[1,-1]]], \
                            "J_r":[["J_u","J_d"],[[1,0],[1,2]]], \
                            "J_u":[["J_l", "J_r"],[[1,1],[-1,0]]]}

    def PlotPiece(self, piece):
        ploted = [list(piece.values())[0][:]]
        for i in range(1,4):
            ploted.append(list(piece.values())[0][:])
            ploted[i][0] += self.__allshapes__[list(piece.keys())[0]][i-1][0]
            ploted[i][1] += self.__allshapes__[list(piece.keys())[0]][i-1][1]
        # print(ploted)
        return ploted

    def PrintScreen(self, direction = None, rotation = None, removal = None):
        screen = [list(_) for _ in self.__screen__]
        # thisBlock = list(self.__tetris__.items())[0][1]
        for block in self.PlotPiece(self.__tetris__):
            screen[block[1]][block[0]] = self.__block__
        screen = "".join(["".join(x)+"\n" for x in reversed(screen)])
        if (direction, rotation, removal).count(None) == 3:
            # sys.stdout.write("="*(self.__size__[0]+2)+"\n")
            # sys.stdout.write(("|"+" "*self.__size__[0]+"|\n")*(self.__size__[1]))
            # sys.stdout.write("="*(self.__size__[0]+2)+"\n")
            # sys.stdout.flush()
            print(screen)
        pass
    
    def Rotate(self, direction):
        if direction == "counter":
            direction = 0
        else:
            direction = 1
        shape = list(self.__tetris__.items())[0][0]
        center = list(self.__tetris__.items())[0][1][:]
        newshape = self.__rotate__[shape][0][direction]
        center[0] += self.__rotate__[shape][1][direction][0]
        center[1] += self.__rotate__[shape][1][direction][1]
        self.__tetris__ = {newshape:center}
    
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
    os.system('cls')
    testPy = PyTetris(3)
    control = "start"
    while control != "Q":
        if control == "flush":
            os.system('cls')
        elif control == "L":
            testPy.Rotate("clock")
            os.system('cls')
            # print(testPy.__tetris__)
            testPy.PrintScreen()
        elif control == "R":
            testPy.Rotate("counter")
            os.system('cls')
            testPy.PrintScreen()
        elif control == "shape":
            print(testPy.__tetris__)
        elif control == "screen":
            print(testPy.__screen__)
        else:
            testPy.PrintScreen()
        control = input("Input Control: ")
    