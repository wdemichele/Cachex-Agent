import aStarSearch
import relevantMoves
import time
import player
import copy

_SKIP_FACTOR = 3
# _PLAYER = "red"
# _BOARD_SIZE = 10

def evaluateReasonableMove(p):

    # p = player.Player(_PLAYER,_BOARD_SIZE)

    # occupiedBoard = [
    #     ["b",8,0],["b",8,1],["b",8,3],["b",8,4],["r",9,0],["r",7,4],["b",8,6],["b",7,8],["b",8,8],["r",8,5],["r",7,9],["b",4,3],["b",5,2],["b",4,6],["b",5,5],["r",4,2],["r",5,6],["b",1,5],["b",3,5],["b",2,2],["b",0,4],["b",1,3],["b",2,7],["b",5,8],["b",6,8],["b",6,3],["b",7,2],["b",9,3],["b",0,7],["b",5,0],["b",4,0],["b",3,0],["r",1,2],["r",3,4],["r",5,4],["r",8,2],["r",7,3],["r",4,5],["r",7,6],["r",8,7],["r",9,6],["r",4,7],["r",2,8],["r",0,8]
    # ]

    # # Initialize board
    # for i in occupiedBoard:
    #     if i[0] == "b":
    #         i[0] = "blue"
    #     else:
    #         i[0] = "red"
    #     p.board.__setitem__((i[1], i[2]), i[0])

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