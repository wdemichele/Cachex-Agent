
import referee.board
import copy
from SebWill import evaluate

# MINIMAX_MIN needs to be lower than anything that eval could return
MINIMAX_MIN = -70

# MINIMAX_MAX needs to be higher than anything that eval could return
MINIMAX_MAX = 70

# DEPTH_LIMIT declared here: subject o change, may be worth change during runtime for better efficiency
DEPTH_LIMIT = 3

# MOVE_MAX_LIMIT: how many moves we are willing to consider at any given layer of minimax
MOVE_MAX_LIMIT = 55

# MOVE_MIN_LIMIT: the min limit representing when we have not considered enough moves to garner 'good' play
MOVE_MIN_LIMIT = 4

_HEX_STEPS = [(1, -1), (1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1)]
_HALF_HEX_STEPS = [(1, -1), (0, 1), (-1, 0)]
_RIGHT_HEX_STEPS = [(0, 1), (1, 0), (-1, 1)]
_LEFT_HEX_STEPS = [(0, -1), (1, -1), (-1, 0)]
_UP_HEX_STEPS = [(1, 0), (1, -1)]
_DOWN_HEX_STEPS = [(-1, 0), (-1, 1)]

_STEAL = ("STEAL",)
_PLACE = ("PLACE",)


def make_state_from_move(curr_state: referee.board, move, player):
    new_board = copy.deepcopy(curr_state)
    new_board.place(player, move)
    return new_board


def get_reasonable_moves(curr_state: referee.board, n_dots, player, red_tokens, blue_tokens):
    n = curr_state.n
    # Feasible to try perfect play
    if n ** 2 - (n_dots * 0.8) < MOVE_MAX_LIMIT:
        return get_all_moves(curr_state)

    return_moves = []
    for move in _HEX_STEPS:
        for spot in red_tokens:
            new_spot = tuple(map(lambda x, y: x + y, spot, move))
            if curr_state.inside_bounds(new_spot) and not curr_state.is_occupied(new_spot):
                return_moves.append(new_spot)
        for spot in blue_tokens:
            new_spot = tuple(map(lambda x, y: x + y, spot, move))
            if curr_state.inside_bounds(new_spot) and not curr_state.is_occupied(new_spot):
                return_moves.append(new_spot)
        if len(return_moves) > MOVE_MAX_LIMIT:
            return return_moves

    if len(return_moves) < (MOVE_MAX_LIMIT / 2):
        if player == "blue":
            for i in range(curr_state.n):
                if not curr_state.is_occupied((i, 0)):
                    return_moves.append((i, 0))
                if not curr_state.is_occupied((i, n)):
                    return_moves.append((i, n))
        else:
            for i in range(curr_state.n):
                if not curr_state.is_occupied((0, i)):
                    return_moves.append((0, i))
                if not curr_state.is_occupied((n, i)):
                    return_moves.append((n, i))

    if len(return_moves) < (MOVE_MAX_LIMIT / 5):
        for move in _HEX_STEPS:
            new_spot = tuple(map(lambda x, y: x + y, move, (n / 2, n / 2)))
            if not curr_state.is_occupied(new_spot):
                return_moves.append(new_spot)
    elif len(return_moves) < (MOVE_MAX_LIMIT / 4):
        for move in _HALF_HEX_STEPS:
            new_spot = tuple(map(lambda x, y: x + y, move, (n / 2, n / 2)))
            if not curr_state.is_occupied(new_spot):
                return_moves.append(new_spot)
    return return_moves


def get_all_moves(curr_state: referee.board):
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


def get_colour_pieces(board, colour):
    colours = []
    for i in reversed(range(board.n)):
        for j in range(board.n):
            if board.__getitem__((i, j)) == colour:
                colours.append((i, j))
    return colours


def eval_func(player: str, opposition: str, curr_state: referee.board):
    # return evaluate.evaluate(player, curr_state)
    # return random.randint(-5, 5)
    return evaluate.state_eval(player, opposition, curr_state)
