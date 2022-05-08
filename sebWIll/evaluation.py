def is_captureable(Board,i,j,player):
    left, right, topLeft, topRight, bottomLeft, bottomRight = (i,j-1), (i,j+1), (i+1,j-1), (i+1,j), (i-1,j), (i-1,j+1)
    n = Board.n
    captureMove = []
    opp = "red"
    if (player == "red"):
        opp = "blue"
    if (j > 0 and i < (n-1)):
        # opp piece to the top left
        if Board.__getitem__(topLeft) == opp:
            if Board.__getitem__(topRight) == player and Board.__getitem__(left) == None:
                captureMove.append(left)
            if Board.__getitem__(topRight) == None and Board.__getitem__(left) == player:
                captureMove.append(topRight)
        if (i > 0):
            # opp piece to the left
            if Board.__getitem__(left) == opp:
                if Board.__getitem__(bottomLeft) == player and Board.__getitem__(topLeft) == None:
                    captureMove.append(topLeft)
                if Board.__getitem__(bottomLeft) == None and Board.__getitem__(topLeft) == player:
                    captureMove.append(bottomLeft)


    if (j < (n-1)):
        if (j > 0):
            if (i < (n-1)):            
                # opp piece to the top right
                if Board.__getitem__(topRight) == opp:
                    if Board.__getitem__(right) == player and Board.__getitem__(topLeft) == None:
                        captureMove.append(topLeft)
                        
                    if Board.__getitem__(right) == None and Board.__getitem__(topLeft) == player:
                        captureMove.append(right)
                        


            if (i > 0):
                # opp piece to the bottom left
                if Board.__getitem__(bottomLeft) == opp:
                    if Board.__getitem__(bottomRight) == player and Board.__getitem__(left) == None:
                        captureMove.append(left)
                        
                    if Board.__getitem__(bottomRight) == None and Board.__getitem__(left) == player:
                        captureMove.append(bottomRight)
                        

        if (i > 0):
            if (i < (n-1)):
                # opp piece to the right
                if Board.__getitem__(right) == opp:
                    if Board.__getitem__(bottomRight) == player and Board.__getitem__(topRight) == None:
                        captureMove.append(topRight)
                    if Board.__getitem__(bottomRight) == None and Board.__getitem__(topRight) == player:
                        captureMove.append(bottomRight)
        
            # opp piece to the bottom right
            if Board.__getitem__(bottomRight) == opp:
                
                if Board.__getitem__(right) == player and Board.__getitem__(bottomLeft) == None:
                    captureMove.append(bottomLeft)
                if Board.__getitem__(right) == None and Board.__getitem__(bottomLeft) == player:
                    captureMove.append(right)

    #outer capturables
    if (j<(n-1) and i>0):
        if (i>0):
            if (i>1):
                if (Board.__getitem__((i-2,j+1)) == opp):
                    #   . . . b . .
                    #  . . . r o .
                    # . . . . b .
                    if Board.__getitem__(bottomLeft) == player and Board.__getitem__(bottomRight) == None:
                        captureMove.append(bottomRight)
                    #   . . . b . .
                    #  . . . o r .
                    # . . . . b .
                    elif Board.__getitem__(bottomLeft) == None and Board.__getitem__(bottomRight) == player:
                        captureMove.append(bottomLeft)

            if (i>0 and j<n-2):
                if (Board.__getitem__((i-1,j+2)) == opp):
                    #   . . . . . .
                    #  . b o . . .
                    # . . r b . .
                    if Board.__getitem__(bottomRight) == player and Board.__getitem__(right) == None:
                        captureMove.append(right)
                    #   . . . . . .
                    #  . b r . . .
                    # . . o b . .
                    elif Board.__getitem__(bottomRight) == None and Board.__getitem__(right) == player:
                        captureMove.append(bottomRight)

        if (i<(n-1)):
            if (Board.__getitem__((i+1,j+1)) == opp):
                #   . . . . . .
                #  . b o . . .
                # . . r b . .
                if Board.__getitem__(topRight) == player and Board.__getitem__(right) == None:
                    captureMove.append(right)
                #   . . . . . .
                #  . b r . . .
                # . . o b . .
                elif Board.__getitem__(topRight) == None and Board.__getitem__(right) == player:
                    
                    captureMove.append(topRight)
    return captureMove

