import referee.board
from SebWill import aStarSearch
from SebWill import relevantMoves
import copy

_SKIP_FACTOR = 3
_MIN = -70
_MAX = 70


# _PLAYER = "red"
# _BOARD_SIZE = 10

def evaluate_reasonable_move(player: str, game_state):
    opposition = "blue"
    if player == "blue":
        opposition = "red"

    reasonableMoves = [[], [], [], []]

    # look for capture opportunities against opposition
    oppOccupy = getColourPieces(game_state, opposition)
    for location in oppOccupy:
        captures = relevantMoves.is_captureable(game_state, location[0], location[1], game_state)
        reasonableMoves[0].extend(captures)

    # prevent capture opportunities against player
    playerOccupy = getColourPieces(game_state, player)
    for location in playerOccupy:
        captures = relevantMoves.is_captureable(game_state, location[0], location[1], opposition)
        reasonableMoves[1].extend(captures)

    # only search for forks if direct captures are empty
    if len(reasonableMoves[0]) == 0 and len(reasonableMoves[1]) == 0:

        # look for fork opportunities against opposition
        for location in oppOccupy:
            forks = relevantMoves.is_forkable(game_state, location[0], location[1], player)
            reasonableMoves[2].extend(forks)

        # prevent fork opportunities against player
        for location in playerOccupy:
            forks = relevantMoves.is_forkable(game_state, location[0], location[1], opposition)
            reasonableMoves[3].extend(forks)

    for i in range(4):
        reasonableMoves[i] = list(set(reasonableMoves[i]))

    # print("Reasonable moves that lead to capture or fork: ")
    # print(reasonableMoves)
    # print()

    starting_board_state = copy.copy(game_state)

    best_move = (None, _MIN)

    for strategyType in reasonableMoves:
        for move in strategyType:
            game_state.place(player, (move[0], move[1]))
            # print("Current Move: " + str(move))
            # print("Evaluation: "+ str(evaluate(p)))
            curr_move = (move, evaluate(player, game_state))
            if curr_move[1] > best_move[1]:
                best_move = curr_move
            game_state = starting_board_state
    print(best_move)
    return best_move[1]


def evaluate(player, game_state):
    opposition = "blue"
    if player == "blue":
        opposition = "red"

    w1 = w2 = 1
    f1 = getShortestWin(game_state, player, _SKIP_FACTOR)

    f2 = getShortestWin(game_state, opposition, _SKIP_FACTOR)
    print("WE GET HERE")
    return w1 * f1 - w2 * f2


def getShortestWin(game_state: referee.board.Board, player: str, skipFactor):
    shortestDist = _MAX
    shortestDistPath = [[-1, -1], [-1, -1]]
    for i in range(0, game_state.n, skipFactor):
        for j in range(0, game_state.n, skipFactor):
            if player == "blue":

                pathDist = aStarSearch.searchStart(game_state, [i, 0], [j, game_state.n - 1], player)

                if pathDist < shortestDist:
                    shortestDist = pathDist
                    shortestDistPath = [[i, 0], [j, game_state.n - 1]]
                # print("("+str(i)+","+str(0)+") to ("+str(j)+","+str(board.size-1)+"): "+str(pathDist),end="|")
            else:
                # print("CHECKPOINT 1")
                pathDist = aStarSearch.searchStart(game_state, [0, i], [game_state.n - 1, j], player)
                # print(f"CHECKPOINT2 with pathdist = {pathDist}")
                if pathDist < shortestDist:
                    shortestDist = pathDist
                    shortestDistPath = [[0, i], [game_state.n - 1, j]]
                # print("("+str(0)+","+str(i)+") to ("+str(board.size-1)+","+str(j)+"): "+str(pathDist),end="|")
        # print()
    # print("Player '"+player+"' Shortest Path: "+str(shortestDistPath[0])+" to "+str(shortestDistPath[1]),end="")
    # print(": "+str(shortestDist))
    return (shortestDist)


def getColourPieces(board, colour):
    colours = []
    for i in reversed(range(board.n)):
        for j in range(board.n):
            if board.__getitem__((i, j)) == colour:
                colours.append((i, j))
    return colours
