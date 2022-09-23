# Cachex-Agent
## Cachex Rules
Cachex is a modified version of the classic game *Hex* [^1], a strategy board game in which players attempt to connect opposite sides of a rhombus-shaped board made of hexagonal cells. 
<p align="center">
<img src="https://user-images.githubusercontent.com/69499183/191873797-6b0ce5f0-e244-4884-9a76-64889fbc51a3.png">
</p>

Cachex includes the modification that players may **capture** their opponents pieces if they are the last piece in diamond shapes as follows:
<p align="center">
<img src="https://user-images.githubusercontent.com/69499183/191873768-6b39afbe-ee10-4b67-8242-83b8798bec0a.png" height=150> <img src="https://user-images.githubusercontent.com/69499183/191873732-18ce9de0-1a5b-464a-b3f7-01870d51aae0.png" height=150>
</p>

# Reactive Agent

## Minimax Search
Minimax assumes that the player is attempting to maximise their chance of winning while the opponent is attempting to minimise the player’s chance of winning. In order to pick an optimal move, we must consider how the opponent will respond to such a move, and how we will respond to the opponent’s move, extending recursively. The best move is recursively found at each depth state, responding to the opponent’s optimal move, until we reach either the win state or the maximum depth search value.

## Alpha Beta Pruning
We optimised our minimax search by implementing alpha beta pruning, which limits the number of nodes needing to be searched by applying the logic that the minimiser will not choose a move that results in a better outcome for the player.
We have Alpha and Beta as the best evaluation move at a given depth for the Maximiser (player) and Minimiser (opponent) respectively.
Branches of the search tree may be cut-off because a better move already exists for either of Maximiser and Minimiser, and we understand that both players are only going to be attempting to optimise their game state by choosing the best move, and such lesser evaluation moves need not be considered.

### Move Ordering
Alpha Beta Pruning is only as successful as the order in which it evaluates the nodes, in perfect case we have the best available node searched first, and can ignore all other nodes immediately, and subsequently square rooting our time complexity.
On the contrary if the best move is searched last, the time complexity of alpha beta pruning does not change, and we are left with simple minimax.
On average we would expect a time complexity of b^(d/2), where b is the branching factor and d is the depth of search, i.e. halving the exponential of minimax search complexity.

As such the ordering of the nodes passed to alpha beta minimax is critically important to the speed of the search, and we needed to optimise the order of the logical moves that were passed.

We defined capture and fork states as very strong game moves, and as such had these nodes appear before all other logical moves on the search tree.

Furthermore we reasoned that moves that increased the player towards their respective win path would likely be higher weighted than moves that were focused on the other axis. As such in our path building when selecting a node to build onto the player path, or block onto the opponent we first appended moves that built in the player’s primary axis or blocked in the opponent’s primary axis.


### Transposition Table
By implementing Move Ordering for our Alpha-Beta Pruning, we were able to skip a number of board states, however there were still a lot of board states being repeatedly visited. This could be optimised using a transposition table, using a dictionary hashmap we enabled efficient access to already visited states, storing the evaluation mapped by a given board state.
However the storage of large and numerous board states will have considerable memory requirements, so to avoid this taxation we implemented a hashing of the board state, as two identical boards will have an identical hash value, and the storage of these hash values is comparably inexpensive.

## Evaluation Function
Our evaluation function was implemented to determine the value of each of the board states, using this value to determine how beneficial each individual move was to advancing the player’s board state.
We used a five-factor function:

Static Board Evaluation Function
E = W1*f1 + W2*f2 + W3*f3 + W4*f4 + W5*f5

Functions:
-	f1: Shortest Win
    -	(See Shortest Win)
-	f2: Longest Connected Coord
    -	Checks the length of the longest path on the Board
-	f3: Capture Potential
    -	Negatively weights moves that allow being captured
-	f4: Number of tokens
-	f5: Piece Square Table
    -	(See Piece Square Table)

Each factor is ‘negatively’ commutative; that is to say for every board state g, if we are evaluating in terms of benefit for player a, the same evaluation of the same state g will be equal and opposite for an opponent b. 

