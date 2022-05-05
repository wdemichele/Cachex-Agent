import math
import structures


PLAYER, OPPOSITION, EMPTY = 'r','b', ''



def is_captureable(Board,i,j,player):

    
    n = Board.size
    captureMove = []
    opp = "r"
    if (player == "r"):
        opp = "b"
    if (j > 0 and i < (n-1)):
        # opp piece to the top left
        if Board.board[n-1-(i+1)][j-1].colour == opp:
            if Board.board[n-1-(i+1)][j].colour == player and Board.board[n-1-(i)][j-1].colour == 'e':
                captureMove.append((i,j-1))
            if Board.board[n-1-(i+1)][j].colour == 'e' and Board.board[n-1-(i)][j-1].colour == player:
                captureMove.append((i+1,j))
        if (i > 0):
            # opp piece to the left
            if Board.board[n-1-(i)][j-1].colour == opp:
                if Board.board[n-1-(i-1)][j].colour == player and Board.board[n-1-(i+1)][j-1].colour == 'e':
                    captureMove.append((i+1,j-1))
                if Board.board[n-1-(i-1)][j].colour == 'e' and Board.board[n-1-(i+1)][j-1].colour == player:
                    captureMove.append((i-1,j))


    if (j < (n-1)):
        if (j > 0):
            if (i < (n-1)):
                
                # opp piece to the top right
                if Board.board[n-1-(i+1)][j].colour == opp:
                    if Board.board[n-1-(i)][j+1].colour == player and Board.board[n-1-(i+1)][j-1].colour == 'e':
                        captureMove.append((i+1,j-1))
                        
                    if Board.board[n-1-(i)][j+1].colour == 'e' and Board.board[n-1-(i+1)][j-1].colour == player:
                        captureMove.append((i,j+1))
                        


            if (i > 0):
                # opp piece to the bottom left
                if Board.board[n-1-(i-1)][j].colour == opp:
                    if Board.board[n-1-(i-1)][j+1].colour == player and Board.board[n-1-(i)][j-1].colour == 'e':
                        captureMove.append((i,j-1))
                        
                    if Board.board[n-1-(i-1)][j+1].colour == 'e' and Board.board[n-1-(i)][j-1].colour == player:
                        captureMove.append((i-1,j+1))
                        

        if (i > 0):
            if (i < (n-1)):
                # opp piece to the right
                if Board.board[n-1-(i)][j+1].colour == opp:
                    if Board.board[n-1-(i-1)][j+1].colour == player and Board.board[n-1-(i+1)][j].colour == 'e':
                        captureMove.append((i+1,j))
                    if Board.board[n-1-(i-1)][j+1].colour == 'e' and Board.board[n-1-(i+1)][j].colour == player:
                        captureMove.append((i-1,j+1))
        
            # opp piece to the bottom right
            if Board.board[n-1-(i-1)][j+1].colour == opp:
                
                if Board.board[n-1-(i)][j+1].colour == player and Board.board[n-1-(i-1)][j].colour == 'e':
                    captureMove.append((i-1,j))
                if Board.board[n-1-(i)][j+1].colour == 'e' and Board.board[n-1-(i-1)][j].colour == player:
                    captureMove.append((i,j+1))
    return captureMove


