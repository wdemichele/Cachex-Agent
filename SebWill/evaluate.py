from SebWill import aStarSearch
from SebWill import relevantMoves
import copy

_SKIP_FACTOR = 3
# _PLAYER = "red"
# _BOARD_SIZE = 10

def evaluateReasonableMove(p, game_state):

    opposition = "blue"
    if p.player=="blue":
        opposition = "red"

    reasonableMoves = [[],[],[],[]]
    
    # look for capture opportunities against opposition
    oppOccupy = getColourPieces(p.board, opposition)
    for location in oppOccupy:
        captures = relevantMoves.is_captureable(p.board,location[0],location[1],p.player)
        reasonableMoves[0].extend(captures)

    # prevent capture opportunities against player
    playerOccupy = getColourPieces(p.board, p.player)
    for location in playerOccupy:
        captures = relevantMoves.is_captureable(p.board,location[0],location[1],opposition)
        reasonableMoves[1].extend(captures)

    # only search for forks if direct captures are empty
    if len(reasonableMoves[0])==0 and len(reasonableMoves[1])==0:

        # look for fork opportunities against opposition
        for location in oppOccupy:
            forks = relevantMoves.is_forkable(p.board,location[0],location[1],p.player)
            reasonableMoves[2].extend(forks)

        # prevent fork opportunities against player
        for location in playerOccupy:
            forks = relevantMoves.is_forkable(p.board,location[0],location[1],opposition)
            reasonableMoves[3].extend(forks)

    for i in range(4):
        reasonableMoves[i] = list(set(reasonableMoves[i]))

    # print("Reasonable moves that lead to capture or fork: ")
    # print(reasonableMoves)
    # print()

    boardState = copy.copy(p.board)

    bestMove = (None,-1000)

    for strategyType in reasonableMoves:
        for move in strategyType:
            p.board.place(p.player, (move[0],move[1]))
            # print("Current Move: " + str(move))
            # print("Evaluation: "+ str(evaluate(p)))
            curMove = (move, evaluate(p))
            if curMove[1] > bestMove[1]:
                bestMove = curMove
                game_state = p.board
            p.board = boardState
            # print()

    return bestMove

def evaluate(p):
    opposition = "blue"
    if p.player=="blue":
        opposition = "red"

    w1 = w2 = 1
    f1 = getShortestWin(p,p.player,_SKIP_FACTOR)
    f2 = getShortestWin(p,opposition,_SKIP_FACTOR)
    return w1*f1 - w2*f2


def getShortestWin(p,player,skipFactor):

    shortestDist = 1000
    shortestDistPath = [[-1,-1],[-1,-1]]
    for i in range(0,p.board.n,skipFactor):
        for j in range(0,p.board.n,skipFactor):
            if player == "blue":
                pathDist = aStarSearch.searchStart(p.board,[i,0],[j,p.board.n-1],player)
                if pathDist < shortestDist:
                    shortestDist = pathDist
                    shortestDistPath = [[i,0],[j,p.board.n-1]]
                # print("("+str(i)+","+str(0)+") to ("+str(j)+","+str(board.size-1)+"): "+str(pathDist),end="|")
            else:
                pathDist = aStarSearch.searchStart(p.board,[0,i],[p.board.n-1,j],player)
                if pathDist < shortestDist:
                    shortestDist = pathDist
                    shortestDistPath = [[0,i],[p.board.n-1,j]]
                # print("("+str(0)+","+str(i)+") to ("+str(board.size-1)+","+str(j)+"): "+str(pathDist),end="|")
        # print()

    # print("Player '"+player+"' Shortest Path: "+str(shortestDistPath[0])+" to "+str(shortestDistPath[1]),end="")
    # print(": "+str(shortestDist))
    return(shortestDist)

def getColourPieces(board, colour):
    colours = []
    for i in reversed(range(board.n)):
        for j in range(board.n):
            if board.__getitem__((i,j)) == colour:
                colours.append((i,j))
    return colours