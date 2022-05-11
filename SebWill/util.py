import random

from typing import Tuple, List

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


def make_state_from_move(curr_state: board.Board, move: Tuple[int, int], player: str):
    """Makes a new board from a move"""
    new_board = copy.deepcopy(curr_state)
    new_board.place(player, move)
    return new_board


def get_reasonable_moves(curr_state: board.Board, n_dots: int, player: str, red_tokens: list,
                         blue_tokens: list, time_used: float):
    """Returns a list of unique moves given any game board state and the player whose turn it is"""
    n = curr_state.n

    # Feasible to try perfect play (if less than forty percent of board has been placed  on and board is not too big)
    if n ** 2 - n_dots <= FULL_SEARCH_MAX and time_used < (n ** 2) * 0.6 and not curr_state.n > 10:
        return get_all_moves(curr_state), False

    return_moves = []

    opposition = "blue"
    if player == "blue":
        opposition = "red"

    # look for capture and fork opportunities against opposition
    opp_occupy = get_colour_pieces(curr_state, opposition)
    for location in opp_occupy:
        captures = capturable.is_captureable(curr_state, location[0], location[1], curr_state)
        return_moves.extend(captures)
        forks = capturable.is_forkable(curr_state, location[0], location[1], player)
        return_moves.extend(forks)

    # prevent capture and fork opportunities against player
    player_occupy = get_colour_pieces(curr_state, player)
    for location in player_occupy:
        captures = capturable.is_captureable(curr_state, location[0], location[1], opposition)
        return_moves.extend(captures)
        forks = capturable.is_forkable(curr_state, location[0], location[1], opposition)
        return_moves.extend(forks)

    return_moves = set(return_moves)

    # If acceptable number of moves, stop move propagation (greedy search)
    if len(return_moves) > n / 6:
        return list(return_moves), False

    n_directions_to_search = 4
    if time_used > (n ** 2) * 0.4 or n >= 10:
        n_directions_to_search = 2
    # Otherwise add some defensive moves
    if player == "red":
        defensive_moves = get_defensive_moves(curr_state, blue_tokens, n_directions_to_search)
    else:
        defensive_moves = get_defensive_moves(curr_state, red_tokens, n_directions_to_search)

    return_moves.update(defensive_moves)

    if len(return_moves) > n / 1.5:
        return list(return_moves), True

    # If still too small, add some offensive moves
    if player == "red":
        offensive_moves = get_defensive_moves(curr_state, red_tokens, n_directions_to_search)
    else:
        offensive_moves = get_defensive_moves(curr_state, blue_tokens, n_directions_to_search)
    return_moves.update(offensive_moves)

    if len(return_moves) < n / 1.15:
        moves_to_go = int(n - len(return_moves))
        for i in range(moves_to_go):
            x, y = random.randint(0, n - 1), random.randint(0, n - 1)
            if curr_state.inside_bounds((x, y)) and not curr_state.is_occupied((x, y)):
                if (x, y) not in return_moves:
                    return_moves.add((x, y))
    return list(return_moves), True


def get_all_moves(curr_state: board.Board):
    return_moves = []
    for i in range(curr_state.n):
        for j in range(curr_state.n):
            spot = (i, j)
            if not curr_state.is_occupied(spot):
                return_moves.append(spot)
    return return_moves


def get_defensive_moves(curr_state: board.Board, opp_tokens: List[Tuple[int, int]], n_moves: int):
    return_moves = set()
    for token in opp_tokens:
        for i in range(n_moves):
            move = _HEX_STEPS[random.randint(0, 5)]
            new_spot = tuple(map(lambda x, y: x + y, token, move))
            if curr_state.inside_bounds(new_spot) and not curr_state.is_occupied(new_spot):
                return_moves.add(new_spot)
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
    """Gets the depth limit for alpha-beta minimax"""
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


def get_colour_pieces(board, colour):
    colours = []
    for i in reversed(range(board.n)):
        for j in range(board.n):
            if board.__getitem__((i, j)) == colour:
                colours.append((i, j))
    return colours


def eval_func(player: str, opposition: str, curr_state: board, piece_square_table: pieceSquareTable,
              n_tokens, n_turns):
    return evaluate.evaluate(player, opposition, curr_state, piece_square_table, n_tokens, n_turns)