def is_forkable(Board,i,j,player):
    n = Board.size
    
    forkMove = []
    opp = "r"
    if (player == "r"):
        opp = "b"

    if Board.board[n-1-(i)][j].colour == opp:
        # left side horizontal three piece fork
        if (i > 1 and j < (n-1) and j > 0):
            if (Board.board[n-1-(i-1)][j].colour == opp and Board.board[n-1-(i-1)][j+1].colour == 'e' and Board.board[n-1-(i)][j-1].colour == 'e' and Board.board[n-1-(i-2)][j].colour == 'e'):
                #      . . . . . .
                #     r b . . . .
                #    o r r . . .
                #   . . o . . .
                #  . . . . . .
                if (Board.board[n-1-(i-2)][j+1].colour == opp):
                    forkMove.append((i-1,j+1))

                #      . . . . . .
                #     . o . . . .
                #    o r r . . .
                #   . r b . . .
                #  . . . . . .
                if (Board.board[n-1-(i-1)][j-1].colour == opp):
                    forkMove.append((i-1,j-1))
        
        # right side horizontal three piece fork
        if (i < (n-2) and j < (n-1) and j > 0):
            if (Board.board[n-1-(i+1)][j].colour == opp and Board.board[n-1-(i)][j+1].colour == 'e' and Board.board[n-1-(i+1)][j-1].colour == 'e' and Board.board[n-1-(i+2)][j].colour == 'e'):
                #      . . . . . .
                #     . . b r . .
                #    . . r r o .
                #   . . . o . .
                #  . . . . . .
                if (Board.board[n-1-(i+1)][j+1].colour == opp):
                    forkMove.append((i,j+1))

                #      . . . . . .
                #     . . o . . .
                #    . . r r o .
                #   . . . b r .
                #  . . . . . .
                if (Board.board[n-1-(i+2)][j-1].colour == opp):
                    forkMove.append((i+1,j-1))

        
        if (j > 0 and i < (n-1) and i > 0 and j < (n-1)):
            # right side vertical three piece fork
            #      . . . . . .
            #     . . . o r .
            #    . . . r b .
            #   . . . o r .
            #  . . . . . .
            if (Board.board[n-1-(i)][j-1].colour == opp and Board.board[n-1-(i-1)][j+1].colour == opp):
                if (Board.board[n-1-(i-1)][j].colour == 'e' and Board.board[n-1-(i)][j+1].colour == 'e' and Board.board[n-1-(i+1)][j-1].colour == 'e'):
                    forkMove.append((i-1,j))
        
            # left side vertical three piece fork
            #      . . . . . .
            #     . . r o . .
            #    . . b r . .
            #   . . r o . .
            #  . . . . . .
            if (Board.board[n-1-(i)][j+1].colour == opp and Board.board[n-1-(i+1)][j-1].colour == opp):
                if (Board.board[n-1-(i-1)][j+1].colour == 'e' and Board.board[n-1-(i+1)][j].colour == 'e' and Board.board[n-1-(i)][j-1].colour == 'e'):
                    forkMove.append((i+1,j))
    return forkMove
       
def twoColumnFork(Board,i,j,n,player):
    opp = "r"
    if (player == "r"):
        opp = "b"
    if Board.board[n-1-(i)][j].colour == 'e':
        if (i>1 and j>0 and i < (n-2) and j < (n-1)):
            # two column fork
            #     . . . . . .
            #    . o r . . .
            #   . . r b r .
            #  . . . . r o
            # . . . . . .
            if (Board.board[n-1-(i-1)][j].colour == opp and Board.board[n-1-(i-1)][j+1].colour == opp and Board.board[n-1-(i+1)][j].colour == opp and Board.board[n-1-(i+1)][j-1].colour == opp):
                if Board.board[n-1-(i-2)][j+1].colour == 'e' and Board.board[n-1-(i+2)][j-1].colour == 'e':
                    return (i,j)
        if (i>0 and j>1 and i < (n-1) and j < (n-2)):
            # two row fork
            #      . . . . . .
            #     . . o . . .
            #    . . r r . .
            #   . . . b . .
            #  . . . r r .
            # . . . . o .
            if (Board.board[n-1-(i)][j+1].colour == opp and Board.board[n-1-(i-1)][j+1].colour == opp and Board.board[n-1-(i)][j-1].colour == opp and Board.board[n-1-(i+1)][j-1].colour == opp):
                if Board.board[n-1-(i-1)][j+2].colour == 'e' and Board.board[n-1-(i+1)][j-2].colour == 'e':
                    return (i,j)