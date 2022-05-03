import structures

PLAYER, OPPOSITION, EMPTY = 'red', 'blue', 'e'

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

def bonusHeuristic(board, location1, location2, noCostColour): 
    steps = 0 if board.board[board.size - 1 - location1.row][location1.column].colour == noCostColour else 1
    if location1 == location2:
        return steps
    steps += 0 if board.board[board.size - 1 - location2.row][location2.column].colour == noCostColour else 1

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
        for row in range(board.size):
            if board.board[board.size - 1 - row][col].colour == noCostColour:
                visited.append([board.size - 1 - row,col])
                yFree += 1
                break 	# max one free node per column
    for row in xAvail:
        for col in range(board.size):
            if board.board[board.size - 1 - row][col].colour == noCostColour:
                if [board.size - 1 - row,col] not in visited:
                    xFree += 1 
                    break 	# max one free node per row

    return max(deltaX - xFree, 0) + max(deltaY - yFree, 0) + steps


def aStarSearch(start, goal, board, player):
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

        next_moves = board.getAdjacentEmptySpots(curr.location, player)
        for move in next_moves:
            if move not in checked_list:
                newMoveNode = AStarNode(curr, move)
                newMoveNode.g = curr.g if board.board[board.size - 1 - move.row][move.column].colour == player else curr.g +1
                newMoveNode.h = bonusHeuristic(board, move, goal, player)
                newMoveNode.f = newMoveNode.h + newMoveNode.g

                for node in queue.queue:
                    if newMoveNode == node and node.g < newMoveNode.g:
                        continue

                queue.insert(newMoveNode)

    return path
