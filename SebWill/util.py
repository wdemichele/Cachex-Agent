import random
from SebWill.structures import pieceSquareTable

from SebWill import board
import copy
from SebWill import evaluate
from SebWill import capturable

# MINIMAX_MIN needs to be lower than anything that eval could return
MINIMAX_MIN = -70

# MINIMAX_MAX needs to be higher than anything that eval could return
MINIMAX_MAX = 70

# DEPTH_LIMIT declared here: subject o change, may be worth change during runtime for better efficiency
DEPTH_LIMIT = 4

# MOVE_MAX_LIMIT: how many moves we are willing to consider at any given layer of minimax
MOVE_MAX_LIMIT = 50

# FULL_SEARCH_MAX: the maximum number we all for a full search tree
FULL_SEARCH_MAX = 16

# MOVE_MIN_LIMIT: the min limit representing when we have not considered enough moves to garner 'good' play
MOVE_MIN_LIMIT_FACTOR = 1.5

_HEX_STEPS = [(1, -1), (1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1)]
_HALF_HEX_STEPS = [(1, -1), (0, 1), (-1, 0)]
_RIGHT_HEX_STEPS = [(0, 1), (1, 0), (-1, 1)]
_LEFT_HEX_STEPS = [(0, -1), (1, -1), (-1, 0)]
_UP_HEX_STEPS = [(1, 0), (1, -1)]
_DOWN_HEX_STEPS = [(-1, 0), (-1, 1)]

_STEAL = ("STEAL",)
_PLACE = ("PLACE",)


def make_state_from_move(curr_state: board.Board, move: tuple((int, int)), player: str):
    new_board = copy.deepcopy(curr_state)
    new_board.place(player, move)
    return new_board


def get_reasonable_moves(curr_state: board.Board, n_dots: int, player: str, red_tokens: list,
                         blue_tokens: list, time_used: float):
    n = curr_state.n

    # Feasible to try perfect play (if less than forty percent of board has been placed on and board is not too big)
    if n_dots <= (0.4 * n ** 2) and n ** 2 <= FULL_SEARCH_MAX:
        return get_all_moves(curr_state)

    return_moves = []

    opposition = "blue"
    if player == "blue":
        opposition = "red"

    # look for capture and fork opportunities against opposition
    oppOccupy = getColourPieces(curr_state, opposition)
    for location in oppOccupy:
        captures = capturable.is_captureable(curr_state, location[0], location[1], curr_state)
        return_moves.extend(captures)
        forks = capturable.is_forkable(curr_state, location[0], location[1], player)
        return_moves.extend(forks)

    # prevent capture and fork opportunities against player
    playerOccupy = getColourPieces(curr_state, player)
    for location in playerOccupy:
        captures = capturable.is_captureable(curr_state, location[0], location[1], opposition)
        return_moves.extend(captures)
        forks = capturable.is_forkable(curr_state, location[0], location[1], opposition)
        return_moves.extend(forks)

    return_moves = list(set(return_moves))

    if len(return_moves) >= 0:
        return (return_moves, False)
    
    steps = _HEX_STEPS
    n_directions_to_search = 4

    if time_used > (n ** 2) * 0.4 or n >= 10:
        n_directions_to_search = 2

    for i in range(n_directions_to_search):
        move = steps[i]
        first_tokens = blue_tokens
        second_tokens = red_tokens
        if player == "blue":
            first_tokens = red_tokens
            second_tokens = blue_tokens
        for spot in first_tokens:
            new_spot = tuple(map(lambda x, y: x + y, spot, move))
            if curr_state.inside_bounds(new_spot) and not curr_state.is_occupied(new_spot):
                return_moves.append(new_spot)
        for spot in second_tokens:
            new_spot = tuple(map(lambda x, y: x + y, spot, move))
            if curr_state.inside_bounds(new_spot) and not curr_state.is_occupied(new_spot):
                return_moves.append(new_spot)
        if len(return_moves) > MOVE_MAX_LIMIT:
            return list(set(return_moves)), True

    # if amount of moves not ideal for good play
    if len(return_moves) < (MOVE_MIN_LIMIT_FACTOR * n):
        moves_to_go = int(MOVE_MIN_LIMIT_FACTOR * n - len(return_moves))
        for i in range(moves_to_go):
            x, y = random.randint(0, n - 1), random.randint(0, n - 1)
            if curr_state.inside_bounds((x, y)) and not curr_state.is_occupied((x, y)):
                if (x, y) not in return_moves:
                    return_moves.append((x, y))
    return list(set(return_moves)), True


def get_all_moves(curr_state: board.Board):
    return_moves = []
    for i in range(curr_state.n):
        for j in range(curr_state.n):
            spot = (i, j)
            if not curr_state.is_occupied(spot):
                return_moves.append(spot)
    return return_moves


def get_right_hex_steps():
    return _RIGHT_HEX_STEPS


def get_left_hex_steps():
    return _LEFT_HEX_STEPS


def get_down_hex_steps():
    return _DOWN_HEX_STEPS


def get_up_hex_steps():
    return _UP_HEX_STEPS


def get_colour_pieces(state: board.Board, colour):
    colours = []
    for i in reversed(range(state.n)):
        for j in range(state.n):
            if board.__getitem__((i, j)) == colour:
                colours.append((i, j))
    return colours


def get_depth_limit(time_spent: float, board_size: int, is_quiescent=True):
    # if lots of time (90% of time limit or greater) and smaller board
    quiescent = 0 if is_quiescent else 1
    if time_spent < (board_size ** 2) / 15.0 and board_size < 4:
        return DEPTH_LIMIT
    elif time_spent < (board_size ** 2) * 0.70:
        return DEPTH_LIMIT - 1 + quiescent
    elif time_spent < (board_size ** 2) * 0.95:
        return DEPTH_LIMIT - 2
    else:
        return DEPTH_LIMIT - 3


def getColourPieces(board, colour):
    colours = []
    for i in reversed(range(board.n)):
        for j in range(board.n):
            if board.__getitem__((i, j)) == colour:
                colours.append((i, j))
    return colours


def eval_func(player: str, opposition: str, curr_state: board, piece_square_table: pieceSquareTable,
              n_tokens, n_turns):
    return evaluate.evaluate(player, opposition, curr_state, piece_square_table, n_tokens, n_turns)
