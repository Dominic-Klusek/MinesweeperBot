import numpy as np
class MineSweeperBot:
    def __init__(self, x, y, numBombs):
        '''
        Initialize the bots parameters with some sort of data
        1. Dimnensions of Board
        2. Number of Bombs
        '''
        self.x = x
        self.y = y
        self.numBombs = numBombs
        self.checkedBoxes = np.zeros((x, y)) #a list of already checked boxes, so that we don't check the same box multiple times
    def performmove(self, revealedBoxes, mineField):
        '''
        Method to have bot perform a move, will need x and y coordinates
        '''
        x, y = thinkofmove(revealedBoxes, mineField)
        x = np.random.randint(low=0, high=self.x)
        y = np.random.randint(low=0, high=self.y)
        return x, y, True
    def thinkofmove(self, revealedBoxes, mineField):
        '''
        Bot will analyze board and decide what is the best move
        (aka what move doesn't hit a mine)
        '''
        # check boxes until we get 
        for i in range(0, self.x+1):
            for j in range(0, self.y+1):
                # if we have a box that is revealed and not checked
                if(revealedBoxes[i][j] == True) and (self.checkedBoxes[i][j] != 0):
                    if(mineField[i][j] in "[" + str(range(0, 10)) + "]"):
                        pass
                else:
                    pass
        pass