import aStarSearch
import structures
import evaluation
import numpy

def main():

    n = 10
    occupiedBoard = [
        ["b",8,1],["b",9,1],["b",8,3],["b",9,3],["b",8,5],["b",8,6],["b",8,8],["b",8,9],["r",9,0],["r",8,4],["r",9,5],["r",7,9]
    ]

    # Initialize board
    board = structures.Board(n)
    for i in occupiedBoard:
        board.fillSpot(i[1], i[2], i[0])
    player = "r"
    opposition = "b"

    reasonableMoves = []

    oppOccupy = board.getColourPieces(opposition)
    for location in oppOccupy:
        captures = set(evaluation.is_captureable(board,location[0],location[1],player))
        forks = set(evaluation.is_forkable(board,location[0],location[1],player))
        reasonableMoves.extend(list(captures.union(forks)))
    reasonableMoves = list(set(reasonableMoves))
    print(reasonableMoves)

    # print(evaluate(board,player))

def evaluate(board, player):
    opposition = "b"
    if player=="b":
        opposition = "r"

    w1 = w2 = 0.5
    f1 = getShortestWin(board,player)
    f2 = getShortestWin(board,opposition)
    return w1*f1 - w2*f2


def getShortestWin(board,player):
    shortestDist = 1000
    shortestDistPath = [[-1,-1],[-1,-1]]
    print("Player: "+player)
    if player == "b":
        for i in range(0,board.size):
            for j in range(0,board.size):
                pathDist = aStarSearch.searchStart(board,[i,0],[j,board.size-1],player)
                if pathDist < shortestDist:
                    shortestDist = pathDist
                    shortestDistPath = [[i,0],[j,board.size-1]]
                print("("+str(i)+","+str(0)+") to ("+str(j)+","+str(board.size-1)+"): "+str(pathDist),end="|")
            print()
    else:
        for i in range(0,board.size):
            for j in range(0,board.size):
                pathDist = aStarSearch.searchStart(board,[0,i],[board.size-1,j],player)
                if pathDist < shortestDist:
                    shortestDist = pathDist
                    shortestDistPath = [[0,i],[board.size-1,j]]
                print("("+str(0)+","+str(i)+") to ("+str(board.size-1)+","+str(j)+"): "+str(pathDist),end="|")
            print()
    print()
    print(shortestDistPath,end="")
    print(": "+str(shortestDist))
    return(shortestDist)