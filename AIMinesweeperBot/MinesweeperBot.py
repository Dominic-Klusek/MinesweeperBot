import numpy as np

def printList(list):
    for i in range(0, 9):
        print("{}".format(list[i][range(0, 9)]))

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
        self.checkedNumbers = []
        self.validNumberedBoxes = [] #we need a list of the numbers that we will be working off of
        for i in range(1, x+1):
            self.validNumberedBoxes.append('[{}]'.format(i))
        self.blackList = []

    def performmove(self, revealedBoxes, mineField):
        '''
        Method to have bot perform a move, will need x and y coordinates
        '''
        performMove = True
        x, y = self.thinkofmove(revealedBoxes, mineField)
        # first move is always a fail
        if x == -1 and y == -1:
            x = np.random.randint(low=0, high=self.x)
            y = np.random.randint(low=0, high=self.y)
            self.checkedBoxes = np.zeros((self.x, self.y))
        elif (x == False) and (y == False):
            # special cases
            performMove = False
        self.checkedNumbers.clear()
        return x, y, performMove

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
                    # create a list of probabilities of nearby boxes
                    probabilityBoard = self.boxProbability(i, j, 0, np.zeros((self.x, self.y)), revealedBoxes, mineField)
                    lowestX, lowestY = self.look_at_probabilities(probabilityBoard, i, j, revealedBoxes, mineField)
                    # return coordinates of block with lowest probability to have bomb
                    return lowestX, lowestY
        return -1, -1 # return statement for first move/ invalid move

    def look_at_probabilities(self, probabilityBoard, x, y, revealedBoxes, mineField):
        '''
        Method to look through probability board 
        to find next tile to select
        '''
        # special case that there are exactly the same number of unrevealed boxes as the number in the tile
        unrevealedBoxes = self.count_unrevealed_boxes(x,y,revealedBoxes)
        numberinTile = self.get_tile_number(x,y,mineField)
        print("Test X: {}\nTest Y: {}".format(x,y))
        print("Tile Number: {}\n# unrevealed tiles: {}\n".format(numberinTile, unrevealedBoxes))
        if(int(numberinTile) == int(unrevealedBoxes)):
            return False, False
        lowestX = 0
        lowestY = 0
        lowestProbability = 999999
        for xi in range(-1, 2, 1):
            for yi in range(-1, 2, 1):
                if ((x + xi >= 0) and (y + yi >= 0)) and (((x + xi) < self.x) and ((y + yi) < self.y)):
                    if(probabilityBoard[x+xi][y+yi] < lowestProbability) and (revealedBoxes[x+xi][y+yi] == False) and not ([x+xi, y+yi] in self.blackList):
                        lowestX = x+xi
                        lowestY = y+yi
                        lowestProbability = probabilityBoard[x+xi][y+yi]
        return lowestX, lowestY

    def boxProbability(self, x, y, iteration, probabilityBoard, revealedBoxes, mineField):
        '''
        if iteration is equal to 3 return immediately
        else
            calculate probabiity of bomb being at block, and add proportion to each unrevealed block
            increment iteration
            call function again with new proportionBoard and iteration
        return proportionBoard
        '''
        # print("X: {}, Y: {}".format(x, y))
        if iteration == 10:
            return probabilityBoard
        else:
            # get tile number so that probability can be scaled
            numberOfTile = self.get_tile_number(x, y, mineField)
            # get probability of a bomb being in nearby unreaveled boxes and scale it by the number in the tile
            probabilityOfNearbyBoxes = self.calculateProbability(x, y, revealedBoxes) * float(numberOfTile)
            self.checkedNumbers.append([x,y])
            for i in range(-1, 2, 1):
                for j in range(-1, 2, 1):
                    # if box is unrevealed then increment value of probabilityBoard at indices by calculated probability
                    if ((x + i >= 0) and (y + j >= 0)) and (((x + i) < self.x) and ((y + j) < self.y)):
                        try:
                            if (revealedBoxes[x+i][y+j] == False) and (self.count_unrevealed_boxes(x,y,revealedBoxes) == int(numberOfTile)):
                                self.blackList.append([x+i, y+j])
                                probabilityBoard[x+i][y+j] = 99999
                                print("BlackList: {}".format(self.blackList))
                            elif (revealedBoxes[x+i][y+j] == False):
                                probabilityBoard[x+i][y+j] += probabilityOfNearbyBoxes
                        except:
                            print("Revealed Error")
            # call function again, with next numbered box
            nextX, nextY = self.findNextNumberedBox(x, y, revealedBoxes, mineField)
            # if the next found numbered box is 
            if not([nextX, nextY] == [-1,-1]):
                probabilityBoard = self.boxProbability(nextX, nextY, iteration + 1, probabilityBoard, revealedBoxes, mineField)
        np.set_printoptions(precision=1)
        if iteration == 0:
            print(probabilityBoard)
        return probabilityBoard

    def calculateProbability(self, x, y, revealedBoxes):
        '''
        take coordinate and then check immediate area, and return probability
        0 0 0
        0 X 0
        0 0 0
        '''
        unrevealedBoxes = self.count_unrevealed_boxes(x, y, revealedBoxes)
        # we have found no boxes that are unrevealed around box, reset checked boxes
        if unrevealedBoxes == 0:
            #self.checkedBoxes = np.zeros((self.x, self.y))
            return 999
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
                elif (revealedBoxes[x+i][y+j] == True) and (mineField[x+i][y+j] in self.validNumberedBoxes) and not ([x+i,y+j] in self.checkedNumbers):
                    nextBlockX = x+i
                    nextBlockY = y+j
        return nextBlockX, nextBlockY

    def count_unrevealed_boxes(self, x, y, revealedBoxes):
        '''
        method to count the number of unrevealed tiles
        '''
        unrevealedBoxes = 0
        # search surrounding boxes
        for i in range(-1, 2, 1):
            for j in range(-1, 2, 1):
                # if box is unrevealed then increment unrevealedBoxes
                try:
                    if revealedBoxes[x+i][y+j] == False:
                        unrevealedBoxes+=1
                except:
                    print("Revealed Error")
        return unrevealedBoxes

    def get_tile_number(self, x, y, mineField):
        '''
        Method to remove unecessary markings from tile element
        '''
        numberOfTile = mineField[x][y]
        numberOfTile = numberOfTile.replace('[','')
        numberOfTile = numberOfTile.replace(']','')
        return numberOfTile
    
    def clear_Lists(self):
        self.checkedBoxes = np.empty((1,0))
        self.checkedNumbers.clear()
        self.blackList.clear()