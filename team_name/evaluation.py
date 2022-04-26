import math

def board_value(n):
    Board = [[0]*n]*n
    for i in range(n):
        for j in range(n):
            # basic evaluation that favours center pieces i.e:
            # 1 2 1
            # 2 3 2
            # 1 2 1
            Board[i][j] = n - abs(n/2 - i -0.5) - abs(n/2 - j -0.5)
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
                        
                        
                        # right side horizontal three piece fork

                        if (i < (n-2)):
                            if (Board[i][j+1] == '' & Board[i+1][j-1] == '' & Board[i+2][j] == ''):
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


                if (i > 0):
                    # opp piece to the left
                    if Board[i-1][j] == opp:
                        if Board[i-1][j+1] == player & Board[i][j-1] == '':
                            return (i,j-1)
                        if Board[i-1][j+1] == '' & Board[i][j-1] == player:
                            return (i-1,j+1)
                        
                        # left side horizontal three piece fork
                        if (i > 1):
                            if (Board[i-1][j+1] == '' & Board[i][j-1] == '' & Board[i-2][j] == ''):
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
                    
                    # right side vertical three piece fork
                    if j > 0 & i < (n-1) & Board[i][j-1] == opp:
                        if (Board[i-1][j] == '' & Board[i][j+1] == '' & Board[i+1][j-1] == ''):
                            return (i-1,j)
    
    if Board[i][j] == '':
        
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