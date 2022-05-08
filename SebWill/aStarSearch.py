import structures

PLAYER, OPPOSITION, EMPTY = 'red', 'blue', None

class AStarNode:
    def __init__(self, parent, location):
        self.parent = parent
        self.location = location

        # G should techincally be 1, doesnt matter overall in algorithm so leave 0
        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.location == other.location

    def __lt__(self, other):
        return self.f < other.f

    def __gt__(self, other):
        return self.f > other.f


def searchStart(board,start,goal,player):

    # Save start and goal
    start = structures.Location(start[0], start[1])
    goal = structures.Location(goal[0], goal[1])

    final_path = aStarSearch(start, goal, board, player)
    # final_path.printPath(board, player)
    # board.printBoard()
    return (final_path.getLength(board, player))

def bonusHeuristic(Board, location1, location2, noCostColour): 
    steps = 0 if Board.__getitem__((location1.row,location1.column)) == noCostColour else 1
    if location1 == location2:
        return steps
    steps += 0 if Board.__getitem__((location2.row,location2.column)) == noCostColour else 1

    deltaX = abs(location1.row - location2.row)
    deltaY = abs(location1.column - location2.column)
    yFree = xFree = 0
    xAvail = []
    yAvail = []
    xDir = yDir = 1
    visited = []

    if location1.row > location2.row:
        xDir = -1
    if location1.column > location2.column:
        yDir = -1

    for x in range(location1.row, location2.row + xDir*1, xDir):
        xAvail.append(x)
    for y in range(location1.column, location2.column + yDir*1, yDir):
        yAvail.append(y)

    for col in yAvail:
        for row in range(Board.n):
            if Board.__getitem__((row,col)) == noCostColour:
                visited.append([row,col])
                yFree += 1
                break 	# max one free node per column
    for row in xAvail:
        for col in range(Board.n):
            if Board.__getitem__((row,col)) == noCostColour:
                if [row,col] not in visited:
                    xFree += 1 
                    break 	# max one free node per row

    return max(deltaX - xFree, 0) + max(deltaY - yFree, 0) + steps


def aStarSearch(start, goal, Board, player):
    goalNode = AStarNode(None, goal)
    goalNode.g = 0
    goalNode.h = 0
    goalNode.f = 0

    queue = structures.PriorityQueue()
    queue.insert(AStarNode(None, start))

    checked_list = []
    path = structures.Path()
    while queue:

        # Get head of queue
        curr = queue.pop()
        checked_list.append(curr.location)
        if curr == goalNode:
            while curr is not None:
                path.path.append(curr.location)
                curr = curr.parent
            return path

        next_moves = getAdjacentSpots(Board, curr.location, player, False)
        for move in next_moves:
            if move not in checked_list:
                newMoveNode = AStarNode(curr, move)
                newMoveNode.g = curr.g if Board.__getitem__((move.row,move.column)) == player else curr.g +1
                newMoveNode.h = bonusHeuristic(Board, move, goal, player)
                newMoveNode.f = newMoveNode.h + newMoveNode.g

                for node in queue.queue:
                    if newMoveNode == node and node.g < newMoveNode.g:
                        continue

                queue.insert(newMoveNode)

    return path

def getAdjacentSpots(Board, location, noCostColour, all):
    retVal = []
    spotsToCheck = [[0, -1], [-1, 0], [-1, 1], [0, 1], [1, 0], [1, -1]]
    for move in spotsToCheck:
        new_location = structures.Location(location.row + move[0], location.column + move[1])
        if new_location.row < 0 or new_location.row >= Board.n or new_location.column < 0 or new_location.column >= Board.n:
            continue
        else:
            if all:
                spot = structures.Spot(new_location, Board.__getitem__((new_location.row,new_location.column)))
                retVal.append(spot)
            else:    
                if Board.__getitem__((new_location.row,new_location.column)) == None:
                    retVal.append(new_location)
                elif Board.__getitem__((new_location.row,new_location.column)) == noCostColour:
                    retVal.append(new_location)
    return retVal
