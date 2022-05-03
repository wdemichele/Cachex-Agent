import math

PLAYER, OPPOSITION, EMPTY = 'r','b', ''

def evaluate(board, player):
    w1, w2, w3, w4 = 1, 2, 3, 4
    f1, f2, f3, f4 = 1, 2, 3, 4
    value = w1*f1 + w2*f2 + w3*f3 + w4*f4
    return value

def board_value(n):
    # basic evaluation that favours center pieces i.e:
    # 1 2 1
    # 2 3 2
    # 1 2 1

    # Board Dict - Key: (i,j), Value (colour, tile value)
    Board = {(i,j):('',(n - abs(n/2 - i -0.5) - abs(n/2 - j -0.5))) for i in range(0,n) for j in range(0,n)}
    return Board

def is_captureable(Board,i,j,n,player):
    opp = "r"
    if (player == "r"):
        opp = "b"
    if Board[i][j] == opp:
        if (j > 0 & i < (n-1)):
            # opp piece to the bottom right
            if Board[i+1][j-1] == opp:
                if Board[i+1][j] == player & Board[i][j-1] == '':
                    return (i,j-1)
                if Board[i+1][j] == '' & Board[i][j-1] == player:
                    return (i+1,j)
            if (i > 0):
                # opp piece to the bottom left
                if Board[i][j-1] == opp:
                    if Board[i-1][j] == player & Board[i+1][j-1] == '':
                        return (i+1,j-1)
                    if Board[i-1][j] == '' & Board[i+1][j-1] == player:
                        return (i,j-1)

        if (j < (n-1)):
            if (j > 0):
                if (i < (n-1)):
                    # opp piece to the right
                    if Board[i+1][j] == opp:
                        if Board[i][j+1] == player & Board[i+1][j-1] == '':
                            return (i+1,j-1)
                        if Board[i][j+1] == '' & Board[i+1][j-1] == player:
                            return (i,j+1)


                if (i > 0):
                    # opp piece to the left
                    if Board[i-1][j] == opp:
                        if Board[i-1][j+1] == player & Board[i][j-1] == '':
                            return (i,j-1)
                        if Board[i-1][j+1] == '' & Board[i][j-1] == player:
                            return (i-1,j+1)

            if (i > 0):
                if (i < (n-1)):
                    # opp piece to the top right
                    if Board[i][j+1] == opp:
                        if Board[i-1][j+1] == player & Board[i+1][j] == '':
                            return (i+1,j)
                        if Board[i-1][j+1] == '' & Board[i+1][j] == player:
                            return (i-1,j+1)
                        
                        # left side vertical three piece fork
                        if j > 0 & Board[i+1][j-1] == opp:
                            if (Board[i-1][j+1] == '' & Board[i+1][j] == '' & Board[i][j-1] == ''):
                                return (i+1,j)

            
                # opp piece to the top left
                if Board[i-1][j+1] == opp:
                    if Board[i][j+1] == player & Board[i-1][j] == '':
                        return (i-1,j)
                    if Board[i][j+1] == '' & Board[i-1][j] == player:
                        return (i,j+1)


def is_forkable(Board,i,j,n,player):
    opp = "r"
    if (player == "r"):
        opp = "b"

    if Board[i][j] == opp:
        # left side horizontal three piece fork
        if (i > 1 & j < (n-1) & j > 0):
            if (Board[i-1][j] == opp & Board[i-1][j+1] == '' & Board[i][j-1] == '' & Board[i-2][j] == ''):
                #      . . . . . .
                #     r b . . . .
                #    o r r . . .
                #   . . o . . .
                #  . . . . . .
                if (Board[i-2][j+1] == opp):
                    return (i-1,j+1)

                #      . . . . . .
                #     . o . . . .
                #    o r r . . .
                #   . r b . . .
                #  . . . . . .
                if (Board[i-1][j-1] == opp):
                    return (i-1,j-1)
        
        # right side horizontal three piece fork
        if (i < (n-2) & j < (n-1) & j > 0):
            if (Board[i+1][j] == opp & Board[i][j+1] == '' & Board[i+1][j-1] == '' & Board[i+2][j] == ''):
                #      . . . . . .
                #     . . b r . .
                #    . . r r o .
                #   . . . o . .
                #  . . . . . .
                if (Board[i+1][j+1] == opp):
                    return (i,j+1)

                #      . . . . . .
                #     . . o . . .
                #    . . r r o .
                #   . . . b r .
                #  . . . . . .
                if (Board[i+2][j-1] == opp):
                    return (i+1,j-1)

        
        if (j > 0 & i < (n-1) & i > 0 & j < (n-1)):
            # right side vertical three piece fork
            #      . . . . . .
            #     . . . o r .
            #    . . . r b .
            #   . . . o r .
            #  . . . . . .
            if (Board[i][j-1] == opp & Board[i-1][j+1] == opp):
                if (Board[i-1][j] == '' & Board[i][j+1] == '' & Board[i+1][j-1] == ''):
                    return (i-1,j)
        
            # left side vertical three piece fork
            #      . . . . . .
            #     . . r o . .
            #    . . b r . .
            #   . . r o . .
            #  . . . . . .
            if (Board[i][j+1] == opp & Board[i+1][j-1] == opp):
                if (Board[i-1][j+1] == '' & Board[i+1][j] == '' & Board[i][j-1] == ''):
                    return (i+1,j)
       

    elif Board[i][j] == '':
        if (i>1 & j>0 & i < (n-2) & j < (n-1)):
            # two column fork
            #     . . . . . .
            #    . o r . . .
            #   . . r b r .
            #  . . . . r o
            # . . . . . .
            if (Board[i-1][j] == opp & Board[i-1][j+1] == opp & Board[i+1][j] == opp & Board[i+1][j-1] == opp):
                if Board[i-2][j+1] == '' & Board[i+2][j-1] == '':
                    return (i,j)
        if (i>0 & j>1 & i < (n-1) & j < (n-2)):
            # two row fork
            #      . . . . . .
            #     . . o . . .
            #    . . r r . .
            #   . . . b . .
            #  . . . r r .
            # . . . . o .
            if (Board[i][j+1] == opp & Board[i-1][j+1] == opp & Board[i][j-1] == opp & Board[i+1][j-1] == opp):
                if Board[i-1][j+2] == '' & Board[i+1][j-2] == '':
                    return (i,j)



def neighbours(board, i, j, n, visitable):
    # visitable is a list ['r','b',''], ['r',''], [''] etc.
    neighbours = []
    spotsToCheck = [[0, -1], [-1, 0], [-1, 1], [0, 1], [1, 0], [1, -1]]
    for move in spotsToCheck:
        i1, j1 = i + move[0], j + move[1]
        if i1 < 0 or i1 >= n or j1 < 0 or j1 >= n:
            continue
        else:
            if board[i1,j1][0] in visitable:
                neighbours.append([i1,j1])
    return neighbours

def longestAxisChain(board, i, j, n, visited, curChain):
    for chain in len(visited):
        if [i,j] in visited[chain]:
            return visited
    visitable = neighbours(board, i, j, n, [PLAYER,EMPTY])
    # removes elements that have already been visited
    visitable = list(set(visitable) - set(curChain))