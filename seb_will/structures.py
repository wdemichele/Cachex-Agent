class Location:
    def __init__(self, row, column):
        self.row = row
        self.column = column

    def __eq__(self, other):
        return (self.row == other.row) and (self.column == other.column)


class Spot:
    # Colour key
    # "r" red
    # "b" blue
    # "e" empty
    def __init__(self, location, colour):
        self.location = location
        self.colour = colour


class Board:
    def __init__(self, size):
        self.size = size
        self.board = []
        for i in range(size):
            line = []
            for j in range(size):
                location = Location((size - i - 1), j)
                spot = Spot(location, "e")
                line.append(spot)
            self.board.append(line)

    def fillSpot(self, row, column, colour):
        self.board[self.size - 1 - row][column].colour = colour

    def getAdjacentEmptySpots(self, location, noCostColour):
        retVal = []
        spotsToCheck = [[0, -1], [-1, 0], [-1, 1], [0, 1], [1, 0], [1, -1]]
        for move in spotsToCheck:
            new_location = Location(location.row + move[0], location.column + move[1])
            if new_location.row < 0 or new_location.row >= self.size or new_location.column < 0 or new_location.column >= self.size:
                continue
            else:
                if self.board[self.size - 1 - new_location.row][new_location.column].colour == "e":
                    retVal.append(new_location)
                elif self.board[self.size - 1 - new_location.row][new_location.column].colour == noCostColour:
                    retVal.append(new_location)
        return retVal
    def printBoard(self):
        for i in reversed(range(self.size)):
            space = "     "*i
            print(space, end = ' | ')
            for j in range(self.size):
                print("("+str(i)+","+str(j)+"):"+self.board[self.size - i - 1][j].colour, end = ' | ')
            print()
            print()


class Path:
    def __init__(self):
        self.path = []

    def getLength(self, board, player):
        length = len(self.path)
        for tile in reversed(self.path):
            # print(f"({tile.row},{tile.column}): {board.board[board.size - 1 - tile.row][tile.column].colour}")
            if board.board[board.size - 1 - tile.row][tile.column].colour == player:
                length -= 1
        return length
        
    def printPath(self):
        for location in reversed(self.path):
            row = location.row
            column = location.column
            print(f"({row},{column})")


# Based on the implementation described here : https://www.geeksforgeeks.org/priority-queue-in-python/
class PriorityQueue(object):
    def __init__(self):
        self.queue = []

    def __str__(self):
        return ' '.join([str(i) for i in self.queue])

    # for checking if the queue is empty
    def isEmpty(self):
        return len(self.queue) == 0

    # for inserting an element in the queue
    def insert(self, data):
        self.queue.append(data)

    # for popping an element based on Priority
    def pop(self):
        try:
            min = 0
            for i in range(len(self.queue)):
                if self.queue[i] < self.queue[min]:
                    min = i
            item = self.queue[min]
            del self.queue[min]
            return item
        except IndexError:
            print()
            exit()
