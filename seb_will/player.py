import referee.board
import util


class Player:
    def __init__(self, player, n):

        """
        Called once at the beginning of a game to initialise this player.
        Set up an internal representation of the game state.

        The parameter player is the string "red" if your player will
        play as Red, or the string "blue" if your player will play
        as Blue.
        """
        self.player_colour = player
        self.board = util.referee.board.Board(n)
        self.n_moves = 0

    def action(self):
        """
        Called at the beginning of your turn. Based on the current state
        of the game, select an action to play.
        """
        # figure out change

        #  don't need to apply it to your own board here

    def turn(self, player, action):
        """
        Called at the end of each player's turn to inform this player of
        their chosen action. Update your internal representation of the
        game state based on this. The parameter action is the chosen
        action itself.

        Note: At the end of your player's turn, the action parameter is
        the same as what your player returned from the action method
        above. However, the referee has validated it at this point.
        """
        self.n_moves += 1
        if action[0] == "STEAL":
            self.board.swap()
        else:
            self.board.place(player, (action[1], action[2]))

    def alpha_beta_minimax(self, depth, game_state, is_maximizing, alpha, beta):

        if depth == util.DEPTH_LIMIT:
            return eval_func(game_state)

        if is_maximizing:
            # set to number below minimum of eval func
            curr_max = util.MINIMAX_MIN

            for move in util.get_reasonable_moves():

                move_state = util.make_state_from_move(game_state, move)
                value = self.alpha_beta_minimax(depth + 1, move_state, False, alpha, beta)

                curr_max = max(curr_max, value)
                alpha = max(alpha, curr_max)

                if beta <= alpha:
                    # pruning principle
                    break

            return curr_max
        else:

            curr_min = util.MINIMAX_MAX
            # Generate children
            for move in util.get_reasonable_moves():

                move_state = util.make_state_from_move(game_state, move)
                value = self.alpha_beta_minimax(depth + 1, move_state, True, alpha, beta)

                curr_min = min(curr_min, value)
                beta = min(beta, curr_min)

                if beta <= alpha:
                    break

            return curr_min
