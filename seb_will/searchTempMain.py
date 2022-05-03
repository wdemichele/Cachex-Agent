import aStarSearch

n = 5
occupiedBoard = [
    ["b",1,0],["b",1,1],["b",1,3],["b",3,2],["r",0,2],["r",0,3],["r",2,2],["r",2,3],["r",3,0],["r",4,3]
]

player = "r"
if player == "b":
    for i in range(0,n):
        for j in range(0,n):
            print("("+str(i)+","+str(0)+") to ("+str(j)+","+str(n-1)+"): "+str(aStarSearch.searchStart(n,occupiedBoard,[i,0],[j,n-1],player)),end="|")
        print()
else:
    for i in range(0,n):
        for j in range(0,n):
            print("("+str(0)+","+str(i)+") to ("+str(n-1)+","+str(j)+"): "+str(aStarSearch.searchStart(n,occupiedBoard,[0,i],[n-1,j],player)),end="|")
        print()
