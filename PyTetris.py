import sys, os, copy, random, msvcrt, curses, time

class PyTetris:
    """
    Create my own tetris game using Python
    """
    def __init__(self, difficulty, size = None, block = "O"):
        levels = range(1,10)
        speed = [0.5/_ for _ in levels]
        self.__difficulty__ = dict(zip([str(_) for _ in levels], speed))
        self.__speed__ = self.__difficulty__[str(difficulty)]
        self.__scoreTable__ = {"1":40*(difficulty+1), \
                               "2": 100*(difficulty+1), \
                               "3": 300*(difficulty+1), \
                               "4": 1200*(difficulty+1)
                              }
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
                              "J_r":[[0,-1],[1,0],[2,0]], \
                              "I_v":[[0,-1],[0,-2],[0,1]], \
                              "I_h":[[-1,0],[-2,0],[1,0]], \
                              "O":[[1,0],[0,1],[1,1]], \
                              "Z_h":[[-1,0],[0,1],[1,1]], \
                              "Z_v":[[0,-1],[-1,0],[-1,1]], \
                              "S_h":[[1,0],[0,1],[-1,1]], \
                              "S_v":[[0,-1],[1,0],[1,1]], \
                              "L_d":[[-1,0],[0,1],[0,2]], \
                              "L_l":[[-1,0],[-2,0],[0,-1]], \
                              "L_u":[[1,0],[0,-1],[0,-2]], \
                              "L_r":[[0,1],[1,0],[2,0]], \
                              }
        self.__rotate__ = {"J_l":[["J_d","J_u"], [[-1,0],[0,1]]], \
                            "J_d":[["J_r","J_l"],[[0,1],[1,0]]], \
                            "J_r":[["J_u","J_d"],[[1,0],[0,-1]]], \
                            "J_u":[["J_l", "J_r"],[[0,-1],[-1,0]]], \
                            "I_v":[["I_h", "I_h"],[[0,0], [0,0]]], \
                            "I_h":[["I_v", "I_v"],[[0,0], [0,0]]], \
                            "O": [["O","O"],[[0,0],[0,0]]], \
                            "Z_v":[["Z_h", "Z_h"],[[0,0], [0,0]]], \
                            "Z_h":[["Z_v", "Z_v"],[[0,0], [0,0]]], \
                            "S_v":[["S_h", "S_h"],[[0,0], [0,0]]], \
                            "S_h":[["S_v", "S_v"],[[0,0], [0,0]]], \
                            "L_l":[["L_d","L_u"], [[0,-1],[-1,0]]], \
                            "L_d":[["L_r","L_l"],[[-1,0],[0,1]]], \
                            "L_r":[["L_u","L_d"],[[0,1],[1,0]]], \
                            "L_u":[["L_l", "L_r"],[[0,1],[0,-1]]]
                            }
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
        if direction == "down" or direction == "auto":
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
                for block in self.FilterBlock(last):
                    screen.addch(block[1], block[0]*2, " ")
                last = copy.deepcopy(self.PlotPiece(self.__tetris__))
                for block in self.__stacks__:
                    screen.addch(block[1], block[0]*2, self.__block__)
            elif direction == "auto":
                curses.flushinp()
                for block in self.FilterBlock(last):
                    screen.addch(block[1], block[0]*2, " ")
                last = copy.deepcopy(self.PlotPiece(self.__tetris__))
                for block in self.__stacks__:
                    screen.addch(block[1], block[0]*2, self.__block__)
            time.sleep(self.__speed__)
            curses.flushinp()
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
        keys = copy.copy(list(stackedRow.keys()))
        for row in keys:
            if len(stackedRow[row]) == self.__size__[0]:
                toRemove.add(int(row))
                del stackedRow[row]
        toRemove = set(sorted(toRemove))
        lengthToRemove = len(toRemove)
        if lengthToRemove > 0:
            for _ in range(6):
                #     # twoBlock = {self.__block__, " "}.remove(onscreen)
                toPaint = [self.__block__," "][_%2]
                # toPaint = " "
                for row in toRemove:
                    screen.addstr(row,1,(" "+toPaint)*self.__size__[0])
                    screen.refresh()
                    if _ == 5:
                        for block in [[_, row] for _ in range(1,self.__size__[0]+1)]:
                            self.__stacks__.remove(block)
                time.sleep(0.3)
            self.AddScore(rows=lengthToRemove)
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
        #     time.sleep(0.3)
        # newStack = []
        # for key in stackedRow:
        #     newStack.extend([[int(key),x] for x in stackedRow[key]])
        # self.__stacks__ = newStack
        pass
    
    def GenerateBlocks(self):
        newblock = random.sample(self.__rotate__.keys(),1)[0]
        self.__tetris__={newblock:[5,0]}
    
    def AddScore(self, rows):
        global controlscreen, dimControl
        self.__score__ += self.__scoreTable__[str(rows)]
        controlscreen.addstr(1,2+len("Score: "), " "*(dimControl[1]-3-len("Score: ")))
        controlscreen.addstr(1,2+len("Score: "),str(self.__score__))
        controlscreen.refresh()
    
    def BoundaryCheck(self, block,action):
        global last,p
        returnBool = False
        if action not in ["down", "auto"]:
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
                    for block in self.PlotPiece(self.__tetris__):
                        if block in self.__stacks__:
                            p = self.GameOver()
                            break
                    break
                if x[0]<=0 or x[0]>self.__size__[0]: 
                    returnBool = True
                    break
        return returnBool

    def GameOver(self):
        return "GameOver"

if __name__ == "__main__":
    tinyblock = "@"
    testPy = PyTetris(difficulty=2, block = tinyblock)
    fullscreen = curses.initscr()
    screen = fullscreen.subwin(0,0)
    screen.resize(testPy.__size__[1]+1, 2*testPy.__size__[0]+4)
    controlscreen = fullscreen.subwin(5, 30, 0, 2*testPy.__size__[0]+5)
    dimControl = controlscreen.getmaxyx()
    controlscreen.border()
    controlscreen.addstr(1,2,"Score: ")
    controlscreen.addstr(1,2+len("Score: "), "0")
    controlscreen.refresh()
    screen.border()
    screen.keypad(True)
    screen.nodelay(True)
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
    lastTimeStamp = time.time()
    while p != ord("q") and p != "GameOver":
        p = screen.getch()
        if p == curses.KEY_DOWN or p == ord(testPy.__keys__["down"]):
            testPy.Move(direction="down")
            next
        elif p == curses.KEY_LEFT or p == ord(testPy.__keys__["left"]):
            testPy.Move(direction="left")
            next
        elif p == curses.KEY_RIGHT or p == ord(testPy.__keys__["right"]):
            testPy.Move(direction="right")
            next
        # Rotate
        elif p == ord(testPy.__keys__["clockwise"]):
            testPy.Rotate(direction="clockwise")
            next
        elif p == ord(testPy.__keys__["counterclockwise"]):
            testPy.Rotate(direction="counter")
            next
        else:
            newTimeStamp = time.time()
            if newTimeStamp < lastTimeStamp + testPy.__speed__:
                time.sleep(lastTimeStamp + testPy.__speed__ - newTimeStamp)
            lastTimeStamp = time.time()
            testPy.Move(direction="auto")
    if p == "GameOver":
        screen.addstr(dims[1]//2,dims[0]//2-len("GAME OVER!")//2,"GAME OVER!")  
    screen.nodelay(False)
    curses.flushinp()
    while p != ord("q"):
        p = screen.getch()
    curses.endwin()
    os.system('cls')
    