#### Shortest Win (Modified A* Search)
Shortest win was the main component of our evaluation function, and provided the least number of empty tiles to be claimed for a player to get from one end of their goal axis to the other. 

A* Search from Project A was modified to allow the inclusion of zero cost nodes, for tiles that the respective player has already claimed, and consequently required changes to the A* heuristic to ensure admissibility (see below). 

The number of tiles required for win was calculated by checking the shortest path from each start state: (0,0),(1,0)…(n,0) to each end state: (0,n),(1,n)…(n,n), and returning the least number of tiles needing to be claimed for a full path.

With an n^2 complexity, this became grossly inefficient, and we quickly realised we would rather prioritise efficiency over accuracy, allowing us to increase the depth of the minimax search.

We included a skip factor, that only checks every skip_factor=3 start nodes and finish nodes, as we rationalised that the difference between a path starting at either (k-1,0),(k,0),(k+1,0) or ending at either (k-1,n),(k,n),(k+1,n) would not have considerable difference, provided that the remaining tile is not captured by the opponent. This decreased complexity by 1/(skip_complexity)^2.

### A-Star Search Heuristic
A* search used a hex-optimised version of Manhattan Distance as an admissible heuristic to limit the number of path searches the algorithm was required to use. This heuristic became no longer usable with the implementation of Zero Cost Nodes, that could be traversed between the start and goal state without costing a tile placement.

![image](https://user-images.githubusercontent.com/69499183/191875085-d771a0ea-40c8-4f34-92fd-6dc917297853.png)

As such in order to build the path search necessary to determine the number of tiles required between start and goal states for either player, a new heuristic would be needed to implement, or else the Manhattan Distance would no longer necessarily be admissible, as a shorter distance may take advantage of the specific colour that has no cost, demonstrated in Figure 1:
Instead we developed our own admissible heuristic.

Our heuristic takes the Manhattan distance as the base value in x and y directions. Then it checks if there are any zero cost nodes along each row of the x axis and separately of each column in the y axis for all rows and columns between the start and goal states.
For each relevant column and row that has at least one zero node, deduct from the Manhattan distance of x and y respectively.
This new heuristic would ensure admissibility by having the cheapest path as the maximum possible potential cheapest path, in the event that all the zero cost nodes are perfectly aligned for traversal across the path.

### Piece-Square Table
We quickly understood that there were certain advantages to areas of the board that enabled certain unique qualities to use to our upper hand. These ‘hotspots’ included the corners and edges of the board, as well as the centre areas.
To represent the weighting of each area of the board, we implemented a piece-square table, a matrix mapped to the board that evaluates the board piece placement based on the value of that area, with higher values mapped to predefined ‘hotspots’.

Edges of the board have the advantage of being only capturable from one axis plane, making them a viable option for both building and blocking paths.

Corners on the other hand are completely uncapturable, provided we don’t supply a tile to the outer-diamond capture tile (which we negatively weighted), and have the added advantage of blocking both the board edge piece for the opponent as well as creating a board edge piece for the player.

The centre pieces were well-weighted specifically for the advantage of opening opportunities for path exploration, and particularly being adaptable to any opponent attempts at blocking.

Primitive heatmap representation of Piece-Square Table with n=9 board:
![image](https://user-images.githubusercontent.com/69499183/191874757-8a3b5cf3-fc81-437a-8094-1d440bb95eb6.png)

### Quiescence Searching
As the minimax search is limited by the depth that we determine for it, there are moves that have immediate short term benefits however may lead to later consequences. Take the example of player “red” performing a capture that enables the opponent “blue” to perform a more important capture.

![image](https://user-images.githubusercontent.com/69499183/191874493-89eb142c-d25f-4210-b629-1856afb40601.png)

These minimax frontier moves cannot be solved by simply increasing the depth, as this response would need to be repeatedly extended to each individual branch's conclusion state.
Instead we want to determine quiescent moves that won’t greatly affect the board state, and ignore further depth searching.
For ‘important’ moves, such as a capture move or a fork attack, we expanded the depth of the minimax search by one to ensure that this move wouldn’t result in an overall negative outcome.




[^1]: https://www.maths.ed.ac.uk/~csangwin/hex/index.html
