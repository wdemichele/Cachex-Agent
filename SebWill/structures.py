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

    def printBoard(self):
        for i in reversed(range(self.size)):
            space = "     "*i
            print(space, end = ' | ')
            for j in range(self.size):
                print("("+str(i)+","+str(j)+"):"+self.board[self.size - i - 1][j].colour, end = ' | ')
            print()
            print()

    def getColourPieces(self, colour):
        colours = []
        for i in reversed(range(self.size)):
            for j in range(self.size):
                if self.board[self.size - i - 1][j].colour == colour:
                    colours.append((i,j))
        return colours

class Path:
    def __init__(self):
        self.path = []

    def getLength(self, board, player):
        length = len(self.path)
        for tile in reversed(self.path):
            # print(f"({tile.row},{tile.column}): {board.board[board.size - 1 - tile.row][tile.column].colour}")
            if board.__getitem__((tile.row,tile.column)) == player:
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
            print("Index error in queue")
            exit()

class pieceSquareTable():
    def __init__(self,n):
        self.values = {(i,j):((n - abs(n/2 - i -0.5) - abs(n/2 - j -0.5))) for i in range(0,n) for j in range(0,n)}

        for i in range(n):
            self.values[(i,0)] += n/2
            self.values[(i,n-1)] += n/2

        for j in range(n):
            self.values[(0,j)] += n/2
            self.values[(n-1,j)] += n/2
    def get_value(self, location):
        return self.values[(location[0],location[1])]