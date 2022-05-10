from SebWill.structures import pieceSquareTable
from SebWill import board
from SebWill import aStarSearch
from SebWill import capturable
import copy
from SebWill import timer


class EvalTimer:

    def __init__(self):
        self.timer = timer.Timer()
        self.curr_n_turns = 0

    def get_curr_turns(self):
        return self.curr_n_turns

    def new_move(self, n_turns):
        self.curr_n_turns = n_turns
        self.timer.reset_restart()

    def get_turn_time(self):
        return self.timer.check_time_since_start()

    def stop(self):
        self.timer.stop()

    def start(self):
        self.timer.start()

    def get_count(self):
        return self.timer.get_count()


_TIMER_FACTOR = 2.9
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

_EVAL_TIMER = EvalTimer()


def evaluate(player: str, opposition: str, game_state: board, piece_square_table: pieceSquareTable,
             n_tokens, n_turns):
    # if new move, reset the move timer
    if _EVAL_TIMER.get_curr_turns() != n_turns:
        _EVAL_TIMER.new_move(n_turns)

    w1, w2, w3, w4, w5 = 1, 0.8, 1.4, 0.92, 1.3

    if game_state.n > 5:
        w5 = 0.42

    f3 = get_potential_to_be_captured(player, opposition, game_state)
    f4 = get_token_numerical_supremacy(player, opposition, game_state)
    f5 = get_piece_square_dominance(player, game_state, piece_square_table)

    if _EVAL_TIMER.get_turn_time() > (2 * game_state.n) / _TIMER_FACTOR:
        w3 = 1
        return w3 * f3 + w4 * f4 + w5 * f5
    elif n_tokens < game_state.n * 2 - 2 or _EVAL_TIMER.get_turn_time() > game_state.n / _TIMER_FACTOR:
        w2 = 1
        f2 = get_longest_connected_coord(player, opposition, game_state)
        return w2 * f2 + w3 * f3 + w4 * f4 + w5 * f5

    f2 = get_longest_connected_coord(player, opposition, game_state)
    f1 = get_shortest_win_path(game_state, player, opposition, game_state.n - 1)
    return f1 * w1 + w2 * f2 + w3 * f3 + w4 * f4 + w5 * f5


def state_eval(player: str, opposition: str, game_state: board, piece_square_table: pieceSquareTable, n_tokens):
    w1 = 1
    w2 = 0.8
    w3 = 0.4
    w4 = 0.4
    if game_state.n < 6:
        w5 = 0.33
    else:
        w5 = 1.6
    if player == "blue":
        if n_tokens < game_state.n * 2 - 2:
            return get_longest_connected_coord(player, opposition, game_state)
        return get_shortest_win_path(game_state, player, opposition, game_state.n - 1)
    return get_longest_connected_coord(player, opposition, game_state)


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
    for i in range(game_state.n, 2):
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
    opposition_gets_capped_potential = 0

    for i in range(game_state.n):
        for j in range(game_state.n):
            if game_state.__getitem__((i, j)) == player:
                player_gets_capped_potential += check_capture_in_one_move((i, j), player, opposition, game_state)
            elif game_state.__getitem__((i, j)) == opposition:
                opposition_gets_capped_potential += check_capture_in_one_move((i, j), opposition, player, game_state)
    return opposition_gets_capped_potential - player_gets_capped_potential


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


def get_shortest_win_path(game_state: board.Board, player: str, opposition: str, skip_factor):
    return -(getShortestWin(game_state, player, skip_factor) - getShortestWin(game_state, opposition, skip_factor))


def getShortestWin(game_state: board.Board, player: str, skipFactor):
    shortest_dist = _MAX
    for i in range(0, game_state.n, skipFactor):
        for j in range(0, game_state.n, skipFactor):
            if player == "blue":
                path_dist = aStarSearch.searchStart(game_state, [i, 0], [j, game_state.n - 1], player)
                if path_dist < shortest_dist:
                    shortest_dist = path_dist
                    if shortest_dist == 0:
                        print("zero cost path detected")
                        return _MIN
            else:
                path_dist = aStarSearch.searchStart(game_state, [0, i], [game_state.n - 1, j], player)
                if path_dist < shortest_dist:
                    shortest_dist = path_dist
                    if shortest_dist == 0:
                        print("zero cost path detected")
                        return _MIN
    return shortest_dist





def get_piece_square_dominance(player, game_state, piece_square_table: pieceSquareTable):
    # edge and corner and central pieces are weighted as more advantageous
    player_token_location_value = 0
    opp_token_location_value = 0
    for i in range(game_state.n):
        for j in range(game_state.n):
            if game_state.__getitem__((i, j)) is None:
                continue
            elif game_state.__getitem__((i, j)) == player:
                player_token_location_value += piece_square_table.get_value((i, j))
            else:
                opp_token_location_value += piece_square_table.get_value((i, j))
    return player_token_location_value - opp_token_location_value
