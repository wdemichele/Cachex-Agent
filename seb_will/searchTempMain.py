import aStarSearch

n = 5
occupiedBoard = [
    ["b",0,3],["b",0,2],["b",4,3],["b",3,4],["b",1,4],["b",0,4],["b",2,1],["b",2,2],["b",1,2],["b",2,0],["b",1,0],["b",2,4]
]
start = [4, 2]
goal = [0, 0]
player = "b"

aStarSearch.searchStart(n,occupiedBoard,start,goal,player)
