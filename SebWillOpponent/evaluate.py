import random

import referee.board
import copy

_SKIP_FACTOR = 3
_MIN = -70
_MAX = 70

_DOWN = (-2, 1)
_UP = (2, -1)
_LEFT = (0, -1)
_RIGHT = (0, 1)
_DIAGONAL_UP_RIGHT = (1, 0)
_DIAGONAL_UP_LEFT = (1, -1)
_DIAGONAL_DOWN_RIGHT = (-1, 1)
_DIAGONAL_DOWN_LEFT = (-1, 0)

_ADD = lambda a, b: (a[0] + b[0], a[1] + b[1])


# _PLAYER = "red"
# _BOARD_SIZE = 10


def state_eval(player: str, opposition: str, game_state: referee.board):
    return random.randint(-5, 5)


def get_longest_connected_coord(player, opposition, game_state):
    player_max = -1
    opp_max = -1
    for i in range(game_state.n):
        for j in range(game_state.n):
            if game_state.__getitem__((i, j)) == player:
                player_max = max(len(game_state.connected_coords((i, j))), player_max)
            elif game_state.__getitem__((i, j)) == opposition:
                opp_max = max(len(game_state.connected_coords((i, j))), opp_max)
    return player_max - opp_max


def get_keyspot_dominance(player, opposition, game_state):
    player_score = 0
    opp_score = 0
    for i in range(game_state.n):
        for j in [0, game_state.n - 1]:
            if game_state.__getitem__((j, i)) == player:
                if i == j:
                    player_score += 2
                else:
                    player_score += 1
            elif game_state.__getitem__((j, i)) == opposition:
                if i == j:
                    opp_score += 2
                else:
                    opp_score += 1
            if game_state.__getitem__((i, j)) == player:
                if i == j:
                    player_score += 2
                else:
                    player_score += 1
            elif game_state.__getitem__((i, j)) == opposition:
                if i == j:
                    opp_score += 2
                else:
                    opp_score += 1
    return player_score - opp_score


def get_token_numerical_supremacy(player, opposition, game_state):
    n_player_tokens = 0
    n_opp_tokens = 0
    for i in range(game_state.n):
        for j in range(game_state.n):
            if game_state.__getitem__((i, j)) is None:
                continue
            elif game_state.__getitem__((i, j)) == player:
                n_player_tokens += 1
            else:
                n_opp_tokens += 1
    return n_player_tokens - n_opp_tokens


def get_potential_to_be_captured(player, opposition, game_state):
    player_gets_capped_potential = 0

    for i in range(game_state.n):
        for j in range(game_state.n):
            if game_state.__getitem__((i, j)) == player:
                player_gets_capped_potential -= check_capture_in_one_move((i, j), player, opposition, game_state)
    return player_gets_capped_potential


def check_capture_in_one_move(coord, player, opposition, game_state):
    ret_val = 0
    if game_state.inside_bounds(_ADD(coord, _RIGHT)) and game_state.__getitem__(
            _ADD(coord, _RIGHT)) == player:
        diag_up = _ADD(coord, _DIAGONAL_UP_RIGHT)
        diag_down = _ADD(coord, _DIAGONAL_DOWN_RIGHT)
        if game_state.inside_bounds(diag_up) and game_state.__getitem__(diag_up) == opposition or \
                game_state.inside_bounds(diag_down) and game_state.__getitem__(diag_down) == opposition:
            ret_val += 1
    if game_state.inside_bounds(_ADD(coord, _LEFT)) and game_state.__getitem__(_ADD(coord, _LEFT)) == player:
        diag_up = _ADD(coord, _DIAGONAL_UP_LEFT)
        diag_down = _ADD(coord, _DIAGONAL_DOWN_LEFT)
        if game_state.inside_bounds(diag_up) and game_state.__getitem__(diag_up) == opposition or \
                game_state.inside_bounds(diag_down) and game_state.__getitem__(diag_down) == opposition:
            ret_val += 1
    if game_state.inside_bounds(_ADD(coord, _UP)) and game_state.__getitem__(_ADD(coord, _UP)) == player:
        diag_left = _ADD(coord, _DIAGONAL_UP_LEFT)
        diag_right = _ADD(coord, _DIAGONAL_UP_RIGHT)
        if game_state.inside_bounds(diag_left) and game_state.__getitem__(diag_left) == opposition or \
                game_state.inside_bounds(diag_right) and game_state.__getitem__(diag_right) == opposition:
            ret_val += 1
    if game_state.inside_bounds(_ADD(coord, _DOWN)) and \
            game_state.__getitem__(_ADD(coord, _DOWN)) == player:
        diag_left = _ADD(coord, _DIAGONAL_DOWN_LEFT)
        diag_right = _ADD(coord, _DIAGONAL_DOWN_RIGHT)
        if game_state.inside_bounds(diag_left) and game_state.__getitem__(diag_left) == opposition or \
                game_state.inside_bounds(diag_right) and game_state.__getitem__(diag_right) == opposition:
            ret_val += 1
    return ret_val
