import referee.board
import copy
# MINIMAX_MIN needs to be lower than anything that eval could return
MINIMAX_MIN = -50

# MINIMAX_MAX needs to be higher than anything that eval could return
MINIMAX_MAX = 50

# DEPTH_LIMIT declared here: subject o change, may be worth change during runtime for better efficiency
DEPTH_LIMIT = 4

# MOVE_MAX_LIMIT: how many moves we are willing to consider at any given layer of minimax
MOVE_MAX_LIMIT = 50

# MOVE_MIN_LIMIT: the min limit representing when we have not considered enough moves to garner 'good' play
MOVE_MIN_LIMIT = 4





def make_state_from_move(curr_state: referee.board, move, player):
    new_board = copy.deepcopy(curr_state)
    new_board.place(player, move)
    return new_board


def get_reasonable_moves(curr_state: referee.board, n_dots, player, red_tokens, blue_tokens):
    # Feasible to try perfect play
    if curr_state.n ** 2 - n_dots < MOVE_MAX_LIMIT:
        return get_all_moves(curr_state)
    else:
        return_moves = []
        for spot in red_tokens:
            #propogate possible moves
        for spot in blue_tokens:
            #propogate possible moves
        if len(return_moves) <= MOVE_MIN_LIMIT:
            # propogate some more moves
        return return_moves




def get_all_moves(curr_state: referee.board):
    pass

def get_depth_limit():
    pass
