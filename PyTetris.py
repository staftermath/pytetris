import sys, os, copy, random, msvcrt, curses, time

class PyTetris:
    """
    Create my own tetris game using Python
    """
    def __init__(self, difficulty, size = None, block = "O"):
        self.__difficulty__ = difficulty
        self.__shapes__ = None
        self.__position__ = None
        self.__score__ = 0
        self.__block__ = block
        self.__keys__ = {"down": "s", \
                         "left": "a", \
                         "right": "d", \
                         "clockwise": "k", \
                         "counterclockwise": "j"
                        }
        
        self.__stacks__ = [[10,21]]
        self.__tetris__ = {"J_l":[5,1]}
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
        if not size:
            self.__size__ = [10,22]
            # Default Size [10, 22]
        else:
            self.__size__ = size[:]
        self.__screen__ =  [[self.__block__ for _ in range(self.__size__[0]+2)]] + \
                            [[self.__block__] +["  " for _ in range(self.__size__[0])] + [self.__block__]
                                         for _ in range(self.__size__[1])] + \
                                [[self.__block__ for _ in range(self.__size__[0]+2)]]

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
        global last
        if direction == "counter":
            direction = 0
        elif direction == "clockwise":
            direction = 1
        shape = list(self.__tetris__.items())[0][0]
        center = list(self.__tetris__.items())[0][1][:]
        newshape = self.__rotate__[shape][0][direction]
        center[0] += self.__rotate__[shape][1][direction][0]
        center[1] += self.__rotate__[shape][1][direction][1]
        new = self.PlotPiece({newshape:center})
        if not self.BoundaryCheck(block=new, action=direction):
            for block in self.FilterBlock(last):
                screen.addch(block[1], block[0]*2, " ")
            for block in self.FilterBlock(new):
                screen.addch(block[1], block[0]*2, self.__block__)
            last = copy.deepcopy(new)
            self.__tetris__ = {newshape:center}
    
    def Move(self, direction):
        global last
        newPiece = copy.deepcopy(self.__tetris__)
        if direction == "down":
            list(newPiece.values())[0][1] += 1
        elif direction == "left":
            list(newPiece.values())[0][0] -= 1
        elif direction == "right":
            list(newPiece.values())[0][0] += 1
        new = self.PlotPiece(newPiece)
        if not self.BoundaryCheck(block=new, action=direction):
            for block in self.FilterBlock(last):
                screen.addch(block[1], block[0]*2, " ")
            for block in self.FilterBlock(new):
                screen.addch(block[1], block[0]*2, self.__block__)
            last = copy.deepcopy(new)
            self.__tetris__ = newPiece
        else:
            if direction == "down":
                controlscreen.addstr(1,1,str(last))
                controlscreen.refresh()
                for block in self.FilterBlock(last):
                    screen.addch(block[1], block[0]*2, " ")
                last = copy.deepcopy(self.PlotPiece(self.__tetris__))
                for block in self.__stacks__:
                    screen.addch(block[1], block[0]*2, self.__block__)
        return None

    def FilterBlock(self, piece):
        returnPiece = []
        for block in piece:
            if block[0] <= 0 or block[0]> self.__size__[0]*2 or block[1] <= 0 or block[1] > self.__size__[1]:
                break
            returnPiece.append(block)
        return returnPiece
    
    def Remove(self):
        stackedRow = {}
        toRemove = set()
        emptySet = {x for x in []}
        for block in self.__stacks__:
            if str(block[1]) in stackedRow:
                stackedRow[str(block[1])].add(block[0])
            else:
                stackedRow[str(block[1])] = set([block[0]])
        # controlscreen.addstr(1,1,str(stackedRow))
        # controlscreen.refresh()
        keys = copy.copy(list(stackedRow.keys()))
        for row in keys:
            if len(stackedRow[row]) == self.__size__[0]:
                toRemove.add(int(row))
                del stackedRow[row]
        # controlscreen.addstr(1,1,str(toRemove))
        # controlscreen.refresh()
        toRemove = set(sorted(toRemove))
        lengthToRemove = len(toRemove)
        if lengthToRemove > 0:
            for _ in range(6):
                time.sleep(0.3)
                #     # twoBlock = {self.__block__, " "}.remove(onscreen)
                toPaint = [self.__block__," "][_%2]
                # toPaint = " "
                for row in toRemove:
                    screen.addstr(row,1,(" "+toPaint)*self.__size__[0])
                    screen.refresh()
                    if _ == 5:
                        for block in [[_, row] for _ in range(1,self.__size__[0]+1)]:
                            controlscreen.addstr(20,1,str(block))
                            controlscreen.refresh()
                            self.__stacks__.remove(block)
            for block in self.__stacks__:
                screen.addch(block[1], block[0]*2, " ")
            newStack = []
            for i in range(lengthToRemove):
                for x in self.__stacks__:
                    if x[1] < list(toRemove)[i]:
                        newStack.append([x[0],x[1]+lengthToRemove-i])
                    elif x[1] > list(toRemove)[-1]:
                        newStack.append(x) 
            self.__stacks__ = copy.deepcopy(newStack)
        controlscreen.addstr(1,1,str(self.__stacks__))
        controlscreen.addstr(10,1,str(last))
        controlscreen.refresh()
        #     time.sleep(0.3)
        # newStack = []
        # for key in stackedRow:
        #     newStack.extend([[int(key),x] for x in stackedRow[key]])
        # self.__stacks__ = newStack
        pass
    
    def GenerateBlocks(self):
        newblock = random.sample(self.__rotate__.keys(),1)[0]
        self.__tetris__={newblock:[5,0]}
    
    def AddScore(self, score):
        pass
    
    def BoundaryCheck(self, block,action):
        global last
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
                if x[1]>=self.__size__[1] or x in self.__stacks__:
                    # value = copy.deepcopy(list(self.__tetris__.items()))[0]
                    # value[1][1] -=1
                    self.__stacks__.extend(copy.deepcopy(last))
                    self.Remove()
                    curses.flushinp()
                    returnBool = True
                    self.GenerateBlocks()
                    # last = copy.deepcopy(self.PlotPiece(self.__tetris__))
                    break
                if x[0]<=0 or x[0]>self.__size__[0]: 
                    returnBool = True
                    break
        return returnBool

    def GameOver(self):
        pass

