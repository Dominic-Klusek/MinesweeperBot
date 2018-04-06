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
        self.validNumberedBoxes = [] #we need a list of the numbers that we will be working off of
        for i in range(1, x+1):
            self.validNumberedBoxes.append('[{}]'.format(i))

    def performmove(self, revealedBoxes, mineField):
        '''
        Method to have bot perform a move, will need x and y coordinates
        '''
        x, y = self.thinkofmove(revealedBoxes, mineField)
        # first move is always a fail
        if x == -1 and y == -1:
            x = np.random.randint(low=0, high=self.x)
            y = np.random.randint(low=0, high=self.y)
        return x, y, True

    def thinkofmove(self, revealedBoxes, mineField):
        '''
        Bot will analyze board and decide what is the best move
        (aka what move doesn't hit a mine)
        '''
        # check boxes until we get 
        for i in range(0, self.x):
            for j in range(0, self.y):
                # if we have a box that is revealed and not checked
                if(revealedBoxes[i][j] == True) and (self.checkedBoxes[i][j] == 0) and (mineField[i][j] in self.validNumberedBoxes):
                    self.checkedBoxes[i][j] = 1
                    # get a list of probabilities of nearby boxes
                    # probabilityBoard = np.zeros((self.x, self.y))
                    probabilities = self.boxProbability(i, j, 0, np.zeros((self.x, self.y)), revealedBoxes, mineField)
                    lowestX = 0
                    lowestY = 0
                    lowestProbability = 1234.56
                    # find block with smallest probability of killing you
                    for xi in range(-1, 2):
                        for yi in range(-1, 2):
                            if ((i + xi >= 0) and (j + yi >= 0)) and (((i + xi) < self.x) and ((j + yi) < self.y)):
                                if(probabilities[i+xi][j+yi] < lowestProbability) and (revealedBoxes[i+xi][j+yi] == False) and ((i+xi >= 0) and (j+yi >= 0)) and ((i+xi < self.x) and (j+yi < self.y)):
                                    lowestX = i+xi
                                    lowestY = j+yi
                                    lowestProbability = probabilities[i+xi][j+yi]
                                    # return coordinates of block with lowest probability to have bomb
                    return lowestX, lowestY
        return -1, -1

    def boxProbability(self, x, y, iteration, probabilityBoard, revealedBoxes, mineField):
        '''
        if iteration is equal to 3 return immediately
        else
            calculate probabiity of bomb being at block, and add proportion to each unrevealed block
            increment iteration
            call function again with new proportionBoard and iteration
        return proportionBoard
        '''
        if iteration == 5:
            return probabilityBoard
        else:
            probabilityOfNearbyBoxes = self.calculateProbability(x, y, revealedBoxes)
            for i in range(-1, 2, 1):
                for j in range(-1, 2, 1):
                    # if box is unrevealed then increment value of probabilityBoard at indices by calculated probability
                    if ((x + i >= 0) and (y + j >= 0)) and (((x + i) < self.x) and ((y + j) < self.y)):
                        if revealedBoxes[x + i][y + i] == False:
                            probabilityBoard[i][j] += probabilityOfNearbyBoxes
                    # call function again, with next numbered box
                nextX, nextY = self.findNextNumberedBox(x, y, revealedBoxes, mineField)
            probabilityBoard = self.boxProbability(nextX, nextY, iteration + 1, probabilityBoard, revealedBoxes, mineField)
        return probabilityBoard

    def calculateProbability(self, x, y, revealedBoxes):
        '''
        take coordinate and then check immediate area, and return probability
        0 0 0
        0 X 0
        0 0 0
        '''
        unrevealedBoxes = 0
        # search surrounding boxes
        for i in range(-1, 2, 1):
            for j in range(-1, 2, 1):
                # if box is unrevealed then increment unrevealedBoxes
                if ((x + i >= 0) and (y + j >= 0)) and (((x + i) < self.x) and ((y + j) < self.y)):
                    if revealedBoxes[x + i][y + i] == False:
                        unrevealedBoxes+=1
        # we have found no boxes that are unrevealed around box, reset checked boxes
        if unrevealedBoxes == 0:
            self.checkedBoxes = np.zeros((self.x, self.y))
            return 99999999
        return float(100 / unrevealedBoxes)

    def findNextNumberedBox(self, x, y, revealedBoxes, mineField):
        '''
        find the next block around the current block
        '''
        nextBlockX = -1
        nextBlockY = -1
        # search around box
        for i in range(-1, 2, 1):
            for j in range(-1, 2, 1):
                #if the box is revealed, and box is a numbered tile, and we are not looking at the current block
                if ((x + i < 0) or (x + i >= self.x)) or ((y + j < 0) or (y + j >= self.y)) or ((x + i == x) and (y + j == y)):
                    pass
                elif (revealedBoxes[x + i][y + j] == True) and (mineField[x + i][y + j] in self.validNumberedBoxes):
                    nextBlockX = x + i
                    nextBlockY = y + j
        if nextBlockX == -1 and nextBlockY == -1:
            return x, y
        else:
            return nextBlockX, nextBlockY