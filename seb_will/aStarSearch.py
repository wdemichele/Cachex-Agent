import structures

PLAYER, OPPOSITION, EMPTY = 'r','b', ''

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


def searchStart(n,occupiedBoard,start,goal,player):

    # Initialize board
    board = structures.Board(n)
    for i in occupiedBoard:
        board.fillSpot(i[1], i[2], i[0])

    # Save start and goal
    start = structures.Location(start[0], start[1])
    goal = structures.Location(goal[0], goal[1])

    final_path = aStarSearch(start, goal, board, n, player)
    final_path.printPath(board, player)

def aStarHeuristic(location1, location2):
    # Must be admissible - this means never overestimate, but can be correct or underestimate
    # Assume an empty board, no obstacles for any path, use basic Manhattan distance as it always
    # under-estimates in our problem domain
    if location1 == location2:
        return 1
    deltaX = abs(location1.row - location2.row)
    deltaY = abs(location1.column - location2.column)
    return deltaY + deltaX

def bonusHeuristic(board, location1, location2, boardSize, noCostColour): 
    if location1 == location2:
        return 1
    deltaX = abs(location1.row - location2.row)
    deltaY = abs(location1.column - location2.column)
    yFree = xFree = 0
    for col in range(boardSize):
        for row in range(boardSize):
            if board.board[row][col] == noCostColour:
                yFree += 1
                continue 	# max one free node per column
    for col in range(boardSize):
        for row in range(boardSize):
            if board.board[row][col] == noCostColour:
                yFree += 1 
                continue 	# max one free node per row
    return max(deltaX - xFree, 0) + max(deltaY - yFree, 0)


def aStarSearch(start, goal, board, n, player):
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
                newMoveNode.g = curr.g if board.board[move.row][move.column] == player else curr.g +1
                newMoveNode.h = bonusHeuristic(board, move, goal, n, player)
                newMoveNode.f = newMoveNode.h + newMoveNode.g

                for node in queue.queue:
                    if newMoveNode == node and node.g < newMoveNode.g:
                        continue

                queue.insert(newMoveNode)

    return path
