import sys, os, copy, random, msvcrt

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
            self.__size__ = [10,22]
            # Default Size [10, 22]
        else:
            self.__size__ = size[:]
        self.__screen__ =  [[self.__block__ for _ in range(self.__size__[0]+2)]] + \
                            [[self.__block__] +["  " for _ in range(self.__size__[0])] + [self.__block__]
                                         for _ in range(self.__size__[1])] + \
                                [[self.__block__ for _ in range(self.__size__[0]+2)]]
        self.__stacks__ = [[5, 21], [4, 21], [3, 21], [5, 22]]
        self.__tetris__ = {"J_l":[5,16]}
        self.__allshapes__ = {"J_d":[[1,0],[0,1],[0,2]], \
                              "J_l":[[-1,0],[-2,0],[0,1]], \
                              "J_u":[[-1,0],[0,-1],[0,-2]], \
                              "J_r":[[0,-1],[1,0],[2,0]] \
                              }
        self.__rotate__ = {"J_l":[["J_d","J_u"], [[-1,-1],[-1,1]]], \
                            "J_d":[["J_r","J_l"],[[-1,2],[1,1]]], \
                            "J_r":[["J_u","J_d"],[[1,0],[1,-2]]], \
                            "J_u":[["J_l", "J_r"],[[1,-1],[-1,0]]]}
        self.__move__ = {"down":[0,1], \
                        "left":[-1,0], \
                        "right":[1,0]
                        }

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
        for block in self.__stacks__:
            screen[block[1]][block[0]] = self.__block__
        screen = "".join(["".join(x)+"\n" for x in screen])
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
        if not self.BoundaryCheck(block=self.PlotPiece({newshape:center}), action=direction):
            self.__tetris__ = {newshape:center}
    
    def Move(self, direction):
        value = copy.deepcopy(list(self.__tetris__.items())[0])
        value[1][0] += self.__move__[direction][0]
        value[1][1] += self.__move__[direction][1]
        if not self.BoundaryCheck(block=self.PlotPiece({value[0]:value[1]}), action=direction):
            self.__tetris__ = {value[0]:value[1]}
        return None
    
    def Remove(self, rows):
        pass
    
    def GenerateBlocks(self):
        newblock = random.sample(self.__rotate__.keys(),1)[0]
        self.__tetris__={newblock:[5,0]}
    
    def AddScore(self, score):
        pass
    
    def BoundaryCheck(self, block,action):
        returnBool = False
        if action != "down":
            for x in block:
                if x[0]<=0 or x[0]>self.__size__[0] or x[1]>=self.__size__[1]:
                    returnBool = True
                    break
                if x in self.__stacks__:
                    returnBool = True
                    break
        else:
            for x in block:
                if x[1]>self.__size__[1] or x in self.__stacks__:
                    value = list(self.__tetris__.items())[0]
                    # value[1][1] -=1
                    self.__stacks__.extend(self.PlotPiece({value[0]:value[1]}))
                    returnBool = True
                    self.GenerateBlocks()
                    break
                if x[0]<=0 or x[0]>self.__size__[0]: 
                    returnBool = True
                    break
        return returnBool

    def GameOver(self):
        pass

if __name__ == "__main__":
    os.system('cls')
    testPy = PyTetris(3)
    control = "start"
    while control != "Q":
        if control == "flush":
            os.system('cls')
        elif control == "j":
            testPy.Rotate("clock")
            os.system('cls')
            # print(testPy.__tetris__)
            testPy.PrintScreen()
        elif control == "l":
            testPy.Rotate("counter")
            os.system('cls')
            testPy.PrintScreen()
        elif control == "s":
            testPy.Move("down")
            os.system('cls')
            testPy.PrintScreen()
        elif control == "a":
            testPy.Move("left")
            os.system('cls')
            testPy.PrintScreen()
        elif control == "d":
            testPy.Move("right")
            os.system('cls')
            testPy.PrintScreen()
        elif control == "shape":
            print(testPy.PlotPiece(testPy.__tetris__))
        elif control == "screen":
            print(testPy.__screen__)
        elif control == "stack":
            print(testPy.__stacks__)
        else:
            os.system('cls')
            testPy.PrintScreen()
        print("Input Control: Down: S, Left: A, Right: D, Clockwise: J, CounterClockwise: L ")
        control = msvcrt.getwch()
    