

from SebWill import util
import time
from SebWill import aStarSearch
from SebWill import relevantMoves
from SebWill import player
import copy

_SKIP_FACTOR = 3


def evaluateReasonableMove(p):

    boardState = copy.copy(p.board)

    bestMove = (None,-1000)
    reasonableMoves = util.get_reasonable_moves
    for strategyType in reasonableMoves:
        for move in strategyType:
            p.board.place(p.player, (move[0],move[1]))
            # print("Current Move: " + str(move))
            # print("Evaluation: "+ str(evaluate(p)))
            curMove = (move, evaluateFunction(p))
            if curMove[1] > bestMove[1]:
                bestMove = curMove
            p.board = boardState
            # print()

    return bestMove

def evaluateFunction(p):
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