def is_forkable(Board,i,j,player):
    left, right, topLeft, topRight, bottomLeft, bottomRight = (i,j-1), (i,j+1), (i+1,j-1), (i+1,j), (i-1,j), (i-1,j+1)
    n = Board.n
    
    forkMove = []
    opp = "red"
    if (player == "red"):
        opp = "blue"

    if (i>=(n-1) or i<=0 or j>=(n-1) or j<=0):
        return forkMove

    if (Board.__getitem__(left) == opp and Board.__getitem__(topLeft) == None and Board.__getitem__(bottomLeft) == None and Board.__getitem__(right) == None):
        #      . . . . . .
        #     . . b r . .
        #    . . r r o .
        #   . . . o . .
        #  . . . . . .
        if (Board.__getitem__(topRight) == opp):
            forkMove.append(topLeft)
        #      . . . . . .
        #     . . b . . .
        #    . . r r o .
        #   . . . o r .
        #  . . . . . .
        if (Board.__getitem__(bottomRight) == opp):
            forkMove.append(bottomLeft)
    
    if (Board.__getitem__(right) == opp and Board.__getitem__(bottomRight) == None and Board.__getitem__(left) == None and Board.__getitem__(topRight) == None):
        #      . . . . . .
        #     r b . . . .
        #    o r r . . .
        #   . . o . . .
        #  . . . . . .
        if (Board.__getitem__(topLeft) == opp):
            forkMove.append(topRight)
        #      . . . . . .
        #     . o . . . .
        #    o r r . . .
        #   . r b . . .
        #  . . . . . .
        if (Board.__getitem__(bottomLeft) == opp):
            forkMove.append(bottomRight)  

    # left side vertical three piece fork
    #      . . . . . .
    #     . . r o . .
    #    . . b r . .
    #   . . r o . .
    #  . . . . . .
    if (Board.__getitem__(topLeft) == opp and Board.__getitem__(bottomLeft) == opp):
        if (Board.__getitem__(left) == None and Board.__getitem__(topRight) == None and Board.__getitem__(bottomRight) == None):
            forkMove.append(left)

    # right side vertical three piece fork
    #      . . . . . .
    #     . . . o r .
    #    . . . r b .
    #   . . . o r .
    #  . . . . . .
    if (Board.__getitem__(topRight) == opp and Board.__getitem__(bottomRight) == opp):
        if (Board.__getitem__(topLeft) == None and Board.__getitem__(bottomLeft) == None and Board.__getitem__(right) == None):
            forkMove.append(right)
    
    return forkMove


def twoColumnFork(Board,i,j,n,player):
    left, right, topLeft, topRight, bottomLeft, bottomRight = (i,j-1), (i,j+1), (i+1,j-1), (i+1,j), (i-1,j), (i-1,j+1)
    opp = "r"
    if (player == "r"):
        opp = "b"
    if Board.__getitem__((i,j)) == None:
        if (i>1 and j>0 and i < (n-2) and j < (n-1)):
            # two column fork
            #     . . . . . .
            #    . o r . . .
            #   . . r b r .
            #  . . . . r o
            # . . . . . .
            if (Board.__getitem__(bottomLeft) == opp and Board.__getitem__(bottomRight) == opp and Board.__getitem__(topRight) == opp and Board.__getitem__(topLeft) == opp):
                if Board.__getitem__((i-2,j+1)) == None and Board.__getitem__((i+2,j-1)) == None:
                    return (i,j)
        if (i>0 and j>1 and i < (n-1) and j < (n-2)):
            # two row fork
            #      . . . . . .
            #     . . o . . .
            #    . . r r . .
            #   . . . b . .
            #  . . . r r .
            # . . . . o .
            if (Board.__getitem__(right) == opp and Board.__getitem__(bottomRight) == opp and Board.__getitem__(left) == opp and Board.__getitem__(topLeft) == opp):
                if Board.__getitem__((i-1,j+2)) == None and Board.__getitem__((i+1,j-2)) == None:
                    return (i,j)