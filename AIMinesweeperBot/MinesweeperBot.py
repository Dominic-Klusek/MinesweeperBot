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
        # if we did not find an appropriate tile to choose, we don't perform the move
        elif (x == False) and (y == False):
            # special cases
            if (self.number_of_unchecked_boxes(revealedBoxes, mineField) == 0):
                self.checkedBoxes = np.zeros((self.x, self.y))
            performMove = False
        # clear checked numbers after each turn
        self.checkedNumbers.clear()
        return x, y, performMove

    def thinkofmove(self, revealedBoxes, mineField):
        '''
        Bot will analyze board and decide what is the best move
        (aka what move doesn't hit a mine)
        '''
        # check boxes until we get 
        for j in range(0, self.x):
            for i in range(0, self.y):
                # if we have a box that is revealed and not checked
                if(revealedBoxes[i][j] == True) and (self.checkedBoxes[i][j] == 0) and (mineField[i][j] in self.validNumberedBoxes):
                    self.checkedBoxes[i][j] = 1
                    print("Origin Coordinates :[{}, {}]".format(i,j))
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
        '''
        Special Cases
        1. if we have the case where the number of unrevealed tiles is equal to number in tiles
        2. if we already know that the tiles near the test block are already bombs
        '''
        if(int(numberinTile) == int(unrevealedBoxes) or (self.number_of_blacklisted_boxes(x, y,revealedBoxes) == int(numberinTile))):
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
        print("Iteration: {}".format(iteration))
        if not (x == -1):
            self.checkedNumbers.append([x,y])
        else:
            return probabilityBoard
        nextX, nextY = self.findNextNumberedBox(x, y, revealedBoxes, mineField)
        while not(nextX == -1):
            # get tile number so that probability can be scaled
            numberOfTile = self.get_tile_number(x, y, mineField)
            # get probability of a bomb being in nearby unreaveled boxes and scale it by the number in the tile
            probabilityOfNearbyBoxes = self.calculateProbability(x, y, revealedBoxes) * float(numberOfTile)
            for i in range(-1, 2, 1):
                for j in range(-1, 2, 1):
                    # if box is unrevealed then increment value of probabilityBoard at indices by calculated probability
                        try:
                            if (revealedBoxes[x+i][y+j] == False) and (self.count_unrevealed_boxes(x,y,revealedBoxes) == int(numberOfTile)) and not([x+i, y+j] in self.blackList):
                                self.blackList.append([x+i, y+j])
                                probabilityBoard[x+i][y+j] = 99999
                                #print("BlackList: {}".format(self.blackList))
                            elif (revealedBoxes[x+i][y+j] == False) and not([x+i, y+j] in self.blackList):
                                probabilityBoard[x+i][y+j] += probabilityOfNearbyBoxes
                        except:
                            pass
            # call function again, with next numbered box
            nextX, nextY = self.findNextNumberedBox(x, y, revealedBoxes, mineField)
            # if the next found numbered box is 
            probabilityBoard = self.boxProbability(nextX, nextY, iteration + 1, probabilityBoard, revealedBoxes, mineField)
        # print out board of probabilities just for debugging
        np.set_printoptions(precision=1)
        if iteration == 0:
            print(np.transpose(probabilityBoard))
            print("Checked numbers: {}".format(self.checkedNumbers))
            print("Blacklisted Tiles: {}".format(self.blackList))
        nextX, nextY = self.findNextNumberedBox(x, y, revealedBoxes, mineField)
        return probabilityBoard

    def calculateProbability(self, x, y, revealedBoxes):
        '''
        Take coordinate and then check immediate area, and return probability
        0 0 0
        0 X 0
        0 0 0
        '''
        # check the number of unrevealed boxes
        unrevealedBoxes = self.count_unrevealed_boxes(x, y, revealedBoxes)
        # we have found no boxes that are unrevealed around box, reset checked boxes
        if unrevealedBoxes == 0:
            #self.checkedBoxes = np.zeros((self.x, self.y))
            return 999
        return float(100 / unrevealedBoxes)

    def findNextNumberedBox(self, x, y, revealedBoxes, mineField):
        '''
        Find the next block around the current block
        '''
        nextBlockX = -1
        nextBlockY = -1
        # search around box
        for j in range(-1, 2, 1):
            for i in range(-1, 2, 1):
                #if the box is revealed, and box is a numbered tile, and we are not looking at the current block
                if ((x + i < 0) or (x + i >= self.x)) or ((y + j < 0) or (y + j >= self.y)) or ((x + i == x) and (y + j == y)):
                    pass
                elif (revealedBoxes[x+i][y+j] == True) and (mineField[x+i][y+j] in self.validNumberedBoxes) and not ([x+i,y+j] in self.checkedNumbers):
                    nextBlockX = x+i
                    nextBlockY = y+j
        return nextBlockX, nextBlockY

    def count_unrevealed_boxes(self, x, y, revealedBoxes):
        '''
        Method to count the number of unrevealed tiles
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
                    pass
        return unrevealedBoxes

    def get_tile_number(self, x, y, mineField):
        '''
        Method to remove unecessary markings from tile element
        '''
        numberOfTile = mineField[x][y]
        numberOfTile = numberOfTile.replace('[','')
        numberOfTile = numberOfTile.replace(']','')
        return numberOfTile
    
    def number_of_unchecked_boxes(self, revealedBoxes, mineField):
        '''
        Method to check the number of unchecked boxes in the grid
        '''
        numberOfUnChecked = 0
        for x in range(0, self.x):
            for y in range(0, self.y):
                if (mineField[x][y] in self.validNumberedBoxes) and (revealedBoxes[x][y] == True) and (self.checkedBoxes[x][y] == False):
                    numberOfUnChecked += 1
        return numberOfUnChecked
    
    def number_of_blacklisted_boxes(self, x, y, revealedBoxes):
        numberofBlacklisted = 0
        # search surrounding boxes
        for i in range(-1, 2, 1):
            for j in range(-1, 2, 1):
                # if box is unrevealed then increment unrevealedBoxes
                try:
                    if revealedBoxes[x+i][y+j] == False and not([x+i,y+j] in self.blackList):
                        numberofBlacklisted += 1
                except:
                    pass
        return numberofBlacklisted

    def clear_Lists(self):
        self.checkedBoxes = np.empty((1,0))
        self.checkedNumbers.clear()
        self.blackList.clear()