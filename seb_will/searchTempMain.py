import aStarSearch

n = 5
occupiedBoard = [["b",1,1],["b",1,2],["b",1,3],["b",3,2],["b",1,2],["b",1,4]]
start = [4, 2]
goal = [0, 0]
player = "b"

aStarSearch.searchStart(n,occupiedBoard,start,goal,player)