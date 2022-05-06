import aStarSearch
import structures
import evaluation
import time

_SKIP_FACTOR = 3

def main():

    n = 10
    occupiedBoard = [
        ["b",8,0],["b",7,2],["r",7,1],["b",8,3],["b",7,5],["r",8,4],["b",3,6],["b",5,5],["b",3,8],["r",4,5],["r",4,8],["b",8,8],["r",8,7],["b",1,2],["b",2,3],["b",4,4],["b",5,2],["b",7,4],["b",1,6],["b",2,5],["b",3,5],["b",0,8],["b",2,8],["b",8,6],["r",0,5],["r",2,2],["r",1,3],["r",3,3],["r",4,3],["r",5,4],["r",6,7],["r",6,5],["r",1,8],["r",7,6]
    ]

    # Initialize board
    board = structures.Board(n)
    for i in occupiedBoard:
        board.fillSpot(i[1], i[2], i[0])
    player = "r"
    opposition = "b"

    reasonableMoves = []

    # look for capture and fork opportunities against opponent
    oppOccupy = board.getColourPieces(opposition)
    for location in oppOccupy:
        captures = set(evaluation.is_captureable(board,location[0],location[1],player))
        forks = set(evaluation.is_forkable(board,location[0],location[1],player))
        reasonableMoves.extend(list(captures.union(forks)))

    # prevent capture and fork opportunities against player
    playerOccupy = board.getColourPieces(player)
    for location in playerOccupy:
        captures = set(evaluation.is_captureable(board,location[0],location[1],opposition))
        forks = set(evaluation.is_forkable(board,location[0],location[1],opposition))
        reasonableMoves.extend(list(captures.union(forks)))

    reasonableMoves = list(set(reasonableMoves))
    print("Reasonable moves that lead to capture or fork: ")
    print(reasonableMoves)
    print()
    for move in reasonableMoves:
        board.fillSpot(board.size - 1 - move[0],move[1],player)
        print("Current Move: " + str(move))
        print("Evaluation: "+ str(evaluate(board,player)))
        board.fillSpot(board.size - 1 - move[0],move[1],"e")
        print()

    # print(evaluate(board,player))

def evaluate(board, player):
    opposition = "b"
    if player=="b":
        opposition = "r"

    w1 = w2 = 1
    f1 = getShortestWin(board,player,_SKIP_FACTOR)
    f2 = getShortestWin(board,opposition,_SKIP_FACTOR)
    return w1*f1 - w2*f2


def getShortestWin(board,player,skipFactor):

    shortestDist = 1000
    shortestDistPath = [[-1,-1],[-1,-1]]
    for i in range(0,board.size,skipFactor):
        for j in range(0,board.size,skipFactor):
            if player == "b":
                pathDist = aStarSearch.searchStart(board,[i,0],[j,board.size-1],player)
                if pathDist < shortestDist:
                    shortestDist = pathDist
                    shortestDistPath = [[i,0],[j,board.size-1]]
                # print("("+str(i)+","+str(0)+") to ("+str(j)+","+str(board.size-1)+"): "+str(pathDist),end="|")
            else:
                pathDist = aStarSearch.searchStart(board,[0,i],[board.size-1,j],player)
                if pathDist < shortestDist:
                    shortestDist = pathDist
                    shortestDistPath = [[0,i],[board.size-1,j]]
                # print("("+str(0)+","+str(i)+") to ("+str(board.size-1)+","+str(j)+"): "+str(pathDist),end="|")
        # print()

    print("Player '"+player+"' Shortest Path: "+str(shortestDistPath[0])+" to "+str(shortestDistPath[1]),end="")
    print(": "+str(shortestDist))
    return(shortestDist)