from SebWill.structures import pieceSquareTable
from SebWill import board
from SebWill import aStarSearch
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


_SKIP_FACTOR = 2
_TIMER_FACTOR = 3.3
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


def evaluate(player: str, opposition: str, game_state: board.Board, piece_square_table: pieceSquareTable,
             n_tokens, n_turns):
    # if new move, reset the move timer
    if _EVAL_TIMER.get_curr_turns() != n_turns:
        _EVAL_TIMER.new_move(n_turns)

    w1, w2, w3, w4, w5 = 1.0, 1.12, 0.73, 0.4, 0.32
    if game_state.n > 5:
        w5 = 0.12

    f4 = get_token_numerical_supremacy(player, opposition, game_state)

    if _EVAL_TIMER.get_turn_time() > (1.6 * game_state.n) / _TIMER_FACTOR:
        return f4 * w4

    elif _EVAL_TIMER.get_turn_time() > (1.2 * game_state.n) / _TIMER_FACTOR:
        f3 = get_potential_to_be_captured(player, opposition, game_state)
        f5 = get_piece_square_dominance(player, game_state, piece_square_table)
        return w3 * f3 + w4 * f4 + w5 * f5

    # If less than a third of the game has been played or we're running low on time, dont use heavy factor
    elif n_tokens < (game_state.n ** 2) / 4 or _EVAL_TIMER.get_turn_time() > (0.9 * game_state.n) / _TIMER_FACTOR or \
            game_state.n > 12:
        f2 = get_longest_connected_coord(player, opposition, game_state)
        f3 = get_potential_to_be_captured(player, opposition, game_state)
        f5 = get_piece_square_dominance(player, game_state, piece_square_table)
        return w2 * f2 + w3 * f3 + w4 * f4 + w5 * f5

    f2 = get_longest_connected_coord(player, opposition, game_state)
    f1 = get_shortest_win_path(game_state, player, opposition, int(game_state.n / _SKIP_FACTOR))
    f3 = get_potential_to_be_captured(player, opposition, game_state)
    f5 = get_piece_square_dominance(player, game_state, piece_square_table)
    return f1 * w1 + w2 * f2 + w3 * f3 + w4 * f4 + w5 * f5


def get_longest_connected_coord(player, opposition, game_state):
    player_max = -1
    opp_max = -1
    for i in range(game_state.n):
        for j in range(game_state.n):
            if game_state.__getitem__((i, j)) == player:
                player_max = max(len(game_state.connected_coords((i, j))), player_max)
            elif game_state.__getitem__((i, j)) == opposition:
                opp_max = max(len(game_state.connected_coords((i, j))), opp_max)
    if player_max > game_state.n - 3:
        player_max *= 2
    if opp_max > game_state.n - 3:
        opp_max *= 2
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
    return -(getShortestWin(game_state, player, opposition, skip_factor) - getShortestWin(game_state, opposition,
                                                                                          player, skip_factor))


def getShortestWin(game_state: board.Board, player: str, opposition: str, skipFactor):
    shortest_dist = _MAX
    for i in range(0, game_state.n, skipFactor):
        for j in range(0, game_state.n, skipFactor):
            # check for available start state within breadth of skip factor
            new_i, new_j = i, j
            for k in range(skipFactor - 1):
                if game_state.__getitem__((new_i, 0)) == opposition:
                    new_i += 1
                    if new_i >= game_state.n:
                        break
                else:
                    break
            if new_i >= game_state.n:
                continue

            # check for available start state within breadth of skip factor
            for k in range(skipFactor - 1):
                if game_state.__getitem__((new_j, game_state.n - 1)) == opposition:
                    new_j += 1
                    if new_j >= game_state.n:
                        break
                else:
                    break
            if new_j >= game_state.n:
                continue

            if player == "blue":
                path_dist = aStarSearch.searchStart(game_state, [new_i, 0], [new_j, game_state.n - 1], player)
                if path_dist < shortest_dist:
                    shortest_dist = path_dist

                    if shortest_dist <= 1:
                        return _MIN
            else:
                path_dist = aStarSearch.searchStart(game_state, [0, new_i], [game_state.n - 1, new_j], player)
                if path_dist < shortest_dist:
                    shortest_dist = path_dist
                    if shortest_dist <= 1:
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
