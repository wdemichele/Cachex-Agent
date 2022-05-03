import referee.board

# MINIMAX_MIN needs to be lower than anything that eval could return
MINIMAX_MIN = -50

# MINIMAX_MAX needs to be higher than anything that eval could return
MINIMAX_MAX = 50

# DEPTH_LIMIT declared here: subject o change, may be worth change during runtime for better efficiency
DEPTH_LIMIT = 4

# MOVE_LIMIT: how many moves we are willing to consider at any given layer of minimax
MOVE_LIMIT = 50


def make_state_from_move(curr_state, move):
    pass


def get_reasonable_moves(curr_state):
    pass