if __name__ == "__main__":
    tinyblock = "@"
    testPy = PyTetris(difficulty=3, block = tinyblock)
    fullscreen = curses.initscr()
    screen = fullscreen.subwin(0,0)
    screen.resize(testPy.__size__[1]+1, 2*testPy.__size__[0]+4)
    controlscreen = fullscreen.subwin(0, 2*testPy.__size__[0]+5)
    controlscreen.border()
    controlscreen.refresh()
    screen.border()
    screen.keypad(True)
    screen.nodelay(True)
    curses.raw()
    curses.cbreak()
    curses.noecho()
    dims = screen.getmaxyx()
    curses.curs_set(0)
    screen.refresh()
    for block in testPy.__stacks__:
        screen.addch(block[1], block[0]*2, tinyblock)
    p = -1
    last = testPy.PlotPiece(testPy.__tetris__)
    for block in last:
            # print(block[1])
            screen.addch(block[1], block[0]*2, tinyblock)
    while p != ord("q"):
        p = screen.getch()
        if p == curses.KEY_DOWN or p == ord(testPy.__keys__["down"]):
            testPy.Move(direction="down")
            next
        if p == curses.KEY_LEFT or p == ord(testPy.__keys__["left"]):
            testPy.Move(direction="left")
            next
        if p == curses.KEY_RIGHT or p == ord(testPy.__keys__["right"]):
            testPy.Move(direction="right")
            next
        # Rotate
        if p == ord(testPy.__keys__["clockwise"]):
            testPy.Rotate(direction="clockwise")
            next
        if p == ord(testPy.__keys__["counterclockwise"]):
            testPy.Rotate(direction="counter")
            next
            # list(testPy.__tetris__.values())[0][1] += 1 
            # new = testPy.PlotPiece(testPy.__tetris__)
            # for block in last:
            #     screen.addch(block[1], block[0]*2, " ")
            # for block in new:
            #     screen.addch(block[1], block[0]*2, "O")
            # last = copy.deepcopy(new)
    curses.endwin()
    os.system('cls')
    # os.system('cls')
    # testPy = PyTetris(3)
    # control = "start"
    # while control != "Q":
    #     if control == "flush":
    #         os.system('cls')
    #     elif control == "j":
    #         testPy.Rotate("clock")
    #         os.system('cls')
    #         # print(testPy.__tetris__)
    #         testPy.PrintScreen()
    #     elif control == "l":
    #         testPy.Rotate("counter")
    #         os.system('cls')
    #         testPy.PrintScreen()
    #     elif control == "s":
    #         testPy.Move("down")
    #         os.system('cls')
    #         testPy.PrintScreen()
    #     elif control == "a":
    #         testPy.Move("left")
    #         os.system('cls')
    #         testPy.PrintScreen()
    #     elif control == "d":
    #         testPy.Move("right")
    #         os.system('cls')
    #         testPy.PrintScreen()
    #     elif control == "shape":
    #         print(testPy.PlotPiece(testPy.__tetris__))
    #     elif control == "screen":
    #         print(testPy.__screen__)
    #     elif control == "stack":
    #         print(testPy.__stacks__)
    #     else:
    #         os.system('cls')
    #         testPy.PrintScreen()
    #     print("Input Control: Down: S, Left: A, Right: D, Clockwise: J, CounterClockwise: L ")
    #     control = msvcrt.getwch()
    